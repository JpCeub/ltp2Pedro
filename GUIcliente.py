import tkinter as tk
from tkinter import ttk, messagebox
import bdcliente
from datetime import datetime

def iniciar_interface():
    root = tk.Tk()
    root.title("Sistema de Clientes e Pedidos")
    root.geometry("900x600")
    root.configure(bg="#f0f0f0")

    # Frame principal
    frame_principal = tk.Frame(root, bg="#f0f0f0")
    frame_principal.pack(padx=10, pady=10, fill="both", expand=True)

    # --- Frame Clientes ---
    frame_clientes = tk.LabelFrame(frame_principal, text="Clientes", bg="#f0f0f0")
    frame_clientes.pack(fill="x", pady=5)

    tk.Label(frame_clientes, text="Nome:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_nome_cliente = tk.Entry(frame_clientes)
    entry_nome_cliente.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_clientes, text="Telefone:", bg="#f0f0f0").grid(row=0, column=2, padx=5, pady=5, sticky="e")
    entry_telefone_cliente = tk.Entry(frame_clientes)
    entry_telefone_cliente.grid(row=0, column=3, padx=5, pady=5)

    tk.Button(frame_clientes, text="Adicionar", command=lambda: adicionar_cliente(), bg="#4CAF50", fg="white").grid(row=0, column=4, padx=5)
    tk.Button(frame_clientes, text="Atualizar", command=lambda: atualizar_cliente_selecionado(), bg="#2196F3", fg="white").grid(row=0, column=5, padx=5)
    tk.Button(frame_clientes, text="Excluir", command=lambda: deletar_cliente_selecionado(), bg="#f44336", fg="white").grid(row=0, column=6, padx=5)
    tk.Button(frame_clientes, text="Ver Pedidos do Cliente", command=lambda: listar_pedidos_do_cliente(), bg="#FF9800", fg="white").grid(row=0, column=7, padx=5)

    tree_clientes = ttk.Treeview(frame_clientes, columns=("ID", "Nome", "Telefone"), show="headings")
    tree_clientes.heading("ID", text="ID")
    tree_clientes.heading("Nome", text="Nome")
    tree_clientes.heading("Telefone", text="Telefone")
    tree_clientes.grid(row=1, column=0, columnspan=8, padx=5, pady=5, sticky="ew")

    # --- Frame Pedidos ---
    frame_pedidos = tk.LabelFrame(frame_principal, text="Pedidos", bg="#f0f0f0")
    frame_pedidos.pack(fill="x", pady=10)

    tk.Label(frame_pedidos, text="Cliente:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    cliente_var = tk.StringVar()
    menu_cliente = ttk.OptionMenu(frame_pedidos, cliente_var, "")
    menu_cliente.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_pedidos, text="Descrição:", bg="#f0f0f0").grid(row=0, column=2, padx=5, pady=5, sticky="e")
    entry_descricao_pedido = tk.Entry(frame_pedidos)
    entry_descricao_pedido.grid(row=0, column=3, padx=5, pady=5)

    tk.Label(frame_pedidos, text="Data (YYYY-MM-DD):", bg="#f0f0f0").grid(row=0, column=4, padx=5, pady=5, sticky="e")
    entry_data_pedido = tk.Entry(frame_pedidos)
    entry_data_pedido.grid(row=0, column=5, padx=5, pady=5)

    tk.Button(frame_pedidos, text="Adicionar Pedido", command=lambda: adicionar_pedido(), bg="#4CAF50", fg="white").grid(row=1, column=0, columnspan=2, pady=5)
    tk.Button(frame_pedidos, text="Atualizar Pedido", command=lambda: atualizar_pedido_selecionado(), bg="#2196F3", fg="white").grid(row=1, column=2, columnspan=2, pady=5)
    tk.Button(frame_pedidos, text="Excluir Pedido", command=lambda: deletar_pedido_selecionado(), bg="#f44336", fg="white").grid(row=1, column=4, columnspan=2, pady=5)

    tree_pedidos = ttk.Treeview(frame_principal, columns=("ID", "Cliente", "Descrição", "Data"), show="headings")
    tree_pedidos.heading("ID", text="ID")
    tree_pedidos.heading("Cliente", text="Cliente")
    tree_pedidos.heading("Descrição", text="Descrição")
    tree_pedidos.heading("Data", text="Data")
    tree_pedidos.pack(fill="both", expand=True, padx=5, pady=5)

    def carregar_clientes():
        tree_clientes.delete(*tree_clientes.get_children())
        menu_cliente['menu'].delete(0, 'end')
        clientes = bdcliente.listar_clientes()
        for cliente in clientes:
            tree_clientes.insert('', 'end', values=cliente)
            menu_cliente['menu'].add_command(label=cliente[1], command=tk._setit(cliente_var, cliente[1]))

    def carregar_pedidos():
        tree_pedidos.delete(*tree_pedidos.get_children())
        pedidos = bdcliente.listar_pedidos()
        for pedido in pedidos:
            tree_pedidos.insert('', 'end', values=pedido)

    def adicionar_cliente():
        nome = entry_nome_cliente.get()
        telefone = entry_telefone_cliente.get()
        if nome:
            bdcliente.inserir_cliente(nome, telefone)
            carregar_clientes()
            entry_nome_cliente.delete(0, 'end')
            entry_telefone_cliente.delete(0, 'end')

    def atualizar_cliente_selecionado():
        selecionado = tree_clientes.selection()
        if selecionado:
            cliente_id = tree_clientes.item(selecionado)['values'][0]
            nome = entry_nome_cliente.get()
            telefone = entry_telefone_cliente.get()
            bdcliente.atualizar_cliente(cliente_id, nome, telefone)
            carregar_clientes()

    def deletar_cliente_selecionado():
        selecionado = tree_clientes.selection()
        if selecionado:
            cliente_id = tree_clientes.item(selecionado)['values'][0]
            if messagebox.askyesno("Confirmação", "Deseja excluir este cliente?"):
                bdcliente.deletar_cliente(cliente_id)
                carregar_clientes()

    def adicionar_pedido():
        cliente_nome = cliente_var.get()
        cliente_id = bdcliente.obter_id_cliente_por_nome(cliente_nome)
        descricao = entry_descricao_pedido.get()
        data = entry_data_pedido.get()
        if cliente_id and descricao:
            bdcliente.inserir_pedido(cliente_id, descricao, data)
            carregar_pedidos()
            entry_descricao_pedido.delete(0, 'end')
            entry_data_pedido.delete(0, 'end')

    def atualizar_pedido_selecionado():
        selecionado = tree_pedidos.selection()
        if selecionado:
            pedido_id = tree_pedidos.item(selecionado)['values'][0]
            cliente_nome = cliente_var.get()
            cliente_id = bdcliente.obter_id_cliente_por_nome(cliente_nome)
            descricao = entry_descricao_pedido.get()
            data = entry_data_pedido.get()
            bdcliente.atualizar_pedido(pedido_id, cliente_id, descricao, data)
            carregar_pedidos()

    def deletar_pedido_selecionado():
        selecionado = tree_pedidos.selection()
        if selecionado:
            pedido_id = tree_pedidos.item(selecionado)['values'][0]
            if messagebox.askyesno("Confirmação", "Deseja excluir este pedido?"):
                bdcliente.deletar_pedido(pedido_id)
                carregar_pedidos()

    def listar_pedidos_do_cliente():
        selecionado = tree_clientes.selection()
        if selecionado:
            cliente_id = tree_clientes.item(selecionado)['values'][0]
            pedidos = bdcliente.listar_pedidos_por_cliente(cliente_id)
            tree_pedidos.delete(*tree_pedidos.get_children())
            for pedido in pedidos:
                tree_pedidos.insert('', 'end', values=pedido)

    carregar_clientes()
    carregar_pedidos()
    root.mainloop()
