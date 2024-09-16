import numpy as np
import sympy as sp
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Definir las funciones disponibles
def f_sin(x):
    return np.sin(x)

def f_cos(x):
    return np.cos(x)

def f_exp(x):
    return np.exp(x)

def f_ln(x):
    return np.log(x)

def f_tan(x):
    return np.tan(x)

# Diccionario con funciones
funciones = {
    'sin(x)': f_sin,
    'cos(x)': f_cos,
    'exp(x)': f_exp,
    'ln(x)': f_ln,
    'tan(x)': f_tan,
}

# Serie de Taylor usando sympy
def serie_taylor(funcion, x0, n, x):
    taylor = sum((funcion.diff(x, i).subs(x, x0) * (x - x0)**i / sp.factorial(i)) for i in range(n))
    return taylor

# Función para graficar la serie de Taylor
def graficar():
    # Definir la variable simbólica x
    x = sp.symbols('x')

    # Obtener valores de entrada
    funcion_str = funcion_seleccionada.get()
    x0 = float(entry_x0.get())
    n = int(entry_n.get())
    
    # Selección de la función
    nombre_funcion = funcion_str
    funcion_numpy = funciones[nombre_funcion]
    funcion_sympy = sp.sympify(nombre_funcion)

    # Generar la serie de Taylor
    taylor_approx = serie_taylor(funcion_sympy, x0, n, x)
    taylor_func = sp.lambdify(x, taylor_approx, "numpy")

    # Valores de x para la gráfica
    x_vals = np.linspace(x0 - 10, x0 + 10, 400)

    # Crear la figura de matplotlib
    fig, ax = plt.subplots(figsize=(5, 4))
    
    # Graficar la función original y la aproximación de Taylor
    ax.plot(x_vals, funcion_numpy(x_vals), label=f"Original {nombre_funcion}")
    ax.plot(x_vals, taylor_func(x_vals), label=f"Taylor (n={n})", linestyle="--")

    # Configuración de la gráfica
    ax.axvline(x0, color='gray', linestyle='--', label=f"Expansión en x0={x0}")
    ax.set_title(f"Serie de Taylor de {nombre_funcion}")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.legend()
    ax.grid(True)

    # Limpiar el canvas anterior si existe
    for widget in frame_grafica.winfo_children():
        widget.destroy()

    # Mostrar la figura en el canvas de tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Expansión en series de Taylor")

# Etiquetas y campos de entrada
ttk.Label(root, text="Selecciona la función:").grid(row=0, column=0, padx=10, pady=5)
funcion_seleccionada = tk.StringVar()
funcion_menu = ttk.Combobox(root, textvariable=funcion_seleccionada)
funcion_menu['values'] = list(funciones.keys())
funcion_menu.grid(row=0, column=1, padx=10, pady=5)
funcion_menu.current(0)

ttk.Label(root, text="Punto de expansión (x0):").grid(row=1, column=0, padx=10, pady=5)
entry_x0 = ttk.Entry(root)
entry_x0.grid(row=1, column=1, padx=10, pady=5)
entry_x0.insert(0, "0")

ttk.Label(root, text="Cantidad de términos (n):").grid(row=2, column=0, padx=10, pady=5)
entry_n = ttk.Entry(root)
entry_n.grid(row=2, column=1, padx=10, pady=5)
entry_n.insert(0, "5")

# Botón para graficar
boton_graficar = ttk.Button(root, text="Graficar", command=graficar)
boton_graficar.grid(row=3, column=0, columnspan=2, pady=10)

# Frame para colocar la gráfica
frame_grafica = ttk.Frame(root)
frame_grafica.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

# Configurar el tamaño del frame de la gráfica
root.columnconfigure(1, weight=1)
root.rowconfigure(4, weight=1)

# Iniciar la ventana
root.mainloop()
