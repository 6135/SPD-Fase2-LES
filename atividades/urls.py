from django.urls import path
from . import views

urlpatterns = [
    path("minhasatividades",views.minhasatividades,name="minhasAtividades"),
    path("proporatividade",views.proporatividade,name="proporAtividade"),
    path('alteraratividade/<int:id>',views.alterarAtividade,name='alterarAtividade'),
    path('inserirsessao/<id>',views.novasessao,name='inserirSessao'),
    path('alteraratividade/<id>',views.alterarAtividade,name='alterarAtividade'),
    path('eliminaratividade/<id>',views.eliminarAtividade,name='eliminarAtividade'),
    path('eliminarsessao/<id>',views.eliminarSessao,name='eliminarSessao'),
]
