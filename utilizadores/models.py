from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from atividades import models as amodels
from colaboradores.models import ColaboradorHorario
from coordenadores import models as coordmodels
from django.db.models import Q
class Utilizador(User):
    contacto = PhoneNumberField(max_length=20, blank=False, null=False)
    valido = models.CharField(max_length=255, blank=False, null=False)

    def getProfiles(self):
        type = ''
        if Administrador.objects.filter(utilizador_ptr_id=self):
            type = self.concat(type=type, string='Administrador')
        if Participante.objects.filter(utilizador_ptr_id=self):
            type = self.concat(type=type, string='Participante')
        if ProfessorUniversitario.objects.filter(utilizador_ptr_id=self):
            type = self.concat(type=type, string='ProfessorUniversitario')
        if Coordenador.objects.filter(utilizador_ptr_id=self):
            type = self.concat(type=type, string='Coordenador')
        if Colaborador.objects.filter(utilizador_ptr_id=self):
            type = self.concat(type=type, string='Colaborador')
        return type

    def concat(self, type, string):
        if type == '':
            type = string
        else:
            type += ', '+string
        return type

    @property
    def firstProfile(self):
        return self.getProfiles().split(' ')[0]

    def getUser(self):
        user = User.objects.get(id=self.id)
        if user.groups.filter(name = "Coordenador").exists():
            result = Coordenador.objects.get(id=self.id)
        elif user.groups.filter(name = "Administrador").exists():
            result = Administrador.objects.get(id=self.id)
        elif user.groups.filter(name = "ProfessorUniversitario").exists():
            result = ProfessorUniversitario.objects.get(id=self.id)
        elif user.groups.filter(name = "Colaborador").exists():
            result = Colaborador.objects.get(id=self.id)
        elif user.groups.filter(name = "Participante").exists():
            result = Participante.objects.get(id=self.id)
        else:
            result = None
        return result   


    def getProfile(self):
        user = User.objects.get(id=self.id)
        if user.groups.filter(name = "Coordenador").exists():
            result = "Coordenador"
        elif user.groups.filter(name = "Administrador").exists():
            result = "Administrador"
        elif user.groups.filter(name = "ProfessorUniversitario").exists():
            result = "ProfessorUniversitario"
        elif user.groups.filter(name = "Colaborador").exists():
            result = "Colaborador"
        elif user.groups.filter(name = "Participante").exists():
            result = "Participante"
        else:
            result = None
        return result 

    def emailValidoUO(self,uo):
        user = User.objects.get(email=self.email)
        if user.groups.filter(name = "Coordenador").exists():
            utilizador = Coordenador.objects.get(email=self.email)
        elif user.groups.filter(name = "Administrador").exists():
            return True
        elif user.groups.filter(name = "ProfessorUniversitario").exists():
            utilizador = ProfessorUniversitario.objects.get(email=self.email)
        elif user.groups.filter(name = "Colaborador").exists():
            utilizador = Colaborador.objects.get(email=self.email)
        else:
            return False
        if utilizador.faculdade == uo:
            return True
        else:
            return False   

    def emailValidoParticipante(self):
        user = User.objects.get(email=self.email)
        if user.groups.filter(name = "Administrador").exists():
            return True
        else:
            return False    
    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name
    class Meta:
        db_table = 'Utilizador'


class Administrador(Utilizador):
    gabinete = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        db_table = 'Administrador'


class Participante(Utilizador):
    class Meta:
        db_table = 'Participante'


class ProfessorUniversitario(Utilizador):
    gabinete = models.CharField(
        db_column='Gabinete', max_length=255, blank=False, null=False)

    faculdade = models.ForeignKey(
        'configuracao.Unidadeorganica', models.CASCADE)

    departamento = models.ForeignKey(
        'configuracao.Departamento', models.CASCADE)

    def __str__(self):
        return str(self.gabinete) + ' ' + str(self.faculdade) + ' ' + str(self.departamento)
    class Meta:
        db_table = 'ProfessorUniversitario'


class Coordenador(Utilizador):
    gabinete = models.CharField(
        db_column='Gabinete', max_length=255, blank=False, null=False)

    faculdade = models.ForeignKey(
        'configuracao.Unidadeorganica', models.CASCADE, db_column='FaculdadeID')

    departamento = models.ForeignKey(
        'configuracao.Departamento', models.CASCADE, db_column='DepartamentoID')

    class Meta:
        db_table = 'Coordenador'

    def __str__(self):
        return self.first_name


class Colaborador(Utilizador):
    curso = models.ForeignKey(
        'configuracao.Curso', models.CASCADE)

    faculdade = models.ForeignKey(
        'configuracao.Unidadeorganica', models.CASCADE)

    departamento = models.ForeignKey(
        'configuracao.Departamento', models.CASCADE)

    class Meta:
        db_table = 'Colaborador'

    @staticmethod
    def get_free_colabs(coord,dia,horario,sessao=None):
        free_colabs=[]
        colabs = Colaborador.objects.filter(faculdade = coord.faculdade,utilizador_ptr_id__valido=True)
        free = True
        for colab in colabs: 
            tarefas = coordmodels.Tarefa.objects.filter(colab = colab.id,horario=horario,dia=dia)
            if tarefas.exists():
                continue
            elif sessao is not None:
                s = amodels.Sessao.objects.get(id=int(sessao))
                inicio = s.horarioid.inicio
                fim = s.horarioid.fim
                if coordmodels.Tarefa.objects.filter(colab = colab.id,dia=dia,horario__gte=inicio).filter(horario__lte=fim).exists(): 
                    continue
                if coordmodels.TarefaAuxiliar.objects.filter(tarefaid__colab = colab.id,tarefaid__dia=dia,sessao__horarioid__inicio__lte=inicio,sessao__horarioid__fim__gte=inicio).exists():
                    continue
                free_colabs.append(colab)
            elif sessao is None:
                free=True
                tarefas = coordmodels.Tarefa.objects.filter(colab = colab.id,dia=dia)
                for t in tarefas:
                    h = datetime.strptime(horario,'%H:%M')     
                    if datetime.strptime(str(t.horario),'%H:%M:%S') - h <  timedelta(hours=0,minutes=15,seconds=0) and h - datetime.strptime(str(t.horario),'%H:%M:%S') > timedelta(days=-1,hours=23,minutes=45) :
                        free=False     
                if coordmodels.TarefaAuxiliar.objects.filter(tarefaid__colab = colab.id,tarefaid__dia=dia)\
                    .filter(sessao__horarioid__inicio__lte=horario,sessao__horarioid__fim__gte=horario).exists(): 
                    continue
                if free == True:
                    free_colabs.append(colab)

        print(free_colabs)
        return free_colabs



    def get_horarios_disponiveis(self):
        return ColaboradorHorario.objects.filter(colab=self.id)

    def get_preferencia_atividade(self):
        horarios = self.get_horarios_disponiveis()
        atividades = []
        for horario in horarios:
            atividades.append(amodels.Atividade.objects.filter(inicio__gte=horario.inicio,fim__lte=horario.fim,estado="Aceite",professoruniversitarioutilizadorid__faculdade=self.faculdade))
        atividades = list(dict.fromkeys(atividades))
        return list_to_queryset(amodels.Atividade,atividades)


def list_to_queryset(model, data):
    from django.db.models.base import ModelBase
    if not isinstance(model, ModelBase):
        raise ValueError(
            "%s must be Model" % model
        )
    if not isinstance(data, list):
        raise ValueError(
            "%s must be List Object" % data
        )
    pk_list = [obj.pk for obj in data]
    return model.objects.filter(pk__in=pk_list)