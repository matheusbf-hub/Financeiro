from django.db import models
from django.utils import timezone


class Perfil(models.Model):
    tipo_usuario = (1, 'admin'), (2, 'user')

    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    documento = models.CharField(max_length=20, blank=True, null=True)
    foto = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    tipo = models.IntegerField(choices=tipo_usuario, default=2, blank=False, null=False)


    def __str__(self):
        return self.usuario.username

class Categoria(models.Model):
    ID = models.BigAutoField(primary_key=True, unique=True)
    nome = models.CharField(max_length=100, unique=True, blank=True, null=True)
    
    def __str__(self):
        return self.nome
    
class Cartao(models.Model):
    bandeira = (1, 'Visa'), (2, 'Mastercard'), (3, 'Elo'), (4, 'American Express')

    ID = models.BigAutoField(primary_key=True, unique=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    banco = models.CharField(max_length=100, blank=True, null=True)
    bandeira = models.IntegerField(choices=bandeira, default=1, blank=False, null=False)
    limite_consumo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    limite_maximo= models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    limite_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.nome} - {self.get_bandeira_display()} - {self.banco} - {self.limite_total}'
    
class Conta_bancaria(models.Model):
    ID = models.BigAutoField(primary_key=True, unique=True)
    perfil = models.ForeignKey('Perfil', on_delete=models.CASCADE)
    nome = models.CharField(max_length=100, blank=True, null=True)
    banco = models.CharField(max_length=100, blank=True, null=True)
    agencia = models.CharField(max_length=20, blank=True, null=True)
    conta = models.CharField(max_length=20, blank=True, null=True)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.nome} - {self.banco} - Agência: {self.agencia} - Conta: {self.conta} - Saldo: {self.saldo}'

class Investimento(models.Model):
    tipo_investimento = (1, 'Ações'), (2, 'Fundos Imobiliários'), (3, 'Tesouro Direto'), (4, 'Criptomoedas')

    ID = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, blank=True, null=True)
    banco = models.CharField(max_length=100, blank=True, null=True)
    tipo_investimento = models.IntegerField(choices=tipo_investimento, default=1)    
    percentual_anual = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)


    def __str__(self):
        return f'{self.nome} - {self.get_tipo_investimento_display()} - Percentual Anual: {self.percentual_anual}%'
    

class mov_investimento(models.Model):
    tipo = (1, 'Credito'), (2, 'Debito')

    ID = models.AutoField(primary_key=True)
    id_investimento = models.ForeignKey('Investimento', on_delete=models.CASCADE, related_name='movimentos_investimento')
    tipo_movimento = models.IntegerField(choices=tipo, default=1)
    data_movimento = models.DateField(default=timezone.now, blank=False, null=False)
    valor_movimento = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Movimento de {self.valor_movimento} para {self.id_investimento.nome} em {self.data_movimento}'
    
class meta(models.Model):
    verbose_name = 'Investimento'
    verbose_name_plural = 'Investimentos'
    ordering = ['-data_investimento']

def __str__(self):
    return f'Meta: {self.nome} - Valor: {self.valor} - Data: {self.data_investimento}'

class Titulos(models.Model):
    Tipo_movimento = (1, 'Receita'), (2, 'Despesa')

    codigo = models.BigAutoField(primary_key=True, blank=False, null=False, unique=True)
    descricao = models.TextField(blank=True)
    tipo_movimento = models.IntegerField(choices=Tipo_movimento, default=1, blank=False, null=False)
    Categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, blank=True, null=True)
    cartao = models.ForeignKey('Cartao', on_delete=models.CASCADE, blank=True, null=True, related_name='titulos_cartao')
    conta_bancaria = models.ForeignKey('Conta_bancaria', on_delete=models.CASCADE, blank=True, null=True)
    data_vencimento = models.DateField(default=timezone.now, blank=False, null=False)
    Valor = models.DecimalField(max_digits=10, decimal_places=2)
    multa = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    juros = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.nome
    
class Movimento(models.Model):
    Tipo = (1, 'Entrada'), (2, 'Saída')

    id = models.BigAutoField(primary_key=True)
    id_titulo = models.ForeignKey('Titulos', on_delete=models.CASCADE, blank=True, null=True)
    caixa = models.ForeignKey('Caixa', on_delete=models.CASCADE)
    tipo = models.IntegerField(choices=Tipo, default=1)
    data_pagamento = models.DateField(default=timezone.now, blank=False, null=False)
    desaconto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    multa_pago = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    juros_pago = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Pagamento de {self.valor_pago} para {self.id_titulo.descricao}'
    
class Caixa(models.Model):
    perfil = models.ForeignKey('Perfil', on_delete=models.CASCADE)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.nome} para {self.perfil.nome}'
    