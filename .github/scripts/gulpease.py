import re
import csv
from pathlib import Path

# =========================
# CONFIGURAZIONE
# =========================

PROJECT_ROOT = Path("src")
AREE = ["RTB", "PB"]  # PB può non esistere

OUTPUT_CSV = Path("metrics-measurements/gulpease_index.csv")

# =========================
# DOCUMENTI DA MISURARE
# =========================
# Qui controlli TU cosa entra nel CSV

DOCUMENTI = {
    "Analisi dei requisiti": {
        "type": "file",
        "filename": "analisi_dei_requisiti.tex"
    },
    "Piano di progetto": {
        "type": "file",
        "filename": "piano_di_progetto.tex"
    },
    "Piano di qualifica": {
        "type": "file",
        "filename": "piano_di_qualifica.tex"
    },
    "Specifica tecnica": {
        "type": "file",
        "filename": "specifica_tecnica.tex"
    },
    "Glossario": {
        "type": "file",
        "filename": "Glossario.tex"
    },
    "Norme di progetto": {
        "type": "file",
        "filename": "norme_di_progetto.tex"
    },
    "Verbali interni": {
        "type": "folder",
        "folder": "verbali_interni"
    },
    "Verbali esterni": {
        "type": "folder",
        "folder": "verbali_esterni"
    }
}

# =========================
# FUNZIONI
# =========================

def clean_latex(text: str) -> str:
    text = re.sub(r"\\[a-zA-Z]+\{.*?\}", " ", text)
    text = re.sub(r"\\[a-zA-Z]+", " ", text)
    text = re.sub(r"\$.*?\$", " ", text)
    text = re.sub(r"[{}]", " ", text)
    return text


def gulpease(text: str) -> float:
    letters = len(re.findall(r"[a-zA-Zàèéìòù]", text))
    words = len(text.split())
    sentences = len(re.findall(r"[.!?]", text))

    if words == 0 or sentences == 0:
        return 0.0

    return round(89 + (300 * sentences - 10 * letters) / words, 2)


def find_file_by_name(base: Path, filename: str):
    return list(base.rglob(filename))


# =========================
# CALCOLO METRICHE
# =========================

rows = []

for doc_name, cfg in DOCUMENTI.items():
    aggregated_text = ""

    for area in AREE:
        area_path = PROJECT_ROOT / area
        if not area_path.exists():
            continue

        if cfg["type"] == "file":
            files = find_file_by_name(area_path, cfg["filename"])

        else:  # folder
            folder = area_path / cfg["folder"]
            files = folder.rglob("*.tex") if folder.exists() else []

        for tex in files:
            try:
                aggregated_text += tex.read_text(
                    encoding="utf-8",
                    errors="ignore"
                ) + "\n"
            except Exception as e:
                print(f"Errore lettura {tex}: {e}")

    score = gulpease(clean_latex(aggregated_text))

    rows.append({
        "Documento": doc_name,
        "Indice_Gulpease": score
    })

# =========================
# SCRITTURA CSV
# =========================

OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(
        csvfile,
        fieldnames=["Documento", "Indice_Gulpease"]
    )
    writer.writeheader()
    writer.writerows(rows)

print("✔ CSV Indice di Gulpease generato correttamente.")
