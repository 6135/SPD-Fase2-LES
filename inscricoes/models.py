from django.db import models
from django.core import validators
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime, time, timedelta
from configuracao.models import Horario
from django.db.models import Max, Min
from collections import OrderedDict


class Escola(models.Model):
    nome = models.CharField(max_length=200)
    local = models.CharField(max_length=128)

    class Meta:
        db_table = 'Escola'
        ordering = ['nome', 'local']

    def __str__(self):
        return self.nome


class Inscricao(models.Model):
    individual = models.BooleanField()
    nalunos = models.IntegerField()
    escola = models.ForeignKey(Escola, models.CASCADE)
    ano = models.IntegerField(
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(12)
        ], default=None, blank=True, null=True
    )
    turma = models.CharField(max_length=1, default=None, blank=True, null=True)
    areacientifica = models.CharField(
        max_length=64, default=None, blank=True, null=True)
    participante = models.ForeignKey(
        'utilizadores.Participante', models.CASCADE)
    dia = models.DateField()
    diaaberto = models.ForeignKey('configuracao.Diaaberto', models.CASCADE)
    MEIO_TRANSPORTE_CHOICES = [
        ('comboio', "Comboio"),
        ('autocarro', "Autocarro"),
        ('outro', "Meios Próprios"),
    ]
    meio_transporte = models.CharField(
        max_length=40, choices=MEIO_TRANSPORTE_CHOICES)
    hora_chegada = models.TimeField(blank=True, null=True)
    local_chegada = models.CharField(max_length=200, blank=True, null=True)
    entrecampi = models.BooleanField(default=False)

    class Meta:
        db_table = 'Inscricao'

    @property
    def horario(self):
        aggr = self.inscricaosessao_set.all().aggregate(
            Min('sessao__horarioid__inicio'), Max('sessao__horarioid__fim'))
        inicio = aggr['sessao__horarioid__inicio__min']
        fim = aggr['sessao__horarioid__fim__max']
        return f"{inicio.strftime('%H:%M')} - {fim.strftime('%H:%M')}"

    def get_departamentos(self):
        return {inscricaosessao.sessao.atividadeid.get_departamento() for inscricaosessao in self.inscricaosessao_set.all()}

    def get_grupo(self):
        return self.id

    def get_dias(self):
        inscricao_sessoes = Inscricaosessao.objects.filter(
            inscricao=self).order_by('sessao__dia')
        dias = []
        dias = [sessao.sessao.dia for sessao in inscricao_sessoes]
        return [{'key': str(dia), 'value': dia} for dia in set(dias)]

    def get_horarios(self, dia):
        inscricao_sessoes = Inscricaosessao.objects.filter(
            inscricao=self, sessao__dia=dia).order_by('sessao__horarioid__inicio')
        horarios = []
        horarios.append({'key': str(inscricao_sessoes.first().sessao.horarioid.inicio),
                         'value': inscricao_sessoes.first().sessao.horarioid.inicio})
        for sessao in inscricao_sessoes:
            if sessao.sessao.horarioid.fim not in horarios:
                horarios.append(
                    {'key': str(sessao.sessao.horarioid.fim), 'value': sessao.sessao.horarioid.fim})
        horarios.pop()
        horarios = sorted(horarios, key=lambda k: k['key']) 
        return horarios

    def get_origem(self, dia, horario):
        first_session = Inscricaosessao.objects.filter(
            inscricao=self, sessao__dia=dia).order_by('sessao__horarioid__inicio').first()
        origem = []
        if horario == time.strftime(first_session.sessao.horarioid.inicio, "%H:%M:%S"):
            origem.append({'key': 'Check in', 'value': 'Check in'})
        else:
            inscricao_sessoes = Inscricaosessao.objects.filter(
                inscricao=self, sessao__dia=dia, sessao__horarioid__fim=horario).order_by('sessao__horarioid__inicio')
            for local in inscricao_sessoes:
                origem.append({'key': local.sessao.atividadeid.espacoid.id,
                               'value': local.sessao.atividadeid.espacoid.nome})
        return origem

    def get_destino(self, dia, horario):
        inscricao_sessoes = Inscricaosessao.objects.filter(
            inscricao=self, sessao__dia=dia).order_by('sessao__horarioid__inicio')
        destino = []
        
        if horario == time.strftime(inscricao_sessoes.first().sessao.horarioid.inicio, "%H:%M"):
            for local in inscricao_sessoes:
                if time.strftime(local.sessao.horarioid.inicio,"%H:%M") == horario:
                        destino.append({'key': local.sessao.atividadeid.espacoid.id,
                                    'value': local.sessao.atividadeid.espacoid.nome})
        else:
            inscricao_sessoes = Inscricaosessao.objects.filter(inscricao=self,
                sessao__dia=dia, sessao__horarioid__inicio__gt=horario).order_by('sessao__horarioid__inicio')
            for local in inscricao_sessoes:
                destino.append({'key': local.sessao.atividadeid.espacoid.id,
                                'value': local.sessao.atividadeid.espacoid.nome})
        print(inscricao_sessoes)
        if len(destino) == 0:
            destino.append({'key': inscricao_sessoes.last().sessao.atividadeid.espacoid.id,
                            'value': inscricao_sessoes.last().sessao.atividadeid.espacoid.nome})

        return destino


class Responsavel(models.Model):
    inscricao = models.ForeignKey(Inscricao, models.CASCADE)
    nome = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)
    tel = PhoneNumberField()

    class Meta:
        db_table = 'Responsavel'


class Inscricaoprato(models.Model):
    inscricao = models.ForeignKey(Inscricao, models.CASCADE)
    # prato = models.ForeignKey('configuracao.Prato', models.CASCADE)
    campus = models.ForeignKey('configuracao.Campus', models.CASCADE)
    npratosalunos = models.IntegerField()
    npratosdocentes = models.IntegerField()

    class Meta:
        db_table = 'InscricaoPrato'
        # unique_together = (('inscricao', 'prato'),)


class Inscricaosessao(models.Model):
    inscricao = models.ForeignKey(
        Inscricao, models.CASCADE)
    sessao = models.ForeignKey(
        'atividades.Sessao', models.CASCADE)
    nparticipantes = models.IntegerField(
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(300),
            # TODO: Adicionar validação de nparticipantes <= vagas na sessão
        ]
    )

    class Meta:
        db_table = 'InscricaoSessao'
        unique_together = (('inscricao', 'sessao'),)
        ordering = ['sessao__horarioid__inicio']


class Inscricaotransporte(models.Model):
    inscricao = models.ForeignKey(
        Inscricao, models.CASCADE)
    transporte = models.ForeignKey(
        'configuracao.Transportehorario', models.CASCADE)
    npassageiros = models.IntegerField(
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(300),
            # TODO: Adicionar validação de npassageiros <= vagas no transporte
        ]
    )

    class Meta:
        db_table = 'InscricaoTransporte'
        unique_together = (('inscricao', 'transporte'),)
