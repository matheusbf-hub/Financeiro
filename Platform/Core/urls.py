from django.urls import path
from .views import *
from django.http import HttpResponse
from django.shortcuts import render


urlpatterns = [
    path('', login, name='login'),
    path('homepage', homepage, name='homepage'),
    path('cadastro/', cadastro, name='cadastro'),
    path('banco', conta_bancaria, name='banco'),
    path('minhaconta/', minhaconta, name='minhaconta'),
    path('salvar_conta/', salvar_conta, name='salvar_conta'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('delete_profile/', delete_profile_view, name='delete_profile'),
    path('resetpassword/', reset_password, name='resetpassword'),
    path('logout/', logout, name='logout'),
    path('contas/', contas, name='contas'),
    path('novotitulo/', novotitulo, name='novotitulo'),
    path('mov/', mov, name='mov'),
    path('caixa/', caixa, name='caixa'),
    path('investimento/', investimento, name='investimento'),
    path('mov.investimento/', mov_investimento, name='mov_investimento'),
    path('novo_investimento/', novo_investimento, name='novo_investimento'),
    path('dashboard/', dashboard, name='dashboard')
]

