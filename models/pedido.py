class Pedido:

    def __init__(
        self,
        codigo,
        cliente,
        telefone,
        produto,
        quantidade,

        valor,
        custo,

        desconto_tipo,
        desconto_valor,

        valor_final,
        lucro,

        origem,
        status,
        data_criacao
    ):
        self.codigo = codigo
        self.cliente = cliente
        self.telefone = telefone
        self.produto = produto
        self.quantidade = quantidade

        self.valor = valor
        self.custo = custo

        self.desconto_tipo = desconto_tipo
        self.desconto_valor = desconto_valor

        self.valor_final = valor_final
        self.lucro = lucro

        self.origem = origem
        self.status = status
        self.data_criacao = data_criacao

class PedidoItem:

    def __init__(
        self,
        produto,
        quantidade,
        valor_unitario,
        custo_unitario,
        desconto_tipo=None,
        desconto_valor=0
    ):
        self.produto = produto
        self.quantidade = quantidade
        self.valor_unitario = valor_unitario
        self.custo_unitario = custo_unitario
        self.desconto_tipo = desconto_tipo
        self.desconto_valor = desconto_valor

        self.valor_final = self.calcular_valor_final()
        self.lucro = self.calcular_lucro()

    def calcular_valor_final(self):
        valor = self.valor_unitario

        if self.desconto_tipo == "Valor Fixo":
            valor -= self.desconto_valor

        elif self.desconto_tipo == "Percentual":
            valor -= (valor * self.desconto_valor / 100)

        return max(0, valor)

    def calcular_lucro(self):
        return (self.valor_final - self.custo_unitario) * self.quantidade