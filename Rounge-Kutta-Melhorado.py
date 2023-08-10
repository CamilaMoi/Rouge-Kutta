import toga
from toga.style import Pack
from toga.style.pack import COLUMN

import sympy as sp

x = sp.symbols('x')

def f(x, y, z):
    return z

def g(x, y, z, expressao):
    return expressao.subs({sp.Symbol('x'): x, sp.Symbol('y'): y, sp.Symbol('z'): z})

def runge_kutta(x0, y0, z0, h, nfinal, expressao):
    valores_x = [x0] * (nfinal + 1)
    valores_y = [y0] * (nfinal + 1)
    valores_z = [z0] * (nfinal + 1)

    for i in range(1, nfinal + 1):
        x_val = valores_x[i - 1]
        y_val = valores_y[i - 1]
        z_val = valores_z[i - 1]

        k1y = h * f(x_val, y_val, z_val)
        k1z = h * g(x_val, y_val, z_val, expressao)

        k2y = h * f(x_val + h/2, y_val + k1y/2, z_val + k1z/2)
        k2z = h * g(x_val + h/2, y_val + k1y/2, z_val + k1z/2, expressao)

        k3y = h * f(x_val + h/2, y_val + k2y/2, z_val + k2z/2)
        k3z = h * g(x_val + h/2, y_val + k2y/2, z_val + k2z/2, expressao)

        k4y = h * f(x_val + h, y_val + k3y, z_val + k3z)
        k4z = h * g(x_val + h, y_val + k3y, z_val + k3z, expressao)

        valores_x[i] = x_val + h
        valores_y[i] = y_val + (k1y + 2*k2y + 2*k3y + k4y) / 6
        valores_z[i] = z_val + (k1z + 2*k2z + 2*k3z + k4z) / 6

    return valores_x, valores_y, valores_z

def on_calcular_button(widget, expressao_input, y0_input, x0_input, h_input, nfinal_input, resultado_label):
    expressao_str = expressao_input.value
    y0 = float(y0_input.value)
    x0 = float(x0_input.value)
    h = float(h_input.value)
    nfinal = int(nfinal_input.value)

    expressao = sp.sympify(expressao_str)

    z0 = sp.Derivative(y0, x).doit().subs(x, x0)  # Calcula a derivada inicial z(0)

    valores_x, valores_y, valores_z = runge_kutta(x0, y0, z0, h, nfinal, expressao)

    resultado_label.text = f"Valores de x: {valores_x}\nValores de y: {valores_y}\nValores de z: {valores_z}"

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
