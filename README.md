# Sistema de Controle Financeiro

Este repositório contém um sistema web em Django para controle financeiro pessoal e corporativo. O projeto oferece cadastro de usuários, edição de perfil, gerenciamento de contas bancárias, cartões, títulos, movimentações, investimentos e dashboard de acompanhamento.

## Tecnologias

- Python
- Django
- HTML
- PostgreSQL 

## Recursos Principais

- Autenticação de usuário: login, cadastro, logout
- Perfil do usuário: edição, foto de perfil e exclusão de conta
- Gestão de contas bancárias e cartões
- Controle de títulos de receita e despesa
- Registro de movimentações financeiras e caixa
- Cadastro e visualização de investimentos
- Dashboard simples para acompanhamento

## Estrutura do Projeto

- `Platform/Platform/` - configuração principal do Django
- `Platform/Core/` - app Django com modelos, views, templates e URLs
- `Platform/build/` - artefatos de build gerados por empacotamento
- `Platform/desktop.py` - ponto de entrada para versão desktop/empacotada

## Requisitos

- Python 3.x
- Django 6.x
- PostgreSQL
- Biblioteca Pillow para upload de imagens, caso necessário

## Configuração

1. Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instale as dependências:

```powershell
pip install django pillow
```

3. Ajuste a configuração do banco de dados em `Platform/Platform/settings.py` se necessário.

A configuração padrão usa PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'financeiro',
        'USER': 'braga',
        'PASSWORD': 'BRCloser',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'client_encoding': 'UTF8',
        }
    }
}
```

Se preferir usar SQLite para desenvolvimento rápido, descomente a configuração SQLite no mesmo arquivo.

## Inicialização

1. Navegue até a pasta do projeto:

```powershell
cd Platform
```

2. Execute migrações:

```powershell
python manage.py migrate
```

3. Crie um superusuário (opcional):

```powershell
python manage.py createsuperuser
```

4. Inicie o servidor de desenvolvimento:

```powershell
python manage.py runserver
```

5. Acesse o sistema em:

```
http://127.0.0.1:8000/
```

## URLs principais

- `/` - Login
- `/cadastro/` - Cadastro de usuário
- `/homepage` - Página inicial
- `/minhaconta/` - Minha conta
- `/edit_profile/` - Editar perfil
- `/resetpassword/` - Redefinir senha
- `/contas/` - Contas
- `/caixa/` - Caixa
- `/investimento/` - Investimentos
- `/dashboard/` - Dashboard

## Observações

- O diretório `Core/Templates/` contém as páginas do projeto.
- `Core/static/` armazena estilos, scripts e imagens.
- A pasta `Platform/build/` contém artefatos gerados por empacotamento; não é necessária para desenvolvimento.

