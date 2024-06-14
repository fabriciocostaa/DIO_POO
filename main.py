from abc import ABC, abstractmethod
from datetime import datetime

class Conta:

    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente 
        self._historico = Historico()

    @property
    def cliente(self):
        return self._cliente
    @property
    def historico(self):
        return self._historico   
    @property
    def numero(self):   
        return self._numero
    @property
    def agencia(self):
        return self._agencia    
    @property
    def saldo(self)->float:
        return self._saldo
      
    def sacar(self, valor):
        if valor > 0 and valor <= self._saldo:
            self._saldo -= valor
            print(f"Saque de {valor} realizado com sucesso.")
            return True
        else:
            print("Saldo insuficiente ou valor inválido.")
            return False

    def depositar(self, valor)->bool:
        if valor > 0:
            self._saldo += valor
            return True
        else:
            return False
            
    @classmethod
    def nova_conta(cls, cliente, numero: int):
        return cls(numero, cliente)
    
class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

   
class Transacao(ABC):

    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor 

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        if conta.sacar(self.valor): 
            conta.historico.adicionar_transacao(self)

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, numero_saques=0, limite_saque=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saque = limite_saque
        self._numero_saques = numero_saques

    def sacar(self, valor):
        excedeu_limite = valor > self._limite
        excedeu_saques = self._numero_saques >= self._limite_saque  # Ajustar para >=

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        else:
            if super().sacar(valor):
                self._numero_saques += 1  # Incrementar o contador de saques apenas quando o saque é bem-sucedido
                return True
        return False

    def __str__(self):
        return f"""
        Agência: \t{self.agencia}
        C/C:\t\t{self.numero}
        Titular:\t{self.cliente._nome}
        """
        
