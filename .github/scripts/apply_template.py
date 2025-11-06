#!/usr/bin/env python3
from pathlib import Path
import sys

template_file = Path(sys.argv[-1])
tex_files = [Path(f) for f in sys.argv[1:-1]]

template_content = template_file.read_text(encoding="utf-8")

for tex_file in tex_files:
    if not tex_file.exists():
        continue
    
    lines = tex_file.read_text(encoding="utf-8").splitlines()
    
    if lines and lines[0].strip() == "% template presente":
        continue
    
    tex_file.write_text(
        "% template presente\n" + template_content + "\n" + "\n".join(lines),
        encoding="utf-8"
    )