import sys
import os

"""Variáveis"""

userLogado = ""
cpfLogado = ""
usuarios = []
contas = []

saldo = 0
limite = 500
numero_saques = 0
LIMITE_SAQUES = 3

"""Funcoes"""
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def login(cpf, senha):    
    for usuario in usuarios:
        if usuario["cpf"] == cpf and usuario["senha"] == senha:
            userLogado = usuario["nome"]
            cpfLogado = usuario["cpf"]
            menu2(userLogado, cpfLogado)
        else:
            print("Tente novamente!")
            menu1()

def cadastrar_usuario(nome, cpf, data_nascimento, endereco, senha):
    usuarios.append({"nome":nome, "cpf":cpf, "data_nascimento":data_nascimento, "endereco":endereco, "senha":senha})
    print(usuarios)

def depositar (userLogado, cpfLogado, saldo, valor, extrato, conta): 
    
    if valor > 0:
        saldo += valor
        extrato += f"\n\n{userLogado} - {cpfLogado} - {conta}\n\nDepósito: R$ {valor:.2f}\n"

    else:
        print("Operação falhou! O valor informado é inválido.")
        
    return saldo, extrato

def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    
    excedeu_saldo = valor > saldo

    excedeu_limite = valor > limite

    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")

    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1

    else:
        print("Operação falhou! O valor informado é inválido.")
    
    return saldo, extrato, numero_saques

def extratoFunc(saldo, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

"""Menu 1"""
def menu1():
    menu = """
    
    #### Banco ####
    
    [1] Acessar conta
    [2] Cadastrar usuário
    [3] Sair

    => """
    
    limpar_tela()
    op = int(input(menu))
    
    if op == 1:
        cpf = input("Insira seu cpf: ")
        senha = input("Insira sua senha: ")
        login(cpf, senha)
        
    elif op == 2:
        cpf = input("Digite o cpf: ")
        for usuario in usuarios:
            if usuario["cpf"] == cpf:
                print("CPF já cadastrado!")
                menu1()
            
        nome = input("Digite o nome: ")
        data_nascimento = input("Digite a data de nascimento: ")
        endereco = input("Digite o endereco (logradouro, nro - bairro - cidade/sigla estado): ")
        senha = input("Digite sua senha: ")
        
        cadastrar_usuario(nome, cpf, data_nascimento, endereco, senha)
        menu1()
    
    elif op == 3:
        sys.exit("Até logo!")

def menu2(userLogado, cpfLogado):
    
    menu = f"""

    Bem vindo {userLogado}

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [c] Criar conta corrente
    [q] Sair

    => """
    
    #limpar_tela()
    opcao = input(menu)
    
    if opcao == "d":
        
        contas2 = [conta for conta in contas if conta["cpf"] == cpfLogado]
        
        if len(contas2) > 0:
            for i, conta in enumerate(contas):
                if conta["cpf"] == cpfLogado:
                    print(f"Opção: {i}: Número da conta: {conta["numero_conta"]}")
            op = int(input("Escolha uma conta: "))
            print(contas[op]["saldo"])
            saldo = contas[op]["saldo"]
            valor = float(input("Informe o valor do depósito: "))
            extrato = contas[op]["extrato"]
            numero_conta = contas[op]["numero_conta"]
            dados = depositar(userLogado, cpfLogado, saldo, valor, extrato, numero_conta)
            contas[op]["saldo"] = dados[0]
            contas[op]["extrato"] = dados[1]
            
            menu2(userLogado, cpfLogado)
            
        else:
            print("Nenhuma conta encontrada. Crie uma conta.")
            menu2(userLogado, cpfLogado)

    elif opcao == "s":
        
        contas2 = [conta for conta in contas if conta["cpf"] == cpfLogado]
        
        if len(contas2) > 0:
            for i, conta in enumerate(contas):
                if conta["cpf"] == cpfLogado:
                    print(f"Opção: {i}: Número da conta: {conta["numero_conta"]}")
            op = int(input("Escolha uma conta: "))
            print(contas[op]["saldo"])
            saldo = contas[op]["saldo"]
            valor = float(input("Informe o valor do saque: "))
            extrato = contas[op]["extrato"]
            numero_conta = contas[op]["numero_conta"]
            numero_saques = contas[op]["numero_saques"]
            dados = saque(saldo=saldo, valor=valor, extrato=extrato, 
                  limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)
            contas[op]["saldo"] = dados[0]
            contas[op]["extrato"] = dados[1]
            contas[op]["numero_saques"] = dados[2]
            
            print(contas[op]["extrato"])
            menu2(userLogado, cpfLogado)
            
            
        else:
            print("Nenhuma conta encontrada. Crie uma conta.")
            menu2(userLogado, cpfLogado)
        

    elif opcao == "e":
        
        contas2 = [conta for conta in contas if conta["cpf"] == cpfLogado]
        
        if len(contas2) > 0:
            for i, conta in enumerate(contas):
                if conta["cpf"] == cpfLogado:
                    print(f"Opção: {i}: Número da conta: {conta["numero_conta"]}")
            op = int(input("Escolha uma conta: "))
            print(contas[op]["saldo"])
            saldo = contas[op]["saldo"]
            extrato = contas[op]["extrato"]
            
            extratoFunc(saldo, extrato=extrato)
            
            print(contas[op]["extrato"])
            menu2(userLogado, cpfLogado)
            
        else:
            print("Nenhuma conta encontrada. Crie uma conta.")
            menu2(userLogado, cpfLogado)

    elif opcao == "c":
        if len(userLogado) == 0:
            print("Faça login primeiro!")
            menu1()
        else:
            numero_conta = len(contas) + 1
            contas.append({"agencia":"0001", "numero_conta":numero_conta, "cpf":cpfLogado, "nome":userLogado, "saldo":0, "extrato":"", "numero_saques":0})
            print(f"Conta: 0001 - {numero_conta} de {userLogado} foi criada com sucesso!")
            menu2(userLogado, cpfLogado)
            
    elif opcao == "q":
        userLogado=""
        cpfLogado=""
        limpar_tela()
        menu1()

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")

menu1()
 