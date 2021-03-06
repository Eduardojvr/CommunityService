from email.mime.text import MIMEText
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import CommunityActionForm, DonationForm, HealthServiceForm, EstablishmentForm , VoluntaryServiceForm
from .models import Establishment, HealthService, Donation, VoluntaryService
# from .models import Divulgacoes
import requests

import urllib, json
import smtplib

# @login_required
# def formevent(request):
#     if request.method == 'POST':
#         divulgacao = Establishment()
#         divulgacao.nomeEvento = request.POST['nomeEvento']
#         divulgacao.categoria = request.POST['categoria']
#         divulgacao.cidade = request.POST['cidade']
#         #divulgacao.bairro = request.POST['bairro']
#         divulgacao.endereco = request.POST['endereco']
#         #divulgacao.cep = request.POST['cep']
#         divulgacao.telefone = request.POST['telefone']
#         divulgacao.horarioInicio = request.POST['horarioInicio']
#         divulgacao.horarioFim = request.POST['horarioFim']
#         divulgacao.data = request.POST['data']
#         divulgacao.user = request.user
#         divulgacao.save()
#         return render(request , 'index.html')
#     return render(request , 'formevent.html')

def mapa(request, id):
    latitude = 0
    longitude = 0
    # if request.method == "POST":
    chave = "AIzaSyDroa8JCUm2JfRZ_7eVMb4Fqx8ufr0Mz_A"
    div = Establishment.objects.get(id=id)
    address = div.endereco+"+"+div.cidade
    r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+address+"&key="+chave)
    if r.status_code == 200:
        dados = json.loads(r.content)
        latitude = dados["results"][0]["geometry"]["location"]["lat"]
        longitude = dados["results"][0]["geometry"]["location"]["lng"]
            #print(latitude)
            #print(longitude)
    return render(request, 'mapa.html', {'latitude':latitude, 'longitude': longitude})
    # return render(request, 'index.html')



def servicolist(request):
    estabelecimentos = Establishment.objects.all()
    saude = HealthService.objects.all()
    doacao = Donation.objects.all()
    return render(request, 'servicolist.html', {'estabelecimentos':estabelecimentos,'saude':saude,'doacao':doacao})

@login_required
def create_establishment(request):
    title = "Cadastrar Estabelecimento"
    if request.method == "POST":
        form = EstablishmentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("index"))
        return render(request, 'establishment.html', {'form': form,'title':title})

    else:
        form = EstablishmentForm()
        return render(request, 'establishment.html', {'form': form,'title':title})

@login_required
def create_voluntary(request):
    title = "Cadastrar Voluntário"
    if request.method == "POST":
        form = VoluntaryServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("index"))
        return render(request, 'establishment.html', {'form': form,'title':title})

    else:
        form =  VoluntaryServiceForm()
        return render(request, 'establishment.html', {'form': form,'title':title})

from .forms import CommunityActionForm, DonationForm, HealthServiceForm, EstablishmentForm 

@login_required 
def create_health_service(request):
    title = "Cadastrar Serviço"
    if request.method == "POST":
        form = HealthServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("index"))
        return render(request, 'establishment.html', {'form': form,'title':title})

    else:
        form = HealthServiceForm()
        return render(request, 'establishment.html', {'form': form,'title':title})

@login_required
def create_donation(request):
    title = "Cadastrar Doação"
    if request.method == "POST":
        form = DonationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("index"))
        return render(request, 'establishment.html', {'form': form,'title':title})

    else:
        form = DonationForm()
        return render(request, 'establishment.html', {'form': form,'title':title})

@login_required
def edit_establishment(request, id):
    title = "Editar Estabelecimento"
    establishment = get_object_or_404(Establishment, id=id)
    if request.method == "POST":
        form = EstablishmentForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
        return render(request, 'establishment.html', {'form': form,'title':title})
    else:
        form = EstablishmentForm(instance=establishment)
        return render(request, 'establishment.html', {'form': form,'title':title})

@login_required
def edit_health_service(request, id):
    title = "Editar Serviço de Saude"
    health_service = get_object_or_404(HealthService, id=id)
    if request.method == "POST":
        form = HealthServiceForm(request.POST, instance=health_service)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
        return render(request, 'establishment.html', {'form': form,'title':title})
    else:
        form = HealthServiceForm(instance=health_service)
        return render(request, 'establishment.html', {'form': form,'title':title})

@login_required
def edit_donation(request, id):
    title = "Editar Doação"
    donation = get_object_or_404(Donation, id=id)
    if request.method == "POST":
        form = DonationForm(request.POST, instance=donation)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
        return render(request, 'establishment.html', {'form': form,'title':title})
    else:
        form = DonationForm(instance=donation)
        return render(request, 'establishment.html', {'form': form,'title':title})

@login_required
def edit_voluntary(request, id):
    title = "Editar Voluntário"
    voluntary = get_object_or_404(VoluntaryService, id=id)
    if request.method == "POST":
        form = VoluntaryServiceForm(request.POST, instance=voluntary)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
        return render(request, 'establishment.html', {'form': form,'title':title})
    else:
        form = VoluntaryServiceForm(instance=voluntary)
        return render(request, 'establishment.html', {'form': form,'title':title})

@login_required
def delete_establishment(request, id):
    establishment = get_object_or_404(Establishment, id=id)
    establishment.delete()
    return render(request, 'delete.html')

@login_required
def delete_health_service(request, id):
    health_service = get_object_or_404(HealthService, id=id)
    health_service.delete()
    return render(request, 'delete.html')

@login_required
def delete_donation(request, id):
    delete_donation = get_object_or_404(Donation, id=id)
    delete_donation.delete()
    return render(request, 'delete.html')

@login_required
def delete_voluntary(request, id):
    delete_voluntary = get_object_or_404(VoluntaryService, id=id)
    delete_voluntary.delete()
    return render(request, 'delete.html')

def list_establishment(request):
    establishments = Establishment.objects.all()
    print(establishments)
    return render(request, 'list_establishment.html', {"establishments": establishments})

def list_health_service(request):
    health_services = HealthService.objects.all() 
    return render(request, 'list_health_service.html', {"health_services": health_services})

def list_donation(request):
    donations = Donation.objects.all()
    return render(request, 'list_donation.html', {"donations": donations})

def list_voluntary(request):
    volunteers = VoluntaryService.objects.all()
    print(volunteers)
    return render(request, 'list_voluntary.html', {"volunteers": volunteers})

def fale_conosco(request, id):
    servico = HealthService.objects.get(id=id)
    if request.method == "POST":
        nome = request.POST['nome']
        email = request.POST['email']
        texto = request.POST['mensagem']
        m = MIMEText(texto)
        m.set_charset('utf-8')
        m['Subject'] = email
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login('noreplayfiscae@gmail.com', 'fiscaeunb')
        mail.sendmail('noreplayfiscae@gmail.com', email, m.as_string())
    return render(request, 'fale-conosco.html', {"servico": servico})

def perfil(request, id):
    servico = HealthService.objects.get(id=id)
    return render(request, 'perfil.html', {"servico":servico})
