import sqlite3
import hashlib
import os  # Certifique-se de que você importou o módulo os


def conectar():
    """Conectar ao banco de dados SQLite."""
    if not os.path.exists("db"):
        os.makedirs("db")
    return sqlite3.connect("db/estoque.db")


def criar_tabelas():
    """Criar as tabelas no banco de dados."""
    conn = conectar()
    cursor = conn.cursor()

    # Tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            perfil TEXT NOT NULL CHECK(perfil IN ('Administrador', 'Comum'))
        )
    ''')

    # Tabela de produtos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            minimo INTEGER NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("Tabelas criadas com sucesso.")


def criar_usuario_admin():
    """Criar o usuário admin no banco de dados, se não existir."""
    nome = "Administrador"
    usuario = "admin"
    senha = "admin123"  # A senha inicial que será criptografada
    perfil = "Administrador"  # Perfil de administrador

    # Criptografando a senha
    senha_cripto = hashlib.sha256(senha.encode()).hexdigest()

    # Conectando ao banco de dados e verificando se o usuário já existe
    conn = conectar()
    cursor = conn.cursor()

    # Verificando se o usuário 'admin' já existe
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,))
    user = cursor.fetchone()

    if user:
        print(f"O usuário '{usuario}' já existe no banco de dados.")
    else:
        try:
            # Inserindo o usuário administrador no banco de dados
            cursor.execute("""
                INSERT INTO usuarios (nome, usuario, senha, perfil)
                VALUES (?, ?, ?, ?)
            """, (nome, usuario, senha_cripto, perfil))

            conn.commit()
            print(f"Usuário '{usuario}' criado com sucesso!")
        except sqlite3.IntegrityError as e:
            print(f"Erro ao criar o usuário '{usuario}': {str(e)}")

    conn.close()


# Criação das tabelas
criar_tabelas()

# Criação do usuário admin
criar_usuario_admin()
