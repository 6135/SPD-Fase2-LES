from django.db import models
from django.core import validators
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime,time,timedelta
from configuracao.models import Horario

class Escola(models.Model):
    nome = models.CharField(max_length=200)
    local = models.CharField(max_length=128)

    class Meta:
        db_table = 'Escola'


class Inscricao(models.Model):
    nalunos = models.IntegerField()
    escola = models.ForeignKey(Escola, models.CASCADE)
    ano = models.IntegerField(
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(12)
        ]
    )
    turma = models.CharField(max_length=1)
    areacientifica = models.CharField(max_length=64)
    # TODO: Descomentar quando a gestão de utilizadores estiver pronta
    # participante = models.ForeignKey(
    #     'utilizadores.Participante', models.CASCADE)
    # TODO: Descomentar quando a configuração do Dia Aberto estiver pronta
    # diaaberto = models.ForeignKey('configuracao.Diaaberto', models.CASCADE)

    class Meta:
        db_table = 'Inscricao'

    def get_dias(self):
        inscricao_sessoes= Inscricaosessao.objects.filter(inscricao=self).order_by('sessao__dia')
        dias=[]
        dias = [sessao.sessao.dia for sessao in inscricao_sessoes]
        return [{'key':str(dia), 'value': dia} for dia in set(dias)]


    def get_horarios(self,dia):
        inscricao_sessoes = Inscricaosessao.objects.filter(inscricao=self,sessao__dia=dia).order_by('sessao__horarioid__inicio')
        horarios = []
        horarios.append({'key':inscricao_sessoes.first().sessao.horarioid.id, 'value':inscricao_sessoes.first().sessao.horarioid.inicio})
        for sessao in inscricao_sessoes:
            if sessao.sessao.horarioid not in horarios:
                horario = sessao.sessao.horarioid.inicio
                duracao = sessao.sessao.atividadeid.duracaoesperada*60
                td = (datetime.combine(datetime.min, horario) - datetime.min)
                secondsTotal = td.total_seconds() + duracao
                time = datetime.strptime(str(timedelta(seconds=secondsTotal)),"%H:%M:%S")
                horarios.append({'key':sessao.sessao.horarioid.id, 'value':time.strftime("%H:%M")})
        return horarios

    def get_origem(self,dia,horario_id):
        horario = Horario.objects.get(id=horario_id)
        first_session =  Inscricaosessao.objects.filter(inscricao=self,sessao__dia=dia).order_by('sessao__horarioid__inicio').first()
        inscricao_sessoes =  Inscricaosessao.objects.filter(inscricao=self,sessao__dia=dia,sessao__horarioid__inicio=horario.inicio).order_by('sessao__horarioid__inicio')
        origem = []

        if first_session.sessao.horarioid.inicio == inscricao_sessoes.first().sessao.horarioid.inicio:
            origem.append({'key':'Check in','value':'Check in'})
        else:
            for local in inscricao_sessoes:
                origem.append({'key':local.sessao.atividadeid.espacoid.nome,'value':local.sessao.atividadeid.espacoid.nome})
        return origem
    
    def get_destino(self,dia,horario_id):
        horario = Horario.objects.get(id=horario_id)
        inscricao_sessoes =  Inscricaosessao.objects.filter(inscricao=self).filter(sessao__dia=dia,sessao__horarioid__inicio=horario.inicio).order_by('sessao__horarioid__inicio')
        destino = []
        print(horario.inicio)
        print(inscricao_sessoes.first().sessao.horarioid.inicio)
        if horario.inicio == inscricao_sessoes.first().sessao.horarioid.inicio:
            destino.append({'key':inscricao_sessoes.first().sessao.atividadeid.espacoid.id,'value':inscricao_sessoes.first().sessao.atividadeid.espacoid.nome})
        else:
            for local in inscricao_sessoes:
                destino.append({'key':local.sessao.atividadeid.espacoid.id,'value':local.sessao.atividadeid.espacoid.nome})
        return destino


class Responsavel(models.Model):
    inscricao = models.ForeignKey(Inscricao, models.CASCADE)
    nome = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)
    tel = PhoneNumberField()

    class Meta:
        db_table = 'Responsavel'


class EscolaPortugal(models.Model):
    nome = models.CharField(max_length=200)

    class Meta:
        db_table = 'EscolaPortugal'


class Inscricaoprato(models.Model):
    inscricao = models.ForeignKey(Inscricao, models.CASCADE)
    # TODO: Descomentar quando a configuração dos pratos estiver pronta
    # prato = models.ForeignKey('configuracao.Prato', models.CASCADE)
    campus = models.ForeignKey('configuracao.Campus', models.CASCADE)
    npessoas = models.IntegerField(
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(300),
        ]
    )

    class Meta:
        db_table = 'InscricaoPrato'
        # TODO: Descomentar quando a configuração dos pratos estiver pronta
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


class Inscricaotransporte(models.Model):
    inscricao = models.ForeignKey(
        Inscricao, models.CASCADE)
    transporte = models.ForeignKey('configuracao.Transporte', models.CASCADE)
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
