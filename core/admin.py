from django.contrib import admin
from .models import Produto


# Register your models here.
@admin.register(Produto)  # Usando decorator pra registrar.
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'estoque', 'slug', 'criado', 'modificado', 'ativo')


# outra forma de registrar:
# admin.site.register(Produto, ProdutoAdmin)
