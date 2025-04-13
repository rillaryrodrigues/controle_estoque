import tkinter as tk
import hashlib
import sqlite3
import banco_db  # Certifique-se de que você tenha um módulo banco.py com a função conectar
import cadastro_produto
import cadastro_usuario
import estoque

# Função para verificar o login do usuário


def verificar_login(usuario_input, senha_input):
    # Conectando ao banco de dados
    conn = banco_db.conectar()
    cursor = conn.cursor()

    # Verificando se o usuário existe no banco de dados
    cursor.execute("""
        SELECT * FROM usuarios WHERE usuario = ?
    """, (usuario_input,))
    user = cursor.fetchone()  # Pega o primeiro usuário encontrado

    if user:
        # Verificando se a senha criptografada corresponde à do banco
        senha_cripto = hashlib.sha256(senha_input.encode()).hexdigest()
        if senha_cripto == user[2]:  # user[2] é a senha criptografada no banco
            return user  # Retorna os dados do usuário se a senha estiver correta
        else:
            return None  # Retorna None se a senha for incorreta
    else:
        return None  # Retorna None se o usuário não existir no banco

# Função para exibir o menu principal do sistema


def menu_principal(user):
    root = tk.Tk()
    root.title("Sistema de Estoque")

    # Exibir saudação
    tk.Label(root, text=f"Bem-vindo, {user[1]} ({user[4]})").pack()

    # Botões do menu principal
    tk.Button(root, text="Cadastrar Produto",
              command=cadastro_produto.tela_cadastro).pack()
    tk.Button(root, text="Estoque", command=estoque.tela_estoque).pack()

    # Mostrar a opção de cadastrar usuário apenas para o admin
    if user[4] == "Administrador":
        tk.Button(root, text="Cadastrar Usuário",
                  command=cadastro_usuario.tela_cadastro_usuario).pack()

    # Iniciar a interface gráfica
    root.mainloop()

# Função para criar a tela de login


def tela_login():
    def login_action():
        usuario_input = entry_usuario.get()
        senha_input = entry_senha.get()

        # Verificar se o login está correto
        user = verificar_login(usuario_input, senha_input)

        if user:
            print("Login bem-sucedido!")
            tela_login.destroy()  # Fecha a tela de login
            # Abre o menu principal com os dados do usuário
            menu_principal(user)
        else:
            print("Usuário ou senha incorretos!")
            tk.Label(tela_login, text="Usuário ou senha incorretos!",
                     fg="red").pack()

    # Criando a janela de login
    tela_login = tk.Tk()
    tela_login.title("Tela de Login")

    # Criar campos para o login
    tk.Label(tela_login, text="Usuário:").pack()
    entry_usuario = tk.Entry(tela_login)
    entry_usuario.pack()

    tk.Label(tela_login, text="Senha:").pack()
    entry_senha = tk.Entry(tela_login, show="*")
    entry_senha.pack()

    tk.Button(tela_login, text="Login", command=login_action).pack()

    tela_login.mainloop()


# Chama a função de login
tela_login()
