import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import customtkinter as ctk
from tkcalendar import DateEntry
import datetime
import json
import os

# caminho  para o arquivo json das tarefas
caminho_json_tarefas = "C:/Users/AFERR136/OneDrive - azureford/DEV PYTHON/INTERFACEGRAFICAS/MY-DAILY-TASKS/BACKUP-2"

if not os.path.exists(caminho_json_tarefas):
    os.makedirs(caminho_json_tarefas)

# caminho para salvar as credenciais de login/senha
caminho_credenciais = "C:/Users/AFERR136/OneDrive - azureford/DEV PYTHON/INTERFACEGRAFICAS/MY-DAILY-TASKS/CREDENCIAIS"

if not os.path.exists(caminho_credenciais):
    os.makedirs(caminho_credenciais)

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
    def salve_no_json(task, path):
        with open(os.path.join(path, f"{task.task_id}.json"), 'w') as f:
            json.dump(task.to_dict(), f, indent=4)

    @staticmethod
    def carregue_tarefas_do_json(task_id, path):
        try:
            with open(os.path.join(path, f"{task_id}.json"), 'r') as f:
                data = json.load(f)
            return Tarefa(**data)
        except FileNotFoundError:
            return None

    @staticmethod
    def deletar_tarefas_do_json(task_id, path):
        os.remove(os.path.join(path, f"{task_id}.json"))

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
        user_caminho_credenciais = os.path.join(caminho_credenciais, f"{username}.json")

        
        if os.path.exists(user_caminho_credenciais):
            with open(user_caminho_credenciais, 'r') as f:
                user_credentials = json.load(f)
         
            if user_credentials.get("password") == password:
                self.login_successful = True
                messagebox.showinfo("Login", "Login bem-sucedido!")
                self.top_level.destroy()  
            else:
              
                reset_password = messagebox.askyesno("Senha Incorreta", "Senha incorreta. Deseja redefinir a senha?")
                if reset_password:
                    self.resetar_senha(username)
        else:
            messagebox.showerror("Erro", "Usuário não encontrado.")

    def resetar_senha(self, username):
        # Solicita a nova senha
        new_password = simpledialog.askstring("Redefinir Senha", "Digite a nova senha:", show="*")
        if new_password:
            self.salvar_credenciais(username, new_password)
            messagebox.showinfo("Redefinição de Senha", "Sua senha foi redefinida com sucesso.")
        else:
            messagebox.showerror("Redefinição de Senha", "Redefinição de senha cancelada.")

    def novo_cadastro(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_caminho_credenciais = os.path.join(caminho_credenciais, f"{username}.json")

        
        if os.path.exists(user_caminho_credenciais):
           
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
        user_caminho_credenciais = os.path.join(caminho_credenciais, f"{username}.json")
        with open(user_caminho_credenciais, 'w') as f:
            json.dump({"username": username, "password": password}, f, indent=4)
    
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
      
        for label in self.task_labels:
            label.destroy()
        self.tasks.clear()
        self.task_labels.clear()

       
        for filename in os.listdir(caminho_json_tarefas):
            if filename.endswith(".json"):
                task_id = filename.split(".")[0]
                task = Tarefa.carregue_tarefas_do_json(task_id, caminho_json_tarefas)
                if task:
                    self.tasks.append(task)
                    self.display_task(task)

    def display_task(self, task):
        row = len(self.tasks)
        data = task.to_dict()
        for col, key in enumerate(data):
            label = ctk.CTkLabel(self.table, text=str(data[key]), anchor="w")
            label.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            self.task_labels.append(label)

       
        status_label = ctk.CTkLabel(self.table, text=data["completed"], anchor="w", fg_color=("green" if data["completed"] == "Concluído" else "red"))
        status_label.grid(row=row, column=self.columns-1, sticky="nsew", padx=2, pady=2)
        self.task_labels.append(status_label)

      
        for i in range(1, len(self.tasks) + 1):
            self.table.grid_rowconfigure(i, weight=0)

    def add_task(self):
       
        task_window = TaskWindow(self, title="Adicionar Tarefa", save_path=caminho_json_tarefas)
        self.wait_window(task_window.top_level)

       
        self.load_tasks()

    def update_task(self):
        
        task_id = simpledialog.askstring("Atualizar Tarefa", "Digite o ID da tarefa que deseja atualizar:")
        task = Tarefa.carregue_tarefas_do_json(task_id, caminho_json_tarefas)
        if task:
            task_window = TaskWindow(self, title="Atualizar Tarefa", task=task, save_path=caminho_json_tarefas, update=True)
            self.wait_window(task_window.top_level)

           
            self.load_tasks()
        else:
            messagebox.showerror("Erro", "Tarefa não encontrada.")

   
    def delete_task(self):
      
        task_id = simpledialog.askstring("Excluir Tarefa", "Digite o ID da tarefa que deseja excluir:")
        task = Tarefa.carregue_tarefas_do_json(task_id, caminho_json_tarefas)
        if task:
            confirm = messagebox.askyesno("Confirmar Exclusão", "Você tem certeza que deseja excluir esta tarefa?")
            if confirm:
                Tarefa.deletar_tarefas_do_json(task_id, caminho_json_tarefas)
                messagebox.showinfo("Sucesso", "Tarefa excluída com sucesso.")
                self.load_tasks()
        else:
            messagebox.showerror("Erro", "Tarefa não encontrada.")

    def on_closing(self):
       
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
    
        data = {field: self.fields[field].get() for field in self.fields if field not in ["start_date", "end_date"]}

  
        data["start_date"] = self.fields["start_date"].get_date().strftime("%d/%m/%Y")
        data["end_date"] = self.fields["end_date"].get_date().strftime("%d/%m/%Y")


        if self.update:
            data["task_id"] = self.task.task_id
        else:
        
            if not data["task_id"]:
                messagebox.showerror("Erro", "O ID da tarefa é obrigatório.")
                return

   
        self.task = Tarefa(**data)
        Tarefa.salve_no_json(self.task, self.save_path)

        messagebox.showinfo("Sucesso", f"Tarefa {'atualizada' if self.update else 'adicionada'} com sucesso.")
        self.top_level.destroy()

if __name__ == "__main__":
    app = MeuApp()
    app.mainloop()
