from django.forms import * 
from .models import *
from atividades.models import Atividade,Sessao
from utilizadores.models import Colaborador,Coordenador
from configuracao.models import Departamento, Diaaberto, Horario, Espaco
from datetime import datetime,timezone,timedelta
from inscricoes.models import Inscricao,Inscricaosessao

def get_dias():
    try:
        today= datetime.now(timezone.utc) 
        diaaberto=Diaaberto.objects.get(datadiaabertoinicio__gte=today,datadiaabertofim__gte=today)
        diainicio= diaaberto.datadiaabertoinicio.date()
        diafim= diaaberto.datadiaabertofim.date()
        totaldias= diafim-diainicio+timedelta(days=1)
        return [('','Escolha o dia')]+[(diainicio+timedelta(days=d),diainicio+timedelta(days=d))for d in range(totaldias.days)]
    except:
        return [('','Escolha o dia')]

class CustomTimeWidget(TimeInput):

    def __init__(self, attrs=None, format=None, input_type=None, default=None):
        input_type = 'time'
        if input_type is not None:
            self.input_type=input_type
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            if default is not None:
                self.attrs = {'class': 'input', 'value': default}
        if format is not None:
            self.format = format
        else: 
            self.format = '%H:%M'

def get_atividades_choices():
    return [(" ",'Escolha a Atividade')]+[(atividade.id,atividade.nome) for atividade in Atividade.tarefas_get_atividades()]

class TarefaAuxiliarForm(Form):
    atividade = ChoiceField(widget=Select(attrs={'onchange':'diasSelect();'}),choices=get_atividades_choices)
    dia = DateField(widget=Select(attrs={'onchange':'sessoesSelect()'}))
    sessao = IntegerField(widget=Select(attrs={'onchange':'colaboradoresSelect()'}))
    colab = CharField(widget=Select(),required=False)

    def save(self,user,id):
        data = self.cleaned_data
        estado = 'naoConcluida'
        
        sessao = Sessao.objects.get(id = data.get('sessao'))
        if data.get('colab') == '':
            estado = 'naoAtribuida'
            colab = None
        else:
            colab = Colaborador.objects.get(id = data.get('colab'))
        atividade = Atividade.objects.get(id = data.get('atividade'))
        nome = 'Auxiliar na atividade ' + atividade.nome
        if id is None:
            tarefa=Tarefa.objects.create(nome= nome,estado= estado,coord=user,colab=colab,dia=data.get('dia'),horario=sessao.horarioid.inicio)
            TarefaAuxiliar.objects.create(tarefaid=tarefa,sessao=sessao)
        else:
            Tarefa.objects.filter(id=id).update(nome= nome,estado= estado,coord=user,colab=colab,dia=data.get('dia'),horario=sessao.horarioid.inicio)
            TarefaAuxiliar.objects.filter(tarefaid=id).update(sessao=sessao)

def get_inscricao_choices():
    return [('','Escolha um grupo')]+[(grupo.id,'Grupo '+str(grupo.id)) for grupo in Inscricao.objects.filter(individual=False)]

class TarefaAcompanharForm(Form):
    grupo = ChoiceField(widget=Select(attrs={'onchange':'diasGrupo();grupoInfo();'}),choices=get_inscricao_choices)
    dia = DateField(widget=Select(attrs={'onchange':'grupoHorario()'}))
    horario = TimeField(widget=Select(attrs={'onchange':'grupoOrigem()'}))
    origem = CharField(widget=Select(attrs={'onchange':'grupoDestino()'}))
    destino = CharField(widget=Select(attrs={'onchange':'colaboradoresSelect()'}))
    colab = CharField(widget=Select(),required=False)
    
    def save(self,user,id):
        data = self.cleaned_data
        nome = 'Acompanhar o grupo ' + data.get('grupo')
        grupo = Inscricao.objects.get(id=data.get('grupo'))
        
        destino = Espaco.objects.get(id=int(data.get('destino')))
        
        estado = 'naoConcluida'
        if data.get('colab') == '':
            estado = 'naoAtribuida'
            colab = None
        else:
            colab = Colaborador.objects.get(id = data.get('colab'))

        origem = data.get('origem')
        

        if  origem != 'Check in':
            local = Espaco.objects.get(id=int(origem))
            origem = str(local.id)  
        
        if id is None:
            tarefa = Tarefa.objects.create(nome= nome,estado= estado,coord=user,colab=colab,dia=data.get('dia'),horario=data.get('horario'))
            TarefaAcompanhar.objects.create(tarefaid=tarefa,origem=origem,destino=str(destino.id),inscricao=grupo)  
        else:
            Tarefa.objects.filter(id=id).update(nome= nome,estado= estado,coord=user,colab=colab,dia=data.get('dia'),horario=data.get('horario'))
            TarefaAcompanhar.objects.filter(tarefaid=id).update(origem=origem,destino=str(destino.id),inscricao=grupo)


