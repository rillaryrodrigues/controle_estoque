import sqlite3  # Importando sqlite3 para manipulação do banco de dados
import banco_db  # Importando o módulo 'banco' que você criou para conectar ao banco
import hashlib  # Para criptografar a senha


def criar_usuario_admin():
    # Dados do administrador
    nome = "Administrador"
    usuario = "admin"
    senha = "admin123"  # A senha inicial que será criptografada
    perfil = "Administrador"  # Perfil de administrador

    # Criptografando a senha
    senha_cripto = hashlib.sha256(senha.encode()).hexdigest()

    # Conectando ao banco de dados e inserindo o usuário
    conn = banco_db.conectar()  # Função 'conectar' deve ser do seu módulo 'banco'
    cursor = conn.cursor()

    # Inserindo o usuário administrador no banco de dados
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


# Rodar a função para criar o usuário admin
criar_usuario_admin()
