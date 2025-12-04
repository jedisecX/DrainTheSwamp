# Louisiana State PDF Harvester (2025 Edition)

> *"The swamp has secrets. This tool finds them — legally."*

A **fully automated, compartmentalized public PDF downloader** that harvests **every publicly available PDF** from **all Louisiana state agencies**, departments, and offices using Yahoo search (`filetype:pdf` + `site:` operators).

Built for researchers, journalists, transparency advocates, and digital archivists.

**100% legal** — only downloads documents already indexed and publicly accessible.

---

### Features

- Matrix-style cyberpunk terminal interface  
- 34+ Louisiana state agencies fully compartmentalized  
- One-click **Z = Bayou Sweep Mode** (download **everything**)  
- Multi-threaded, polite downloading (8 concurrent threads)  
- Automatic subfolder organization by agency  
- CSV logs for every agency  
- Zero external dependencies beyond standard libs  
- Works on Linux, macOS, Windows (WSL/Terminal)

---

### Agencies Included

| Code | Agency |
|------|------|
| 01 | Coastal Protection and Restoration Authority |
| 02 | Dept. of Agriculture and Forestry |
| 03 | Dept. of Children and Family Services |
| 04 | Dept. of Corrections |
| 05 | Dept. of Culture, Recreation & Tourism |
| 06 | Dept. of Education |
| 07 | Dept. of Environmental Quality |
| 08 | Dept. of Health |
| 09 | Dept. of Insurance |
| 10 | Dept. of Justice (Attorney General) |
| 11 | Dept. of Natural Resources |
| 12 | Dept. of Public Safety |
| 13 | Dept. of Revenue |
| 14 | Dept. of Treasury |
| 15 | Dept. of Transportation and Development |
| 16 | Dept. of Veterans Affairs |
| 17 | Dept. of Wildlife and Fisheries |
| 18 | Division of Administration |
| 19 | GOHSEP (Emergency Preparedness) |
| 20 | Louisiana Community & Technical Colleges |
| 21 | Louisiana Economic Development |
| 22 | Ethics Administration |
| 23 | Louisiana Legislature |
| 24 | LSU System |
| 25 | Louisiana Supreme Court |
| 26 | Workforce Commission |
| 27 | Office of the Governor |
| 28 | Office of Juvenile Justice |
| 29 | Public Service Commission |
| 30 | Secretary of State |
| 31 | Southern University System |
| 32 | State Civil Service |
| 33 | University of Louisiana System |

> Press **Z** to harvest **all 34+ agencies** in one run.

---

### Installation

```bash
git clone https://github.com/yourusername/louisiana-pdf-harvester.git
cd louisiana-pdf-harvester
pip install requests beautifulsoup4 tqdm lxml
