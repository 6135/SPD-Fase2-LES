from django import template
from django.core.exceptions import ObjectDoesNotExist
from configuracao.forms import *
from configuracao.models import *
from atividades.models import Atividade
from configuracao import views
import json
from django.utils.html import format_html

register = template.Library()


@register.filter
def atividades_count_dep(value):
    return Atividade.objects.filter(
        professorutilizadorid__departamento_id=value
    ).count()


@register.filter
def atividades_count_uo(value):
    return Atividade.objects.filter(
        professorutilizadorid__departamento_id__unidadeorganicaid=value
    ).count()


@register.filter
def get_atividades_count(value):
    return Atividade.objects.filter(tema=value).count()


@register.filter
def get_salas_count(value):
    return Espaco.objects.filter(edificio=value).count()


@register.filter
def force_required(value):
    value_str = str(value)
    value_str = value_str[:-1] + " required>"
    print(value_str)
    return value_str


@register.filter
def transport_type(value):
    tipo = "Transporte Universitario"
    try:
        trans = value.transporte  # .transportepessoal
        # tipo = trans.tipo
    except ObjectDoesNotExist:
        pass
    return tipo


@register.filter
def transport_id(value):
    id = "Não aplicável"
    try:
        trans = value.transporte.transporteuniversitario
        id = value.transporte.identificador
    except ObjectDoesNotExist:
        pass
    return id


@register.filter
def vagas_cap(value):
    # vagas = "Não disponivel"
    cap = "Não disponivel"
    try:
        # vagas = value.transporte.transporteuniversitario.vagas
        cap = value.transporte.transporteuniversitario.capacidade
        # if value == 0:
        # vagas = "Sem vagas"
    except ObjectDoesNotExist:
        pass
    return str(cap)  # str(vagas) + '/' + str(cap)


@register.filter
def pretty_json(value):
    return json.dumps(value, indent=4)


@register.simple_tag
def current_email():
    return format_html(Diaaberto.current().emaildiaaberto)


@register.simple_tag
def current_ano():
    return Diaaberto.current().ano
