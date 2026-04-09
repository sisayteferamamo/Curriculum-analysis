import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import re

# --- CONFIGURATION ---
BASE_URL = "https://intranet.fd.cvut.cz"
SEARCH_URL = "https://intranet.fd.cvut.cz/en/students/courses.html?kp=&np=&vp=&ks=&nu=all&odeslano=ano&po=B3710%2CB3710_SCS%2CB0716A040001%2CB1041A040001%2CB1041A040001_DOS%2CB1041A040001_ITS%2CB1041A040001_LED%2CB1041A040001_LOG%2CB1041A040001_spole%C4%8Dn%C3%A1+%C4%8D%C3%A1st+studia%2CB1041A040004%2CN%2CN1041A040003%2CN1041A040004%2CN1041A040005%2CN1041A040006%2CN1041A040007%2CN1041A040010%2CP%2CP3710%2CP3710_D%2CP3710_P%2CP3710_T%2CP3713%2CP3713_L%2CP3902%2CP3902_I"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

FIELD_MAP = {
    "Academic Degree": "academic_degree",
    "Study Programme": "study_programme",
    "Credits": "credits",
    "Number of Hours": "hours",
    "Type of Course": "course_type",
    "Course Completion": "completion_type",
    "Keywords": "keywords",
    "Abstract": "abstract",
    "Objectives": "objectives",
}

def parse_study_programmes(dd_tag):
    """Parses nested programs and their specific variation tables."""
    program_list = []
    # Identify program headers and their associated data tables
    current_divs = dd_tag.find_all('div', recursive=False)
    current_tables = dd_tag.find_all('table', recursive=False)

    for i, div in enumerate(current_divs):
        prog_name = div.get_text(strip=True)
        variations = []
        
        if i < len(current_tables):
            table = current_tables[i]
            rows = table.find_all('tr')[1:] # Skip header row
            for row in rows:
                cols = row.find_all('td')
                if not cols: continue
                
                var_data = {
                    'semester': cols[0].get_text(strip=True),
                    'language': cols[1].find('img')['alt'] if cols[1].find('img') else "N/A"
                }
                if len(cols) >= 3:
                    var_data['specialization'] = cols[2].get_text(separator=" ", strip=True)
                
                variations.append(var_data)
        
        program_list.append({
            "program_name": prog_name,
            "variations": variations
        })
    return program_list

def get_course_details(detail_url):
    """Primary parser for the description list structure."""
    try:
        response = requests.get(detail_url, headers=HEADERS, timeout=15)
        if response.status_code != 200: return None
        
        soup = BeautifulSoup(response.content, 'html.parser')
        results = {v: "N/A" for v in FIELD_MAP.values()}
        
        dl = soup.find('dl', class_='dl-horizontal')
        if not dl: return results
        
        dts = dl.find_all('dt')
        dds = dl.find_all('dd')
        
        for dt, dd in zip(dts, dds):
            label = dt.get_text(separator=" ", strip=True).replace(":", "")
            if label == "Study Programme":
                results["study_programme"] = parse_study_programmes(dd)
            elif label in FIELD_MAP:
                clean_key = FIELD_MAP[label]
                results[clean_key] = dd.get_text(separator=" ", strip=True)
                
        return results
    except Exception:
        return None

def main():
    print("Initiating Thesis Data Extraction...")
    try:
        res = requests.get(SEARCH_URL, headers=HEADERS)
        res.raise_for_status()
    except Exception as e:
        print(f"Connection Error: {e}")
        return

    soup = BeautifulSoup(res.content, 'html.parser')
    all_tables = soup.find_all('table')
    
    dataset = []
    seen_codes = set()
    skipped_count = 0

    print(f"Detected {len(all_tables)} sections. Starting deep scrape...")

    for table in all_tables:
        for row in table.find_all('tr'):
            cols = row.find_all('td')
            if len(cols) < 2: continue
            
            course_code = cols[0].get_text(strip=True)
            if not course_code or len(course_code) < 3: continue
            
            # --- DEDUPLICATION ---
            if course_code in seen_codes:
                skipped_count += 1
                continue
            
            link_tag = cols[1].find('a')
            if not link_tag: continue
            
            course_name = link_tag.get_text(strip=True)
            full_url = BASE_URL + link_tag['href']
            
            print(f"[{len(dataset)+1}] Scraping: {course_code}")
            
            details = get_course_details(full_url)
            if details:
                dataset.append({
                    'code': course_code, 
                    'name': course_name, 
                    'url': full_url, 
                    **details
                })
                seen_codes.add(course_code)
            
            # Auto-save progress
            if len(dataset) % 50 == 0:
                pd.DataFrame(dataset).to_csv('syllabi_research_progress.csv', index=False, encoding='utf-8-sig')
            
            time.sleep(0.3)

    # --- FINAL EXPORT ---
    if dataset:
        # Save JSON (Structured)
        with open('final_thesis_data.json', 'w', encoding='utf-8') as f:
            json.dump(dataset, f, ensure_ascii=False, indent=4)
        
        # Save CSV (Flattened)
        pd.DataFrame(dataset).to_csv('final_thesis_data.csv', index=False, encoding='utf-8-sig')
        
        print("\n" + "="*45)
        print("COLLECTION SUMMARY")
        print("-" * 45)
        print(f"Unique Syllabi Collected: {len(dataset)}")
        print(f"Redundant Rows Skipped:   {skipped_count}")
        print(f"Files: final_thesis_data.csv / .json")
        print("="*45)

if __name__ == "__main__":
    main()