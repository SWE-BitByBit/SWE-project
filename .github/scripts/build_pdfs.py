#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path
import os # Importa os per os.chdir (anche se cd in bash è sufficiente)

SRC_DIR = Path("src")
DOCS_DIR = Path("docs")
IGNORED_FILES = {"spazio_firma.tex"}

def main():
    if len(sys.argv) > 1:
        tex_files = [Path(f) for f in sys.argv[1:] if Path(f).suffix == ".tex"]
    else:
        tex_files = list(SRC_DIR.rglob("*.tex"))
    
    tex_files = [f for f in tex_files if f.exists() and f.name not in IGNORED_FILES]
    
    if not tex_files:
        return

    for tex_file in tex_files:
        rel_path = tex_file.relative_to(SRC_DIR) if tex_file.is_relative_to(SRC_DIR) else tex_file
        # Directory finale dove il PDF deve risiedere
        final_output_dir = DOCS_DIR / rel_path.parent
        final_output_dir.mkdir(parents=True, exist_ok=True)

        # 1. Directory di esecuzione
        current_dir = tex_file.parent
        
        # 2. Nome del file PDF atteso
        pdf_name = tex_file.stem + ".pdf"
        
        print(f"Compiling {tex_file.name} in {current_dir}...")

        try:
            # Esegui la compilazione nella directory del file.tex
            subprocess.run(
                [
                    "bash", "-c",
                    # 🛑 NUOVO COMANDO: Nessun -outdir, compila nel posto corrente (current_dir)
                    f"cd '{current_dir}' && "
                    f"latexmk -pdf -interaction=nonstopmode -halt-on-error '{tex_file.name}'"
                ],
                check=True,
                capture_output=True # Togli questo se vuoi vedere l'output RAW in caso di errore
            )
            
            # 3. Sposta il PDF generato dalla directory di compilazione a docs/...
            generated_pdf_path = current_dir / pdf_name
            final_pdf_path = final_output_dir / pdf_name
            
            if generated_pdf_path.exists():
                generated_pdf_path.rename(final_pdf_path)
                print(f"✅ Success: Moved to {final_pdf_path}")
            else:
                print(f"⚠️ Warning: PDF file not found after successful compilation at {generated_pdf_path}")

        except subprocess.CalledProcessError as e:
            # Cattura l'errore per mostrare l'output se capture_output è True
            print(f"--- FAILED TO COMPILE {tex_file.name} ---")
            print(f"STDOUT:\n{e.stdout.decode()}")
            print(f"STDERR:\n{e.stderr.decode()}")
            print(f"Return Code: {e.returncode}")
            sys.exit(e.returncode) # Termina lo script con l'errore originale
