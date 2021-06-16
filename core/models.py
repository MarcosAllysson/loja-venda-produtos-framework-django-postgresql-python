from django.db import models
from stdimage.models import StdImageField  # importando módulo stdimage instalado na criação do projeto
from django.db.models import signals  # antes de inserir no banco ou depois, faça algo com eles
from django.template.defaultfilters import slugify  # criar slug (criar url válida a partir do que eu escolher)


# Create your models here.
class Base(models.Model):
    """
    Classe de atributos base, ou seja, que aparece em outras aplicação
    """
    criado = models.DateField('Data da Criação', auto_now_add=True)
    modificado = models.DateField('Data de Atualizcação', auto_now_add=True)
    ativo = models.BooleanField('Ativo?', default=True)

    class Meta:
        """
        Abstrata porque não é criada no banco de dados. Serve apenas de rascunho pra outras classes.
        """
        abstract = True


class Produto(Base):
    """
    Classe que extende (herda) Base, com seus atributos específicos.
    """
    nome = models.CharField('Nome', max_length=100)
    preco = models.DecimalField('Preço', max_digits=8, decimal_places=2)
    estoque = models.IntegerField('Estoque')

    # tipo StdImage, salvo no diretório 'produtos'. Variação de nome, thumnail com tamanho 124x124
    imagem = StdImageField('Imagem', upload_to='produtos', variations={'thumbnail': (124, 124)})
    slug = models.SlugField('Slug', max_length=100, blank=True, editable=False)

    def __str__(self):
        """
        Printar nome do produto na tela administrativa.
        """
        return self.nome


def produto_pre_save(signal, instance, sender, **kwargs):
    """
    Função que coloca o slug ao final do nome. slug é referente ao atributo nome da classe Produto.
    Similar quando um novo post é criado no wordpress. O título vira o slug
    instance.nome_do_atributo_da_classe
    """
    instance.slug = slugify(instance.nome)


# antes de salvar no banco, executa essa função quando class Produto for instanciada. Esse é o 'sinal'
signals.pre_save.connect(produto_pre_save, sender=Produto)
