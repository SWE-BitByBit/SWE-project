import os
import subprocess
from pathlib import Path

SRC_DIR = Path("src")
DOCS_DIR = Path("docs")

# 🔧 File da ignorare: aggiungi qui altri nomi in futuro
IGNORED_FILES = {"spazio_firma.tex"}

def main():
    tex_files = [f for f in SRC_DIR.rglob("*.tex") if f.name not in IGNORED_FILES]
    if not tex_files:
        print("Nessun file .tex da compilare trovato in src/")
        return

    for tex_file in tex_files:
        rel_path = tex_file.relative_to(SRC_DIR)
        output_dir = DOCS_DIR / rel_path.parent
        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"Compilo: {tex_file} → {output_dir}")

        try:
            # latexmk eseguito nella cartella del file
            # Output PDF nella cartella corrispondente in docs/
            subprocess.run(
                [
                    "bash",
                    "-c",
                    f"cd '{tex_file.parent}' && "
                    f"latexmk -pdf -interaction=nonstopmode -halt-on-error "
                    f"-outdir='{output_dir}' '{tex_file.name}'"
                ],
                check=True
            )

        except subprocess.CalledProcessError as e:
            print(f"Errore durante la compilazione di {tex_file}")
            print(f"   Codice di ritorno: {e.returncode}")

    print("✅ Compilazione completata.")

if __name__ == "__main__":
    main()
