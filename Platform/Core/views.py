from multiprocessing import context
from django.db.models import Max
from django.db import transaction, IntegrityError

from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import *

@login_required
def delete_profile_view(request):
    user = request.user
    perfil = Perfil.objects.get(usuario=request.user)
    perfil.delete()
    user.delete()
    if request.user.is_authenticated:
        auth_logout(request)
        messages.success(request, 'Conta excluída com sucesso.')
    else:
        messages.error(request, 'Não foi possível excluir a conta.')

    return redirect('login')

def login(request):
    if request.user.is_authenticated:
        return redirect('homepage')
    
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'Credenciais inválidas. Tente novamente.')
    return render(request, 'user_login.html')

@login_required
def homepage(request):
    try:
        perfil = Perfil.objects.get(usuario=request.user)
        messages.success(request, f'Bem-vindo, {perfil.usuario.username}!')
        return render(request, 'homepage.html', {'perfil': perfil})
     

    except Perfil.DoesNotExist:
        messages.error(request, 'Perfil não encontrado. Por favor, complete seu perfil.')
        return redirect('edit_profile')

@login_required
def edit_profile(request):

    try:
        perfil = Perfil.objects.get(usuario=request.user)

    except Perfil.DoesNotExist:
        perfil = Perfil(usuario=request.user)

    if request.method == 'POST':

        foto = request.FILES.get('foto')

        if foto:
            perfil.foto = foto

        perfil.documento = request.POST.get('documento', '')
        perfil.tipo = request.POST.get('tipo', '')

        perfil.save()

        messages.success(request, 'Perfil atualizado com sucesso.')
        return redirect('edit_profile')

    return render(request, 'user_edit_profile.html', {
        'perfil': perfil
    })

@login_required
def minhaconta(request):
    authenticated_user = request.user
    Perfil.objects.get_or_create(usuario=authenticated_user)
    return render(request, 'user_minhaconta.html',{ 'perfil': Perfil.objects.get(usuario=authenticated_user) } )

@login_required
def salvar_conta(request):
    if request.method == 'POST':
        user = request.user
        nome = request.POST.get('nome', '')
        sobrenome = request.POST.get('sobrenome', '')
        email = request.POST.get('email', '')
        username = request.POST.get('username', '')

        user.first_name = nome
        user.last_name = sobrenome
        user.email = email
        user.username = username
        user.save()

        return redirect('minhaconta')
    
    return redirect('minhaconta')

@login_required
def reset_password(request):
    authenticated_user = request.user
    Perfil.objects.get_or_create(usuario=authenticated_user)

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(current_password):
            messages.error(request, 'Senha atual incorreta.')
            return redirect('resetpassword')

        if new_password != confirm_password:
            messages.error(request, 'As novas senhas não coincidem.')
            return redirect('resetpassword')

        request.user.set_password(new_password)
        request.user.save()
        messages.success(request, 'Senha alterada com sucesso. Faça login novamente.')
        auth_logout(request)
        return redirect('login')

    return render(request, 'user_resetar_senha.html', { 'perfil': Perfil.objects.get(usuario=authenticated_user) } )


@login_required
def logout(request):
    auth_logout(request)
    return redirect('login')

def cadastro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        nome_completo = request.POST.get('nome_completo')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Nome de usuário já existe. Escolha outro.')
            return redirect('register')
        
        user = User.objects.create_user(username=username, password=password)
        Perfil.objects.create(usuario=user, nome_completo=nome_completo)
        messages.success(request, 'Cadastro realizado com sucesso. Faça login para acessar sua conta.')
        return redirect('login')
    
    return render(request, 'user_cadastro.html')


def menor_id_livre(perfil):
    ids_usados = set(
        Conta_bancaria.objects
        .filter(perfil=perfil)
        .values_list('ID', flat=True)
    )

    proximo_id = 1

    while proximo_id in ids_usados:
        proximo_id += 1

    return proximo_id

