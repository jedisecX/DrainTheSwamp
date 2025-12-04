#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import csv
import threading
import time
import os
import re
import random
import sys
from urllib.parse import urljoin, urlparse, unquote
from tqdm import tqdm

# === MATRIX MODE ===
if os.name == 'nt':
    os.system('cls')
else:
    os.system('clear')

# Comment out if you want full rain on startup
# def matrix_rain(): ... (same as before, but skipping for brevity)

# ------------------------------------------------------------------
# Core engine
# ------------------------------------------------------------------
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Safari/605.1.15',
]

lock = threading.Lock()
downloaded_count = failed_count = 0
current_agency_name = ""

# ------------------------------------------------------------------
# LOUISIANA STATE AGENCIES (All Compartmentalized – Dec 2025)
# ------------------------------------------------------------------
AGENCIES = {
    "01": ("Coastal Protection and Restoration Authority", "site:coastal.la.gov filetype:pdf"),
    "02": ("Department of Agriculture and Forestry", "site:ldaf.la.gov filetype:pdf"),
    "03": ("Department of Children and Family Services", "site:dcfs.louisiana.gov filetype:pdf"),
    "04": ("Department of Corrections", "site:doc.louisiana.gov filetype:pdf"),
    "05": ("Department of Culture, Recreation, and Tourism", "site:crt.state.la.us filetype:pdf"),
    "06": ("Department of Education", "site:doe.louisiana.gov filetype:pdf"),
    "07": ("Department of Environmental Quality", "site:deq.la.gov filetype:pdf"),
    "08": ("Department of Health", "site:ldh.louisiana.gov filetype:pdf"),
    "09": ("Department of Insurance", "site:ldi.la.gov filetype:pdf"),
    "10": ("Department of Justice", "site:ag.louisiana.gov filetype:pdf"),
    "11": ("Department of Natural Resources", "site:dnr.louisiana.gov filetype:pdf"),
    "12": ("Department of Public Safety", "site:dps.louisiana.gov filetype:pdf"),
    "13": ("Department of Revenue", "site:revenue.louisiana.gov filetype:pdf"),
    "14": ("Department of Treasury", "site:treasury.la.gov filetype:pdf"),
    "15": ("Department of Transportation and Development", "site:dotd.la.gov filetype:pdf"),
    "16": ("Department of Veterans Affairs", "site:vetaffairs.la.gov filetype:pdf"),
    "17": ("Department of Wildlife and Fisheries", "site:wlf.louisiana.gov filetype:pdf"),
    "18": ("Division of Administration", "site:doa.la.gov filetype:pdf"),
    "19": ("Governor's Office of Homeland Security and Emergency Preparedness", "site:gohsep.la.gov filetype:pdf"),
    "20": ("Louisiana's Community and Technical College System", "site:lctcs.edu filetype:pdf"),
    "21": ("Louisiana Division of Administrative Law", "site:adminlaw.state.la.us filetype:pdf"),
    "22": ("Louisiana Economic Development", "site:opportunitylouisiana.com filetype:pdf"),
    "23": ("Louisiana Ethics Administration Program", "site:ethics.la.gov filetype:pdf"),
    "24": ("Louisiana Legislature", "site:legis.la.gov filetype:pdf"),
    "25": ("Louisiana State University System", "site:lsu.edu filetype:pdf"),
    "26": ("Louisiana Supreme Court", "site:lasc.org filetype:pdf"),
    "27": ("Louisiana Workforce Commission", "site:laworks.net filetype:pdf"),
    "28": ("Office of the Governor", "site:gov.louisiana.gov filetype:pdf"),
    "29": ("Office of Juvenile Justice", "site:ojj.la.gov filetype:pdf"),
    "30": ("Public Service Commission", "site:lpsc.louisiana.gov filetype:pdf"),
    "31": ("Secretary of State", "site:sos.la.gov filetype:pdf"),
    "32": ("Southern University System", "site:sus.edu filetype:pdf"),
    "33": ("State Civil Service", "site:civilservice.louisiana.gov filetype:pdf"),
    "34": ("University of Louisiana System", "site:ulsystem.edu filetype:pdf"),
}

