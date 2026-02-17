import re
import json
from pathlib import Path

GLOSSARY_FILE = Path(".github/glossary_terms.json")
TERM_DEF = r"\newcommand{\term}[1]{\textbf{#1}$^\mathbf{G}$}"
IGNORE_GLOSSARY_DEF = r"\newcommand{\ignoreglossary}{}"

def load_terms():
    with GLOSSARY_FILE.open("r", encoding="utf-8") as f:
        terms = json.load(f)
    return [t.strip() for t in terms if isinstance(t, str) and t.strip()]


def insert_term_command(text: str) -> str:
    """
    Inserisce o sostituisce la definizione \newcommand{\term}.
    - Se esiste già un \newcommand{\term}{...} lo rimpiazza con TERM_DEF.
    - Se non esiste, inserisce TERM_DEF nel preambolo.
    """
    # Sostituzione del comando già presente
    text = re.sub(
        r"\\newcommand\s*\{\\term\}\s*\{[^}]*\}",
        TERM_DEF.replace("\\", r"\\"),  # Escape dei backslash per re.sub
        text
    )

    if TERM_DEF in text:
        return text

    # Inserimento comando se assente
    m = re.search(r"\\begin\{document\}", text)
    if m:
        return text[:m.start()] + TERM_DEF + "\n\n" + text[m.start():]
    else:
        return TERM_DEF + "\n\n" + text


import re

def insert_ignoreglossary_command(text: str) -> str:
    """
    Inserisce o sostituisce la definizione \\newcommand{\\ignoreglossary}{}.
    - Se esiste già un \\newcommand{\\ignoreglossary}{...} lo rimpiazza.
    - Se non esiste, lo inserisce nel preambolo (prima di \\begin{document}).
    """

    # Sostituzione del comando già presente
    text = re.sub(
        r"\\newcommand\s*\{\\ignoreglossary\}\s*\{[^}]*\}",
        IGNORE_GLOSSARY_DEF.replace("\\", r"\\"),
        text
    )

    # Se ora è presente, abbiamo finito
    if IGNORE_GLOSSARY_DEF in text:
        return text

    # Inserimento nel preambolo
    m = re.search(r"\\begin\{document\}", text)
    if m:
        return text[:m.start()] + IGNORE_GLOSSARY_DEF + "\n\n" + text[m.start():]
    else:
        return IGNORE_GLOSSARY_DEF + "\n\n" + text


def remove_all_term_wrappers(text: str) -> str:
    """
    Rimuove tutti i comandi \\term{X}, sostituendoli con X.
    """
    pattern = re.compile(r"\\term\{([^}]*)\}")
    return pattern.sub(r"\1", text)

def remove_term_wrappers(text: str, terms_set):
    """
    Rimuove \term{X} quando X NON è nel glossario.
    """
    pattern = re.compile(r"\\term\{([^}]*)\}")

    def replace(m):
        word = m.group(1)
        if word.lower() not in terms_set:
            return word
        return m.group(0)

    # ogni occorrenza di \term è sostituita dal valore restituito da replace sul match
    return pattern.sub(replace, text)


