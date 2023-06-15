import tkinter as tk
import tkinter.font as tkfont
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.headerregistry import Address
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# Definir data de hoje
hoje = datetime.today().date()

# Definir função para enviar e-mail
def enviar_email(destinatarios, mensagem):
    # Configurar servidor SMTP
    smtp_server = 'servidor_smtp'
    smtp_port = 587
    smtp_username = 'seu_email'
    smtp_password = 'sua_senha'

    # Criar mensagem
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = ', '.join(destinatarios)
    msg['Subject'] = 'Mensalidade a vencer'
    msg.attach(MIMEText(mensagem, 'plain'))

    # Enviar mensagem
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, destinatarios, msg.as_string())

def cadastrar():
    # Pegar dados do formulário
    nome = nome_entry.get()
    valor = valor_entry.get()
    vencimento = vencimento_entry.get()
    email = email_entry.get()

    # Salvar dados em arquivo
    with open('irmaos.txt', 'a') as f:
        f.write(f'{nome};{valor};{vencimento};{email}\n')

    # Limpar formulário
    nome_entry.delete(0, 'end')
    valor_entry.delete(0, 'end')
    vencimento_entry.delete(0, 'end')
    email_entry.delete(0, 'end')

def consultar():
    # Ler dados do arquivo
    with open('irmaos.txt', 'r') as f:
        dados = f.readlines()

    # Criar janela para mostrar dados
    consulta_janela = tk.Toplevel(root)
    consulta_janela.title('Irmãos cadastrados')

    # Adicionar dados na janela
    for linha, dado in enumerate(dados):
        nome, valor, vencimento, email = dado.strip().split(';')
        tk.Label(consulta_janela, text=nome).grid(row=linha, column=0)
        tk.Label(consulta_janela, text=valor).grid(row=linha, column=1)
        tk.Label(consulta_janela, text=vencimento).grid(row=linha, column=2)
        tk.Label(consulta_janela, text=email).grid(row=linha, column=3)

def atualizar():
    # Pegar dados do formulário
    nome_antigo = nome_antigo_entry.get()
    nome_novo = nome_novo_entry.get()
    valor_novo = valor_novo_entry.get()
    vencimento_novo = vencimento_novo_entry.get()

    # Ler dados do arquivo
    with open('irmaos.txt', 'r') as f:
        dados = f.readlines()

    # Atualizar dados no arquivo
    with open('irmaos.txt', 'w') as f:
        for dado in dados:
            nome, valor, vencimento, email = dado.strip().split(';')
            if nome == nome_antigo:
                nome = nome_novo
                valor = valor_novo
                vencimento = vencimento_novo
            f.write(f'{nome};{valor};{vencimento};{email}\n')

    # Limpar formulário
    nome_antigo_entry.delete(0, 'end')
    nome_novo_entry.delete(0, 'end')
    valor_novo_entry.delete(0, 'end')
    vencimento_novo_entry.delete(0, 'end')

def verificar_mensalidades():
    # Ler dados do arquivo
    with open('irmaos.txt', 'r') as f:
        dados = f.readlines()

    # Verificar mensalidades
    for dado in dados:
        nome, _, vencimento, email = dado.strip().split(';')
        data_vencimento = datetime.strptime(vencimento, '%d/%m/%Y').date()
        dias_restantes = (data_vencimento - hoje).days

        if dias_restantes <= 7:
            mensagem = f'A mensalidade do Irmão/Tio {nome}, no valor de R$ {_}, vencerá em {dias_restantes} dias.'
            enviar_email([email, 'e-mail_2'], mensagem)  

            # Adicionar um mês à data de vencimento
            nova_data_vencimento = data_vencimento + relativedelta(months=1)
            nova_data_vencimento_str = nova_data_vencimento.strftime('%d/%m/%Y')

            # Atualizar data de vencimento no arquivo
            with open('irmaos.txt', 'r') as f:
                linhas = f.readlines()
            
            with open('irmaos.txt', 'w') as f:
                for linha in linhas:
                    if vencimento in linha:
                        linha = linha.replace(vencimento, nova_data_vencimento_str)
                    f.write(linha)

