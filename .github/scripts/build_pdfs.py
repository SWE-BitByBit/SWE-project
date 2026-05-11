#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

SRC_DIR = Path("src")
DOCS_DIR = Path("docs")
IGNORED_FILES = {"spazio_firma.tex"}

def main():
    tex_files = list(SRC_DIR.rglob("*.tex"))
    tex_files = [f for f in tex_files if f.exists() and f.name not in IGNORED_FILES]

    if not tex_files:
        print("Nessun file .tex da compilare trovato")
        return

    print("==== File .tex da compilare: ====")
    for f in tex_files:
        print(f" - {f}")

    failed_files = []

    for tex_file in tex_files:
        rel_path = tex_file.relative_to(SRC_DIR)
        output_dir = DOCS_DIR / rel_path.parent
        output_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n==============================")
        print(f"Compilando: {tex_file}")
        print(f"Output: {output_dir}")
        print(f"==============================\n")
        
        signed_file = output_dir / (tex_file.stem + "_firmato.pdf" )
        if (not signed_file.exists()):
            result = subprocess.run(
                [
                    "bash",
                    "-c",
                    f"cd '{tex_file.parent}' && "
                    f"latexmk -pdf -interaction=nonstopmode -halt-on-error -silent "
                    f"-outdir='{output_dir.resolve()}' '{tex_file.name}'"
                ]
            )

            if result.returncode != 0:
                print(f"\n❌ ERRORE compilando {tex_file}")
                failed_files.append(tex_file)
            else:
                print(f"\n✅ PDF generato correttamente: {tex_file}")
        else:
            print(f"\n PDF saltato per presenza file firmato: {tex_file}")
    if failed_files:
        print("\n=================================")
        print("FILE CHE NON HANNO COMPILATO:")
        for f in failed_files:
            print(f" - {f}")
        print("=================================\n")
        sys.exit(1)

if __name__ == "__main__":
    main()