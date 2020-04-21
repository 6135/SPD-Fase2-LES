from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import *
from .models import *
from utilizadores.models import *
from datetime import datetime, timezone,date, time
from atividades.models import Espaco
from django.core import serializers
from django.core.serializers import json

# Create your views here.

def homepage(request):
	return render(request=request,
				  template_name="configuracao/inicio.html",)

def orderBy(request, list_diaaberto):
	if request.method == 'POST':
		search_specific = request.POST['searchAno']
		if search_specific != "" and int(search_specific) > 0:
			list_diaaberto = list_diaaberto.filter(ano=search_specific)
		sort_by = request.POST['orderBy']
		if sort_by == "":
			sort_by = '-ano'
		list_diaaberto = list_diaaberto.order_by(sort_by)

	else:
		list_diaaberto = list_diaaberto.order_by('-ano')
		search_specific = ""
	
	return {'list_diaaberto': list_diaaberto, 
			'current': {'specific_year': search_specific,}
			}

def showBy(request, list_diaaberto):
	if request.method == 'POST':
		today = datetime.now(timezone.utc)
		if request.POST['showBy'] == '1':
			list_diaaberto = list_diaaberto.filter(datadiaabertofim__gte=today)
		elif request.POST['showBy'] == '2':
			list_diaaberto = list_diaaberto.filter(dataporpostaatividadesfim__gte=today)
		elif request.POST['showBy'] == '3':
			list_diaaberto = list_diaaberto.filter(datainscricaoatividadesfim__gte=today)
	return list_diaaberto

def viewDays(request):

	if request.method == 'POST':
		formFilter = diaAbertoFilterForm(request.POST)
	else:
		formFilter = diaAbertoFilterForm()

	list_diaaberto = Diaaberto.objects.all()	#Obtain all days

	earliest = Diaaberto.objects.all().order_by('ano').first()	#Obtain some constants
	latest = Diaaberto.objects.all().order_by('ano').last()
	current = Diaaberto.objects.get(ano=datetime.now().year)
	is_open =(current.datadiaabertofim > datetime.now(timezone.utc))

	filterRes = orderBy(request, list_diaaberto)		#Filter/order
	list_diaaberto = filterRes['list_diaaberto']
	current = filterRes['current']

	list_diaaberto = showBy(request,list_diaaberto)

	return render(request=request,
				  template_name='configuracao/listaDiaAberto.html', 
				  context = {'form':formFilter, 'diaabertos': list_diaaberto, 'earliest': (earliest.ano), 
							'latest': (latest.ano), 'is_open': is_open, 'current': current,
							}
					)

def newDay(request, id=None):

	if id is None:
		dia_aberto = Diaaberto(administradorutilizadorid=Administrador.objects.get(id='1'))
	else:
		dia_aberto = Diaaberto.objects.get(id=id,administradorutilizadorid=1)
		
	dia_aberto_form = diaAbertoSettingsForm(instance=dia_aberto)

	if request.method == 'POST':
		submitted_data = request.POST.copy()
		dia_aberto_form = diaAbertoSettingsForm(submitted_data, instance=dia_aberto)

		if dia_aberto_form.is_valid():
			dia_aberto_form.save()
			return redirect('diasAbertos')

	return render(request=request,
				template_name = 'configuracao/diaAbertoForm.html',
				context = {'form': dia_aberto_form})

def delDay(request, id=None):

	if id is not None:
		dia_aberto = Diaaberto.objects.filter(id=id,administradorutilizadorid=1)
		dia_aberto.delete()
	return redirect('diasAbertos')

def view_days_as_json(request): 
	dias = Edificio.objects.all()
	dias_as_json = serializers.serialize('json',list(dias))
	return render(request=request,
				  template_name='configuracao/blank.html', 
				  context = {'dias_as_json': dias_as_json}
				)
def viewMenus(request):
	return render(request=request,
				  template_name='configuracao/listaMenu.html',
				  context = {'menus': Menu.objects.all()}
				)

def newMenu(request, id = None):
	menu_object = Menu()
	if id is not None:
		menu_object = Menu.objects.get(id=id)
	menu_form = menuForm(instance=menu_object)
	if request.method == 'POST':
		submitted_data = request.POST.copy()
		menu_form = menuForm(submitted_data,instance=menu_object)

		if menu_form.is_valid():
			menu_form_object = menu_form.save(commit=False)
			menu_form_object.horarioid = Horario.objects.get(inicio='12:00:00',fim='14:00:00')
			menu_form_object.campus = Campus.objects.get(id=submitted_data['campus'])
			menu_form_object.diaaberto = Diaaberto.objects.get(id=submitted_data['diaaberto'])
			menu_form_object.save()
			return redirect('novoPrato', menu_form_object.id)

	return render(request=request,
				  template_name='configuracao/menuForm.html',
				  context = {'form': menu_form}
				)

def delMenu(request, id = None):
	menu=Menu.objects.get(id=id)
	menu.delete()
	return redirect('verMenus')


def newPrato(request, id):
	pratos = Prato.objects.filter(menuid=Menu.objects.get(id=id))
	has_one = pratos.count() > 0
	prato_object = Prato(menuid=Menu.objects.get(id=id))
	prato_form=pratosForm(instance=prato_object)
	if request.method == 'POST':
		prato_form=pratosForm(request.POST,instance=prato_object)
		if prato_form.is_valid():
			prato_form.save()
			if 'save' in request.POST:
				print('save found')
				return redirect('verMenus')
			else:
				return redirect('novoPrato',id)
	return render(request=request,
				  template_name='configuracao/pratoForm.html',
				  context = {'form': prato_form, 'pratos': pratos, 'has_one': has_one}
				)

def delPrato(request, id):
	prato=Prato.objects.get(id=id)
	menuid=prato.menuid.id
	prato.delete()
	return redirect('novoPrato',menuid)