def deletar():
    # Pegar nome do irmão a ser deletado
    nome_deletar = nome_deletar_entry.get()

    # Ler dados do arquivo
    with open('irmaos.txt', 'r') as f:
        dados = f.readlines()

    # Remover o irmão do arquivo
    with open('irmaos.txt', 'w') as f:
        for dado in dados:
            nome, _, _, _ = dado.strip().split(';')
            if nome != nome_deletar:
                f.write(f'{dado}')

    # Limpar formulário
    nome_deletar_entry.delete(0, 'end')

# Criar janela principal
root = tk.Tk()
root.title('Controle de Mensalidades')
root.geometry('500x740')

# Criar campos de entrada
fonte = tkfont.Font(family="Sans-Serif", weight="bold", size=10)
titulo_label = tk.Label(root, text='\nControle de Mensalidades Capítulo Alegre N° 463 - V1.0')
titulo_label.config(font=fonte)
titulo_label.pack()

descnome_label = tk.Label(root, text='____________________________________\nCadastrar irmãos:')
descnome_label.pack()
nome_label = tk.Label(root, text='Nome:')
nome_label.pack()
nome_entry = tk.Entry(root)
nome_entry.pack()

valor_label = tk.Label(root, text='Valor:')
valor_label.pack()
valor_entry = tk.Entry(root)
valor_entry.pack()

vencimento_label = tk.Label(root, text='Vencimento (dd/mm/aaaa):')
vencimento_label.pack()
vencimento_entry = tk.Entry(root)
vencimento_entry.pack()

email_label = tk.Label(root, text='Email:')
email_label.pack()
email_entry = tk.Entry(root)
email_entry.pack()

# Criar botões
cadastrar_button = tk.Button(root, text='Cadastrar', command=cadastrar)
cadastrar_button.pack()

descconsultar_label = tk.Label(root, text='____________________________________\nConsultar irmãos cadastrados:\n')
descconsultar_label.pack()
consultar_button = tk.Button(root, text='Consultar', command=consultar)
consultar_button.pack()

atualizar_label = tk.Label(root, text='____________________________________\nAtualização Cadastral:')
atualizar_label.pack()
nome_antigo_label = tk.Label(root, text='Nome Antigo:')
nome_antigo_label.pack()
nome_antigo_entry = tk.Entry(root)
nome_antigo_entry.pack()

nome_novo_label = tk.Label(root, text='Nome Novo:')
nome_novo_label.pack()
nome_novo_entry = tk.Entry(root)
nome_novo_entry.pack()

valor_novo_label = tk.Label(root, text='Valor Novo:')
valor_novo_label.pack()
valor_novo_entry = tk.Entry(root)
valor_novo_entry.pack()

vencimento_novo_label = tk.Label(root, text='Vencimento Novo (dd/mm/aaaa):')
vencimento_novo_label.pack()
vencimento_novo_entry = tk.Entry(root)
vencimento_novo_entry.pack()

atualizar_button = tk.Button(root, text='Atualizar', command=atualizar)
atualizar_button.pack()

deletar_label = tk.Label(root, text='____________________________________\nDeletar irmão:')
deletar_label.pack()
nome_deletar_label = tk.Label(root, text='Nome do irmão:')
nome_deletar_label.pack()
nome_deletar_entry = tk.Entry(root)
nome_deletar_entry.pack()

deletar_button = tk.Button(root, text='Deletar', command=deletar)
deletar_button.pack()

verificar_label = tk.Label(root, text='____________________________________\nVerificador de mensalidades:')
verificar_label.pack()
verificar_button = tk.Button(root, text='Enviar E-Mails', command=verificar_mensalidades)
verificar_button.pack()

# Iniciar aplicação
root.mainloop()