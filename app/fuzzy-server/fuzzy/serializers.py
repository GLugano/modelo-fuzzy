from rest_framework import serializers
from .models import Variavel,Atributo, Regra


class AtributoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atributo
        fields = '__all__'
        read_only_fields  = ['variavel']
   
class VariavelSerializer(serializers.ModelSerializer):
    atributos =  AtributoSerializer(many=True)
    class Meta:
        model = Variavel
        fields = '__all__'
    
class RegraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Regra
        fields = '__all__'