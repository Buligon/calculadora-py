from Calculadora import Calculadora
import tkinter as tk

BT_TAMANHO_W = 9
BT_TAMANHO_H = 4

operacao = {
    'num1': '',
    'num2': '',
    'operacao': '',
    'resultado': ''
}

calc = Calculadora()


def btn_click_num(valor):
    if (operacao['resultado'] != ''):
        limpa_mostrador()
    if (operacao['operacao'] == ''):
        operacao['num1'] += valor
    else:
        operacao['num2'] += valor

    atualiza_mostrador()


def btn_click_op(op):
    if (operacao['num1'] == '' and op == '-'):  # número negativo
        operacao['num1'] += '-'
    elif (operacao['operacao'] != '' and '-' not in operacao['num2'] and operacao['num2'] == ''):
        operacao['num2'] += '-'
    elif (operacao['num1'] == ''):  # tenta adicionar * + / antes de inserir um número
        return
    else:
        operacao['operacao'] = op

    atualiza_mostrador()


def mostra_resultado():
    operacao['resultado'] = str(calc.executa_operacao(operacao['num1'], operacao['num2'], operacao['operacao']))
    if (operacao['resultado'] == ''):
        return
    atualiza_mostrador()


def inicializar_janela_historico():
    janela_historico = tk.Tk()
    janela_historico.title("Histórico")
    janela_historico.geometry("200x200")  # Largura x Altura
    janela_historico.iconbitmap("calculator.ico")

    return janela_historico


def mostra_historico():
    janela_historico = inicializar_janela_historico()

    def fecha_historico(event):
        janela_historico.destroy()

    if (len(Calculadora.historico) == 0):
        hist = tk.Label(janela_historico, text='Histórico vazio')
        hist.pack()

    for op in Calculadora.historico:
        operacao = ''.join(map(str, op))
        operacao = operacao.replace(str(op[3]), '=' + str(op[3]))
        hist = tk.Label(janela_historico, text=operacao)
        hist.pack()

    janela_historico.bind('<Escape>', fecha_historico)

    janela_historico.mainloop()


def atualiza_mostrador():
    if (operacao['resultado'] != ''):
        conta = operacao['resultado']
        limpa_mostrador()
        operacao['num1'] = conta
    else:
        conta = operacao['num1'] + operacao['operacao'] + operacao['num2']

    label = frame_campo.winfo_children()
    label[1].configure(text=conta)


def limpa_mostrador():
    for key in operacao:
        operacao[key] = ''

    label = frame_campo.winfo_children()
    label[1].configure(text='')


def backspace():
    if (operacao['resultado'] != ''):
        limpa_mostrador()
    elif (operacao['operacao'] != '' and operacao['num2'] == ''):  # apaga operador
        operacao['operacao'] = ''
    elif (operacao['operacao'] == ''):  # apaga num 1
        operacao['num1'] = operacao['num1'][:-1]
    else:
        operacao['num2'] = operacao['num2'][:-1]  # apaga num 2
    atualiza_mostrador()


def botao_ponto():
    if (operacao['operacao'] == ''):  # valida se é o primeiro ou segundo número
        if ('.' not in operacao['num1']):  # valida se já não tem ponto
            if (operacao['num1'] == ''):  # valida se já foi inserido algum número (opcional)
                operacao['num1'] += '0.'
            else:
                operacao['num1'] += '.'
    else:
        if ('.' not in operacao['num2']):  # valida se já não tem ponto
            if (operacao['num2'] == ''):  # valida se já foi inserido algum número (opcional)
                operacao['num2'] += '0.'
            else:
                operacao['num2'] += '.'
    atualiza_mostrador()


def keybinds(event):
    if event.char == '.' or event.char == ',':
        botao_ponto()
    elif event.keysym == 'BackSpace':
        backspace()
    elif event.keysym == 'Escape':
        limpa_mostrador()
    elif event.char == 'h':
        mostra_historico()
    elif event.keysym == 'Return':
        mostra_resultado()
    elif event.char in ['-', '+', '/', '*']:
        btn_click_op(event.char)
    else:
        btn_click_num(event.char)