class TarefaOutraForm(Form):
    dia = ChoiceField(widget=Select(attrs={'onchange':'sessoesSelect()'}),choices=get_dias())
    horario = TimeField(widget=TimeInput(attrs={'class':'input','type':'time','min':'09:00','max':'18:00','onchange':'colaboradoresSelect();'}))
    descricao = CharField(widget=Textarea(attrs={'class':'textarea'}))
    colab = CharField(widget=Select(),required=False)

    def save(self,user,id=None):
        data = self.cleaned_data
        nome = self.data.get('descricao')
        estado = 'naoConcluida'
        if data.get('colab') == '':
            estado = 'naoAtribuida'
            colab = None
        else:
            colab = Colaborador.objects.get(id = data.get('colab'))
        if id is None:
            tarefa = Tarefa.objects.create(nome= nome[0:18] + '...',estado= estado,coord=user,colab=colab,dia=data.get('dia'),horario=data.get('horario'))
            TarefaOutra(tarefaid=tarefa,descricao=data.get('descricao')).save()
        elif id:
            Tarefa.objects.filter(id=id).update(nome= nome[0:18] + '...',estado= estado,coord=user,colab=colab,dia=data.get('dia'),horario=data.get('horario'))
            TarefaOutra.objects.filter(tarefaid=id).update(descricao=data.get('descricao'))











