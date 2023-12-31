import toga
from toga.style import Pack
from toga.style.pack import COLUMN

import sympy as sp

def f(x, y, expressao):
    return expressao.subs({sp.Symbol('x'): x, sp.Symbol('y'): y})

def runge_kutta(x0, y0, h, nfinal, expressao):
    print(f"x0: {x0}, y0: {y0}, h: {h}, nfinal: {nfinal}")
    valores_x = [x0] * (nfinal + 1)
    valores_y = [y0] * (nfinal + 1)

    for i in range(1, nfinal +1):
        x_val = valores_x[i - 1]
        y_val = valores_y[i - 1]

        k1 = h * f(x_val, y_val, expressao)
        k2 = h * f(x_val + h/2, y_val + k1/2, expressao)
        k3 = h * f(x_val + h/2, y_val + k2/2, expressao)
        k4 = h * f(x_val + h, y_val + k3, expressao)

        valores_x[i] = x_val + h
        valores_y[i] = y_val + (k1 + 2*k2 + 2*k3 + k4) / 6

    return valores_x, valores_y

def on_calcular_button(widget, expressao_input, y0_input, x0_input, h_input, nfinal_input, resultado_label):
    print("Função on_calcular_button executada")
    expressao_str = expressao_input.value
    y0 = float(y0_input.value)
    x0 = float(x0_input.value)
    h = float(h_input.value)
    nfinal = int(nfinal_input.value)


    expressao = sp.sympify(expressao_str)  # Converte a expressão em um objeto do SymPy

    valores_x, valores_y = runge_kutta(x0, y0, h, nfinal, expressao)

    # Convertendo os resultados para strings
    valores_x_str = ', '.join(map(str, valores_x))
    valores_y_str = ', '.join(map(str, valores_y))

    # Exibindo os resultados na interface gráfica
    valores_x_str = ", ".join([f"{x_val:.4f}" for x_val in valores_x])
    valores_y_str = ", ".join([f"{y_val:.4f}" for y_val in valores_y])

    resultado_label.text = f"Valores de x: {valores_x_str}\nValores de y: {valores_y_str}"


def build(app):
    expressao_label = toga.Label("Digite a expressão:", style=Pack(padding=5))
    expressao_input = toga.TextInput(style=Pack(flex=1, padding=5))

    x0_label = toga.Label("x0:", style=Pack(padding=5))
    x0_input = toga.TextInput(style=Pack(padding=5))

    y0_label = toga.Label("y0:", style=Pack(padding=5))
    y0_input = toga.TextInput(style=Pack(padding=5))

    h_label = toga.Label("h:", style=Pack(padding=5))
    h_input = toga.TextInput(style=Pack(padding=5))

    nfinal_label = toga.Label("n_final:", style=Pack(padding=5))
    nfinal_input = toga.TextInput(style=Pack(padding=5))

    calcular_button = toga.Button("Calcular",
                                  on_press=lambda widget: on_calcular_button(widget, expressao_input, y0_input,
                                                                             x0_input, h_input, nfinal_input,
                                                                             resultado_label), style=Pack(padding=5))

    resultado_label = toga.Label("", style=Pack(padding=5))

    box = toga.Box(
        children=[
            expressao_label, expressao_input,
            x0_label, x0_input,
            y0_label, y0_input,
            h_label, h_input,
            nfinal_label, nfinal_input,
            calcular_button,
            resultado_label
        ],
        style=Pack(direction=COLUMN, padding=10)
    )

    return box

def main():
    app = toga.App("Runge-Kutta com Toga", "org.example.rungekutta", startup=build)
    app.main_loop()

if __name__ == '__main__':
    main()
