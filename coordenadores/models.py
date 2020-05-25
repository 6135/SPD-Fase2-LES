# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Tarefa(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)  # Field name made lowercase.
    estado = models.CharField(max_length=64)
    coord = models.ForeignKey('utilizadores.Coordenador', models.DO_NOTHING, db_column='CoordenadorUtilizadorID',null=True)  # Field name made lowercase.
    colab = models.ForeignKey('utilizadores.Colaborador', models.DO_NOTHING, db_column='ColaboradorUtilizadorID',null=True,blank=True)  # Field name made lowercase.
    tipo = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Tarefa'


class TarefaAcompanhar(models.Model):
    tarefaid = models.OneToOneField(Tarefa, models.CASCADE, db_column='tarefaid', primary_key=True)
    inscricao = models.ForeignKey('inscricoes.Inscricao', models.CASCADE, db_column='inscricao')
    origem = models.CharField(max_length=255, db_column='origem', blank=False, null=False)
    destino = models.CharField(max_length=255, db_column='destino', blank=False, null=False)
    horario = models.ForeignKey('configuracao.Horario',models.DO_NOTHING,db_column='horario')
    dia = models.DateField()
    
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
    horario = models.TimeField(blank=False, null=False)
    dia = models.DateField()

    class Meta:
        db_table = 'TarefaOutra'

