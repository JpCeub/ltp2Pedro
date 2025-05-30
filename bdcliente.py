import sqlite3

def conectar():
    return sqlite3.connect("mercadinho.db")

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            descricao TEXT,
            data TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )
    ''')
    conn.commit()
    conn.close()

def inserir_cliente(nome, telefone):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes (nome, telefone) VALUES (?, ?)", (nome, telefone))
    conn.commit()
    conn.close()

def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, telefone FROM clientes")
    clientes = cursor.fetchall()
    conn.close()
    return clientes

def atualizar_cliente(cliente_id, nome, telefone):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE clientes SET nome = ?, telefone = ? WHERE id = ?", (nome, telefone, cliente_id))
    conn.commit()
    conn.close()

def deletar_cliente(cliente_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
    conn.commit()
    conn.close()

def inserir_pedido(cliente_id, descricao, data):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pedidos (cliente_id, descricao, data) VALUES (?, ?, ?)", (cliente_id, descricao, data))
    conn.commit()
    conn.close()

def listar_pedidos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT pedidos.id, clientes.nome, pedidos.descricao, pedidos.data
        FROM pedidos
        JOIN clientes ON pedidos.cliente_id = clientes.id
    ''')
    pedidos = cursor.fetchall()
    conn.close()
    return pedidos

def atualizar_pedido(pedido_id, cliente_id, descricao, data):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE pedidos SET cliente_id = ?, descricao = ?, data = ? WHERE id = ?", (cliente_id, descricao, data, pedido_id))
    conn.commit()
    conn.close()

def deletar_pedido(pedido_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pedidos WHERE id = ?", (pedido_id,))
    conn.commit()
    conn.close()
