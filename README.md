# Logo3D

## Requisits

Per tal d'executar el codi d'aquest projecte, en primer lloc caldrà tenir instal·lat Python 3 i ANTLR4. El desenvolupament s'ha realitzat utilitzant concretament la versió `3.9.5` de Python i la `4.9.2` de ANTLR.

A més a més serà necessari instal·lar dos mòduls de Python: el runtime d'ANTLR4 per Python i VPython. El primer serà necessari per tal d'utilitzar ANTLR amb Python mentre que el segón l'utilitzarem per dibuixar gràfics 3D al navegador de forma fàcil. Per tal d'instal·lar-los mitjançant `pip` només haurém d'executar la següent commanda:

```
pip install -r requirements.txt
```

## Generar gramàtica

Abans d'executar res haurem de generar el codi Python de la gràmatica utilitzant `antlr4`. Ho podem fer amb la següent commanda:

```
antlr4 -Dlanguage=Python3 -no-listener -visitor logo3d.g
```

Amb això ja tindriem tot lo necessari per executar l'interpret.

## Execució

Per executar l'interpret utilitzarem la següent comanda:


```
python logo3d.py <programa> <main>* <parametres>*
```

On `programa` és el nom del fitxer `.l3d` que es vol interpretar, `main` és el nom de la primera funció a executar i `parametres` són els seus parametres (separats per espais). Cal recalcar que tant la funció main com els seus parametres són arguments opcionals, en cas de no ser especificats s'intentarà trobar una funció amb la capçalera `main()`.

## Estructura del projecte

El projecte està estructurat en els següents fitxers:
- `turtle3d.py`: client de gràfics tortuga en un espai de tres dimensions implementat amb VPython.
- `logo3d.g`: especificació de la gràmatica del llenguatge Logo3D feta amb ANTLR4.
- `visitor.py`: classe útil per visitar i interpretar l'arbre generat per la gramàtica de Logo3D.
- `logo3d.py`: programa principal, obté els arguments de l'usuari per consola i executa l'interpret.

A continuació veurem detalladament com funcióna cada part.

## Turtle3D

Turtle3D és una classe que ens permetrá renderitzar gràfics 3D utilitzant el sistema de tortuga en un espai de tres dimensions. El seu constructor accepta els següents parametres opcionals:

- `strokeColor`: el seu tipus esperat és una tupla amb tres floats entre 0 i 1 i simbolitza el color del pinzell en espai rgb. El seu valor per defecte és `(1, 0, 0)`.
- `strokeWeight`: el seu tipus esperat és un float i simbolitza el tamany del pinzell. El seu valor per defecte és 0.1.
- `backgroundColor`: el seu valor esperat és una tupla amb tres floats entre 0 i 1 i simbolitza el color de fons de la finestra en espai rgb. El seu valor per defecte és `(0, 0, 0)`.
- `windowHeight`: el seu valor esperat és un enter i simbolitza l'alçada de la finestra de l'escena en píxels. El seu valor per defecte és `1000`.
- `windowWidth`: el seu valor esperat és un enter i simbolitza l'amplada de la finestra de l'escena en píxels. El seu valor per defecte és `1000`.

En el constructor de la classe és on es crea la instància de l'escena de VPython amb el tamany i el color de fons especificats.

La forma en la que he implementat aquesta classe és prou senzilla. Les variables que la formen són aquestes:

- `visible`: bool que guarda si la tortuga està amagada o no. Inicialment és `true`.
- `position`: vpython.vector que guarda la posició actual de la tortuga. Inicialment és `vector(0, 0, 0)`.
- `head`: vpython.vector que guarda la posició actual de la tortuga. Inicialment és `vector(0, 0, 0)`.
- `alpha`: angle de rotació horitzontal en graus sexagesimals, útil per computar l'axis. Inicialment és `0`.
- `beta`: angle de rotació vertical en graus sexagesimals, útil per computar l'axis. Inicialment és `0`.
- `strokeColor`: vpython.vector que guarda el color de traç de la tortuga. El seu valor inicial és el `strokeColor` del constructor.
- `strokeWeight`: float que guarda el tamany del traç de la tortuga. El seu valor inicial és el `strokeWeight` del constructor.

Les funcions són les següents:

- `color(red, green, blue)`: actualitza la variable de color amb els nous valors especificats.
- `up(rotation)`: augmenta l'angle de rotació vertical `rotation` graus.
- `down(rotation)`: disminueix l'angle de rotació vertical `rotation` graus.
- `left(rotation)`: augmenta l'angle de rotació horitzontal `rotation` graus.
- `right(rotation)`: disminueix l'angle de rotació horitzontal `rotation` graus.
- `forward(size)`: actualitza el vector de direcció de la tortuga, en el cas de ser visible dibuixa el traç amb una llargada de `size` i actualitza la seva posició.
- `backward(size)`: fa el mateix que forward però es mou i traça en direcció contraria.
- `hide()`: fa invisible la tortuga.
- `show()`: fa visible la tortuga.
- `home()`: fa "reset" de la variable de posició posant-la a l'eix de coordenades.

