from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect

from .forms import ContatoForm, ProdutoModelForm
from .models import Produto

def index(request):
    context = {
        'produtos': Produto.objects.all()
    }
    return render(request, 'index.html', context)


def contact(request):
    form = ContatoForm(request.POST or None)
    print(f'POST: {request.POST}')

    if str(request.method) == 'POST':
        if form.is_valid():
            form.send_mail()
            messages.success(request, 'E-mail enviado com sucesso!')
            form = ContatoForm()
        else:
            messages.error(request, 'Erro ao enviar o e-mail!')

    context = {
        'form': form
    }
    return render(request, 'contact.html', context)


def product(request):
    if str(request.user) != "AnonymousUser":
        print(f"Usuário: {request.user}")
        if str(request.method) == 'POST':
            form = ProdutoModelForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()

                messages.success(request, 'Produto salvo com sucesso...')
                form = ProdutoModelForm()
            else:
                messages.error(request, 'Erro ao salvar o produto!')
        else:
            form = ProdutoModelForm()
        context = {
            'form': form
        }
        return render(request, 'product.html', context)
    else:
        return redirect('index.html')