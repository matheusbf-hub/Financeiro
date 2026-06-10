from .models import  Perfil, Conta_bancaria, Categoria, Cartao

def menor_id_livre(modelo, campo='ID', **filtros):
    ids_usados = set(modelo.objects.filter(**filtros).values_list(campo, flat=True))
    proximo_id = 1
    while proximo_id in ids_usados:
        proximo_id += 1
    return proximo_id

def dados_globais(request):
    if not request.user.is_authenticated:
        return {}

    perfil, created = Perfil.objects.get_or_create(usuario=request.user)

    conta_bancaria = Conta_bancaria.objects.filter(perfil=perfil).order_by('ID')
    categorias = Categoria.objects.filter(perfil=perfil).order_by('ID')
    cartao = Cartao.objects.filter(perfil=perfil).order_by('ID')


    return {
        'perfil': perfil,
        'contas': conta_bancaria,
        'categorias': categorias,
        'cartoes': cartao,

        'proximo_codigo_banco': menor_id_livre(Conta_bancaria, 'ID', perfil=perfil),
        'proximo_codigo_categoria': menor_id_livre(Categoria, 'ID', perfil=perfil),
        'proximo_codigo_cartao': menor_id_livre(Cartao, 'ID', perfil=perfil),
    }