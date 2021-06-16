from django.shortcuts import render, redirect  # retornar página renderizada
from .forms import ContatoForm, ProdutoModelForm  # importando formulário
from django.contrib import messages  # módulo de mensagens do django para retornar na página para o usuário
from .models import Produto


# Create your views here.
def index(request):
    context = {
        'produtos': Produto.objects.all()  # todos os objetos do banco
    }
    return render(request, 'index.html', context)


def contato(request):
    """
    Função que lida com o formulário da página contato.html
    """
    # instanciando ContatoForm
    # formulário pode ou não ter dados. Vai ter quando clicar no botão, então método POST
    # não vai ter se somente a página for carregada
    formulario = ContatoForm(request.POST or None)

    # analisar se o método é post ou get:
    if str(request.method) == 'POST':
        # se foi enviado, verificar se é válido
        if formulario.is_valid():
            """
            # pego esses dados usando cleaned_data['nome_do_campo']
            nome = formulario.cleaned_data['nome']
            email = formulario.cleaned_data['email']
            assunto = formulario.cleaned_data['assunto']
            mensagem = formulario.cleaned_data['mensagem']

            print('MENSAGEM ENVIADA!')
            print(f'Nome: {nome}')
            print(f'Email: {email}')
            print(f'Assunto: {assunto}')
            print(f'Mensagem: {mensagem}')
            """

            # enviar email chamando o método da classe
            formulario.send_mail()

            # retornando mensagem de sucesso
            messages.success(request, 'E-mail enviado com sucesso.')

            # limpando / zerando dados preenchidos do formulário e instanciando novamente
            formulario = ContatoForm()

        # se o formulário não é válido
        else:
            messages.error(request, 'Erro ao enviar seu email. Tente novamente.')

    # retornando dados
    context = {
        'formulario': formulario
    }
    return render(request, 'contato.html', context)


def produto(request):
    # Validando se o usuário está ou não logado:
    if str(request.user) != 'AnonymousUser':

        # Se a requisição é do tipo Post.
        if str(request.method) == 'POST':
            # Recebe dados preenchidos no post e files, porque este formulário contém imagem
            formulario = ProdutoModelForm(request.POST, request.FILES)

            # verificando se o formulário é válido
            if formulario.is_valid():
                # printar os dados no terminal
                # prod = formulario.save(commit=False)
                # print(f'Nome: {prod.nome}\nPreço: {prod.preco}\nEstoque: {prod.estoque}\nImagem: {prod.imagem}')

                # salvar os dados no banco
                formulario.save()

                # mensagem de sucesso
                messages.success(request, 'Produto salvo com sucesso!')

                # limpando formulário e instanciado objeto
                formulario = ProdutoModelForm()

            # se formulário é inválido, retorno mensagem de erro
            else:
                messages.error(request, 'Erro ao salvar produto. Tente novamente!')

        # se não for um post, apenas instancio o objeto da classe ProdutoModelForm
        else:
            formulario = ProdutoModelForm()

        # objeto de retorno
        context = {
            'formulario': formulario
        }

        return render(request, 'produto.html', context)


    # usuário anônimo, redirecionado pra index:
    else:
        return redirect('index')