Per tal d'implementar `forward` i `backward` sense repetir codi he creat aquestes dues funcions privades:

- `__computeHead(size)`: utilitza funcions trigonomètriques per computar el vector direccional de la tortuga segons els seus angles i el retorna multiplicat per `size` (un float que indica el tamany del traç).
- `__draw()`: utilitza les funcions de VPython per dibuixar un cilindre i dues esferes per arrodonir el traç en l'estat actual de la tortiga i actualitza la variable de posició.

## Logo3D

### Gramàtica

La definició de la gramàtica es troba en el fitxer logo3d.g.

La gramàtica dona suport a tres tipus:
- Identificador (`ID`): permet lletres majuscules i minuscules, números i barra baixa, el primer caràcter no pot ser un número.
- Enter (`INT`): permet només números.
- Decimal (`DEC`): permet un o més números seguits de un punt seguit de un o més números.

En quant a les regles, he definit 4 tipus de regla diferents: `expr`, `boolExpr`, `stat` i `procedure`. Només m'ha fet falta diferenciar entre aquestes per tal de definir la gramàtica de Logo 3D. La jerarquia de regles amb les corresponents subregles és la següent:

- Expressions (`expr`):
    - Negació: `-expr`
    - Multiplicació: `expr * expr`
    - Divisió: `expr / expr`
    - Suma: `expr + expr`
    - Resta: `expr - expr`
    - Enter: `INT`
    - Decimal: `DEC`
    - Variable: `ID`
- Expressions booleanes (`boolExpr`):
    - Major: `expr > expr`
    - Menor: `expr < expr`
    - Major o igual: `expr >= expr`
    - Menor o igual: `expr < expr`
    - Igual: `expr == expr`
    - Not equal: `expr != expr`
- Statements (`stat`):
    - Assignació: `ID := expr`
    - Lectura per consola : `>> ID`
    - Escriptura per consola: `>> expr`
    - Bucle while: `WHILE boolExpr DO stat* END`
    - Bucle for: `FOR ID FROM expr TO expr DO stat* END`
    - If then else: `IF boolExpr THEN stat* (ELSE stat*)? END`
    - Crida a un procediment: `ID((expr(,expr)*)?)`
- Definició d'un procediment (`procedure`)
    - `PROC ID((ID(,ID)*)?) IS stat* END`

El punt d'entrada o root de la gramàtica és zero o més procediments.

Finalment he afegit regles per tal d'ignorar espais, salts de línia i comentaris.

### Visitor

En el cas del visitor **l'explicació de com funciona es pot trobar en els comentaris del propi codi** del fitxer `visitor.py`. Resumidament la classe `Visitor` hereda de la classe `logo3dVisitor` generada a partir del fitxer de gramàtica i implementa la funcionalitat de cada una de les regles vistes en l'apartat anterior.

El constructor de la classe necessita rebre el nom de la funció inicial així com una llista amb els valors dels seus parametres per tal de saber on començar.

En quant a la integració amb els gràfics tortuga, la classe `Visitor` crea una instància de `Turtle3D` en el seu constructor que permetrà generar gràfics 3D quan sigui necessari a mesura que es va interpretant el programa.

### Programa principal

El programa principal `logo3d.py` en primer lloc llegeix per consola el nom del fitxer `.l3d` a executar així com la primera funció a executar i els seus corresponents parametres. Si cap funció és especificada s'assignarà de nom `main` i una llista de parametres buida.

En segón lloc fa parsing del programa i visita el seu arbre començant per l'arrel i utilitzant la classe `Visitor`.

## Extensións

### Extensió #1: Log

La primera extensió que he implementat ha estat una funció de log. Aquesta funció és semblant al write però en comptes de mostrar expressions per la consola el que mostra és strings.

El primer he fet ha estat definir un tipus `STR` a la gramàtica el qual consisteix en un conjunt de zero o més lletres, numeros o espais entre cometes.

```
STR : '"'[a-zA-Z0-9 ]*'"' ;
```

Utilitzant aquest nou tipus he creat una regla nova anomenada `stringExpr` la qual es compleix al trobar "àtoms" del tipus `STR`.

```
stringExpr : STR #atomString ;
```

La funció de visita de la classe `Visitor` per aquesta regla és molt senzilla, només converteix la regla a text i la retorna:

```python
def visitAtomString(self, ctx):
    l = list(ctx.getChildren())
    # l[0]
    # tant sols retornem el text del fill
    return l[0].getText()
```

Finalment he definit una nova regla dins dels statements (regla `stat`) amb la sintaxi de la crida a la funció de log:

```
'LOG' stringExpr #log
```

La funció de visita de la classe `Visitor` per aquesta regla tant sols ha de fer un print de la string eliminant les cometes:

```python
def visitLog(self, ctx):
    l = list(ctx.getChildren())
    # LOG l[1]
    # visitem l'expressió i mostrem el log per pantalla eliminant les cometes del principi i del final
    print(self.visit(l[1])[1:-1])
```

### Extensió #2: Switch

