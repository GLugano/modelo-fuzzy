import numpy as np
class Atributo():
    def __init__(self, nome, inicioBase, fimBase, inicioNucleo, fimNucleo, objetivo):
        self.name = nome
        self.inicioBase = inicioBase
        self.fimBase = fimBase
        self.inicioNucleo = inicioNucleo
        self.fimNucleo = fimNucleo
        self.hasLeftShaft = inicioNucleo > inicioBase
        self.hasRightShaft = fimNucleo < fimBase
        self.pertinencia = 0
        
    def calculaPertinencia(self, x):
        if self.hasLeftShaft and self.hasRightShaft:
            self.pertinencia = self.innerFunction(x)
        elif self.hasLeftShaft:
            self.pertinencia = self.leftShaftFunction(x)
        elif self.hasRightShaft:
            self.pertinencia = self.rightShaftFunction(x)
            
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
            return (self.inicioNucleo - x)/(self.inicioNucleo - self.inicioBase)
        
    def rightShaftFunction(self, x):
        if x >= self.fimBase:
            return 0
        elif x >= self.inicioNucleo and x <= self.fimNucleo:
            return 1
        else:
            return (self.fimBase - x)/(self.fimBase - self.fimNucleo)

class Variavel():
    def __init__(self, nome, atributos, inputValue, isObjective):
        self.name = nome
        self.atributos = atributos
        self.inputValue = inputValue
        self.isObjective = isObjective
    
    def getAtributeByName(self, name):
        for atributo in self.atributos:
            if name.casefold() == atributo.name.casefold():
                return atributo
    
    def getUniverso(self):
        universo = [None,None]
        for atrib in self.atributos:
            if universo[0] == None:
                universo[0] = atrib.inicioBase
                universo[1] = atrib.fimBase
            else:
                universo[0] = atrib.inicioBase if atrib.inicioBase < universo[0] else universo[0]
                universo[1] = atrib.fimBase if atrib.fimBase > universo[1] else universo[1]
        return universo

class Regra():
    #      SE 0  TEMP 1  = 2 ALTA 3  E 4  HUMI 5 = 6 MEDIA 7 ENTAO IRRIGACAO 9 = BAIXA 11
    def __init__(self, descricao):
        self.descricao = descricao.split(' ')
        self.finalResult = 0
    
class Projeto():

    def __init__(self, variaveis, regras):
        self.variaveis = variaveis
        self.regras = regras
        self.ruleSetValues = {}
    

    def fuzzify(self):
        self.calculaPertinencias()
        self.ativacaoDosAntecedentes()

    def calculaPertinencias(self):
        for variavel in self.variaveis:
            if variavel.isObjective:
                continue
            for atributo in variavel.atributos:
                atributo.calculaPertinencia(variavel.inputValue)

    def getVariavleByName(self, name):
        for variavel in self.variaveis:
            if name.casefold() == variavel.name.casefold():
                return variavel
            
    def getObjectiveVariable(self):
        for variavel in self.variaveis:
            if variavel.isObjective:
                return variavel

    def ativacaoDosAntecedentes(self):
        self.ruleSetValues = {}
        universo = self.getObjectiveVariable().getUniverso()
        alvos = []
        for regra in self.regras:
            var1 = self.getVariavleByName(regra.descricao[1])
            atrib1 = var1.getAtributeByName(regra.descricao[3]) 
            operator = regra.descricao[4]
            var2 = self.getVariavleByName(regra.descricao[5])
            atrib2 = var2.getAtributeByName(regra.descricao[7])
            varObjet = self.getVariavleByName(regra.descricao[9])
            atribObjet = varObjet.getAtributeByName(regra.descricao[11])
            if operator.casefold() == 'E'.casefold():
                result = min([atrib1.pertinencia, atrib2.pertinencia])
            else:
                result = max([atrib1.pertinencia, atrib2.pertinencia])
            if self.ruleSetValues.get(atribObjet.name) == None:
                self.ruleSetValues[atribObjet.name] = [result]
                alvos.append(atribObjet)
            else:
                self.ruleSetValues[atribObjet.name].append(result)
            
        for key in self.ruleSetValues:
            print(self.ruleSetValues)
            self.ruleSetValues[key] = max(self.ruleSetValues[key])
            if self.ruleSetValues[key] == 0:
                self.ruleSetValues.pop(key, None)  
            print(self.ruleSetValues)
        
        values = list(self.ruleSetValues.values())
        dividendo = []
        divisor = []
        for i,value in enumerate(values):
            dividendo.append([])
            antAscendente = i > 0 and value > values[i-1]
            posAscendente = (len(values) - 1 >= i + 1  and value < values[i+1])
            
            arrayUniverso = np.arange(universo[0],universo[1]+1)
            
            for j in arrayUniverso:
                if (j >= alvos[i].inicioNucleo and j <= alvos[i].fimNucleo) or (j >= alvos[i].inicioBase and j <= alvos[i].fimBase and (antAscendente or posAscendente)):
                    dividendo[i].append(j*value)
                    
            divisor.append(value * len(dividendo[i]))
            dividendo[i] = np.sum(dividendo[i])
        
        print(np.sum(dividendo)/np.sum(divisor))