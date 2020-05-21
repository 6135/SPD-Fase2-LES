from django.forms import * 
from .models import Atividade, Sessao,Materiais,Tema
from datetime import datetime
from configuracao.models import Campus, Horario, Espaco, Departamento


def get_choices_time():
    return [(str(t),t) for t in range(5, 61, 5)]  

class DateTimeWidget(DateTimeInput):
    
    def __init__(self, attrs=None, format=None, input_type=None, default=None):
        #input_type = 'datetime-local'
        now = datetime.now()
        if input_type is not None:
            self.input_type=input_type
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            if default is not None:
                self.attrs = {'class': 'input', 'value': default}
            else:
                self.attrs = {'class': 'input', 'value': str(now.date()) + ' ' + str(now.time().strftime('%H:%M'))}
        if format is not None:
            self.format = format
        else: 
            self.format = '%Y-%m-%d'


class AtividadeForm(ModelForm):
    tema = ChoiceField(choices=[(tema.id,tema.tema) for tema in Tema.objects.all()])
    duracaoesperada= ChoiceField(choices=get_choices_time())
    class Meta:  
        model = Atividade  
        exclude = ['coordenadorutilizadorid', 'professoruniversitarioutilizadorid','datasubmissao', 'dataalteracao','estado','id','diaabertoid','tema','espacoid',]
        widgets = {
            'nome': TextInput(attrs={'class': 'input'}),
            'tipo': Select(),
            'descricao': Textarea(attrs={'class':'textarea'}),
            'publicoalvo': Select(),
            'nrcolaboradoresnecessario': NumberInput(attrs={'class': 'input'}),
            'tempo': DateField(widget=DateInput(attrs={'class':'timepicker'})),
            'participantesmaximo': NumberInput(attrs={'class': 'input'}),
            'duracaoesperada': Select(),
            }


class SessaoForm(ModelForm):
    class Meta:
        model = Sessao
        fields = ["dia"]
        

class MateriaisForm(ModelForm):
    class Meta:
        model = Materiais  
        exclude = ["atividadeid"]
        widgets = {
            'nomematerial': TextInput(attrs={'class': 'input'}),
            }

class atividadesFilterForm(Form):
    searchAtividade = CharField(widget=TextInput(attrs={'class': 'input','placeholder':'Atividade'}), required=False)
    Aceite=BooleanField(widget=CheckboxInput(),required=False)
    Recusada=BooleanField(widget=CheckboxInput(),required=False)
    Pendente=BooleanField(widget=CheckboxInput(),required=False)
    diaAbertoAtual=BooleanField(widget=CheckboxInput(),required=False)
    dep=[(-1,'Mostra todos os Departamentos')] + [(departamento.id,departamento.nome) for departamento in Departamento.objects.all()]
    departamentos = ChoiceField(choices=dep,widget=Select(), required=False)
    tipo = ChoiceField(choices=[
        (" ", "Mostrar todos os tipos de Atividade"),
        ("Atividade Laboratorial", "Atividade Laboratorial"),
        ("Tertulia", "Tertulia"),
        ("Palestra", "Palestra")
     ],widget=Select())


class CampusForm(Form):
    campus= ChoiceField(choices= Campus.objects.all(),label='Campus')

    class Meta:
        fields=('campus')