from turtle3d import Turtle3D

if __name__ is not None and '.' in __name__:
    from .logo3dParser import logo3dParser
    from .logo3dVisitor import logo3dVisitor
else:
    from logo3dParser import logo3dParser
    from logo3dVisitor import logo3dVisitor


class Visitor(logo3dVisitor):
    # llista de noms de procediments prohibits
    RESERVED_PROCEDURE_NAMES = ('color', 'up', 'down', 'left', 'right', 'forward', 'backward', 'hide', 'show', 'home')

    def __init__(self, main, parameters):
        self.variables = {}  # key-value que guarda els noms de les variables amb els seus valors
        self.procedures = {}  # key-value que guarda els noms dels procediments amb el seu context i les variables requerides
        self.procedureStack = []  # pila per guardar les variables dels procediments
        self.main = main  # nom del procediment d'entrada
        self.parameters = parameters  # parametres del procediment d'entrada
        self.turtle = Turtle3D()  # tortuga que executa el programa interpretat

    def visitAdd(self, ctx):
        l = list(ctx.getChildren())
        # l[0] + l[2]
        # visitem les dues expressions a sumar i retornem la seva suma
        return self.visit(l[0]) + self.visit(l[2])

    def visitSubtract(self, ctx):
        l = list(ctx.getChildren())
        # l[0] - l[2]
        # visitem les dues expressions a restar i retornem la seva resta
        return self.visit(l[0]) - self.visit(l[2])

    def visitMultiply(self, ctx):
        l = list(ctx.getChildren())
        # l[0] * l[2]
        # visitem les dues expressions a multiplicar i retornem la seva multiplicació
        return self.visit(l[0]) * self.visit(l[2])

    def visitDivide(self, ctx):
        l = list(ctx.getChildren())
        # l[0] / l[2]
        # visitem el segon element de la divisió (divisor)
        divisor = self.visit(l[2])
        # comprovem que el divisor no sigui 0
        if divisor == 0:
            raise Exception('Divisions with 0 as divisor are not allowed'.format(main=self.main))
        # retornem la divisio entre la visita del primer element i la del segón
        return self.visit(l[0]) / divisor

    def visitAtomDecimal(self, ctx):
        l = list(ctx.getChildren())
        # l[0]
        # convertim l'string llegida a float i el retornem
        return float(l[0].getText())

    def visitAtomInteger(self, ctx):
        l = list(ctx.getChildren())
        # l[0]
        # convertim l'string llegida a enter i el retornem
        return int(l[0].getText())

    def visitAtomIdentifier(self, ctx):
        l = list(ctx.getChildren())
        # l[0]
        variableName = l[0].getText()
        # busquem el valor de la variable al nostre diccionari i el retornem, en cas de que no hi sigui retornem 0
        return self.variables[variableName] if variableName in self.variables else 0

    def visitAtomString(self, ctx):
        l = list(ctx.getChildren())
        # l[0]
        # tant sols retornem el text del fill
        return l[0].getText()

    def visitNegativeExpression(self, ctx):
        l = list(ctx.getChildren())
        # -l[0]
        # retornem la visita de l'expressió negada
        return self.visit(l[1]) * -1

    def visitGreaterThan(self, ctx):
        l = list(ctx.getChildren())
        # l[0] > l[2]
        # visitem les dues expressions i retornem 1 si la primera és més gran que la segona, 0 en cas contraric
        return self.visit(l[0]) > self.visit(l[2])

    def visitSmallerThan(self, ctx):
        l = list(ctx.getChildren())
        # l[0] < l[2]
        # visitem les dues expressions i retornem 1 si la primera és més petita que la segona, 0 en cas contraric
        return self.visit(l[0]) < self.visit(l[2])

    def visitGreaterThanOrEqual(self, ctx):
        l = list(ctx.getChildren())
        # l[0] >= l[2]
        # visitem les dues expressions i retornem 1 si la primera és més gran o igual a la segona, 0 en cas contraric
        return self.visit(l[0]) >= self.visit(l[2])

    def visitSmallerThanOrEqual(self, ctx):
        l = list(ctx.getChildren())
        # l[0] <= l[2]
        # visitem les dues expressions i retornem 1 si la primera és més petita o igual a la segona, 0 en cas contraric
        return self.visit(l[0]) <= self.visit(l[2])

    def visitEqual(self, ctx):
        l = list(ctx.getChildren())
        # l[0] == l[2]
        # visitem les dues expressions i retornem 1 si la primera és igual a la segona, 0 en cas contraric
        return self.visit(l[0]) == self.visit(l[2])

    def visitNotEqual(self, ctx):
        l = list(ctx.getChildren())
        # l[0] != l[2]
        # visitem les dues expressions i retornem 1 si la primera no és igual a la segona, 0 en cas contraric
        return self.visit(l[0]) != self.visit(l[2])

    def visitAssign(self, ctx):
        l = list(ctx.getChildren())
        # l[0] := l[2]
        # visitem l'expressió i guardem el seu valor al diccionari de variables
        self.variables[l[0].getText()] = self.visit(l[2])

    def visitRead(self, ctx):
        l = list(ctx.getChildren())
        # >> l[1]
        # llegim un valor mitjançant consola
        value = input()
        # intentem convertir el que hem llegit a float o enter, depenent de si hi ha '.' o no
        try:
            value = float(value) if '.' in value else int(value)
        # en el cas de que no s'hagi pogut fer la conversió retornem un error
        except:
            raise Exception('"{value}" could not be converted to neither integer nor float'.format(value=value))
        # guardem el que hem llegit en el diccionari de variables
        self.variables[l[1].getText()] = value

    def visitWrite(self, ctx):
        l = list(ctx.getChildren())
        # << l[1]
        # visitem l'expressió i mostrem el resultat per pantalla
        print(self.visit(l[1]))

    def visitLog(self, ctx):
        l = list(ctx.getChildren())
        # LOG l[1]
        # visitem l'expressió i mostrem el log per pantalla eliminant les cometes del principi i del final
        print(self.visit(l[1])[1:-1])

    def visitWhileLoop(self, ctx):
        l = list(ctx.getChildren())
        # WHILE l[1] DO l[3] l[4] ... END
        # mentre visitem la expressió l[1]
        while abs(self.visit(l[1])) > 1e-6:
            # visitem els statements l[3] l[4] ... fins trobar END
            childIndex = 3
            while l[childIndex].getText() != 'END':
                self.visit(l[childIndex])
                childIndex += 1

    def visitForLoop(self, ctx):
        l = list(ctx.getChildren())
        # FOR l[1] FROM l[3] TO l[5] DO l[7] l[8] ... END
        # obtenim el nom de la variable del bucle i els bounds d'inici i de fi
        variableName = l[1].getText()
        fr = self.visit(l[3])
        to = self.visit(l[5]) + 1
        # iterem de fr a to
        for i in range(fr, to):
            # actualitzem la variable iteradora al diccionari de variables
            self.variables[variableName] = i
            # visitem els statements l[7], l[8], ... fins trobar END
            childIndex = 7
            while l[childIndex].getText() != 'END':
                self.visit(l[childIndex])
                childIndex += 1
            # actualitzem la variable iteradora
            i = self.variables[variableName]

    def visitIfThenElse(self, ctx):
        l = list(ctx.getChildren())
        # IF l[1] THEN l[3] l[4] ... l[n] ELSE l[n+2] l[n+3] ... END
        childIndex = 3
        # visitem la expressió booleana del bucle
        if abs(self.visit(l[1])) > 1e-6:
            # la expressió booleana del bucle ha resultat ser 1
            # visitem els statements l[3], l[4], ... fins trobar ELSE o END
            while l[childIndex].getText() not in ['ELSE', 'END']:
                self.visit(l[childIndex])
                childIndex += 1
        else:
            # la expressió booleana del bucle ha resultat ser 0
            # iterem fins trobar un ELSE o un END, en el cas de trobar END la visita acaba
            while l[childIndex].getText() not in ['ELSE', 'END']:
                childIndex += 1
            if l[childIndex].getText() == 'ELSE':
                # hem trobat un ELSE, visitem els statements l[n+2], l[n+3], ... fins trobar END
                while l[childIndex].getText() != 'END':
                    self.visit(l[childIndex])
                    childIndex += 1

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

    def visitProcedure(self, ctx):
        l = list(ctx.getChildren())
        # PROC l[1](l[3], l[4], ..., l[n]) IS l[n+3], l[n+4], ... END
        # obtenim el nom del procediment
        procedureName = l[1].getText()
        # comprovem que el nom no estigui a la llista de noms prohibits
        if procedureName in self.RESERVED_PROCEDURE_NAMES:
            raise Exception('"{name}" is a reserved procedure name and should not be used'.format(name=procedureName))
        # comprovem que no s'hagi evaluat un procediment amb el mateix nom previament
        if procedureName in self.procedures:
            raise Exception('Procedure "{name}" has been defined multiple times'.format(name=procedureName))
        # afegim el procediment al diccionari de procediments
        self.procedures[procedureName] = [[], []]  # [statements, variables]
        # iterem per els parametres d'entrada del procediment i els afegim al diccionari
        childIndex = 3
        while l[childIndex].getText() != ')':
            if l[childIndex].getText() == ',':
                childIndex += 1
                continue
            # comprovem que no hi hagi parametres amb el mateix nom
            if l[childIndex].getText() in self.procedures[procedureName][1]:
                raise Exception('There are multiple parameters with name "{varName}" in the declaration of procedure "{procName}"'.format(
                    varName=l[childIndex].getText(), procName=procedureName))
            # afegim el parametre al diccionari
            self.procedures[procedureName][1].append(l[childIndex].getText())
            childIndex += 1
        # afegim els statements del procediment al diccionari fins trobar el END
        while l[childIndex].getText() != 'END':
            self.procedures[procedureName][0].append(l[childIndex])
            childIndex += 1

    def visitCallProcedure(self, ctx):
        l = list(ctx.getChildren())
        # l[0](l[2], l[3], ...)
        # visitem les expressions dels parametres saltant les comes fins trobar el parentesis de tancar i guardem els resultats
        procedureParameters = []
        for i in range(2, len(l)):
            value = l[i].getText()
            if value == ')':
                break
            if value == ',':
                continue
            procedureParameters.append(self.visit(l[i]))
        # obtenim el nom del procediment que estem executant
        procedureName = l[0].getText()
        # en el cas de que sigui ua crida a un dels procediments del llenguatge (una de les opcions de control de la tortuga)
        #   executem la part de codi corresponent sempre comprovant que el nombre de parametres sigui l'adequat
        if procedureName == 'color':
            assert(len(procedureParameters) == 3)
            self.turtle.color(*procedureParameters)
        elif procedureName == 'up':
            assert(len(procedureParameters) == 1)
            self.turtle.up(*procedureParameters)
        elif procedureName == 'down':
            assert(len(procedureParameters) == 1)
            self.turtle.down(*procedureParameters)
        elif procedureName == 'left':
            assert(len(procedureParameters) == 1)
            self.turtle.left(*procedureParameters)
        elif procedureName == 'right':
            assert(len(procedureParameters) == 1)
            self.turtle.right(*procedureParameters)
        elif procedureName == 'forward':
            assert(len(procedureParameters) == 1)
            self.turtle.forward(*procedureParameters)
        elif procedureName == 'backward':
            assert(len(procedureParameters) == 1)
            self.turtle.backward(*procedureParameters)
        elif procedureName == 'hide':
            assert(len(procedureParameters) == 0)
            self.turtle.hide(*procedureParameters)
        elif procedureName == 'show':
            assert(len(procedureParameters) == 0)
            self.turtle.show(*procedureParameters)
        elif procedureName == 'home':
            assert(len(procedureParameters) == 0)
            self.turtle.home(*procedureParameters)
        # en el cas de que sigui una crida a un procediment del programa
        else:
            # afegim l'estat actual al stack per poder recuperar-lo al acabar d'executar el procediment
            self.procedureStack.append(self.variables)
            # com que cada procediment te les seves variables i cap procediment pot accedir a les d'un altre fem reset del diccionari
            self.variables = {}
            # construim el diccionari a partir dels noms dels parametres i els seus valors
            for i, variableName in enumerate(self.procedures[procedureName][1]):
                self.variables[variableName] = procedureParameters[i]
            # visitem els statements del procediment
            for statement in self.procedures[procedureName][0]:
                self.visit(statement)
            # recuperem l'estat abans d'executar el procediment per poder seguir executant el programa
            self.variables = self.procedureStack.pop()

    def visitRoot(self, ctx):
        l = list(ctx.getChildren())
        # llegim tots els procediments del programa construint el diccionari de procediments
        for procedure in l:
            self.visit(procedure)
        # en el cas de que no hi hagi cap procediment amb el main definit, retornem una excepció
        if self.main not in self.procedures:
            raise Exception('Main procedure with name "{main}" was not found'.format(main=self.main))
        # llegim el procediment main del diccionari així com els seus parametres i statements
        procedure = self.procedures[self.main]
        procedureStatements = procedure[0]
        procedureParameters = procedure[1]
        # verifiquem que el nombre de parametres donats per l'usuari es igual al nombre de parametres del procediment main
        neededParameters = len(procedureParameters)
        providedParameters = len(self.parameters)
        if neededParameters != providedParameters:
            raise Exception('"{main}" procedure requires {needed} parameters, {provided} were provided'.format(
                main=self.main, needed=neededParameters, provided=providedParameters))
        # construim el diccionari de variables a partir dels parametres del procediment main
        for i, parameterName in enumerate(procedureParameters):
            parameterValue = self.parameters[i]
            parameterValue = float(parameterValue) if '.' in parameterValue else int(parameterValue)
            self.variables[parameterName] = parameterValue
        # visitem els statements del procediment main
        for statement in procedureStatements:
            self.visit(statement)
