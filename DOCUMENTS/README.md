# Aplicativo Minhas Tarefas Diárias

## Visão Geral

O aplicativo Minhas Tarefas Diárias é uma aplicação desktop desenvolvida em Python, criada para auxiliar os usuários na gestão eficiente de suas tarefas cotidianas. Oferece uma interface gráfica simples e intuitiva para adicionar, atualizar e excluir tarefas. Com a capacidade de salvar detalhes das tarefas e credenciais dos usuários em formato JSON, garante que os dados estejam organizados e facilmente acessíveis.

## Recursos

- Autenticação de Usuário
  - Funcionalidade de login com nome de usuário e senha.
  - Opção para registrar um novo usuário.
  - Recurso para redefinição de senha para usuários existentes.

- Gerenciamento de Tarefas
  - Adicionar novas tarefas com detalhes como ID, pessoa responsável, nome da tarefa, datas de início e término e status de conclusão.
  - Atualizar tarefas existentes modificando qualquer detalhe.
  - Excluir tarefas que não são mais necessárias.
  - Armazenamento persistente de tarefas em formato JSON.
  - Lista de tarefas de fácil navegação com exibição clara dos detalhes e do status da tarefa.

## Instalação

Antes de executar a aplicação, certifique-se de que você tem os seguintes requisitos instalados:

- Python 3.6 ou superior
- Biblioteca `tkinter`
- Biblioteca `customtkinter`
- Biblioteca `tkcalendar`

Para instalar as bibliotecas de terceiros necessárias, você pode usar o `pip`:

```bash
pip install customtkinter tkcalendar
```

## Uso

Para começar a usar o aplicativo Minhas Tarefas Diárias, siga estes passos:

1. Clone ou baixe o repositório para a sua máquina local.
2. Navegue até o diretório que contém os arquivos do aplicativo.
3. Execute o arquivo principal do aplicativo:
   ```bash
   python web.py
   ```

O aplicativo será iniciado e você será solicitado a fazer login ou se registrar se for um novo usuário.

## Estrutura da Aplicação

A aplicação é estruturada em várias classes que encapsulam diferentes funcionalidades:

- `Task`: Representa uma tarefa com atributos como ID, pessoa responsável, nome, data de início, data de término e status de conclusão. Inclui métodos para converter objetos de tarefa em dicionários, salvar em JSON, carregar de JSON e excluir arquivos JSON correspondentes às tarefas.

- `LoginWindow`: Gerencia o processo de autenticação do usuário, incluindo login, registro e redefinição de senhas.

- `MyApp`: A classe principal da aplicação que configura a interface do usuário e as funcionalidades de gerenciamento de tarefas.

- `TaskWindow`: Fornece uma janela pop-up para adicionar ou atualizar tarefas.

- `json_save_path`: Caminho do diretório para salvar arquivos JSON das tarefas.

- `credentials_path`: Caminho do diretório para salvar arquivos JSON das credenciais de usuário.

## Estrutura de Arquivos

O código da aplicação lida com caminhos de arquivos para armazenar dados. Os dados JSON para tarefas e credenciais de usuários são armazenados nos seguintes diretórios:

- Tarefas: `C:/Users/AFERR136/OneDrive - azureford/DEV PYTHON/INTERFACEGRAFICAS/MY-DAILY-TASKS/BACKUP-2`
- Credenciais de Usuário: `C:/Users/AFERR136/OneDrive - azureford/DEV PYTHON/INTERFACEGRAFICAS/MY-DAILY-TASKS/CREDENCIAIS`

## Contribuição

Contribuições para a aplicação Minhas Tarefas Diárias são bem-vindas. Siga estes passos para contribuir:

1. Faça um fork do repositório.
2. Crie uma nova branch para sua funcionalidade.
3. Faça commit das suas alterações.
4. Envie para a branch.
5. Abra um pull request.

## Suporte

Caso você encontre algum problema ou tenha alguma dúvida sobre a aplicação, por favor abra uma issue no repositório do projeto ou entre em contato com o mantenedor.

## Créditos

A aplicação Minhas Tarefas Diárias foi desenvolvida por [Nome do Desenvolvedor ou Equipe de Desenvolvedores] como uma ferramenta para auxiliar na gestão de atividades diárias.

## Instruções Adicionais

- Certifique-se de que os caminhos para os diretórios de salvamento dos arquivos JSON sejam acessíveis e tenham as permissões necessárias para leitura e escrita.
- A interface gráfica é construída usando a biblioteca `tkinter` e `customtkinter`, assegurando uma experiência de usuário agradável e consistente.
- A aplicação utiliza o `tkcalendar` para fornecer seletores de datas fáceis de usar ao definir datas de início e término das tarefas.

## Notas Finais

Este documento README.md destina-se a fornecer todas as informações necessárias para entender, instalar e utilizar a aplicação Minhas Tarefas Diárias. As instruções e informações foram detalhadas de forma técnica, visando um público que possui alguma familiaridade com a execução de programas Python e o uso do sistema operacional Windows.