class DownloadThread(threading.Thread):
    def __init__(self, url, filename, semaphore):
        super().__init__()
        self.url = url
        self.filename = filename
        self.semaphore = semaphore

    def run(self):
        global downloaded_count, failed_count, current_agency_name
        with self.semaphore:
            time.sleep(0.8)
            try:
                r = requests.get(self.url, stream=True, timeout=40,
                                 headers={'User-Agent': random.choice(USER_AGENTS)})
                r.raise_for_status()
                if 'pdf' not in r.headers.get('content-type', '').lower() and not self.url.lower().endswith('.pdf'):
                    return

                safe = re.sub(r'[<>:"/\\|?*]', '_', self.filename)
                if not safe.lower().endswith('.pdf'):
                    safe += '.pdf'

                folder = os.path.join("la_downloads", current_agency_name.replace(" ", "_").replace("/", "_"))
                os.makedirs(folder, exist_ok=True)
                path = os.path.join(folder, safe)

                with lock:
                    with open(path, 'wb') as f:
                        for c in r.iter_content(32768):
                            if c: f.write(c)
                    downloaded_count += 1
                    print(f"\033[92m[+] {current_agency_name[:20]:20} ▸ {safe[:45]}\033[0m")
            except:
                with lock:
                    failed_count += 1

def get_pdf_links(query, name):
    pdfs = set()
    s = requests.Session()
    for p in range(18):
        params = {'p': query, 'b': p * 10 + 1}
        s.headers.update({'User-Agent': random.choice(USER_AGENTS)})
        try:
            r = s.get('https://search.yahoo.com/search', params=params, timeout=20)
            soup = BeautifulSoup(r.text, 'html.parser')
            for a in soup.find_all('a', href=True):
                h = a['href']
                if '/RU=' in h:
                    m = re.search(r'/RU=(.*?)/RK=', h)
                    url = unquote(m.group(1)) if m else None
                else:
                    url = h if h.startswith('http') else None
                if url and url.lower().endswith('.pdf'):
                    pdfs.add(url)
            print(f"  \033[93m[{name[:25]:25}] Page {p+1:2} → {len(pdfs):4} PDFs\033[0m")
            time.sleep(2)
        except: pass
    return list(pdfs)

def launch_downloads(urls, agency):
    global downloaded_count, failed_count, current_agency_name
    downloaded_count = failed_count = 0
    current_agency_name = agency

    csv_name = f"la_downloads_{agency.replace(' ', '_')}.csv"
    with open(csv_name, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['URL', 'Filename'])
        sem = threading.Semaphore(8)
        threads = []
        for url in tqdm(urls, desc=f"\033[96m{agency}\033[0m", leave=False):
            fn = os.path.basename(urlparse(url).path) or f"doc_{hash(url)}.pdf"
            w.writerow([url, fn])
            t = DownloadThread(url, fn, sem)
            threads.append(t)
            t.start()
        for t in threads: t.join()

    print(f"\n\033[92m{agency} complete → {downloaded_count} saved | {failed_count} failed\033[0m\n")

# ------------------------------------------------------------------
# LOUISIANA MATRIX MENU
# ------------------------------------------------------------------
def matrix_menu():
    os.system('clear' if os.name != 'nt' else 'cls')
    print("\033[92m")
    print("╔" + "═" * 78 + "╗")
    print("║       LOUISIANA STATE PDF HARVESTER – COMPARTMENTALIZED EDITION       ║")
    print("╚" + "═" * 78 + "╝\033[0m")
    print("\033[93m")
    for code, (name, _) in AGENCIES.items():
        print(f"  \033[96m[{code}]\033[0m  {name}")
    print("\033[92m")
    print("  [Z]  →  DOWNLOAD ALL LOUISIANA AGENCIES (BAYOU SWEEP MODE)")
    print("  [Q]  →  Exit the Bayou")
    print("\033[0m" + "─" * 80)
    return input("\033[92mThe swamp awaits... → \033[0m").strip().upper()

# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
if __name__ == "__main__":
    os.makedirs("la_downloads", exist_ok=True)
    print("\033[92m\n> Welcome to the Louisiana matrix. PDFs incoming.\033[0m")
    time.sleep(1.5)

    while True:
        choice = matrix_menu()
        if choice == "Q":
            print("\033[91m> Gator's gone.\033[0m")
            break
        elif choice == "Z":
            print("\033[91m\n> BAYOU SWEEP MODE – ALL LOUISIANA AGENCIES\033[0m")
            for code in AGENCIES:
                name, q = AGENCIES[code]
                print(f"\n\033[95m{'='*25} [{code}] {name} {'='*25}\033[0m")
                urls = get_pdf_links(q, name)
                if urls:
                    launch_downloads(urls, name)
            print("\033[92m\n> Full Louisiana archive harvested.\033[0m")
            break
        elif choice in AGENCIES:
            name, q = AGENCIES[choice]
            print(f"\n\033[96m> Diving into {name}...\033[0m")
            urls = get_pdf_links(q, name)
            launch_downloads(urls, name)
        else:
            print("\033[91m> Invalid path.\033[0m")

        if choice != "Z":
            if input("\033[93m> Another dive? (y/n): \033[0m").lower() != "y":
                break
