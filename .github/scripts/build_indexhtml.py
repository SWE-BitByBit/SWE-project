from pathlib import Path
import fnmatch as fn

C_PATH = Path("docs/candidatura")
RTB_PATH = Path("docs/RTB")
PB_PATH = Path("docs/PB")

#FILE_FIRMATI = {"*_firmato.pdf"}

def main():
    #Legge file template e poi lo chiude dopo aver creato una variabile

    with open(Path('site_template.txt'), 'r') as temp:
        template = temp.read()

    #Ottieni lista di file (con percorso trimmato) dalla action
    files_candidatura = list(C_PATH.rglob("*.pdf"))
    files_rtb = list(RTB_PATH.rglob("*.pdf"))
    files_pb = list(PB_PATH.rglob("*.pdf"))

    #Crea sezioni
    docsections = ''
    if files_pb:
        docsections = docsections + '<section id="pb">\n<h2>PB</h2>'
        for pb_file in files_pb:
            docsections = docsections + create_sec_links(pb_file)
        docsections = docsections + '</section>\n'

    if files_rtb:
        docsections = docsections + '<section id="rtb">\n<h2>RTB</h2>'
        for rtb_file in files_rtb:
            docsections = docsections + create_sec_links(rtb_file)
        docsections = docsections + '</section>\n'

    if files_candidatura:
        docsections = docsections + '<section id="candidatura">\n<h2>Candidatura</h2>'
        for cnd_file in files_candidatura:
            docsections = docsections + create_sec_links(cnd_file)
        docsections = docsections + '</section>\n'


    #Rimpiazza placeholder nel template
    template = template.replace('[docs]', docsections)

    #Scrive il nuovo file index.html con le sezioni aggiunte
    with open("index.html", 'w') as out:
        out.write(template)



#Funzione per creare i link di ciascun file indipendentemente dalla sezione
def create_sec_links(file):
    out = ''
    if not fn.fnmatch(file.name, '[verbale]*.pdf'):
        #Non è verbale
        filename = file.name.capitalize().replace('_', ' ')
        out = out + '<h3>' + filename +'</h3>\n<ul>\n<li>Il <a href="' + file.as_posix() + '" target="blank">file pdf</a> del ' + filename + '</li>\n</ul>\n'
    else:
        #è verbale
        filename = ''
        if '/verbali_interni/' in file:  #verbale interno
            filename = file.name.replace('verbale_', 'Verbale interno del ').replace('_',' ').replace('-','/')
        else: #verbale esterno
            filename = file.name.replace('esterno_','').replace('verbale_', 'Verbale esterno del ').replace('_',' ').replace('-','/')
            out = out + '<h3>' + filename +'</h3>\n<ul>\n<li>Il <a href="' + file.as_posix() + '" target="blank">file pdf</a> del ' + filename + '</li>\n</ul>\n'
    return out

if __name__ == "__main__":
    main()

