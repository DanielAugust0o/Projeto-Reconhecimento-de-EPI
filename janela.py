
from tkinter import *
import customtkinter as ctk
import sqlite3
from tkinter import messagebox
from janela_ferramentas import janela2



class BackEnd():
    def conecta_db(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        print('Banco de dados conectado com sucesso!')

    def desconecta_db(self):
        self.conn.close()
        print('Banco de dados desconectado')

    def cria_tabela(self):
        self.conecta_db()

        self.cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS Usuarios (
            Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            Username TEXT NOT NULL,
            Email TEXT NOT NULL,
            Senha TEXT NOT NULL,
            Confirma_Senha TEXT NOT NULL   
        );
        ''')
        self.conn.commit()
        print('Tabela criada com sucesso!')
        self.desconecta_db()

    def cadastrar_usuario(self):
        self.username_cadastro = self.username_cadastro_entry.get()
        self.email_cadastro = self.email_cadastro_entry.get()
        self.senha_cadastro = self.senha_cadastro_entry.get()
        self.confirma_senha_cadastro = self.confirma_senha_entry.get()

        self.conecta_db()


        self.cursor.execute('''
            INSERT INTO Usuarios (Username, Email, Senha, Confirma_Senha)
            VALUES (?, ?, ?, ?)''',(self.username_cadastro, self.email_cadastro, self.senha_cadastro, self.confirma_senha_cadastro))

        try:
            if(self.username_cadastro == '' or self.email_cadastro == '' or self.senha_cadastro == '' or self.confirma_senha_cadastro == ''):
                messagebox.showerror(title='Sistema de login', message= 'ERRO!!\nPor favor preencha todos os campos!')
            elif(len(self.username_cadastro) < 4 ):
                messagebox.showerror(title='Sistema de Login', message='O nome de usuário deve ter pelo menos 4 caracteres.')
            elif(len(self.senha_cadastro or self.confirma_senha_cadastro) < 4 ):
                messagebox.showerror(title='Sistema de Login', message='A senha deve conter mais que 4 caracteres.')

            elif(self.senha_cadastro != self.confirma_senha_cadastro):
                messagebox.showerror(title='Sistema de login',message= 'ERRO!\nAs senhas colocadas não são iguais.')
            else:
                self.conn.commit()
                messagebox.showinfo(title='Cadastro', message=f'Parabens {self.username_cadastro}\n Casdastro realizado com sucesso!')
                self.desconecta_db()
                self.tela_login()
        except:
            messagebox.showerror(title='Cadastro', message='Erro no processamento do seu cadasttro!\n Por favor tente novamente!')
            self.desconecta_db()

    def verifica_login(self):
        self.username_login = self.username_login_entry.get()
        self.senha_login = self.senha_login_entry.get()

        self.conecta_db()

        self.cursor.execute('''SELECT * FROM Usuarios WHERE (Username = ? AND Senha = ?)''',
                            (self.username_login, self.senha_login))

        self.verifica_dados = self.cursor.fetchone()  # Percorrendo na tabela usuarios

        if self.verifica_dados:
            messagebox.showinfo(title='Login', message=f'Parabéns {self.username_login}\nLogin feito com sucesso!')
            self.desconecta_db()
            self.abrir_nova_tela()
        else:
            messagebox.showerror(title='Login',
                                 message='ERRO!!\n Dados não encontrados.\n Por favor digite novamente seus dados ou cadastre-se no sistema! ')
            self.limpa_entry_login()
            self.desconecta_db()
class App(ctk.CTk, BackEnd):
    def __init__(self):
        super().__init__()
        self.conf_janela_ini()
        self.tela_login()
        self.cria_tabela()

    #Conf Janela Principal
    def conf_janela_ini(self):
        self.geometry('700x400')
        self.title('Tela de Login')
        self.resizable(False, False)

    def tela_login(self):
        #Trabalhando com as imagens
        self.img = PhotoImage(file='Imagens/ppe1.png')
        self.lb_img = ctk.CTkLabel(self, text=None, image=self.img)
        self.lb_img.grid(row=1, column=0, padx=10, pady=20)

        # Titulo da imagem - janela login
        self.title = ctk.CTkLabel(self, text='Entre em sua conta e tenha \n acesso a plataforma', font=('Roboto', 24, 'bold'), text_color='#EEAD2D')
        self.title.grid(row=0, column=0, padx=20, pady=20)

        #criar o frame do formulario de login
        self.frame_login = ctk.CTkFrame(self, width=350, height=380)
        self.frame_login.place(x=350, y=50)

        #Colocando widgets dentro do frame - formulário de login
        self.lb_title = ctk.CTkLabel(self.frame_login, text='Faça o seu login!', font=('Roboto', 22, 'bold'))
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)

        #lbl usuário
        self.username_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text='Usuário', font=('Roboto bold', 16, 'bold'), corner_radius=15)
        self.username_login_entry.grid(row=1, column=0, padx=10, pady=10)

        #lbl senha
        self.senha_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text='Senha', font=('Roboto bold', 16, 'bold'), corner_radius=15, show='*')
        self.senha_login_entry.grid(row=2, column=0, padx=10, pady=10)

        #check box ver senha
        self.ver_senha = ctk.CTkCheckBox(self.frame_login, text='Clique para ver a senha', font=('Roboto bold', 16, 'bold'), corner_radius=20)
        self.ver_senha.grid(row=3, column=0, padx=10, pady=10)

        #btn login
        self.btn_login = ctk.CTkButton(self.frame_login, width=300, text='Login'.upper(), font=('Roboto bold', 16, 'bold'), corner_radius=20, command=self.verifica_login)
        self.btn_login.grid(row=4, column=0, padx=10, pady=10)

        #btn cadastro
        self.span = ctk.CTkLabel(self.frame_login, text='Não possuí uma conta?', font=('Roboto', 12, 'bold'))
        self.span.grid(row=5, column=0, padx=20, pady=10, sticky='W')

        #btn cadastro
        self.btn_cadastro = ctk.CTkButton(self.frame_login, width=140, fg_color='green', hover_color='#050', text='Cadastre-se', font=('Roboto bold', 16), corner_radius=15, command=self.tela_cadastro)
        self.btn_cadastro.grid(row=5, column=0, padx=0, pady=15, sticky='E')

    def tela_cadastro(self):
        #Remover o formulário de Login
        self.frame_login.place_forget()

        #criar o frame do formulario de cadastro
        self.frame_cadastro = ctk.CTkFrame(self, width=350, height=380)
        self.frame_cadastro.place(x=350, y=50)

        #Criando widgets do form cadastro
        #titulo frorm cadastro
        self.lb_title = ctk.CTkLabel(self.frame_cadastro, text='Cadastre-se', font=('Roboto', 22, 'bold'))
        self.lb_title.grid(row=0, column=0, padx=10, pady=10)

        #lbl cad_usuário
        self.username_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text='Usuário', font=('Roboto bold', 16, 'bold'), corner_radius=15)
        self.username_cadastro_entry.grid(row=1, column=0, padx=10, pady=10)

        #lbl cad_email
        self.email_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text='E-mail', font=('Roboto bold', 16, 'bold'), corner_radius=15)
        self.email_cadastro_entry.grid(row=2, column=0, padx=10, pady=10)

        #lbl cad_senha
        self.senha_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text='Senha', font=('Roboto bold', 16, 'bold'), corner_radius=15)
        self.senha_cadastro_entry.grid(row=3, column=0, padx=10, pady=10)

        #lbl conf_senha
        self.confirma_senha_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text='Confirme sua senha', font=('Roboto bold', 16, 'bold'), corner_radius=15, show='*')
        self.confirma_senha_entry.grid(row=4, column=0, padx=10, pady=10)

        #btn cadastrar
        self.btn_cadastrar = ctk.CTkButton(self.frame_cadastro, width=140, fg_color='#4c6c8c', hover_color='#4682B4', text='Cadastrar', font=('Roboto bold', 16), corner_radius=15, command=self.cadastrar_usuario)
        self.btn_cadastrar.grid(row=5, column=0, padx=5, pady=15, sticky='E')

        #btn voltar
        self.btn_voltar = ctk.CTkButton(self.frame_cadastro, width=140, fg_color='#FF0000', hover_color='#8B0000', text='Voltar', font=('Roboto bold', 16), corner_radius=15, command=self.tela_login)
        self.btn_voltar.grid(row=5, column=0, padx=5, pady=15, sticky='W')

    def limpa_entry_cadastro(self):
        self.username_cadastro_entry.delete(0, END)
        self.email_cadastro_entry.delete(0, END)
        self.senha_cadastro_entry.delete(0, END)
        self.confirma_senha_entry.delete(0, END)

    def limpa_entry_login(self):
        self.username_login_entry.delete(0, END)
        self.senha_login_entry.delete(0, END)

    def abrir_nova_tela(self):
        self.destroy() #fechando janela principal
        self.janelaferramentas = janela2()
        self.janelaferramentas(self)




if __name__ == '__main__':
    app = App()
    app.mainloop()
