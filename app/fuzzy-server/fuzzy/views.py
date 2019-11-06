from rest_framework.renderers import JSONRenderer
from django.shortcuts import render
from .serializers import AtributoSerializer, VariavelSerializer, RegraSerializer
from .models import Variavel, Atributo, Regra
from rest_framework import viewsets
from rest_framework.response import Response

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
