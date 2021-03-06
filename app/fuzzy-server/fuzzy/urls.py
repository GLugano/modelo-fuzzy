from django.urls import path, include
from . import views 
from rest_framework import routers 

router = routers.DefaultRouter()
router.register('atributo', views.AtributoViewSet)
router.register('variavel', views.VariavelViewSet)
router.register('regra', views.RegraViewSet)
router.register('cadastro', views.VariavelCustomViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('simular', views.simulateFuzzy),
    path('plot', views.plotVariable),
    path('graficos', views.getAllGraphics)
]
