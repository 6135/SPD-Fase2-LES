# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Administrador(models.Model):
    # Field name made lowercase.
    utilizadorid = models.OneToOneField(
        'Utilizador', models.CASCADE, db_column='UtilizadorID', primary_key=True)
    # Field name made lowercase.
    gabinete = models.CharField(
        db_column='Gabinete', max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Administrador'


class Participante(models.Model):
    # Field name made lowercase.
    utilizadorid = models.OneToOneField(
        'Utilizador', models.CASCADE, db_column='UtilizadorID', primary_key=True)

    class Meta:
        managed = False
        db_table = 'Participante'


class Utilizador(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255)
    # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255)
    # Field name made lowercase.
    telefone = models.CharField(
        db_column='Telefone', max_length=255, blank=True, null=True)
    # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=255)
    # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=255)

    class Meta:
        managed = False
        db_table = 'Utilizador'


class Professoruniversitario(models.Model):
    # Field name made lowercase.
    utilizadorid = models.OneToOneField(
        Utilizador, models.CASCADE, db_column='UtilizadorID', primary_key=True)
    # Field name made lowercase.
    gabinete = models.CharField(
        db_column='Gabinete', max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ProfessorUniversitario'
