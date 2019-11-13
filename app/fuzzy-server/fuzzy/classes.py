class Atributo():
    def __init__(self, nome, inicioBase, fimBase, inicioNucleo, fimNucleo, objetivo):
        self.nome = nome
        self.inicioBase = inicioBase
        self.fimBase = fimBase
        self.inicioNucleo = inicioNucleo
        self.fimNucleo = fimNucleo
        self.hasLeftShaft = inicioNucleo > inicioBase
        self.hasRightShaft = fimNucleo < fimBase
        self.isTarget = objetivo
        
    def fuzzify(self, x):
        if self.isTarget: 
            return
        if self.hasLeftShaft and self.hasRightShaft:
            return self.innerFunction(x)
        elif self.hasLeftShaft:
            return self.leftShaftFunction(x)
        elif self.hasRightShaft:
            return self.rightShaftFunction(x)
            
    def innerFunction(self ,x):
        if x <= self.inicioBase or x >= self.fimBase:
            return 0
        elif x >= self.inicioNucleo and x <= self.fimNucleo:
            return 1
        elif x >= self.inicioBase and x <= self.inicioNucleo:
            return (x - self.inicioBase) / (self.inicioNucleo - self.inicioBase)
        elif x >= self.fimNucleo and x <= self.fimBase:
            return (self.fimBase - x) / (self.fimBase - self.fimNucleo)
    
    def leftShaftFunction(self, x):
        if x <= self.inicioBase:
            return 0
        elif x >= self.inicioNucleo and x <= self.fimNucleo:
            return 1
        else:
            print((x - self.inicioNucleo))
            print((self.inicioNucleo - self.inicioBase))
            return (self.inicioNucleo - x)/(self.inicioNucleo - self.inicioBase)
        
    def rightShaftFunction(self, x):
        if x >= self.fimBase:
            return 0
        elif x >= self.inicioNucleo and x <= self.fimNucleo:
            return 1
        else:
            return (self.fimBase - x)/(self.fimBase - self.fimNucleo)