La segona extensió que he fet ha estat el típic switch. Pot ser especialment útil ja que la sintaxi del if-then-else no dona suport a "else if" i per fer check de moltes condicions sense tal pot ser una mica farragós. Així doncs  he afegit la següent regla als statements de la gramàtica:

```
'SWITCH' ID ('CASE' expr 'DO' stat*)* ('DEFAULT' 'DO' stat*)? 'END' #switch
```

Com podem veure, el switch està format per la keyword `SWITCH` seguida de la variable que volem comparar seguida de mútiples casos. Els casos estàn indicats amb la keyword `CASE` seguida de l'expressió que volem comparar seguida seguida de la keyword `DO` seguida dels mútiples statements que s'executaràn en cas de que la comparació sigui certa. Pot haver-hi un cas per defecte al final de tot, que s'executarà en cas de que cap dels comparacions dels altres casos hagi esdevingut certa, aquest ve indicat per la keyword `DEFAULT` seguida de la keyword `DO` seguida de els statements a executar. Finalment trobem la keyword `END` que indica el final del bloc.

El switch s'executarà seqüencialment de dalt cap a baix i pararà en el primer cas que compleixi la comparació, comparacions repetides no s'executaran.

La forma en la que ha estat implementada la visita del switch en el `Visitor` és la següent:


```python
def visitSwitch(self, ctx):
    l = list(ctx.getChildren())
    # SWITCH ID (CASE expr DO stat*)* (DEFAULT DO stat*)? END
    variableName = l[1].getText()
    # comprovem que la variable que es vol avaluar s'ha declarat previament
    if variableName not in self.variables:
        raise Exception('Variable "{name}" not found'.format(name=variableName))
    variableValue = self.variables[variableName]
    childIndex = 2
    scope = ''
    # iterem els elements de la regla guardant el scope en cada pas
    while True:
        # en el cas de trobar un CASE, canviem el scope i seguim
        if l[childIndex].getText() == 'CASE':
            scope = 'CASE'
            childIndex += 1
        # en el cas de trobar un DEFAULT, canviem el scope i seguim
        elif l[childIndex].getText() == 'DEFAULT':
            scope = 'DEFAULT'
            childIndex += 2  # saltem el DO
        # en el cas de trobar un END, sortim del bucle
        elif l[childIndex].getText() == 'END':
            break
        # en el cas d'estar en el scope DEFAULT, avaluem els statements
        # al trobar END sortim del bucle
        elif scope == 'DEFAULT':
            while l[childIndex].getText() != 'END':
                self.visit(l[childIndex])
                childIndex += 1
            break
        # en el cas de que la condició d'un CASE es compleixi, avaluem els statements
        # al trobar CASE, END o DEFAULT sortim del bucle
        elif variableValue == self.visit(l[childIndex]):
            childIndex += 2  # saltem el DO
            while l[childIndex].getText() not in ['CASE', 'DEFAULT', 'END']:
                self.visit(l[childIndex])
                childIndex += 1
            break
        # en el cas de que la condició d'un CASE no es compleixi
        # saltem el DO i tots els statements fins trobar un CASE, DEFAULT o END
        else:
            childIndex += 2
            while l[childIndex].getText() not in ['CASE', 'DEFAULT', 'END']:
                childIndex += 1
```

### Exemple

He escrit un exemple senzill per tal de demostrar les dues extensións. El seu codi és el següent:

```
PROC main() IS
    LOG "choose your favorite color"
    LOG "    1 orange"
    LOG "    2 pink"
    LOG "    3 green"
    LOG "    4 blue"
    >> option
    SWITCH option
        CASE 1 DO
            LOG "orange is your favorite color"
        CASE 2 DO
            LOG "pink is your favorite color"
        CASE 3 DO
            LOG "green is your favorite color"
        CASE 4 DO
            LOG "blue is your favorite color"
        DEFAULT DO
            LOG "invalid option"
    END
END
```

El primer que fa és mostrar una llista numerada de colors per pantalla.

Just després es fa un read i s'espera que l'usuari seleccioni un dels colors. Aquests estan numerats de l'1 al 4, s'espera que l'usuari escrigui un enter dins d'aquest rang.

Un cop l'usuari ha seleccionat una opció s'executa un switch que mostra un misatge diferent depenent de quin dels 4 colors hagi estat seleccionat, també pot mostrar un missatge d'error en cas de que s'hagi introduït un valor invalid (diferent a 1, 2, 3 i 4).

L'escenari en el que l'usuari selecciona un color vàlid (en aquest cas el 2) és el següent:

```
╰─$ python logo3d.py test-switch-log.l3d
choose your favorite color
    1 orange
    2 pink
    3 green
    4 blue
2
pink is your favorite color
```

En el cas de que l'usuari introdueixi un valor fora del rang de valors podem veure que s'executa el bloc de codi del default:

```
╰─$ python logo3d.py test-switch-log.l3d
choose your favorite color
    1 orange
    2 pink
    3 green
    4 blue
5
invalid option
```

El codi d'aquest exemple es troba al fitxer `test-switch-log.l3d` i es pot executar mitjançant la següent comanda:

```
python logo3d.py test-switch-log.l3d
```