@login_required
def conta_bancaria(request):
    authenticated_user = request.user
    perfil, created = Perfil.objects.get_or_create(usuario=request.user)

    contas = Conta_bancaria.objects.filter(perfil=perfil).order_by('ID')

    conta_editando = None

    proximo_codigo = (
        conta_editando.ID if conta_editando else menor_id_livre(perfil)
    )

    if request.method == 'POST':
        acao = request.POST.get('acao')
        editar_id = request.POST.get('editar_id')
        delete_id = request.POST.get('delete_id')

        if acao == 'excluir':
            delete_id = request.POST.get('delete_id')
            Conta_bancaria.objects.filter(
                ID=delete_id, 
                perfil=perfil
            ).delete()
            messages.success(request, 'Conta bancária excluída com sucesso.')

            return redirect('homepage')

        if editar_id:
            conta_obj = Conta_bancaria.objects.get(
                ID=editar_id,
                perfil=perfil
            )

            conta_obj.nome = request.POST.get('nome')
            conta_obj.banco = request.POST.get('banco')
            conta_obj.agencia = request.POST.get('agencia')
            conta_obj.conta = request.POST.get('conta')
            conta_obj.save()

            messages.success(request,'Conta bancária editada com sucesso.')

        else:
            with transaction.atomic():
                proximo_id = menor_id_livre(perfil)

                Conta_bancaria.objects.create(
                    ID=proximo_id,
                    perfil=perfil,
                    nome=request.POST.get('nome'),
                    banco=request.POST.get('banco'),
                    agencia=request.POST.get('agencia'),
                    conta=request.POST.get('conta')
                )

            messages.success(request, 'Conta bancária cadastrada com sucesso.')

        return redirect('homepage')
    
    return render(request, 'homepage', {
        'perfil': perfil,
    })

@login_required
def contas(request):
    authenticated_user = request.user
    Perfil.objects.get_or_create(usuario=authenticated_user)
    return render(request, 'contas_base.html',{ 'perfil': Perfil.objects.get(usuario=authenticated_user) } )

@login_required
def novotitulo(request):
    perfil = Perfil.objects.get(usuario=request.user)
    return render(request, 'contas_novotitulo.html', { 'perfil': perfil })

@login_required
def caixa(request):
    authenticated_user = request.user
    Perfil.objects.get_or_create(usuario=authenticated_user)

    return render(request, 'caixa_base.html', { 'perfil': Perfil.objects.get(usuario=authenticated_user) } )

@login_required
def mov(request):
    authenticated_user = request.user
    Perfil.objects.get_or_create(usuario=authenticated_user)
    return render(request, 'mov_base.html', { 'perfil': Perfil.objects.get(usuario=authenticated_user) } )

@login_required
def investimento(request):
    authenticated_user = request.user
    Perfil.objects.get_or_create(usuario=authenticated_user)
    return render(request, 'inv_base.html', { 'perfil': Perfil.objects.get(usuario=authenticated_user) } )

@login_required
def mov_investimento(request):
    authenticated_user = request.user
    Perfil.objects.get_or_create(usuario=authenticated_user)
    return render(request, 'mov_investimento.html', { 'perfil': Perfil.objects.get(usuario=authenticated_user) } )

@login_required
def lista_movimentos(request):
    authenticated_user = request.user
    Perfil.objects.get_or_create(usuario=authenticated_user)
    movimentos = mov_investimento.objects.select_related(
        'investimento'
    )

    return render(
        request,
        'inv_base.html',
        {'movimentos': movimentos}
    )

@login_required
def novo_investimento(request):
    return render(request, 'inv_novo_investimento.html', { 'perfil': Perfil.objects.get(usuario=request.user) } )

@login_required
def dashboard(request):
    authenticated_user = request.user
    Perfil.objects.get_or_create(usuario=authenticated_user)
    return render(request, 'ret_dashboard.html', { 'perfil': Perfil.objects.get(usuario=authenticated_user) } )

    
