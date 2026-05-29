import psycopg2

conn = psycopg2.connect(
    dbname="financeiro",
    user="braga",
    password="BRCloser",
    host="localhost",
    port="5432"
)

print("Conectado com sucesso!")