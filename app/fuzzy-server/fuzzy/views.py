from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from .serializers import AtributoSerializer, VariavelSerializer, RegraSerializer
from .models import Variavel, Atributo, Regra
from rest_framework import viewsets
from rest_framework.response import Response
from .classes import Regra as Rg ,Atributo as Atr ,Variavel as Var ,Projeto
import jsons
import numpy as np
from PIL import Image
import base64
# Create your views here.


class VariavelViewSet(viewsets.ModelViewSet):
    queryset = Variavel.objects.all()
    serializer_class = VariavelSerializer


class AtributoViewSet(viewsets.ModelViewSet):
    queryset = Atributo.objects.all()
    serializer_class = AtributoSerializer

class RegraViewSet(viewsets.ModelViewSet):
    queryset = Regra.objects.all()
    serializer_class = RegraSerializer


class VariavelCustomViewSet(viewsets.ViewSet):
    queryset = Variavel.objects.all()
    def list(self, request):
        atr = self.queryset
        print(atr)
        return Response(AtributoSerializer(atr).data)
    def create(self, request):
        data = VariavelSerializer(data=request.data)
        data.is_valid()
        atributos = data.validated_data.pop('atributos')
        obj = data.save()
        for atributo in atributos:
            Atributo.objects.create(variavel=obj, **atributo)

        return Response(data.data)

@api_view(['GET'])
def simulateFuzzy(request):
    if request.method == 'GET':
        variaveis = Variavel.objects.all()
        variaveis = list(variaveis.values())
        req = jsons.load(request.data)
        print(req)
        for i,variavel in enumerate(variaveis):
           atributos = Atributo.objects.filter(variavel_id = variavel['id'])
           variavel['atributos'] = list(atributos.values())
           variavel['inputValue'] = req[variavel['nome']] if variavel['flObjetivo'] == False else 0
           variaveis[i] = jsons.loads(jsons.dumps(variavel),Var)

        regras = list(Regra.objects.all().values())
        for i, regra in enumerate(regras):
            regras[i] = jsons.loads(jsons.dumps(regra),Rg)

        projeto = Projeto(variaveis, regras)
        result = projeto.fuzzify()        
        
        return Response(result)

@api_view(['GET'])
def plotVariable(request):
    variavel = jsons.loads(jsons.dumps(request.data), Var)
    img = variavel.plot()
    img = Image.open(img)
    resp = HttpResponse(content_type='image/png')
    img.save(resp,'png')
    return resp

@api_view(['GET'])
def getAllGraphics(request):
    variaveis = Variavel.objects.all()
    variaveis = list(variaveis.values())
    imgList = []
    for i,variavel in enumerate(variaveis):
        atributos = Atributo.objects.filter(variavel_id = variavel['id'])
        variavel['atributos'] = list(atributos.values())
        variaveis[i] = jsons.loads(jsons.dumps(variavel),Var)
        img = variaveis[i].plot()
        imgList.append(base64.b64encode(img.getvalue()))
    return Response(imgList)




