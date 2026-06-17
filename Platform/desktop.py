import os
import sys
import json
import threading
import time
import tkinter as tk
from tkinter import messagebox
import webview


CONFIG_FILE = "config.json"


def app_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def config_path():
    return os.path.join(app_dir(), CONFIG_FILE)


def salvar_config():
    config = {
        "DB_ENGINE": engine_var.get(),
        "DB_NAME": db_name.get(),
        "DB_USER": db_user.get(),
        "DB_PASSWORD": db_password.get(),
        "DB_HOST": db_host.get(),
        "DB_PORT": db_port.get(),
    }

    with open(config_path(), "w", encoding="utf-8") as file:
        json.dump(config, file, indent=4)

    messagebox.showinfo("Sucesso", "Configuração salva com sucesso!")
    janela.destroy()


def abrir_tela_config():
    global janela
    global engine_var, db_name, db_user, db_password, db_host, db_port

    janela = tk.Tk()
    janela.title("Configuração do Banco de Dados")
    janela.geometry("420x360")
    janela.resizable(False, False)

    engine_var = tk.StringVar(value="postgresql")

    tk.Label(janela, text="Tipo do banco").pack()
    tk.OptionMenu(janela, engine_var, "postgresql", "mysql", "sqlite").pack()

    tk.Label(janela, text="Nome do banco").pack()
    db_name = tk.Entry(janela, width=40)
    db_name.pack()

    tk.Label(janela, text="Usuário").pack()
    db_user = tk.Entry(janela, width=40)
    db_user.pack()

    tk.Label(janela, text="Senha").pack()
    db_password = tk.Entry(janela, width=40, show="*")
    db_password.pack()

    tk.Label(janela, text="Host / IP").pack()
    db_host = tk.Entry(janela, width=40)
    db_host.insert(0, "127.0.0.1")
    db_host.pack()

    tk.Label(janela, text="Porta").pack()
    db_port = tk.Entry(janela, width=40)
    db_port.insert(0, "5432")
    db_port.pack()

    tk.Button(
        janela,
        text="Salvar Configuração",
        command=salvar_config,
        width=25
    ).pack(pady=20)

    janela.mainloop()


def carregar_config():
    with open(config_path(), "r", encoding="utf-8") as file:
        return json.load(file)


def start_server():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Platform.settings")

    import django
    django.setup()

    from django.core.management import call_command

    call_command(
        "runserver",
        "127.0.0.1:8000",
        "--noreload",
        use_reloader=False
    )


if __name__ == "__main__":
    if not os.path.exists(config_path()):
        abrir_tela_config()

    config = carregar_config()

    for key, value in config.items():
        os.environ[key] = value

    servidor = threading.Thread(target=start_server)
    servidor.daemon = True
    servidor.start()

    time.sleep(3)

    webview.create_window(
        "Minhas Finanças",
        "http://127.0.0.1:8000",
        width=1400,
        height=900
    )

    webview.start()