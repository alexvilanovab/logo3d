from turtle3d import Turtle3D

if __name__ is not None and '.' in __name__:
    from .logo3dParser import logo3dParser
    from .logo3dVisitor import logo3dVisitor
else:
    from logo3dParser import logo3dParser
    from logo3dVisitor import logo3dVisitor

class Visitor(logo3dVisitor):
    def __init__(self):
        self.variables = {}
        self.procedures = {}
        self.procedureStack = []
        self.turtle = Turtle3D()
    
    def visitAdd(self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[0]) + self.visit(l[2])

    def visitSubtract(self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[0]) - self.visit(l[2])

    def visitMultiply(self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[0]) * self.visit(l[2])

    def visitDivide(self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[0]) / self.visit(l[2])

    def visitAtomDecimal(self, ctx):
        l = list(ctx.getChildren())
        return float(l[0].getText())

    def visitAtomInteger(self, ctx):
        l = list(ctx.getChildren())
        return int(l[0].getText())

    def visitAtomIdentifier(self, ctx):
        l = list(ctx.getChildren())
        variableName = l[0].getText()
        return self.variables[variableName] if variableName in self.variables else 0

    def visitGreaterThan(self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[0]) > self.visit(l[2])

    def visitSmallerThan(self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[0]) < self.visit(l[2])

    def visitGreaterTHanOrEqual(self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[0]) >= self.visit(l[2])

    def visitSmallerThanOrEqual(self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[0]) <= self.visit(l[2])

    def visitEqual(self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[0]) == self.visit(l[2])

    def visitNotEqual(self, ctx):
        l = list(ctx.getChildren())
        return self.visit(l[0]) != self.visit(l[2])

    def visitAssign(self, ctx):
        l = list(ctx.getChildren())
        self.variables[l[0].getText()] = self.visit(l[2])
    
    def visitRead(self, ctx):
        l = list(ctx.getChildren())
        self.variables[l[1].getText()] = float(input())
    
    def visitWrite(self, ctx):
        l = list(ctx.getChildren())
        print(self.visit(l[1]))

    def visitWhileLoop(self, ctx):
        l = list(ctx.getChildren())
        while self.visit(l[1]):
            childIndex = 3
            while l[childIndex].getText() != 'END':
                self.visit(l[childIndex])
                childIndex += 1

    def visitForLoop(self, ctx):
        l = list(ctx.getChildren())
        variableName = l[1].getText()
        fr = self.visit(l[3])
        to = self.visit(l[5])
        for i in range(fr, to+1):
            self.variables[variableName] = i
            childIndex = 7
            while l[childIndex].getText() != 'END':
                self.visit(l[childIndex])
                childIndex += 1
    
    def visitIfThenElse(self, ctx):
        l = list(ctx.getChildren())
        childIndex = 3
        if self.visit(l[1]):
            while l[childIndex].getText() not in ['ELSE', 'END']:
                self.visit(l[childIndex])
                childIndex += 1
        else:
            while l[childIndex].getText() not in ['ELSE', 'END']:
                childIndex += 1
            if l[childIndex].getText() == 'ELSE':
                while l[childIndex].getText() != 'END':
                    self.visit(l[childIndex])
                    childIndex += 1

    def visitProcedure(self, ctx):
        l = list(ctx.getChildren())
        procedureName = l[1].getText()
        self.procedures[procedureName] = [[], []]
        childIndex = 3
        while l[childIndex].getText() != ')':
            if l[childIndex].getText() == ',':
                childIndex += 1
                continue
            self.procedures[procedureName][1].append(l[childIndex].getText())
            childIndex += 1
        while l[childIndex].getText() != 'END':
            self.procedures[procedureName][0].append(l[childIndex])
            childIndex += 1

    def visitCallProcedure(self, ctx):
        l = list(ctx.getChildren())
        procedureVariables = []
        for i in range(2, len(l)):
            value = l[i].getText()
            if value == ')':
                break
            if value == ',':
                continue
            procedureVariables.append(self.visit(l[i]))
        procedureName = l[0].getText()
        if procedureName == 'color':
            self.turtle.color(*procedureVariables)
        elif procedureName == 'up':
            self.turtle.up(*procedureVariables)
        elif procedureName == 'down':
            self.turtle.down(*procedureVariables)
        elif procedureName == 'left':
            self.turtle.left(*procedureVariables)
        elif procedureName == 'right':
            self.turtle.right(*procedureVariables)
        elif procedureName == 'forward':
            self.turtle.forward(*procedureVariables)
        elif procedureName == 'backward':
            self.turtle.backward(*procedureVariables)
        elif procedureName == 'hide':
            self.turtle.hide(*procedureVariables)
        elif procedureName == 'show':
            self.turtle.show(*procedureVariables)
        elif procedureName == 'home':
            self.turtle.home(*procedureVariables)
        else:
            self.procedureStack.append(self.variables)
            self.variables = {}
            for i, variableName in enumerate(self.procedures[procedureName][1]):
                self.variables[variableName] = procedureVariables[i]
            for statement in self.procedures[procedureName][0]:
                self.visit(statement)
            self.variables = self.procedureStack.pop()

    def visitRoot(self, ctx):
        l = list(ctx.getChildren())
        for procedure in l:
            self.visit(procedure)
        for statement in self.procedures['main'][0]:
            self.visit(statement)
