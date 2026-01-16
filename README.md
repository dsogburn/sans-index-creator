# SANS Index Creator (Compact & Print-Optimized)
This repository is a fork of [Ge0rg3/sans-index-creator](https://github.com/Ge0rg3/sans-index-creator), enhanced with a high-density, print-optimized formatter. It is specifically designed for SANS GIAC exams (such as GICSP, SEC504, or FOR508) where rapid lookup speed and minimal physical paper bulk are critical for success.

---

## 🛠️ How it Works
The indexing process is split into two distinct steps:

**Extraction:** Automatically parse your SANS PDFs to create a raw text index.

**Formatting:** Convert that text into a professional, multi-column, compact HTML file ready for printing.

---

## Step 1: Extract the Index (Original Script)
Use the original extraction logic to pull terms and page references from your courseware.

1) Download course pdf from https://www.sans.org/account/download-materials
2) Remove pdf password through qpdf:
  `qpdf --password=enterpasswordhere -decrypt "InputFilename.pdf" "OutputFilename.pdf"`
3) Convert new pdf to txt:
  `pdftotext unencryptedfile.pdf coursetxt.txt`
4) Create index based off txt file (this can take ~5 minutes because each word is searched for in the full English dictionary):
  `python3 sans_indexer.py -i coursetxt.txt -o courseindex.txt -n "John Smith"`

Please note that the -n field is used to split the txt into pages, as we use the License name as the page delimiter (it is the only string persistant across pages).

If your course has multiple books, you can combine the indexes created by `sans_indexer.py` into one index with the following command:
`python3 index_combiner.py index1.txt index2.txt index3.txt > combined_index.txt`. This will create an index which displays both book number and page number of each keyword.


### Output example
Here is a snippet of the output for a course pdf:
```
shell-item: 2(38)
shellbag-hives: 2(59)
shellbag: 3(110, 260)
shellbags: 1(113, 286) | 3(244, 286)
shelllinkheader: 2(9)
shellnoroam: 2(55) | 3(287)
shift+delete: 2(225)
shimcache: 1(47, 208) | 2(239) | 3(5)
shimcacheparser.py: 1(210)
shimcacheparser: 1(210)
showkeys: 1(136)
sic-c: 1(275)
sid: 2(224, 225, 263, 264, 269) | 3(286)
siem: 1(257) | 2(180)
sign-out: 3(229)
signed-off: 3(229)
signedin_time: 3(205, 206, 287)
signedinuser.json: 3(186)
signons.sqlite: 3(128)
simple-to-create-and-modify: 1(46)
sin: 2(19)
single-use: 3(194)
single-user: 1(11)
sister: 1(89)
site-by-site: 3(189)
site-specific: 3(181)
site/remove: 3(248)
site_engagement: 3(205, 287)
sitecollectionadminadded: 1(243)
sites/: 3(197)
six: 1(17, 19, 36) | 2(180, 263) | 3(174, 187)
siz: 2(151)
sizeofimage: 1(213)
skydrive: 1(10, 11, 231)
skype: 1(10, 36, 37, 75, 86, 89, 117, 223, 230) | 2(28, 69, 130, 201, 275, 330) | 3(110, 260, 287)
sleuthkit: 1(136)
```

---

## Step 2: Format for Printing (txt2index.py)
Once you have your combined_index.txt, use the Compact Generator to create a clean, Black & White, multi-column index.


### Usage
1) Run the script and follow the interactive prompts for the Course Title and Column Count: `python3 txt2index.py combined_index.txt Printable_Index.html`
2) Open GICSP_Index.html in any modern web browser (Chrome, Edge, or Firefox) and Print to PDF.

### Recommended Print Settings:

Layout: Portrait

Margins: Small or None

Headers/Footers: Unchecked

Background Graphics: Checked (to ensure formatting renders correctly)

### Example Output

<img width="529" height="364" alt="image" src="https://github.com/user-attachments/assets/9afdd9fb-bb8b-4f12-b4c0-92f1f78724e5" />


---

## 📜 Credits
Core Extraction Logic: Originally created by [Ge0rg3](https://github.com/Ge0rg3/sans-index-creator).

Compact Formatter: Added by [dsogburn](https://github.com/dsogburn) to optimize the index for physical exam use.

---

## ⚖️ Disclaimer & Academic Integrity
This tool is a formatter designed to help students organize their own personal study notes. 
- **User Responsibility:** Users are responsible for ensuring their use of this tool complies with the SANS/GIAC Academic Integrity Policy.
- **No Content Included:** This repository does NOT contain SANS courseware, copyrighted text, or exam content. 
- **Usage:** This script should only be used with data the student has generated themselves from their own legally obtained course materials.

---

## ⚖️ License
This project is licensed under the MIT License.

