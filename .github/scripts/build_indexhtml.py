from pathlib import Path
import fnmatch as fn


#Path scomposti perchè altrimenti non si riesce a ordinare i link
C_PATH_DOCS = Path("docs/candidatura")
C_PATH_VERB_EXT = Path("docs/candidatura/verbali_esterni")
C_PATH_VERB_INT = Path("docs/candidatura/verbali_interni")

RTB_PATH_ESTERNI = Path("docs/RTB/documenti_esterni")
RTB_PATH_INTERNI = Path("docs/RTB/documenti_interni")
RTB_PATH_VERB_EXT = Path("docs/RTB/verbali_esterni")
RTB_PATH_VERB_INT = Path("docs/RTB/verbali_interni")

PB_PATH_ESTERNI = Path("docs/PB/documenti_esterni")
PB_PATH_INTERNI = Path("docs/PB/documenti_interni")
PB_PATH_VERB_EXT = Path("docs/PB/verbali_esterni")
PB_PATH_VERB_INT = Path("docs/PB/verbali_interni")


#FILE_FIRMATI = {"*_firmato.pdf"}

#Funzione per creare i link di ciascun file indipendentemente dalla sezione
def create_doc_link(file):
    #Si assume che il documento non sia un verbale
    out = ''
    filename = file.with_suffix("").name.capitalize().replace('_', ' ')
    print(f"{filename}\n")
    out = out + '<h3>' + filename +'</h3>\n<ul>\n<li>Il <a href="' + file.as_posix() + '" target="blank">file pdf</a> del ' + filename + '</li>\n</ul>\n'
    print(f"{filename}\n")
    return out

def create_verb_link(file):
    out = ''
    filename = file.with_suffix("").name
    filename = filename.replace("esterno_",'')
    filename = filename.replace("interno_",'')
    filename = filename.replace("verbale_", "Verbale del ")
    filename = filename.replace("-","/")
    out = out + '<li>\n<a href="' + file.as_posix() + '" target="blank">' + filename +'</a>\n</li>\n'
    print(f"{filename}\n")
    return out

#Legge file template e poi lo chiude dopo aver creato una variabile
with open(Path('site_template.txt'), 'r') as temp:
    template = temp.read()

#Ottieni lista di file dai percorsi
doc_candidatura = list(C_PATH_DOCS.rglob("*.pdf"))
#rimuovi verbali da doc candidatura
doc_candidatura = [f for f in doc_candidatura if fn.fnmatch(f.name,"*!verbale*")]
verb_esterni_candidatura = list(C_PATH_VERB_EXT.rglob("*.pdf"))
verb_interni_candidatura = list(C_PATH_VERB_INT.rglob("*.pdf"))

esterni_rtb = list(RTB_PATH_ESTERNI.rglob("*.pdf"))
interni_rtb = list(RTB_PATH_INTERNI.rglob("*.pdf"))
#Togli glossario da doc rtb
interni_rtb = [f for f in interni_rtb if f.exists() and f.name not in {"Glossario.pdf"}]
verb_esterni_rtb = list(RTB_PATH_VERB_EXT.rglob("*.pdf"))
verb_interni_rtb = list(RTB_PATH_VERB_INT.rglob("*.pdf"))

esterni_pb = list(PB_PATH_ESTERNI.rglob("*.pdf"))
interni_pb = list(PB_PATH_INTERNI.rglob("*.pdf"))
#Togli glossario da doc pb
interni_pb = [f for f in interni_pb if f.exists() and f.name not in {"Glossario.pdf"}]
verb_esterni_pb = list(PB_PATH_VERB_EXT.rglob("*.pdf"))
verb_interni_pb = list(PB_PATH_VERB_INT.rglob("*.pdf"))

#Recupero glossario - recupera quello della milestone più recente
file_glossario = list(RTB_PATH_INTERNI.rglob("*Glossario.pdf"))
if interni_pb:
    file_glossario = list(PB_PATH_INTERNI.rglob("*Glossario.pdf"))


#Crea sezioni
docsections = ''

#documenti PB
if esterni_pb or interni_pb or verb_interni_pb or verb_esterni_pb:
    docsections = docsections + '<section id="pb">\n<h2>PB</h2>\n'
    docs = ''
    verb_ext = ''
    verb_int = ''
    
    for file in esterni_pb:
        docs = docs + create_doc_link(file)
    for file in interni_pb:
        docs = docs + create_doc_link(file)

    if verb_esterni_pb:
        verb_ext = "<h3>Verbali esterni</h3>\n<ul>\n"
        for file in verb_esterni_pb:
            verb_ext = verb_ext + create_verb_link(file)
        verb_ext = verb_ext + "</ul>\n"

    if verb_interni_pb:
        verb_int = "<h3>Verbali interni</h3>\n<ul>\n"
        for file in verb_interni_pb:
            verb_int = verb_int + create_verb_link(file)
        verb_int = verb_int + "</ul>\n"
    docsections = docsections + docs + verb_ext + verb_int + '</section>\n'

#documenti RTB
if esterni_rtb or interni_rtb or verb_interni_rtb or verb_esterni_rtb:
    docsections = docsections + '<section id="rtb">\n<h2>RTB</h2>\n'
    docs = ''
    verb_ext = ''
    verb_int = ''
    
    for file in esterni_rtb:
        docs = docs + create_doc_link(file)
    for file in interni_rtb:
        docs = docs + create_doc_link(file)

    if verb_esterni_rtb:
        verb_ext = "<h3>Verbali esterni</h3>\n<ul>\n"
        for file in verb_esterni_rtb:
            verb_ext = verb_ext + create_verb_link(file)
        verb_ext = verb_ext + "</ul>\n"

    if verb_interni_rtb:
        verb_int = "<h3>Verbali interni</h3>\n<ul>\n"
        for file in verb_interni_rtb:
            verb_int = verb_int + create_verb_link(file)
        verb_int = verb_int + "</ul>\n"
    docsections = docsections + docs + verb_ext + verb_int + '</section>\n'

#documenti candidatura
if doc_candidatura or verb_interni_candidatura or verb_esterni_candidatura:
    docsections = docsections + '<section id="candidatura">\n<h2>Candidatura</h2>\n'
    docs = ''
    verb_ext = ''
    verb_int = ''
    
    for file in doc_candidatura:
        docs = docs + create_doc_link(file)

    if verb_esterni_candidatura:
        verb_ext = "<h3>Verbali esterni</h3>\n<ul>\n"
        for file in verb_esterni_candidatura:
            verb_ext = verb_ext + create_verb_link(file)
        verb_ext = verb_ext + "</ul>\n"

    if verb_interni_candidatura:
        verb_int = "<h3>Verbali interni</h3>\n<ul>\n"
        for file in verb_interni_candidatura:
            verb_int = verb_int + create_verb_link(file)
        verb_int = verb_int + "</ul>\n"
    docsections = docsections + docs + verb_ext + verb_int + '</section>\n'

#Glossario
if file_glossario:
    for f in file_glossario:
        docsections = docsections + '<section id="glossario">\n<h2>Glossario</h2>\n' + create_doc_link(f) + '</section>\n'

#Rimpiazza placeholder nel template
template = template.replace('[docs]', docsections)

#Scrive il nuovo file index.html con le sezioni aggiunte
output_path = Path("index.html")
output_path.parent.mkdir(parents=True, exist_ok=True)
with output_path.open('w', encoding="utf-8") as out:
    out.write(template)
    print(f"File creato con successo")





