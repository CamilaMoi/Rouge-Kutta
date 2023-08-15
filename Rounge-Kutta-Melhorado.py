import toga
from toga.style import Pack
from toga.style.pack import COLUMN

import sympy as sp

x = sp.symbols('x')
y = sp.Function('y')(x)
z = sp.Function('z')(x)

def f(x_val, y_val, z_val):
    return y_val, x_val

def g(x_val, y_val, z_val, expressao):
    edo_reduzida = expressao.subs({y: y_val, x: x_val, y.diff(x): z, y.diff(x, x): z.diff(x)})
    return edo_reduzida

def runge_kutta(x0, y0, z0, h, nfinal, expressao):
    print(f"x0: {x0}, y0: {y0}, h: {h}, nfinal: {nfinal}")
    valores_x = [x0] * (nfinal + 1)
    valores_y = [y0] * (nfinal + 1)
    valores_z = [z0] * (nfinal + 1)
    for i in range(1, nfinal + 1):
        x_val = valores_x[i - 1]
        y_val = valores_y[i - 1]
        z_val = valores_z[i - 1]


        x0=x0+h
        k1y = h * f(x_val, y_val, z_val)[1]
        k2y = h * f(x_val + h / 2, y_val + k1y / 2, z_val + k1y / 2)[1]
        k3y = h * f(x_val + h / 2, y_val + k2y / 2, z_val + k2y / 2)[1]
        k4y = h * f(x_val + h, y_val + k3y, z_val + k3y)[1]

        k1z = h * g(x0, z_val,y_val, expressao)
        k2z = h * g(x0 + h / 2, z_val + k1z / 2, y_val + k1y / 2, expressao)
        k3z = h * g(x0 + h / 2, z_val + k2z / 2, y_val + k1y / 2, expressao)
        k4z = h * g(x0 + h, z_val + k3z, y_val + k1y / 2, expressao)

        valores_z[i] = z_val + (k1z + 2 * k2z + 2 * k3z + k4z) / 6
        valores_y[i] = y_val + (k1y + 2 * k2y + 2 * k3y + k4y) / 6
        valores_x[i] = x0


    return valores_x, valores_y, valores_z

def on_calcular_button(widget, x0_input, y0_input, z0_input, h_input, nfinal_input, expressao_input, resultado_label):
    x0 = float(x0_input.value)
    y0 = float(y0_input.value)
    z0 = float(z0_input.value)
    h = float(h_input.value)
    nfinal = int(nfinal_input.value)
    expressao_str = expressao_input.value
    expressao = sp.sympify(expressao_str)

    valores_x, valores_y, valores_z = runge_kutta(x0, y0, z0, h, nfinal, expressao)

    resultado_text = ""
    for i in range(nfinal + 1):
        resultado_text += f"x = {valores_x[i]:.1f}, y = {valores_y[i]:.3f}, z = {valores_z[i]:.3f}\n"
    resultado_label.text = resultado_text


def build(app):
    x0_label = toga.Label("x0:", style=Pack(padding=5))
    x0_input = toga.TextInput(style=Pack(padding=5))

    y0_label = toga.Label("y0:", style=Pack(padding=5))
    y0_input = toga.TextInput(style=Pack(padding=5))

    z0_label = toga.Label("z0:", style=Pack(padding=5))
    z0_input = toga.TextInput(style=Pack(padding=5))

    h_label = toga.Label("h:", style=Pack(padding=5))
    h_input = toga.TextInput(style=Pack(padding=5))

    nfinal_label = toga.Label("n_final:", style=Pack(padding=5))
    nfinal_input = toga.TextInput(style=Pack(padding=5))

    expressao_label = toga.Label("Digite a expressão:", style=Pack(padding=5))
    expressao_input = toga.TextInput(style=Pack(flex=1, padding=5))

    calcular_button = toga.Button("Calcular",
                                  on_press=lambda widget: on_calcular_button(widget, x0_input, y0_input, z0_input,
                                                                             h_input, nfinal_input, expressao_input,
                                                                             resultado_label), style=Pack(padding=5))

    resultado_label = toga.Label("", style=Pack(padding=5))

    box = toga.Box(
        children=[
            x0_label, x0_input,
            y0_label, y0_input,
            z0_label, z0_input,
            h_label, h_input,
            nfinal_label, nfinal_input,
            expressao_label, expressao_input,
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



'''import toga
from toga.style import Pack
from toga.style.pack import COLUMN

import sympy as sp

x = sp.symbols('x')
y = sp.Function('y')(x)
z = sp.Function('z')(x)

def g(val_x, z_val, expressao):
    edo_reduzida = expressao.subs({x: val_x, y.diff(x): z, y.diff(x, x): z.diff(x), z.diff(x):z_val})
    return edo_reduzida

def runge_kutta( x0, z0, h, nfinal, expressao):
    valores_x = [x0] * (nfinal + 1)
    valores_z = [z0] * (nfinal + 1)

    for i in range(1, nfinal + 1):
        z_val = valores_z[i - 1]
        val_x = valores_x[i-1]

        k1z = h/20 * g(val_x, z_val, expressao)
        k2z = h/20 * g(val_x + h / 2 , z_val + k1z / 2, expressao)
        k3z = h/20 * g(val_x + h / 2 , z_val + k2z / 2, expressao)
        k4z = h/20 * g(val_x + h , z_val + k3z, expressao)

        valores_z[i] = z_val + (k1z + 2 * k2z + 2 * k3z + k4z) / 6
        valores_x[i]=val_x+h
        #x0 = x0 + h

    return valores_x, valores_z

def on_calcular_button(widget, x0_input, z0_input, h_input, nfinal_input, expressao_input, resultado_label):
    x0 = float(x0_input.value)
    z0 = float(z0_input.value)
    h = float(h_input.value)
    nfinal = int(nfinal_input.value)
    expressao_str = expressao_input.value
    expressao = sp.sympify(expressao_str)

    valores_x, valores_z = runge_kutta(x0, z0, h, nfinal, expressao)

    resultado_text = ""
    for i in range(nfinal + 1):
        resultado_text += f"x = {valores_x[i]}, z = {valores_z[i]}\n"
    resultado_label.text = resultado_text

def build(app):
    x0_label = toga.Label("x0:", style=Pack(padding=5))
    x0_input = toga.TextInput(style=Pack(padding=5))

    z0_label = toga.Label("z0:", style=Pack(padding=5))
    z0_input = toga.TextInput(style=Pack(padding=5))

    h_label = toga.Label("h:", style=Pack(padding=5))
    h_input = toga.TextInput(style=Pack(padding=5))

    nfinal_label = toga.Label("n_final:", style=Pack(padding=5))
    nfinal_input = toga.TextInput(style=Pack(padding=5))

    expressao_label = toga.Label("Digite a expressão:", style=Pack(padding=5))
    expressao_input = toga.TextInput(style=Pack(flex=1, padding=5))

    calcular_button = toga.Button("Calcular",
                                  on_press=lambda widget: on_calcular_button(widget, x0_input, z0_input,
                                                                             h_input, nfinal_input, expressao_input,
                                                                             resultado_label), style=Pack(padding=5))

    resultado_label = toga.Label("", style=Pack(padding=5))

    box = toga.Box(
        children=[
            x0_label, x0_input,
            z0_label, z0_input,
            h_label, h_input,
            nfinal_label, nfinal_input,
            expressao_label, expressao_input,
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
    main()'''
