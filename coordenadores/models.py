# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from configuracao.models import *
from colaboradores.models import *
from atividades.models import *
from inscricoes.models import *

class Coordenador(models.Model):
    # Field name made lowercase.
    utilizadorid = models.OneToOneField(
        'utilizadores.Utilizador', models.CASCADE, db_column='UtilizadorID', primary_key=True)
    # Field name made lowercase.
    gabinete = models.CharField(
        db_column='Gabinete', max_length=255, blank=True, null=True)
    unidadeorganicaid = models.ForeignKey('configuracao.Unidadeorganica', models.CASCADE, db_column='unidadeOrganicaID')  # Field name made lowercase.

    class Meta:
        db_table = 'Coordenador'

class Tarefa(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    dia = models.DateField()
    estado = models.CharField(max_length=64)
    coordenadorutilizadorid = models.ForeignKey(Coordenador, models.CASCADE, db_column='CoordenadorUtilizadorID')  # Field name made lowercase.
    colaboradorutilizadorid = models.ForeignKey(Colaborador, models.CASCADE, db_column='ColaboradorUtilizadorID')  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=64)  # Field name made lowercase.
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'Tarefa'


class TarefaAcompanhar(models.Model):
    tarefaid = models.OneToOneField(Tarefa, models.CASCADE, db_column='tarefaid', primary_key=True)
    inscricaoid = models.ForeignKey(Inscricao, models.CASCADE, db_column='inscricaoid')
    origem = models.CharField(max_length=255, db_column='origem', blank=False, null=False)
    destino = models.CharField(max_length=255, db_column='destino', blank=False, null=False)
    horario = models.DateField( blank=False, null=False)

    class Meta:
        db_table = 'TarefaAcompanhar'


class TarefaAuxiliar(models.Model):
    tarefaid = models.OneToOneField(Tarefa, models.CASCADE, db_column='tarefaid', primary_key=True)
    sessaoid = models.ForeignKey('atividades.Sessao', models.CASCADE, db_column='sessaoid')

    class Meta:
        db_table = 'TarefaAuxiliar'


class TarefaOutra(models.Model):
    tarefaid = models.OneToOneField(Tarefa, models.CASCADE, db_column='tarefaid', primary_key=True)
    descricao = models.TextField(db_column='descricao', blank=False, null=False)
    horario = models.DateField( blank=False, null=False)
    
    class Meta:
        db_table = 'TarefaOutra'