#class TarefaForm(ModelForm):
#    horarioTime = TimeField(widget=TimeInput(attrs={'class':'timepicker','type':'time','min':'09:00','max':'18:00'}),required=False)
#    horarioSelect = ChoiceField(widget=Select(),choices=[('','Escolha o horario')],required=False)
#    dias = ChoiceField(widget=Select(),choices = get_dias(),required=False)
#    diasDependentes = ChoiceField(widget=Select(),choices = [('','Escolha o horario')],required=False)
#
#    def clean(self):
#        cleaned_data=super().clean()
#        if cleaned_data.get('tipo') == 'tarefaOutra':
#            self.instance.horario = cleaned_data.get('horarioTime')
#            self.instance.dia = cleaned_data.get('dias')
#        else:
#            if cleaned_data.get('tipo') == 'tarefaAuxiliar':
#                sessao = Sessao.objects.get(id=self.data['sessao'])
#                self.instance.horario = sessao.horarioid.inicio
#            else:   
#                self.instance.horario = cleaned_data.get('horarioSelect')
#            self.instance.dia = cleaned_data.get('diasDependentes')
#
#        estado = 'naoConcluida'
#        if cleaned_data.get('colab') is None:
#            estado = 'naoAtribuida'
#        self.instance.estado = estado
#        if self.data.get('atividades'):
#            nome = Atividade.objects.get(id=self.data.get('atividades')).nome
#        if cleaned_data.get('tipo') == 'tarefaAuxiliar':
#            self.instance.nome = 'Auxiliar na atividade '+nome
#        if cleaned_data.get('tipo') == 'tarefaAcompanhar':
#            nome = self.data.get('inscricao')
#            self.instance.nome = 'Acompanhar o Grupo '+nome
#        elif cleaned_data.get('tipo') == 'tarefaOutra':
#            nome = self.data.get('descricao')
#            self.instance.nome = nome[0:18] + '...'
#            
#    class Meta:  
#        model = Tarefa 
#        exclude = ['coord','id','nome','created_at','estado','horario','dia']
#        widgets = {
#            'tipo': RadioSelect(attrs={'class':'radio'},choices=[('tarefaAuxiliar','Auxiliar Atividade'),('tarefaAcompanhar','Acompanhar participantes'),('tarefaOutra','Outra')]),
#            }
#
#    def __init__(self,user,*args, **kwargs):
#        super().__init__(*args, **kwargs)
#        coordenador = Coordenador.objects.get(user_ptr_id=user)
#        self.fields['colab'].queryset =  Colaborador.objects.filter(faculdade = coordenador.faculdade,utilizador_ptr_id__valido=True).order_by('utilizador_ptr_id__user_ptr_id__first_name')
#        self.instance.coord = Coordenador.objects.get(utilizador_ptr_id__user_ptr_id=user)
#        if 'atividades' in self.data:
#            try:
#                sessoes = Sessao.objects.filter(atividadeid=self.data['atividades'])
#                self.fields['colab'].queryset = Colaborador.objects.filter().order_by('utilizador_ptr_id__user_ptr_id__first_name')
#            except (ValueError, TypeError):
#                pass  
#        elif self.instance.pk:
#            self.fields['colab'].queryset = Colaborador.objects.none()
#
#def get_atividades_choices():
#    return [(" ",'Escolha a Atividade')]+[(atividade.id,atividade.nome) for atividade in Atividade.objects.filter(nrcolaboradoresnecessario__gt=0,estado='Aceite')]
#
#class TarefaAuxiliarForm(ModelForm):
#    atividades= ChoiceField(choices=get_atividades_choices,widget=Select(attrs={'onchange':'diasSelect();'}))
#
#    def __init__(self,*args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self.fields['sessao'].queryset =  Sessao.objects.none()
#        if 'diasDependentes' in self.data:
#            try:
#                dia = self.data.get('diasDependentes')
#                atividade = self.data.get('atividades')
#                self.fields['sessao'].queryset = Sessao.objects.filter(dia=dia,atividadeid=atividade)
#            except (ValueError, TypeError):
#                pass  
#        elif self.instance.pk:
#            self.fields['sessao'].queryset = Sessao.objects.none()
#            
#    class Meta:
#        model= TarefaAuxiliar
#        exclude = ['tarefaid']
#        widgets = {   
#            'sessao' : Select(choices=[('','Escolha o horario')])      
#        } 
#            
#def get_inscricao_choices():
#    return [('','Escolha um grupo')]+[(grupo.id,'Grupo '+str(grupo.id)) for grupo in Inscricao.objects.filter(nalunos__gt=1)]
#
#class TarefaAcompanharForm(ModelForm):
#    inscricao =  ChoiceField(choices=get_inscricao_choices,widget=Select(attrs={'onchange':'grupoInfo();diasGrupo();'}))
#    class Meta:
#        model= TarefaAcompanhar
#        exclude = ['tarefaid','inscricao','dias']
#        widgets ={
#            'origem' : Select(choices=[('','Escolha o local de encontro')],attrs={'onchange':'grupoDestino();'}),
#            'destino' : Select(choices=[('','Escolha o local de destino')],)
#        }
#
#    def clean(self):
#        cleaned_data=super().clean()
#        self.instance.inscricao = Inscricao.objects.get(id=cleaned_data['inscricao']) 
#        
#def get_dia_choices():
#    return [('','Escolha o dia')]+get_dias()
#
#class TarefaOutraForm(ModelForm):
#    class Meta:
#        model= TarefaOutra
#        exclude = ['tarefaid']
#        widgets = {
#            'descricao' : Textarea(attrs={'class':'textarea'}),
#            }           
#   
def get_dep_choices():
    return [(-1,'Mostra todos os Departamentos')] + [(departamento.id,departamento.nome) for departamento in Departamento.objects.all()]

class tarefaFilterForm(Form):
    searchTarefa = CharField(widget=TextInput(attrs={'class': 'input','placeholder':'Pesquisa'}), required=False)
    Concluida=BooleanField(widget=CheckboxInput(),required=False)
    naoConcluida=BooleanField(widget=CheckboxInput(),required=False)
    naoAtribuida=BooleanField(widget=CheckboxInput(),required=False)
    departamentos = ChoiceField(choices=get_dep_choices,widget=Select(), required=False)
    tipo = ChoiceField(choices=[
        (" ", "Mostrar todos os tipos de Tarefa"),
        ("tarefaAcompanhar", "Acompanhar"),
        ("tarefaAuxiliar", "Auxiliar"),
        ("tarefaOutra", "Outra")
     ],widget=Select())
