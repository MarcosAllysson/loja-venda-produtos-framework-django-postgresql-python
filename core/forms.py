from django import forms
from django.core.mail.message import EmailMessage
from .models import Produto


class ContatoForm(forms.Form):
    # Geralmente os formulários pedem nome, email, assunto e mensagem:
    nome = forms.CharField(label='Nome')
    email = forms.EmailField(label='E-mail')
    assunto = forms.CharField(label='Assunto')
    mensagem = forms.CharField(label='Mensagem', widget=forms.Textarea())

    def send_mail(self):
        """
        Método que coleta os dados, instancia EmailMessage passando assunto, conteudo, email e headers.
        Por fim, faz o envio do email.
        """
        nome = self.cleaned_data['nome']
        email = self.cleaned_data['email']
        assunto = self.cleaned_data['assunto']
        mensagem = self.cleaned_data['mensagem']

        # mensagem a ser enviada no email
        conteudo = f'Nome: {nome}\nEmail: {email}\nAssunto: {assunto}\nMensagem: {mensagem}'

        # instanciando objeto
        mail = EmailMessage(
            subject='Email enviado pelo sistema django2',
            body=conteudo,
            from_email='contato@seudominio.com.br',  # email do meu site ou empresa
            to=['contato@seudominio.com.br',],  # é uma lista porque posso enviar para vários emails se quiser
            headers={'Reply-To': email}
        )

        # enviando email conforme definido no settings.py do projeto
        mail.send()


# classe formulário do produto
class ProdutoModelForm(forms.ModelForm):
    """
    Notar o Model Form, que é diferente de Form.
    Pois essa classe é um formulário cujo dados vão ser salvos no banco.
    """
    class Meta:
        """
        Meta de metadados, model = Classe Model importada
        E os dados foram especificado: nome, preco, estoque e imagem. Os mesmos declarados no models e que vão ser
        informados pelos usuários.
        """
        # model da Classe Formulário
        model = Produto

        # Campos a serem informados pelo usuário
        fields = ['nome', 'preco', 'estoque', 'imagem']
