import re
import json

with open('src/RTB/documenti_interni/Glossario.tex', 'r', encoding='utf-8') as f:
    content = f.read()

# Espressione regolare per estrarre i termini dal glossario
# Fa il match di \term{NOME_TERMINE} catturando il termine
regex = r'\\termdefinition\{([^}]+)\}'

terms = []
matches = re.findall(regex, content)

for match in matches:
    if '/' in match:
        # Split dei termini che hanno sinonimi, es: JavaScript / JS
        sub_terms = [term.strip() for term in match.split('/')]
        sub_terms = [term for term in sub_terms if term]
        terms.extend(sub_terms)
    else:
        # Termine singolo, solo trim
        terms.append(match.strip())

with open('.github/glossary_terms.json', 'w', encoding='utf-8') as f:
    json.dump(terms, f, ensure_ascii=False, indent=2)

print(f"Estratti {len(terms)} termini")