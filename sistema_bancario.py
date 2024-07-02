from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

# Classe Cliente representa um cliente do banco
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    # Método para realizar uma transação em uma conta específica
    def realizar_transacao(self, conta, Transacao):
        Transacao.registrar(conta)

    # Método para adicionar uma conta ao cliente
    def adicionar_conta(self, conta):
        self.contas.append(conta)

# Classe PessoaFisica herda de Cliente, representando uma pessoa física
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

# Classe Conta representa uma conta bancária genérica
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = '0001'
        self._cliente = cliente
        self._historico = Historico()

    # Método de classe para criar uma nova conta
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    # Propriedades para acesso aos atributos privados
    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    # Método para sacar dinheiro da conta
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print('\nOperação falhou! Você não tem saldo suficiente.')
        elif valor > 0:
            self._saldo -= valor
            print('\nSaque realizado com sucesso!')
            return True
        else:
            print('\nOperação falhou! O valor informado é inválido.')

        return False

    # Método para depositar dinheiro na conta
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print('Depósito realizado com sucesso!')
            return True
        else:
            print('Operação falhou! O valor informado é inválido.')

        return False

# Classe ContaCorrente herda de Conta, representando uma conta corrente
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saque=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saque = limite_saque

    # Método sobrescrito para saque, considerando limites de saque e número de saques
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.trasacoes if transacao['tipo'] == Saque.__name__]
        )
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saque 

        if excedeu_limite:
            print('\nOperação falhou! O valor do saque excedeu o limite.')
        elif excedeu_saques:
            print('\nOperação falhou! Número máximo de saques excedido.')
        else:
            return super().sacar(valor)

        return False

    # Método para representação em string da conta corrente
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

# Classe Historico para registrar transações
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def trasacoes(self):
        return self._transacoes

    # Método para adicionar uma transação ao histórico
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                'tipo': transacao.__class__.__name__,
                'valor': transacao.valor,
                'data': datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            }
        )

# Classe abstrata Transacao
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

# Classe Saque, herda de Transacao, representa uma transação de saque
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    # Método para registrar a transação de saque
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

# Classe Deposito, herda de Transacao, representa uma transação de depósito
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    # Método para registrar a transação de depósito
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