def inicializar_janela():
    # Criação da janela principal
    janela = tk.Tk()
    janela.geometry("290x410")  # Largura x Altura
    janela.resizable(False, False)  # Não redimensionável
    janela.iconbitmap("calculator.ico")
    janela.title('Calculadora')
    return janela


def criar_botoes():
    # Criação do frame para os botões
    frame_botoes = tk.Frame(janela)
    frame_botoes.grid(row=1, column=0, columnspan=5)

    # Criação dos botões
    num = 1
    for i in range(1, 4):
        for j in range(1, 4):
            btn = tk.Button(frame_botoes, text=str(num), command=lambda num=num: btn_click_num(str(num)), width=BT_TAMANHO_W,
                            height=BT_TAMANHO_H)
            btn.grid(row=i, column=j)
            janela.bind(str(num), keybinds)  # inicializa atalhos de teclado
            num += 1

    operacoes = ['+', '-', '/', '*']

    for i in range(0, 4):
        btn = tk.Button(frame_botoes, text=operacoes[i], command=lambda i=operacoes[i]: btn_click_op(i), width=BT_TAMANHO_W,
                        height=BT_TAMANHO_H)
        janela.bind(operacoes[i], keybinds)  # inicializa atalhos de teclado
        btn.grid(row=i + 1, column=4)

    # Botão '0'
    btn_zero = tk.Button(frame_botoes, text="0", command=lambda i=0: btn_click_num(str(i)), width=BT_TAMANHO_W, height=BT_TAMANHO_H)
    btn_zero.grid(row=4, column=2)
    janela.bind('0', keybinds)

    # Botão de igual (para mostrar o resultado)
    btn_igual = tk.Button(frame_botoes, text="=", command=mostra_resultado, width=BT_TAMANHO_W, height=BT_TAMANHO_H)
    btn_igual.grid(row=5, column=3, columnspan=2, sticky="ew")
    janela.bind('<Return>', keybinds)

    # Botão de limpar
    btn_limpar = tk.Button(frame_botoes, text="C", command=limpa_mostrador, width=BT_TAMANHO_W, height=BT_TAMANHO_H)
    btn_limpar.grid(row=4, column=3)
    janela.bind('<Escape>', keybinds)

    # Botão de backspace
    btn_backspace = tk.Button(frame_botoes, text="\u2190", command=backspace, width=BT_TAMANHO_W, height=BT_TAMANHO_H)
    btn_backspace.grid(row=5, column=1, columnspan=2, sticky="ew")
    janela.bind('<BackSpace>', keybinds)

    # Botão de ponto
    btn_ponto = tk.Button(frame_botoes, text=".", command=botao_ponto, width=BT_TAMANHO_W, height=BT_TAMANHO_H)
    btn_ponto.grid(row=4, column=1)
    janela.bind('.', keybinds)
    janela.bind(',', keybinds)

    return frame_botoes


def criar_mostrador():
    # Criação do frame para o campo de texto
    frame_campo = tk.Frame(janela)
    frame_campo.grid(row=0, column=0)

    # Botão de histórico
    btn_ponto = tk.Button(frame_campo, text="\u23F3", command=mostra_historico, width=BT_TAMANHO_W, height=3)
    btn_ponto.grid(row=0, column=0, sticky='w')
    janela.bind('h', keybinds)

    # Criação do campo de texto para exibir a entrada/saída
    campo_texto = tk.Label(frame_campo, text="0", height=2, width=23, font=2, padx=0)
    campo_texto.grid(row=0, column=1, columnspan=4, sticky='nsew')

    return frame_campo


janela = inicializar_janela()

frame_campo = criar_mostrador()
frame_botoes = criar_botoes()

# Iniciar o loop de eventos da interface gráfica
janela.mainloop()
