import re
import sys
from collections import defaultdict

def build_compact_index(input_file, output_file):
    # Interactive Prompts
    course_title = input("Enter the Course Title (e.g., GCFA, GREM, etc.): ").strip()
    try:
        num_cols = int(input("Enter the number of columns (e.g., 2 or 3): ").strip())
    except ValueError:
        num_cols = 2
        print("Invalid input. Defaulting to 2 columns.")
    try:
        broadNum = int(input("Set Broad Term Limit (Items w/ a number of entries over this number will be ignored): ").strip())
    except ValueError:
        broadNum = 10
        print("Invalid input. Defaulting to 10 columns.")
    
    # Regex Patterns
    line_pattern = re.compile(r'^(.*?):\s*(.*)$')
    source_pattern = re.compile(r'(\d+)\(([\d,\s]+)\)')
    source_marker_pattern = re.compile(r'^\\s*')
    
    index_data = defaultdict(lambda: defaultdict(set))
    removed_count = 0

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or ':' not in line: continue
                
                match = line_pattern.match(line)
                if match:
                    raw_title = match.group(1).strip()
                    title = source_marker_pattern.sub('', raw_title)
                    source_info = match.group(2)
                    sources = source_pattern.findall(source_info)
                    
                    for book_num, pages_str in sources:
                        pages = [p.strip() for p in pages_str.split(',')]
                        index_data[title][book_num].update(pages)
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        return

    # Generate Optimized HTML
    html_content = f"""
    <html><head><style>
        @media print {{
            @page {{ margin: 0.4in; }}
        }}
        body {{ font-family: 'Arial', sans-serif; font-size: 8.5pt; margin: 10px; color: black; line-height: 1.2; }}
        header {{ 
            text-align: center; 
            border-bottom: 2px solid black; 
            margin-bottom: 8px; 
            padding-bottom: 3px;
        }}
        .index-container {{ 
            column-count: {num_cols}; 
            column-gap: 20px; 
            column-rule: 0.5px solid black; 
        }}
        /* REMOVED break-inside: avoid to allow sections to split across columns */
        .letter-section {{ margin-bottom: 8px; }} 
        
        .letter-header {{ 
            font-size: 11pt; 
            font-weight: bold; 
            border-bottom: 1px solid black; 
            margin-top: 4px; 
            margin-bottom: 2px;
            break-after: avoid;
        }}
        .entry {{ 
            display: block; /* Changed to block for better wrapping */
            margin-bottom: 2px;
            padding-left: 15px;
            text-indent: -15px; /* Creates hanging indent for wrapped lines */
        }}
        .term {{ font-weight: normal; }}
        .pages {{ font-weight: bold; }}
        h1 {{ margin: 0; font-size: 14pt; }}
    </style></head><body>
    <header><h1>{course_title} Index</h1></header>
    <div class="index-container">
    """

    current_letter = ""
    sorted_terms = sorted(index_data.keys(), key=lambda s: s.lower().lstrip('%$/*.'))

    for term in sorted_terms:
        # Check for broad term rule 
        all_pages = set()
        for b in index_data[term]:
            all_pages.update(index_data[term][b])
        
        if len(all_pages) >= broadNum:
            removed_count += 1
            continue

        clean_term = term.lstrip('%$/*.')
        first_char = clean_term[0].upper() if clean_term else "#"
        
        if first_char != current_letter:
            current_letter = first_char
            html_content += f'<div class="letter-section"><div class="letter-header">{current_letter}</div>'

        source_list = []
        for book in sorted(index_data[term].keys(), key=int):
            pages = sorted(list(index_data[term][book]), key=int)
            source_list.append(f"{book}({', '.join(pages)})")
        
        sources_final = " — " + " | ".join(source_list)
        html_content += f'<div class="entry"><span class="term">{term}</span><span class="pages">{sources_final}</span></div>'

    html_content += "</div></body></html>"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\nOptimization Complete:")
    print(f"- {removed_count} broad terms ({broadNum}+ pages) were excluded")
    print(f"- Saved to: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 SANS_Index_Generator_Final.py input.txt output.html")
    else:
        build_compact_index(sys.argv[1], sys.argv[2])