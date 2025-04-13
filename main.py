import tkinter as tk
from tkinter import messagebox
import hashlib
import sqlite3
import banco_db  # Certifique-se de que você tem um módulo banco_db.py com a função conectar
import cadastro_produto
import cadastro_usuario
import estoque

# Função para criar o usuário administrador


def criar_usuario_admin():
    nome = "Administrador"
    usuario = "admin"
    senha = "admin123"
    perfil = "Administrador"

    senha_cripto = hashlib.sha256(senha.encode()).hexdigest()

    conn = banco_db.conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO usuarios (nome, usuario, senha, perfil)
            VALUES (?, ?, ?, ?)
        """, (nome, usuario, senha_cripto, perfil))

        conn.commit()
        print("Usuário administrador criado com sucesso!")
    except sqlite3.IntegrityError:
        print("Erro: O usuário já existe.")
    finally:
        conn.close()

# Função de login


def abrir_login():
    def verificar_login():
        usuario_input = usuario_entry.get()
        senha_input = senha_entry.get()
        # Criptografa a senha fornecida
        senha_cripto = hashlib.sha256(senha_input.encode()).hexdigest()

        conn = banco_db.conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuarios WHERE usuario=? AND senha=?",
                       (usuario_input, senha_cripto))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Login bem-sucedido",
                                f"Bem-vindo, {user[1]} ({user[4]})")
            app.destroy()  # Fecha a tela de login
            # Abre o menu principal com o usuário autenticado
            menu_principal(user)
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")

        conn.close()

    app = tk.Tk()
    app.title("Login")
    app.geometry("300x200")

    tk.Label(app, text="Usuário:").pack(pady=10)
    usuario_entry = tk.Entry(app)
    usuario_entry.pack(pady=5)

    tk.Label(app, text="Senha:").pack(pady=10)
    senha_entry = tk.Entry(app, show="*")
    senha_entry.pack(pady=5)

    tk.Button(app, text="Login", command=verificar_login).pack(pady=20)

    app.mainloop()

# Função para exibir o menu principal do sistema


def menu_principal(user):
    root = tk.Tk()
    root.title("Sistema de Estoque")

    # Exibir saudação
    tk.Label(
        root, text=f"Bem-vindo, {user[1]} ({user[4]})", font=("Arial", 12)).pack(pady=10)

    # Botões do menu principal
    tk.Button(root, text="Cadastrar Produto",
              command=cadastro_produto.tela_cadastro_produto).pack()
    tk.Button(root, text="Estoque", command=estoque.tela_estoque).pack()

    # Mostrar a opção de cadastrar usuário apenas para o admin
    if user[4] == "Administrador":
        tk.Button(root, text="Cadastrar Usuário",
                  command=cadastro_usuario.tela_cadastro_usuario).pack()

    # Iniciar a interface gráfica
    root.mainloop()


# Chama a função para criar o usuário admin (isso é feito ao iniciar o programa)
criar_usuario_admin()

# Chama a função de login
abrir_login()
