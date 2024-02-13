import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import customtkinter as ctk
from tkcalendar import DateEntry
import datetime
import json
import os
import sqlite3

# Conexão com o banco de dados
conexao = sqlite3.connect('meu_banco_de_dados.db')
cursor = conexao.cursor()

# Classe de tarefa
class Tarefa:
    def __init__(self, task_id, responsible, name, start_date, end_date, completed):
        self.task_id = task_id
        self.responsible = responsible
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.completed = completed

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "responsible": self.responsible,
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "completed": self.completed
        }

    @staticmethod
    def salve_no_db(task):
        cursor.execute('''
        INSERT INTO MinhasTarefas (task_id, responsible, name, start_date, end_date, completed)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (task.task_id, task.responsible, task.name, task.start_date, task.end_date, task.completed))
        conexao.commit()

    @staticmethod
    def carregue_tarefas_do_db(task_id):
        cursor.execute('SELECT * FROM MinhasTarefas WHERE task_id = ?', (task_id,))
        row = cursor.fetchone()
        if row:
            return Tarefa(*row)
        return None
   
    @staticmethod
    def atualizar_tarefa_no_db(task_id, responsible, name, start_date, end_date, completed):
        cursor.execute('''
        UPDATE MinhasTarefas
        SET responsible = ?, name = ?, start_date = ?, end_date = ?, completed = ?
        WHERE task_id = ?
        ''', (responsible, name, start_date, end_date, completed, task_id))
        conexao.commit()

    @staticmethod
    def deletar_tarefas_do_db(task_id):
        cursor.execute('DELETE FROM MinhasTarefas WHERE task_id = ?', (task_id,))
        conexao.commit()

# Classe de Login/Cadastro
class JanelaLogin:
    def __init__(self, parent):
        self.top_level = ctk.CTkToplevel(parent)
        self.top_level.title("Login / Cadastro")
        self.top_level.geometry("400x200")
        self.top_level.resizable(False, False)
        self.login_successful = False

       
        self.username_entry = ctk.CTkEntry(self.top_level, placeholder_text="Nome de usuário")
        self.username_entry.pack(pady=10)

       
        self.password_entry = ctk.CTkEntry(self.top_level, placeholder_text="Senha", show="*")
        self.password_entry.pack(pady=10)

      
        self.login_button = ctk.CTkButton(self.top_level, text="Login", command=self.login)
        self.login_button.pack(pady=5)

     
        self.register_button = ctk.CTkButton(self.top_level, text="Cadastrar", command=self.novo_cadastro)
        self.register_button.pack(pady=5)

      
        self.username_entry.focus_set()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        cursor.execute('SELECT * FROM credenciais_de_acesso WHERE login = ?', (username,))
        user_credentials = cursor.fetchone()
        if user_credentials and user_credentials[1] == password:
            self.login_successful = True
            messagebox.showinfo("Login", "Login bem-sucedido!")
            self.top_level.destroy()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")

    def novo_cadastro(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        cursor.execute('SELECT * FROM credenciais_de_acesso WHERE login = ?', (username,))
        if cursor.fetchone():
            mudar_senha = messagebox.askyesno("Usuário Existente", "Usuário já existe. Deseja trocar a senha?")
            if mudar_senha:
                self.salvar_credenciais(username, password)
                messagebox.showinfo("Cadastro", "Senha atualizada com sucesso.")
                self.top_level.destroy()
        else:
            self.salvar_credenciais(username, password)
            messagebox.showinfo("Cadastro", "Usuário cadastrado com sucesso.")
            self.top_level.destroy()

    def salvar_credenciais(self, username, password):
        cursor.execute('REPLACE INTO credenciais_de_acesso (login, senha) VALUES (?, ?)', (username, password))
        conexao.commit()
    
    def on_closing(self):
        if not self.login_successful:
            self.top_level.destroy()

# Class principal da aplicação
class MeuApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.login_successful = False

         # Iniciar a tela de login antes de mostrar a tela principal de tarefas
        self.show_login()

    def show_login(self):
        login_window = JanelaLogin(self)
        self.wait_window(login_window.top_level)
        if not login_window.login_successful: 
            self.destroy() 
        else:
            self.login_successful = True  
            self.initialize_ui()

    def initialize_ui(self):
        self.title("MINHAS TAREFAS DIÁRIAS")
        self.geometry("1100x600")
        self.minsize(1100, 800)

        
        # Botão para adicionar uma nova tarefa, atualizar tarefas e excluir tarefas dentro do frame a esquerda
        self.frame_buttons = ctk.CTkFrame(self, width=200, height=500)
        self.frame_buttons.pack(side="left", fill="y", padx=10, pady=10)

        self.btn_add_task = ctk.CTkButton(self.frame_buttons, text="Adicionar tarefa", command=self.add_task)
        self.btn_add_task.pack(pady=10)

        self.btn_update_task = ctk.CTkButton(self.frame_buttons, text="Atualizar tarefa", command=self.update_task)
        self.btn_update_task.pack(pady=10)

        self.btn_delete_task = ctk.CTkButton(self.frame_buttons, text="Excluir tarefa", command=self.delete_task)
        self.btn_delete_task.pack(pady=10)

        
        # Criar a tela principal de tarefas
        self.frame_table = ctk.CTkFrame(self, width=500, height=500)
        self.frame_table.pack(side="left", fill="both", expand=True, padx=10, pady=10)
              
        self.table_headers = [
            "ID da tarefa", "Nome do responsável", "Nome da tarefa",
            "Data de início", "Data de fim", "Status"
        ]
        self.columns = len(self.table_headers)
        self.table = ctk.CTkFrame(self.frame_table)
        self.table.pack(fill="both", expand=True)

        for i, header in enumerate(self.table_headers):
            label = ctk.CTkLabel(self.table, text=header, anchor="w", fg_color=("gray75", "gray30"))
            label.grid(row=0, column=i, sticky="nsew", padx=2, pady=2)

        
        for i in range(self.columns):
            self.table.grid_columnconfigure(i, weight=1)

        self.table.grid_rowconfigure(0, weight=0)  

      
        self.tasks = []
        self.task_labels = []

        self.load_tasks()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)  

    def load_tasks(self):
        # Limpa a lista de tarefas e labels
        for label in self.task_labels:
            label.destroy()
        self.tasks.clear()
        self.task_labels.clear()

        # Carrega as tarefas do banco de dados
        cursor.execute('SELECT * FROM MinhasTarefas')
        rows = cursor.fetchall()
        for i, row in enumerate(rows, start=1):
            task = Tarefa(*row)
            self.tasks.append(task)
            for j, value in enumerate(row):
                label = ctk.CTkLabel(self.table, text=value, anchor="w")
                label.grid(row=i, column=j, sticky="nsew", padx=2, pady=2)
                self.task_labels.append(label)
            # Cria o status_label para a coluna de status, usando dados da tarefa atual
            status_label = ctk.CTkLabel(self.table, text=row[-1], anchor="w", fg_color=("green" if row[-1] == "Concluído" else "red"))
            status_label.grid(row=i, column=self.columns-1, sticky="nsew", padx=2, pady=2)
            self.task_labels.append(status_label)

        for i in range(self.columns):
            self.table.grid_columnconfigure(i, weight=1)

        for i in range(1, len(self.tasks) + 1):
            self.table.grid_rowconfigure(i, weight=0)


    def add_task(self):
        task_window = TaskWindow(self, title="Adicionar Tarefa")
        self.wait_window(task_window.top_level)
        self.load_tasks()

    def update_task(self):
        task_id = simpledialog.askstring("Atualizar Tarefa", "Digite o ID da tarefa que deseja atualizar:")
        task = Tarefa.carregue_tarefas_do_db(task_id)
        if task:
            task_window = TaskWindow(self, title="Atualizar Tarefa", task=task, update=True)
            self.wait_window(task_window.top_level)
            self.load_tasks()
        else:
            messagebox.showerror("Erro", "Tarefa não encontrada.")

    def delete_task(self):
        task_id = simpledialog.askstring("Excluir Tarefa", "Digite o ID da tarefa que deseja excluir:")
        task = Tarefa.carregue_tarefas_do_db(task_id)
        if task:
            confirm = messagebox.askyesno("Confirmar Exclusão", "Você tem certeza que deseja excluir esta tarefa?")
            if confirm:
                Tarefa.deletar_tarefas_do_db(task_id)
                messagebox.showinfo("Sucesso", "Tarefa excluída com sucesso.")
                self.load_tasks()
        else:
            messagebox.showerror("Erro", "Tarefa não encontrada.")

    def on_closing(self):
        # Fecha a conexão com o banco de dados antes de fechar a janela
        cursor.close()
        conexao.close()
        self.destroy()

class TaskWindow:
    def __init__(self, parent, title, task=None, save_path="", update=False):
        self.top_level = ctk.CTkToplevel(parent)
        self.top_level.title(title)
        self.save_path = save_path
        self.update = update
        self.top_level.geometry("600x400")
        self.top_level.resizable(False, True)

        self.task = task if task else Tarefa(task_id="", responsible="", name="", start_date="", end_date="", completed="Não Concluído")
        self.fields = {}

        # Adicione rótulos e campos de entrada para cada atributo da tarefa
        label_texts = {
            "task_id": "Coloque o ID da tarefa:",
            "responsible": "Nome do responsável:",
            "name": "Nome da tarefa:",
            "start_date": "Data de início:",
            "end_date": "Data de fim:",
            "completed": "Status da conclusão:"
        }

        for field, text in label_texts.items():
            # Criar e empacotar o rótulo
            label = ctk.CTkLabel(self.top_level, text=text)
            label.pack(pady=2)

            # Criar e empacotar o campo de entrada correspondente
            if field in ["start_date", "end_date"]:
                entry = DateEntry(self.top_level, date_pattern='dd/mm/yyyy')
                if self.task and getattr(self.task, field):
                    entry.set_date(datetime.datetime.strptime(getattr(self.task, field), "%d/%m/%Y"))
            elif field == "completed":
                entry = ctk.CTkComboBox(self.top_level, values=["Concluído", "Não Concluído"])
                entry.set(self.task.completed if self.task else "Não Concluído")
            else:
                entry = ctk.CTkEntry(self.top_level, placeholder_text=text)
                if self.task and getattr(self.task, field):
                    entry.insert(0, getattr(self.task, field))
                    if field == "task_id":
                        entry.configure(state='disabled')

            entry.pack(pady=2)
            self.fields[field] = entry

        entry.pack(pady=2)
        self.fields[field] = entry

        action_text = "Atualizar" if update else "Adicionar"
        self.btn_action = ctk.CTkButton(self.top_level, text=action_text, command=self.save_task)
        self.btn_action.pack(pady=10)

        self.top_level.grab_set()

    def save_task(self):
        # Recupera os valores dos campos de texto
        data = {field: self.fields[field].get() for field in self.fields if field not in ["start_date", "end_date"]}

        # Formata as datas de início e fim
        data["start_date"] = self.fields["start_date"].get_date().strftime("%d/%m/%Y")
        data["end_date"] = self.fields["end_date"].get_date().strftime("%d/%m/%Y")
        
        if self.update:
            # Atualiza a tarefa existente no banco de dados
            Tarefa.atualizar_tarefa_no_db(self.task.task_id, data['responsible'], data['name'], data["start_date"], data["end_date"], data['completed'])
        else:
            if not data["task_id"]:
                messagebox.showerror("Erro", "O ID da tarefa é obrigatório.")
                return
            # Cria uma nova instância de Tarefa e salva no banco de dados
            nova_tarefa = Tarefa(**data)
            Tarefa.salve_no_db(nova_tarefa)
        
        messagebox.showinfo("Sucesso", f"Tarefa {'atualizada' if self.update else 'adicionada'} com sucesso.")
        self.top_level.destroy()


if __name__ == "__main__":
    app = MeuApp()
    app.mainloop()
