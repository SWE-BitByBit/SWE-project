import sys
from pathlib import Path
import os
from bs4 import BeautifulSoup, Tag

GITHUB_PAGE_FILE = Path("index.html") 
SRC_DIR = Path("src")
DOCS_DIR = Path("docs")

# Mappaggio: associa la directory PDF di destinazione (Path) al suo segnaposto nell'HTML e al prefisso del testo.
# AGGIORNA QUESTO DIZIONARIO PER TUTTE LE TUE SEZIONI DINAMICHE!
SECTION_MAP = {

    # candidatura/verbali_esterni
    DOCS_DIR / "candidatura" / "verbali_esterni": {
        "html_id": "",
        "title_prefix": "Verbale del "
    },

    # candidatura/verbali_interni
    DOCS_DIR / "candidatura" / "verbali_interni": {
        "html_id": "",
        "title_prefix": "Verbale del "
    },

    # documenti_interni/glossario.pdf
    DOCS_DIR / "documenti_interni" : {
        "html_id": "",
        "title_prefix": ""
    }

    #documenti_interni/norme_di_progetto.pdf
    DOCS_DIR / "documenti_interni" : {
        "html_id": "",
        "title_prefix": ""
    }
}


def get_placeholder_for_tex_file(tex_file: Path) -> Path | None:

    rel_path = tex_file.relative_to(SRC_DIR) if tex_file.is_relative_to(SRC_DIR) else tex_file
    pdf_directory_key = DOCS_DIR / rel_path.parent
    for mapped_path in SECTION_MAP.keys():
        if mapped_path == pdf_directory_key:
            return mapped_path
            
    return None

def update_html_section(pdf_directory: Path, insert_info: dict):
    
    try:
        with open(GITHUB_PAGE_FILE, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        ul_element = soup.find('ul', id=insert_info['html_id'])

        if not ul_element:
            print(f"Errore: Elemento <ul> con ID='{insert_info['html_id']}' non trovato.")
            return

        ul_element.clear()
        
        pdf_files = sorted(pdf_directory.glob("*.pdf"))
        
        for pdf_path in pdf_files:
            link_text = pdf_path.stem.replace('verbale_', '').replace('_', ' ').title()
            relative_pdf_url = pdf_path.as_posix() 

            new_li = Tag(name='li')
            li_text = soup.new_string(f'{insert_info["title_prefix"]}')
            new_li.append(li_text)
            new_a = Tag(name='a', attrs={
                'href': relative_pdf_url,
                'target': '_blank'
            })
            new_a.append(soup.new_string(link_text))
            new_li.append(new_a)
            
            ul_element.append(new_li)
            ul_element.append(soup.new_string('\n'))

        with open(GITHUB_PAGE_FILE, 'w', encoding='utf-8') as f:
            f.write(str(soup.prettify()))
        
        print(f"✅ Sezione ID='{insert_info['html_id']}' aggiornata. Rigenerati {len(pdf_files)} link.")

    except Exception as e:
        print(f"Errore durante l'aggiornamento: {e}")


def main():
    if len(sys.argv) < 2:
        print("Errore: Nessun file .tex passato come argomento.")
        return

    directories_to_update = set()

    for tex_file_str in sys.argv[1:]:
        tex_file_path = Path(tex_file_str)
        
        pdf_dir_key = get_placeholder_for_tex_file(tex_file_path)
        
        if pdf_dir_key and pdf_dir_key in SECTION_MAP:
            directories_to_update.add(pdf_dir_key)

    if directories_to_update:
        for pdf_dir in directories_to_update:
            insert_info = SECTION_MAP[pdf_dir]
            update_html_section(pdf_dir, insert_info)
    else:
        print("Nessuna directory PDF corrispondente ai file .tex modificati trovata per l'aggiornamento HTML.")


if __name__ == "__main__":
    main()

