import tkinter as tk
from tkinter import Frame, PhotoImage, messagebox, ttk
import mysql.connector
from mysql.connector import Error
import customtkinter as Ctk  
from PIL import ImageTk, Image  
import pyglet  
import webbrowser  

# Função para fazer login
def login(usuario, senha):
    try:
        # Conexão com o banco de dados
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="clothing-system"
        )
        cursor = conn.cursor()
        consulta = "SELECT * FROM admins WHERE Usuario = %s AND Senha = %s"
        dados = (usuario, senha)
        cursor.execute(consulta, dados)

        if cursor.fetchone():
            return True
        else:
            return False

    except mysql.connector.Error as erro:
        print("Erro ao conectar ao MySQL:", erro)
        return False

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()    

# Função para validar o login e abrir a tela administrativa
def validar_login():
    usuario = input_usuario.get()
    senha = input_senha.get()

    try:
        if login(usuario, senha):  
            tela_login.withdraw()  
            abrir_hud()  
        else:
            messagebox.showerror("Login", "Login falhou. Verifique suas credenciais.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
        
def hud_de_selecao():
    
    # Função voltar à tela inicial
    def voltar_tela_inicial():
        hud_selecao.withdraw()
        tela_login.deiconify()

    # Cria o HUD de seleção
    hud_selecao = Ctk.CTkToplevel(tela_login)
    hud_selecao.title("Selecione o que Deseja")
    hud_selecao.geometry("700x700")
    hud_de_selecao.attributes('-fullscreen', True)

    # Configuração de layout
    hud_selecao.grid_rowconfigure(0, weight=1)
    hud_selecao.grid_rowconfigure(1, weight=1)
    hud_selecao.grid_rowconfigure(2, weight=1)
    hud_selecao.grid_rowconfigure(3, weight=1)
    hud_selecao.grid_columnconfigure(0, weight=1)
    hud_selecao.grid_columnconfigure(1, weight=1)

    # Botões do HUD de seleção
    botao_usuarios = Ctk.CTkButton(hud_selecao, width=200, height=200, text="Usuários")
    botao_usuarios.grid(row=0, column=0, padx=10, pady=10)

    botao_adm = Ctk.CTkButton(hud_selecao, width=200, height=200, text="Admin")
    botao_adm.grid(row=0, column=1, padx=10, pady=10)

    botao_produtos = Ctk.CTkButton(hud_selecao, width=200, height=200, text="Produtos", command=produtos) 
    botao_produtos.grid(row=1, column=0, padx=10, pady=10)

    botao_cadastro = Ctk.CTkButton(hud_selecao, width=200, height=200, text="Cadastro")
    botao_cadastro.grid(row=1, column=1, padx=10, pady=10)

    botao_voltar = Ctk.CTkButton(hud_selecao, text="Voltar", command=voltar_tela_inicial)
    botao_voltar.grid(row=2, column=0)
    
def abrir_hud():
    hud_de_selecao()


def produtos():
    # Conecta ao banco de dados
    conn = mysql.connector.connect(
        host="localhost",  # ajuste para o seu host
        user="root",  # ajuste para o seu usuário
        password="",  # ajuste para a sua senha
        database="clothing-system"  # ajuste para o seu banco
    )
    cursor = conn.cursor()

    # Cria uma nova janela para produtos
    tabelas_produtos = Ctk.CTkToplevel()
    tabelas_produtos.title("Selecione seu produto")
    tabelas_produtos.geometry("1280x720")

    # Cria o notebook (abas)
    notebook = ttk.Notebook(tabelas_produtos)
    notebook.pack(fill='both', expand=True)

    # Frame para a aba de visualização (camisas e shorts)
    frame_visualizar = Ctk.CTkFrame(notebook)
    notebook.add(frame_visualizar, text="Visualizar Produtos")

    # Frame para a aba de edição e exclusão
    frame_editar_deletar = Ctk.CTkFrame(notebook)
    notebook.add(frame_editar_deletar, text="Editar/Deletar Produtos")

    # Frame para a aba de adição
    frame_adicionar = Ctk.CTkFrame(notebook)
    notebook.add(frame_adicionar, text="Adicionar Produto")


# Tela de Login
def criar_tela_login():
    global tela_login, input_usuario, input_senha

    tela_login = Ctk.CTk() 
    tela_login.title("Login")
    tela_login.config(bg="white")
    tela_login.resizable(False, False)

    # Carregar imagem de fundo
    bg_img = Ctk.CTkImage(dark_image=Image.open("App/logo.jpg"), size=(500, 500))
    bg_lab = Ctk.CTkLabel(tela_login, image=bg_img, text="")
    bg_lab.grid(row=0, column=0)

    # Frame principal
    frame1 = Ctk.CTkFrame(tela_login, fg_color="white", height=350, width=300)
    frame1.grid(row=0, column=1, padx=40)

    # Título do login
    title = Ctk.CTkLabel(frame1, text="Login", text_color="Black", font=("Bahnschrift", 35))
    title.grid(row=0, column=0,pady=30, padx=100)

    # Entradas de texto para o usuário e senha
    input_usuario = Ctk.CTkEntry(frame1, text_color="black", placeholder_text="Usuário", fg_color="white",
                                 placeholder_text_color="black", font=("Bahnschrift", 15), width=200, height=45)
    input_usuario.grid(row=1, column=0, padx=30)

    input_senha = Ctk.CTkEntry(frame1, text_color="black", placeholder_text="Senha", fg_color="white",
                               placeholder_text_color="black", font=("Bahnschrift", 15), width=200, height=45, show="*")
    input_senha.grid(row=2, column=0, padx=30, pady=20)

    # Botão de Login
    l_btn = Ctk.CTkButton(frame1, text="Login", font=("Bahnschrift", 15), height=40, width=60, fg_color="#000",
                          cursor="hand2", command=validar_login)
    l_btn.grid(row=3, column=0, pady=20, padx=100)

    tela_login.mainloop()


# Iniciar a aplicação
criar_tela_login()
