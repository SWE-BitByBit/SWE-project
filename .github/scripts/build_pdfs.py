
#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

SRC_DIR = Path("src")
DOCS_DIR = Path("docs")
IGNORED_FILES = {"spazio_firma.tex"}

def main():
    # Se ci sono argomenti, usa quelli, altrimenti cerca tutti i .tex
    if len(sys.argv) > 1:
        tex_files = [Path(f) for f in sys.argv[1:] if Path(f).suffix == ".tex"]
    else:
        tex_files = list(SRC_DIR.rglob("*.tex"))
    
    tex_files = [f for f in tex_files if f.exists() and f.name not in IGNORED_FILES]
    
    if not tex_files:
        return

    for tex_file in tex_files:
        rel_path = tex_file.relative_to(SRC_DIR) if tex_file.is_relative_to(SRC_DIR) else tex_file
        output_dir = DOCS_DIR / rel_path.parent
        output_dir.mkdir(parents=True, exist_ok=True)

        subprocess.run(
            [
                "bash", "-c",
                f"cd '{tex_file.parent}' && "
                f"latexmk -pdf -interaction=nonstopmode -halt-on-error "
                f"-outdir='{output_dir.resolve()}' '{tex_file.name}'"
            ],
            check=True,
            capture_output=True
        )

if __name__ == "__main__":
    main()
