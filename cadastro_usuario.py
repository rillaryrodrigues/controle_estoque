import tkinter as tk
from tkinter import messagebox
import banco_db
import hashlib

def tela_cadastro_usuario():
    def salvar():
        nome = entry_nome.get()
        usuario = entry_usuario.get()
        senha = entry_senha.get()
        perfil = var_perfil.get()
        if not nome or not usuario or not senha:
            messagebox.showwarning("Erro", "Todos os campos são obrigatórios.")
            return
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        conn = banco_db.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (nome, usuario, senha, perfil) VALUES (?, ?, ?, ?)",
                           (nome, usuario, senha_hash, perfil))
            conn.commit()
            messagebox.showinfo("OK", "Usuário cadastrado.")
            janela.destroy()
        except:
            messagebox.showerror("Erro", "Usuário já existe.")
        conn.close()

    janela = tk.Toplevel()
    janela.title("Cadastro de Usuário")

    tk.Label(janela, text="Nome").pack()
    entry_nome = tk.Entry(janela)
    entry_nome.pack()

    tk.Label(janela, text="Usuário").pack()
    entry_usuario = tk.Entry(janela)
    entry_usuario.pack()

    tk.Label(janela, text="Senha").pack()
    entry_senha = tk.Entry(janela, show="*")
    entry_senha.pack()

    var_perfil = tk.StringVar(value="Comum")
    tk.Label(janela, text="Perfil").pack()
    tk.OptionMenu(janela, var_perfil, "Administrador", "Comum").pack()

    tk.Button(janela, text="Salvar", command=salvar).pack()
