import tkinter as tk
import banco_db

def tela_estoque():
    janela = tk.Toplevel()
    janela.title("Estoque Atual")

    conn = banco_db.conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, quantidade, minimo FROM produtos")
    produtos = cursor.fetchall()
    conn.close()

    for nome, qtd, min_qtd in produtos:
        cor = "red" if qtd < min_qtd else "black"
        tk.Label(janela, text=f"{nome} - {qtd}", fg=cor).pack()
