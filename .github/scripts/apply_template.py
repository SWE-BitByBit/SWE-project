#!/usr/bin/env python3
from pathlib import Path
import sys

tex_file = Path(sys.argv[1])
template_file = Path(sys.argv[2])

if not tex_file.exists():
    print(f"File {tex_file} non trovato.")
    sys.exit(1)

lines = tex_file.read_text(encoding="utf-8").splitlines()

if lines and lines[0].strip() == "% template presente":
    print(f"Template già presente in {tex_file}")
    sys.exit(0)

template_content = template_file.read_text(encoding="utf-8")

tex_file.write_text("% template presente\n" + template_content + "\n" + "\n".join(lines), encoding="utf-8")
print("Template applicato")