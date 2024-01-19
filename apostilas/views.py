from django.shortcuts import redirect, render
from .models import Apostila, ViewApostila, AvaliacaoApostila
from django.contrib import messages
from django.contrib.messages import constants

# Create your views here.
#TODO trabalhar com tags


def adicionar_apostilas(request):
    if request.method == 'GET':
        apostilas = Apostila.objects.filter(user=request.user)    
        views_totais = ViewApostila.objects.filter(apostila__user = request.user).count()
            
        return render(request, 'adicionar_apostilas.html', {'apostilas': apostilas, 'views_totais': views_totais})
    elif request.method == 'POST':
        titulo = request.POST.get('titulo')
        arquivo = request.FILES['arquivo']

        apostila = Apostila(user=request.user, titulo=titulo, arquivos=arquivo)
        apostila.save()
        messages.add_message(
            request, constants.SUCCESS, 'Apostila adicionada com sucesso.'
        )
        return redirect('/apostilas/adicionar_apostilas/')
    
    
def apostila(request, id):
    if request.method == 'POST':
        avaliacao = request.POST.get('avaliacao')
        apostila = Apostila.objects.get(id=id)
        
        avaliacao = AvaliacaoApostila(
            user= request.user,
            apostila = apostila,
            avaliacao = avaliacao            
        )
        avaliacao.save()
    
    apostila = Apostila.objects.get(id=id)
    view = ViewApostila(
        ip=request.META['REMOTE_ADDR'],
        apostila=apostila
    )
    view.save()
    views_unicas = ViewApostila.objects.filter(apostila=apostila).values('ip').distinct().count()
    views_totais = ViewApostila.objects.filter(apostila=apostila).count()
    
    avaliacoes = AvaliacaoApostila.AVALIACAO_CHOICES
    avaliacoes_filtrar = request.GET.get('avaliacao')
    
    #if avaliacoes_filtrar:
    #        flashcards = flashcards.filter(dificuldade=avaliacoes_filtrar)
    
    
    
    return render(request, 'apostila.html', {'apostila': apostila, 'views_unicas': views_unicas, 'views_totais': views_totais, 'avaliacoes':avaliacoes})



#def avaliacao(request, id):
#    if request.method == 'POST':
#        avaliacao = request.POST.get('avaliacao')
#        apostila = Apostila.objects.get(id=id)
#        
#        avaliacao = AvaliacaoApostila(
#            apostila = apostila,
#            avaliacao = avaliacao            
#        )
#        avaliacao.save()
    