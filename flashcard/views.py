#from django.http import HttpResponse
import json
from django.http import Http404
from django.shortcuts import redirect, render
from .models import Categoria, Flashcard, Desafio, FlashcardDesafio
from django.contrib import messages
from django.contrib.messages import constants

# Create your views here.
#TODO: Não permnitir criar desafios com uma quantidade menor de perguntas por categoria e apresentar uma msg

def novo_flashcard(request):
    if not request.user.is_authenticated:
        return redirect('/usuarios/login')
    
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        dificuldades = Flashcard.DIFICULDADE_CHOICES
        flashcards = Flashcard.objects.filter(user = request.user)

        categoria_filtrar = request.GET.get('categoria')
        dificuldade_filtrar = request.GET.get('dificuldade')
        
        if categoria_filtrar:
            flashcards = flashcards.filter(categoria__id=categoria_filtrar)
            
        if dificuldade_filtrar:
            flashcards = flashcards.filter(dificuldade=dificuldade_filtrar)
        
        return render (request, 'novo_flashcard.html',{'categorias':categorias, 'dificuldades': dificuldades, 'flashcards': flashcards })
    elif request.method == 'POST':
        pergunta = request.POST.get('pergunta')
        resposta = request.POST.get('resposta')
        categoria = request.POST.get('categoria')
        dificuldade = request.POST.get('dificuldade')

        if len(pergunta.strip()) == 0 or len(resposta.strip()) == 0:
            messages.add_message(
                request,
                constants.ERROR,
                'Preencha os campos de pergunta e resposta',
            )
            return redirect('/flashcard/novo_flashcard')

        flashcard = Flashcard(
            user=request.user,
            pergunta=pergunta,
            resposta=resposta,
            categoria_id=categoria,
            dificuldade=dificuldade,
        )

        flashcard.save()

        messages.add_message(
            request, constants.SUCCESS, 'Flashcard criado com sucesso'
        )
        return redirect('/flashcard/novo_flashcard')
    
    
    
def deletar_flashcard(request, id):
    if not request.user.is_authenticated:
      messages.add_message(
           request, constants.ERROR, 'Voce Não tem permissão para remover este card (login)'
       )
    return redirect('/usuarios/login')
    
    flashcard = Flashcard.objects.get(id=id)
    
    ##Validacao para evitar que um usuario delete cards de outro
    if not flashcard.user == request.user:
        messages.add_message(
            request, constants.ERROR, 'Voce não tem permissão de remover este Card!'
        )
        return redirect('/flashcard/novo_flashcard')
    
    flashcard.delete()
    messages.add_message(
        request, constants.SUCCESS, 'Flashcard deletado com sucesso!'
    )
    return redirect('/flashcard/novo_flashcard')
   
   
def iniciar_desafio(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        dificuldades = Flashcard.DIFICULDADE_CHOICES
        return render(
            request,
            'iniciar_desafio.html',
            {'categorias': categorias, 'dificuldades': dificuldades},
        )
    elif request.method == 'POST':
        titulo = request.POST.get('titulo')
        categorias = request.POST.getlist('categoria')
        dificuldade = request.POST.get('dificuldade')
        qtd_perguntas = request.POST.get('qtd_perguntas')

        desafio = Desafio(
            user=request.user,
            titulo=titulo,
            quantidade_perguntas=qtd_perguntas,
            dificuldade=dificuldade,
        )
        desafio.save()

        ##Este FOR pode substituir a linha abaixo sem perder performace
        #for categoria in categorias
        #   desafio.categoria.add(categoria)
        
        desafio.categoria.add(*categorias)

        flashcards = (
            Flashcard.objects.filter(user=request.user)
            .filter(dificuldade=dificuldade)
            .filter(categoria_id__in=categorias)
            .order_by('?')
        )

        if flashcards.count() < int(qtd_perguntas):
            return redirect('/flashcard/iniciar_desafio/')

        flashcards = flashcards[: int(qtd_perguntas)]

        for f in flashcards:
            flashcard_desafio = FlashcardDesafio(
                flashcard=f,
            )
            flashcard_desafio.save()
            desafio.flashcards.add(flashcard_desafio)

        desafio.save()

        return redirect(f'/flashcard/desafio/{desafio.id}')
    

def listar_desafio(request):
    desafios = Desafio.objects.filter(user=request.user)
    #print(request.user)
    return render(
        request,
        'listar_desafio.html',
        {
            'desafios': desafios,
        },
    )    
    
    
def desafio(request, id):
    desafio = Desafio.objects.get(id=id)
    
    if not desafio.user == request.user:
        raise Http404()
    
    if request.method == 'GET':
        acertos = desafio.flashcards.filter(respondido=True).filter(acertou=True).count()
        erros = desafio.flashcards.filter(respondido=True).filter(acertou=False).count()
        faltantes = desafio.flashcards.filter(respondido=False).count()
    return render(request, 'desafio.html', {'desafio': desafio, 'acertos': acertos, 'erros': erros, 'faltantes': faltantes})
    
    
def responder_flashcard(request, id):
    
    flashcard_desafio = FlashcardDesafio.objects.get(id=id)
    acertou = request.GET.get('acertou')
    desafio_id = request.GET.get('desafio_id')

    if not flashcard_desafio.flashcard.user == request.user:
        raise Http404()
    
    flashcard_desafio.respondido = True
    flashcard_desafio.acertou = True if acertou == '1' else False
    flashcard_desafio.save()
    return redirect(f'/flashcard/desafio/{desafio_id}')


def relatorio(request, id):
    desafio = Desafio.objects.get(id=id)
    
    acertos = desafio.flashcards.filter(acertou=True).count()
    erros = desafio.flashcards.filter(acertou=False).count()

    dados = [acertos, erros]
    
    categorias = desafio.categoria.all()
    name_categoria = [i.nome for i in categorias]

    dados2 = []
    for categoria in categorias:
        dados2.append(desafio.flashcards.filter(flashcard__categoria=categoria).filter(acertou=True).count())
        
   # print (name_categoria)
    
    return render(request, 'relatorio.html', {'desafio': desafio, 'dados': dados, 'categorias': name_categoria, 'dados2': dados2,} )
    
    
        
        
            
    