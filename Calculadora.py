class Calculadora:
    historico = []

    def __init__(self):
        self.__operacoes = [
            {'-': lambda a, b: a - b},
            {'+': lambda a, b: a + b},
            {'*': lambda a, b: a * b},
            {'/': lambda a, b: a / b}
        ]

    def executa_operacao(self, a, b, op_escolhida):
        if (a == '' or b == ''):
            return ''

        num_a = int(''.join(map(str, a))) if '.' not in a else float(''.join(map(str, a)))
        num_b = int(''.join(map(str, b))) if '.' not in b else float(''.join(map(str, b)))

        if (num_b == 0 and op_escolhida == '/'):
            return 'Resultado indefinido'

        resultado = None

        for op_dict in self.__operacoes:
            if op_escolhida in op_dict:
                resultado = op_dict[op_escolhida](num_a, num_b)
                break

        if resultado is None:
            return 'Operação inválida'

        self.historico.append([num_a, op_escolhida, num_b, resultado])
        return resultado
