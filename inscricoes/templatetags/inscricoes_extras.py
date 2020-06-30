import base64
from io import StringIO
import urllib
from django import template
from ..models import Inscricao
from utilizadores.models import Participante
from configuracao.models import Diaaberto

register = template.Library()


@register.filter
def inscrito(user):
    return Inscricao.objects.filter(participante=user.id).exists()


@register.filter
def get64(url):
    """
    Method returning base64 image data instead of URL
    """
    if url.startswith("http"):
        image = StringIO(urllib.urlopen(url).read())
        return 'data:image/jpg;base64,' + base64.b64encode(image.read())

    return url


@register.simple_tag
def sala(request, atividade):
    return atividade.get_sala_str(request)


@register.filter
def min_date(diaaberto):
    try:
        return Diaaberto.objects.get(id=diaaberto).datadiaabertoinicio.strftime("%d/%m/%Y")
    except:
        return ''


@register.filter
def max_date(diaaberto):
    try:
        return Diaaberto.objects.get(id=diaaberto).datadiaabertofim.strftime("%d/%m/%Y")
    except:
        return ''
