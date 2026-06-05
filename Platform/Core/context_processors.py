from .models import Conta_bancaria, Perfil

def dados_globais(request):
    if not request.user.is_authenticated:
        return {}

    perfil, created = Perfil.objects.get_or_create(usuario=request.user)

    contas = Conta_bancaria.objects.filter(perfil=perfil).order_by('ID')

    ids_usados = set(contas.values_list('ID', flat=True))

    proximo_codigo = 1
    while proximo_codigo in ids_usados:
        proximo_codigo += 1

    return {
        'perfil': perfil,
        'contas': contas,
        'proximo_codigo': proximo_codigo,
    }