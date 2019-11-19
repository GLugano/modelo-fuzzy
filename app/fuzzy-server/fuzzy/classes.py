import matplotlib.pyplot as plt
import numpy as np
import jsons
import io
import base64
from PIL import Image

class Atributo(jsons.JsonSerializable):
    def __init__(self, nome, inicioBase, fimBase, inicioNucleo, fimNucleo, objetivo):
        self.name = nome
        self.inicioBase = inicioBase
        self.fimBase = fimBase
        self.inicioNucleo = inicioNucleo
        self.fimNucleo = fimNucleo
        self.hasLeftShaft = inicioNucleo > inicioBase
        self.hasRightShaft = fimNucleo < fimBase
        self.pertinencia = 0

    def __repr__(self):
        return f'{self.name} {self.inicioBase}  {self.fimBase} {self.inicioNucleo}  {self.fimNucleo}'
        
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



class Variavel(jsons.JsonSerializable):
    def __init__(self, nome, atributos, inputValue, flObjetivo):
        self.name = nome
        self.atributos = self.atributosDictToAtributos(atributos)
        self.inputValue = inputValue
        self.isObjective = flObjetivo
    
    def __repr__(self):
        return f' NOME {self.name} INPUT :{self.inputValue} Atributos: {self.atributos}'

    def atributosDictToAtributos(self, atributos):
        atrib = []
        for atributo in atributos:
            atrib.append(jsons.loads(jsons.dumps(atributo),Atributo))
        return atrib
        
    
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
    
    def plot(self, doClear):
        legenda = []
        for atributo in self.atributos:
            yPositions = []
            legenda.append(atributo.name)
            if atributo.hasLeftShaft and atributo.hasRightShaft:
                yPositions = [0,1,1,0]
            elif atributo.hasLeftShaft and not atributo.hasRightShaft:
                yPositions = [0,1,1,1]
            elif not atributo.hasLeftShaft and atributo.hasRightShaft:
                yPositions = [1,1,1,0]
            plt.plot([atributo.inicioBase,atributo.inicioNucleo,atributo.fimNucleo,atributo.fimBase],yPositions)
        plt.legend(legenda, loc='lower left')
        plt.title(self.name, loc='center')
        bytes_image = io.BytesIO()
        plt.savefig(bytes_image, format='PNG')
        if (doClear):
            plt.clf()
        return bytes_image
    
class Regra():
    #      SE 0  TEMP 1  = 2 ALTA 3  E 4  HUMI 5 = 6 MEDIA 7 ENTAO IRRIGACAO 9 = BAIXA 11
    def __init__(self, descricao):
        self.descricao = descricao.split(' ')
        self.finalResult = 0

    def __repr__(self):
        return str(self.descricao)
    
class Projeto():

    def __init__(self, variaveis, regras):
        self.variaveis = variaveis
        self.regras = regras
        self.ruleSetValues = {}
    

    def fuzzify(self):
        self.calculaPertinencias()
        return self.ativacaoDosAntecedentes()

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
        objetivo = None
        for regra in self.regras:
            print(regra)
            var1 = self.getVariavleByName(regra.descricao[1])
            atrib1 = var1.getAtributeByName(regra.descricao[3]) 
            operator = regra.descricao[4]
            var2 = self.getVariavleByName(regra.descricao[5])
            atrib2 = var2.getAtributeByName(regra.descricao[7])
            varObjet = self.getVariavleByName(regra.descricao[9])
            objetivo = varObjet
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
            self.ruleSetValues[key] = max(self.ruleSetValues[key])
        
        values = list(self.ruleSetValues.values())
        dividendo = []
        x = []
        y = []
        divisor = []
        print(values)
        for i,value in enumerate(values):
            
            dividendo.append([])
            arrayUniverso = np.arange(universo[0],universo[1]+1)
            antAscendente = i > 0 and value > values[i-1]
            posAscendente = (len(values) - 1 >= i + 1  and value < values[i+1])
            for j in arrayUniverso:
                if (j >= alvos[i].inicioNucleo and j <= alvos[i].fimNucleo) or (j >= alvos[i].inicioBase and j <= alvos[i].fimBase and (antAscendente or not posAscendente)):
                    dividendo[i].append(j*value)
                    x.append(j)
                    y.append(value)
            divisor.append(value * len(dividendo[i]))
            dividendo[i] = np.sum(dividendo[i])
        sumDivisor = np.sum(divisor)
        objetivo.plot(False)
        plt.fill_between(x,0,y[1])
        bytes_image = io.BytesIO()
        plt.savefig(bytes_image, format='PNG')
        plt.clf()
        result = {}
        result['valor'] = np.sum(dividendo)/sumDivisor if sumDivisor != 0 else 0
        result['imagem'] = base64.b64encode(bytes_image.getvalue())
        return result