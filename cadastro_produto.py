import tkinter as tk
from tkinter import messagebox
import banco_db


def tela_cadastro_produto():
    janela = tk.Toplevel()
    janela.title("Cadastrar Produto")

    # Campos para o cadastro de produto
    nome_produto = tk.Entry(janela)
    qtd_produto = tk.Entry(janela)
    minimo_produto = tk.Entry(janela)

    tk.Label(janela, text="Nome do Produto:").grid(row=0, column=0)
    tk.Label(janela, text="Quantidade:").grid(row=1, column=0)
    tk.Label(janela, text="Quantidade Mínima:").grid(row=2, column=0)

    nome_produto.grid(row=0, column=1)
    qtd_produto.grid(row=1, column=1)
    minimo_produto.grid(row=2, column=1)

    def salvar_produto():
        # Lógica para salvar o produto no banco de dados
        nome = nome_produto.get()
        qtd = int(qtd_produto.get())
        minimo = int(minimo_produto.get())

        conn = banco_db.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO produtos (nome, quantidade, minimo)
            VALUES (?, ?, ?)
        """, (nome, qtd, minimo))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso")
        janela.destroy()

    tk.Button(janela, text="Salvar", command=salvar_produto).grid(
        row=3, columnspan=2)

    janela.mainloop()
