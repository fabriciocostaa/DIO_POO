import textwrap
from main import Conta, Cliente, PessoaFisica, Historico, Transacao, Deposito, Saque, ContaCorrente

def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [c]\tCriar Cliente
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def filtrar_cliente(cpf, clientes:list):
    clientes_filtrados = [cliente for cliente in clientes if cliente._cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente._contas:
        print("@@@ Cliente não possui conta. @@@")
        return 

    return cliente._contas[0]

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Digite o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

def listar_contas(contas):
  
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def criar_clientes(clientes):
    cpf = input("Digite o CPF do cliente: ")
    cliente= filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Cliente já cadastrado.@@@")
        return
    
    nome= input("Digite o nome do cliente: ")
    data_nascimento = input("Digite a data de nascimento do cliente: ")
    endereco = input("Digite o endereço do cliente: ")
    cliente = PessoaFisica(nome= nome, cpf= cpf, data_nascimento= data_nascimento, endereco= endereco)
    clientes.append(cliente)

    print("\n=== Cliente cadastrado com sucesso.===")

def criar_conta(clientes, numero_conta, contas):

    cpf = input("Digite o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return
    
    nova_conta = ContaCorrente.nova_conta(cliente =cliente, numero= numero_conta)
    contas.append(nova_conta)
    cliente._contas.append(nova_conta)
    
    print("\n=== Conta criada com sucesso.===")

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ NÃO FOI POSSIVEL FAZER O SAQUE, CPF NAO ENCONTRADO! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == 'e':
            exibir_extrato(clientes)

        elif opcao == 'c': 
            criar_clientes(clientes)

        elif opcao == 'nc':
            numero_contas = len(contas) + 1
            criar_conta(clientes, numero_contas, contas)

        elif opcao == 's':
            sacar(clientes)

        elif opcao == 'q':
            break 

        elif opcao == "lc":
            listar_contas(contas)
main() 