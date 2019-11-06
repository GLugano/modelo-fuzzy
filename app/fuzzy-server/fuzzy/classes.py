class Atributo():
    def __init__(self, nome, inicioBase, fimBase, inicioNucleo, fimNucleo):
        self.nome = nome
        self.inicioBase = inicioBase
        self.fimBase = fimBase
        self.inicioNucleo = inicioNucleo
        self.fimNucleo = fimNucleo
        self.hasLeftShaft = inicioNucleo > inicioBase
        self.hasRightShaft = fimNucleo < fimBase
        
    def fuzzify(self, x):
        if self.hasLeftShaft and self.hasRightShaft:
            self.innerFunction(x)
        elif self.hasLeftShaft:
            self.leftShaftFunction(x)
        elif self.hasRightShaft:
            self.rightShaftFunction(x)
            
    def innerFunction(self ,x):
        if x < self.inicioBase or x > self.fimBase:
            return 0
        elif x >= self.inicioNucleo or x <= self.fimNucleo:
            return 1
        elif x >= self.inicioBase and x <= self.inicioNucleo:
            return (x - self.inicioBase) / (self.inicioNucleo - self.inicioBase)
        elif x >= self.inicioBase and x <= self.inicioNucleo:
            return (self.finalBase - x) / (self.fimBase - self.fimNucleo)
    
    def leftShaftFunction(x):
        if x < self.inicioBase:
            return 0
        elif x >= self.inicioNucleo or x <= self.fimNucleo:
            return 1
        else:
            return (x - inicioNucleo)/(self.inicioNucleo - self.inicioBase)
        
    def rightShaftFunction(x):
        if x > self.fimBase:
            return 0
        elif x >= self.inicioNucleo or x <= self.fimNucleo:
            return 1
        else:
            return (self.fimNucleo - x)/(self.fimNucleo - self.fimBase)
       
