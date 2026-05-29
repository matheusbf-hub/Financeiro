import threading
import subprocess
import webview
import time

def start_server():
    subprocess.run(["python manage.py runserver 127.0.0.1:8000", "server.py"])

t = threading.Thread(target=start_server)
t.daemon = True
t.start()

time.sleep(2)

webview.create_window(
    "Minhas Financas",
    "http://127.0.0.1:8000",
    width=1400,
    height=900
)

webview.start()