from datetime import datetime  # >>> NOVO: importa a data e hora atual do sistema

clientes = []  # >>> NOVO: lista para armazenar os cadastros dos clientes

def cadastrar_cliente():
    print("\n=== Cadastro de Cliente ===")
    cpf = input("Informe o CPF (Somente números): ")

    # >>> NOVO: verifica se o CPF já está cadastrado
    cliente_existente = next((c for c in clientes if c["cpf"] == cpf), None)
    if cliente_existente:
        print("CPF já cadastrado! Tente outro.")
        return

    nome = input("Informe o nome completo: ")
    nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")

    # >>> NOVO: validação da senha com 8 dígitos numéricos
    while True:
        senha = input("Crie uma senha de 8 dígitos: ")
        if len(senha) == 8 and senha.isdigit():
            break
        print("Senha inválida. Digite exatamente 8 números.")

    # >>> NOVO: cria o dicionário do cliente com informações e saldo inicial
    cliente = {
        "cpf": cpf,
        "nome": nome,
        "nascimento": nascimento,
        "senha": senha,
        "saldo": 0,
        "extrato": "",
        "saques": 0
    }
    clientes.append(cliente)
    print(f"Cliente {nome} cadastrado com sucesso!")

def login():
    print("\n=== Login ===")
    cpf = input("CPF: ")
    senha = input("Senha (8 dígitos): ")

    # >>> NOVO: valida o CPF e senha para autenticação
    for cliente in clientes:
        if cliente["cpf"] == cpf and cliente["senha"] == senha:
            print(f"\nBem-vindo(a), {cliente['nome']}!")
            return cliente

    print("CPF ou senha incorretos.")
    return None

def menu_transacoes(cliente):
    menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

Digite a opção desejada => """

    LIMITE_SAQUES = 3
    LIMITE_SAQUE_VALOR = 500

    while True:
        opcao = input(menu)

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))

            if valor > 0:
                cliente["saldo"] += valor
                # >>> NOVO: adiciona data e hora no extrato do depósito
                data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                cliente["extrato"] += f"Depósito: R$ {valor:.2f} | {data_hora}\n"
                print("Deposito realizado com sucesso.")
            else:
                print("Operação falhou! O valor informado é inválido.")

        elif opcao == "s":
            entrada = input("Informe o valor do saque: ")

            # >>> NOVO: valida se o valor é inteiro e positivo (sem vírgula ou ponto)
            if not entrada.isdigit():
                print("Valor inválido! Digite um valor inteiro sem vírgulas ou pontos")
                continue

            valor = int(entrada)

            if valor > cliente["saldo"]:
                print("Operação falhou! Você não tem saldo suficiente.")

            elif valor > LIMITE_SAQUE_VALOR:
                print("Operação falhou! O valor do saque excede o limite.")

            elif cliente["saques"] >= LIMITE_SAQUES:
                print("Operação falhou! Número máximo de saques excedido.")

            elif valor > 0:
                cliente["saldo"] -= valor
                # >>> NOVO: adiciona data e hora no extrato do saque
                data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                cliente["extrato"] += f"Saque: R$ {valor:.2f} | {data_hora}\n"
                cliente["saques"] += 1
                print("Saque realizado com sucesso")
            else:
                print("Operação falhou! O valor informado é inválido.")

        elif opcao == "e":
            print("\n================ EXTRATO ================")
            # >>> CORRIGIDO: imprime o extrato real, não uma string fixa
            print("Não foram realizadas movimentações." if not cliente["extrato"] else cliente["extrato"])
            print(f"\nSaldo: R$ {cliente['saldo']:.2f}")
            print("==========================================")

        elif opcao == "q":
            print("Encerrando sessão...")
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

# ======== PROGRAMA PRINCIPAL ========
while True:
    print("""
====== MENU PRINCIPAL ======
[1] Cadastrar cliente
[2] Fazer login
[0] Sair
""")
    escolha = input("Escolha uma opção => ")

    if escolha == "1":
        cadastrar_cliente()
    elif escolha == "2":
        cliente_logado = login()
        if cliente_logado:
            menu_transacoes(cliente_logado)
    elif escolha == "0":
        print("Encerrando o sistema...")
        break
    else:
        print("Opção inválida.")