def wrap_terms(text: str, terms):
    """
    Avvolge i termini del glossario con \term{...}, evitando
    di avvolgere quelli già dentro \term{...}, \href{...}{...}, ecc.
    """
    # Pattern da proteggere (non applicare \term dentro questi)
    protected_patterns = [
        r'\\ignoreglossary\{[^}]*\}',                 # comando custom per ignorare l'applicazione di \term
        r'\\texttt\{[^}]*\}',                         # per evitare problemi con sezioni di "codice"
        r'\\term\{[^}]*\}',                          # \term{...}
        r'\\href\{[^}]*\}\{[^}]*\}',                 # \href{url}{text} - protezione completa
        r'\\url\{[^}]*\}',                           # \url{...}
        r'%.*?$',                                    # % commento
        
        # Label e riferimenti
        r'\\label\{[^}]*\}',                         # \label{...}
        r'\\ref\{[^}]*\}',                           # \ref{...}
        r'\\pageref\{[^}]*\}',                       # \pageref{...}
        r'\\nameref\{[^}]*\}',                       # \nameref{...}
        r'\\autoref\{[^}]*\}',                       # \autoref{...}
        r'\\eqref\{[^}]*\}',                         # \eqref{...}
        
        # File e path
        r'\\includegraphics(?:\[[^\]]*\])?\{[^}]*\}', # \includegraphics[opzioni]{file}
        r'\\input\{[^}]*\}',                         # \input{file}
        r'\\include\{[^}]*\}',                       # \include{file}
        r'\\graphicspath\{\{[^}]*\}\}',              # \graphicspath{{path}}
        
        # Definizioni di comandi
        r'\\newcommand\{[^}]*\}(?:\[[^\]]*\])?\{[^}]*\}', # \newcommand{\cmd}[args]{def}
        r'\\renewcommand\{[^}]*\}(?:\[[^\]]*\])?\{[^}]*\}', # \renewcommand
        r'\\providecommand\{[^}]*\}(?:\[[^\]]*\])?\{[^}]*\}', # \providecommand
        
        # Bibliografia e citazioni
        r'\\cite(?:\[[^\]]*\])?\{[^}]*\}',           # \cite[optional]{key}
        r'\\bibitem(?:\[[^\]]*\])?\{[^}]*\}',        # \bibitem[label]{key}
        r'\\bibliography\{[^}]*\}',                  # \bibliography{file}
        
        # Hyperref - link e riferimenti
        r'\\hypertarget\{[^}]*\}\{[^}]*\}',          # \hypertarget{name}{text}
        r'\\hyperlink\{[^}]*\}\{[^}]*\}',            # \hyperlink{name}{text}
        r'\\hyperref\[[^\]]*\]\{[^}]*\}',            # \hyperref[label]{text}
        r'\\hyperref\{[^}]*\}\{[^}]*\}\{[^}]*\}\{[^}]*\}', # \hyperref{url}{category}{name}{text}
        
        # Contatori
        r'\\newcounter\{[^}]*\}',                    # \newcounter{name}
        r'\\setcounter\{[^}]*\}\{[^}]*\}',           # \setcounter{counter}{value}
        r'\\addtocounter\{[^}]*\}\{[^}]*\}',         # \addtocounter{counter}{value}
        r'\\stepcounter\{[^}]*\}',                   # \stepcounter{counter}
        r'\\refstepcounter\{[^}]*\}',                # \refstepcounter{counter}
        r'\\value\{[^}]*\}',                         # \value{counter}
        
        # Ambienti
        r'\\newenvironment\{[^}]*\}(?:\[[^\]]*\])?\{[^}]*\}\{[^}]*\}', # \newenvironment{name}[args]{begin}{end}
        r'\\renewenvironment\{[^}]*\}(?:\[[^\]]*\])?\{[^}]*\}\{[^}]*\}', # \renewenvironment
        
        # Package e classi
        r'\\usepackage(?:\[[^\]]*\])?\{[^}]*\}',     # \usepackage[options]{package}
        r'\\RequirePackage(?:\[[^\]]*\])?\{[^}]*\}', # \RequirePackage[options]{package}
        r'\\documentclass(?:\[[^\]]*\])?\{[^}]*\}',  # \documentclass[options]{class}
        
        # Index e glossary
        r'\\index\{[^}]*\}',                         # \index{entry}
        r'\\glossary\{[^}]*\}',                      # \glossary{entry}
        
        # Caption con argomento opzionale (solo la parte opzionale)
        r'\\caption\[[^\]]*\]',                      # \caption[short] - protegge solo [short]
        
        # Tabelle di contenuti
        r'\\addcontentsline\{[^}]*\}\{[^}]*\}\{[^}]*\}', # \addcontentsline{file}{sec}{text}
        
        # Lunghezze
        r'\\setlength\{[^}]*\}\{[^}]*\}',            # \setlength{length}{value}
        r'\\addtolength\{[^}]*\}\{[^}]*\}',          # \addtolength{length}{value}
        r'\\newlength\{[^}]*\}',                     # \newlength{length}
    ]
    
    # Combina tutti i pattern in uno solo
    combined_pattern = '(' + '|'.join(protected_patterns) + ')'
    
    terms_sorted = sorted(terms, key=len, reverse=True)

    for t in terms_sorted:
        # Split per proteggere le parti già wrappate
        parts = re.split(combined_pattern, text)
        
        # Applica sostituzione solo alle parti con indice pari (testo non protetto)
        for i in range(0, len(parts), 2):
            pattern = r'\b' + re.escape(t) + r'\b'
            regex = re.compile(pattern, flags=re.IGNORECASE)
            parts[i] = regex.sub(lambda m: r"\term{" + m.group(0).title() + "}", parts[i])
        
        text = ''.join(parts)

    return text


def main():
    terms = load_terms()
    terms_set = {t.lower() for t in terms}

    tex_files = [
        p for p in Path(".").rglob("*.tex")
        if "glossario" not in p.name.lower()
    ]

    for path in tex_files:
        original = path.read_text(encoding="utf-8")
        text = original

        text = remove_all_term_wrappers(text)
        text = insert_term_command(text)
        text = insert_ignoreglossary_command(text)
        text = wrap_terms(text, terms)

        if text != original:
            path.write_text(text, encoding="utf-8")
            print(f"[MODIFICATO] {path}")
        else:
            print(f"[OK] {path} nessuna modifica")


if __name__ == "__main__":
    main()
