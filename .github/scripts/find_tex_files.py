#!/usr/bin/env python3
import os

# Esplora ricorsivamente tutte le cartelle a partire dalla root (".")
for root, _, files in os.walk("."):
    for f in files:
        # Considera solo i file .tex, tranne "spazio_firma.tex"
        if f.endswith(".tex") and f != "spazio_firma.tex":
            # Stampa il percorso relativo (root + nome file)
            print(os.path.join(root, f))
