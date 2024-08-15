# import tkinter as tk
# import ply.lex as lex
# import ply.yacc as yacc
# import re
# import random
# from anytree import Node, RenderTree, AsciiStyle
# from treelib import Node as TreeNode, Tree
# import matplotlib.pyplot as plt
# from anytree.exporter import UniqueDotExporter
# from tkinter import scrolledtext
# from PIL import Image, ImageTk

# # Definición de tokens
# tokens = [
#     'NUMBER',
#     'CONVERSION',
#     'END'
# ]

# # Expresiones regulares para tokens
# t_CONVERSION = r'Hexadecimal|Octal|Binario|Romano|Duodecimal|Aleatorio'
# t_END = r'\$'

# def t_NUMBER(t):
#     r'\d+'
#     t.value = int(t.value)
#     t.lexer.lineno = t.lineno
#     return t

# # Ignorar espacios en blanco y saltos de línea
# t_ignore = ' \t\n'

# # Manejo de errores
# def t_error(t):
#     print("Error léxico: Caracter no válido '%s'" % t.value[0])
#     t.lexer.skip(1)

# # Construcción del analizador léxico
# lexer = lex.lex()

# # Definición de la gramática
# def p_expression(p):
#     '''expression : NUMBER CONVERSION END'''
#     p[0] = (p[1], p[2])

# # Manejo de errores sintácticos
# def p_error(p):
#     print("Error sintáctico en la entrada")

# # Construcción del analizador sintáctico
# parser = yacc.yacc()

# # Función para realizar la conversión a números romanos
# def decimal_to_roman(n):
#     val = [
#         1000, 900, 500, 400,
#         100, 90, 50, 40,
#         10, 9, 5, 4,
#         1
#     ]
#     syb = [
#         "M", "CM", "D", "CD",
#         "C", "XC", "L", "XL",
#         "X", "IX", "V", "IV",
#         "I"
#     ]
#     roman_num = ''
#     i = 0
#     while n > 0:
#         for _ in range(n // val[i]):
#             roman_num += syb[i]
#             n -= val[i]
#         i += 1
#     return roman_num

# # Función para realizar la conversión a binario
# def decimal_to_bin(n):
#     return bin(n)[2:]

# # Función para realizar la conversión a octal
# def decimal_to_oct(n):
#     return oct(n)[2:]

# # Función para realizar la conversión a hexadecimal
# def decimal_to_hex(n):
#     return hex(n)[2:].upper()

# # Función para realizar la conversión a duodecimal
# def decimal_to_duodecimal(n):    # n=decimal
#     if n == 0:
#         return "0"

#     duodecimal_digitos = "0123456789AB"  # Dígitos en duodecimal
#     duodecimal_resultado = ""

#     while n > 0:
#         remainder = n % 12
#         duodecimal_resultado = duodecimal_digitos[remainder] + duodecimal_resultado
#         n //= 12

#     return duodecimal_resultado


# # Función para realizar las conversiones
# def do_conversion(number, conversion):
#     if conversion == 'Binario':
#         return decimal_to_bin(number), conversion
#     elif conversion == 'Octal':
#         return decimal_to_oct(number), conversion
#     elif conversion == 'Hexadecimal':
#         return decimal_to_hex(number), conversion
#     elif conversion == 'Romano':
#         return decimal_to_roman(number), conversion
#     elif conversion == 'Duodecimal':
#         return decimal_to_duodecimal(number), conversion
#     elif conversion == 'Aleatorio':
#         conversion_options = ['Binario', 'Octal', 'Hexadecimal', 'Romano', 'Duodecimal']
#         chosen_conversion = random.choice(conversion_options)
#         result = do_conversion(number, chosen_conversion)
#     return result, chosen_conversion
    
# # Función para leer las cadenas desde un archivo
# def read_input_file(filename):
#     try:
#         with open(filename, 'r') as file:
#             lines = file.readlines()
#         return [line.strip() for line in lines]
#     except Exception as e:
#         print("Error al leer el archivo:", e)
#         return []

# # Función para procesar las conversiones y generar los resultados
# def process_conversions(input_strings):
#     results = []
#     for input_string in input_strings:
#         lexer.input(input_string)
#         tokens = []
#         while True:
#             tok = lexer.token()
#             if not tok:
#                 break
#             tokens.append(tok)
#         try:
#             parsed_data = parser.parse(input_string)
#             number, conversion = parsed_data
#             result, actual_conversion = do_conversion(number, conversion)
#             result_info = {
#                 "input_string": input_string,
#                 "result": result,
#                 "tokens": tokens,
#                 "actual_conversion": actual_conversion
#             }
#             results.append(result_info)
#         except Exception as e:
#             print("Error:", e)
#     return results

# # Función para mostrar los resultados en la interfaz
# def show_results():
#     input_strings = read_input_file("./input.txt")
#     conversion_results = process_conversions(input_strings)
#     output_text.config(state="normal")
#     output_text.delete("1.0", "end")

#     image_labels.clear()  # Limpiar las etiquetas de imagen anteriores

#     row = 2
#     col = 0

#     for result_info in conversion_results:
#         output_text.insert("end", f"Cadena: {result_info['input_string']} => Salida: {result_info['result']}\n")
#         output_text.insert("end", "Detalle del análisis léxico:\n")

#         for token in result_info['tokens']:
#             output_text.insert("end", f"Línea: {token.lineno}, Tipo: {token.type}, Valor: {token.value}\n")

#         output_text.insert("end", "Árbol sintáctico:\n")
#         root_node = Node("Expression")
#         number_node = Node(f"Number: {result_info['result']}", parent=root_node)
#         conversion_node = Node(f"Conversion: {result_info['actual_conversion']}", parent=root_node)

#         tree_str = ""
#         for pre, _, node in RenderTree(root_node, style=AsciiStyle()):
#             tree_str += f"{pre}{node.name}\n"

#         output_text.insert("end", f"{tree_str}\n\n")

#         tree_filename = f"tree_{result_info['actual_conversion']}.png"
#         generate_tree_representation(root_node, tree_filename)

#         img = Image.open(tree_filename)
#         img.thumbnail((250, 250))
#         img_tk = ImageTk.PhotoImage(img)
#         image_label = tk.Label(root, image=img_tk)
#         image_label.image = img_tk

#         # Usar grid para colocar la etiqueta de imagen
#         image_label.grid(row=row, column=col, padx=10, pady=5)
#         col += 1
#         if col >= 3:
#             col = 0
#             row += 1

#         image_labels.append(image_label)

#     output_text.config(state="disabled")


# def generate_tree_representation(node, filename):
#     UniqueDotExporter(node).to_picture(filename)

# root = tk.Tk()
# root.title("Conversor desde Archivo")


# # Crear elementos de la interfaz
# input_label = tk.Label(root, text="Resultados de Conversión:")
# input_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

# # Agregar una barra de desplazamiento al área de texto de salida
# scrollbar = tk.Scrollbar(root)
# output_text = scrolledtext.ScrolledText(root, height=15, width=50, state="disabled", yscrollcommand=scrollbar.set)
# output_text.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
# scrollbar.config(command=output_text.yview)

# image_labels = []

# show_results()
# # Iniciar la ventana principal
# root.mainloop()

import tkinter as tk
import ply.lex as lex
import ply.yacc as yacc
import re
import random
from anytree import Node, RenderTree, AsciiStyle
from treelib import Node as TreeNode, Tree
import matplotlib.pyplot as plt
from anytree.exporter import UniqueDotExporter, DotExporter
from tkinter import scrolledtext
from PIL import Image, ImageTk
import networkx as nx

# Definición de tokens
tokens = [
    'NUMBER',
    'CONVERSION',
    'END'
]

# Expresiones regulares para tokens
t_CONVERSION = r'Hexadecimal|Octal|Binario|Romano|Duodecimal|Aleatorio'
t_END = r'\$'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    t.lexer.lineno = t.lineno
    return t

# Ignorar espacios en blanco y saltos de línea
t_ignore = ' \t\n'

# Manejo de errores
def t_error(t):
    print("Error léxico: Caracter no válido '%s'" % t.value[0])
    t.lexer.skip(1)

# Construcción del analizador léxico
lexer = lex.lex()

# Definición de la gramática
def p_expression(p):
    '''expression : NUMBER CONVERSION END'''
    p[0] = (p[1], p[2])

# Manejo de errores sintácticos
def p_error(p):
    print("Error sintáctico en la entrada")

# Construcción del analizador sintáctico
parser = yacc.yacc()

# Funciones de conversión
def decimal_to_roman(n):
    val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    syb = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    roman_num = ''
    i = 0
    while n > 0:
        for _ in range(n // val[i]):
            roman_num += syb[i]
            n -= val[i]
        i += 1
    return roman_num

def decimal_to_bin(n):
    return bin(n)[2:]

def decimal_to_oct(n):
    return oct(n)[2:]

def decimal_to_hex(n):
    return hex(n)[2:].upper()

def decimal_to_duodecimal(n):
    if n == 0:
        return "0"
    duodecimal_digitos = "0123456789AB"
    duodecimal_resultado = ""
    while n > 0:
        remainder = n % 12
        duodecimal_resultado = duodecimal_digitos[remainder] + duodecimal_resultado
        n //= 12
    return duodecimal_resultado

def do_conversion(number, conversion):
    if conversion == 'Binario':
        return decimal_to_bin(number), conversion
    elif conversion == 'Octal':
        return decimal_to_oct(number), conversion
    elif conversion == 'Hexadecimal':
        return decimal_to_hex(number), conversion
    elif conversion == 'Romano':
        return decimal_to_roman(number), conversion
    elif conversion == 'Duodecimal':
        return decimal_to_duodecimal(number), conversion
    elif conversion == 'Aleatorio':
        conversion_options = ['Binario', 'Octal', 'Hexadecimal', 'Romano', 'Duodecimal']
        chosen_conversion = random.choice(conversion_options)
        result = do_conversion(number, chosen_conversion)
        return result, chosen_conversion

# Leer archivo de entrada
def read_input_file(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
        return [line.strip() for line in lines]
    except Exception as e:
        print("Error al leer el archivo:", e)
        return []

# Procesar conversiones
def process_conversions(input_strings):
    results = []
    for input_string in input_strings:
        lexer.input(input_string)
        tokens = []
        while True:
            tok = lexer.token()
            if not tok:
                break
            tokens.append(tok)
        try:
            parsed_data = parser.parse(input_string)
            number, conversion = parsed_data
            result, actual_conversion = do_conversion(number, conversion)
            result_info = {
                "input_string": input_string,
                "result": result,
                "tokens": tokens,
                "actual_conversion": actual_conversion
            }
            results.append(result_info)
        except Exception as e:
            print("Error:", e)
    return results

# Alternativa 1: Mostrar árbol en texto (ASCII)
def display_tree_textually(root_node):
    tree_str = ""
    for pre, _, node in RenderTree(root_node, style=AsciiStyle()):
        tree_str += f"{pre}{node.name}\n"
    return tree_str

def show_results_textual():
    input_strings = read_input_file("./input.txt")
    conversion_results = process_conversions(input_strings)
    output_text.config(state="normal")
    output_text.delete("1.0", "end")

    for result_info in conversion_results:
        output_text.insert("end", f"Cadena: {result_info['input_string']} => Salida: {result_info['result']}\n")
        output_text.insert("end", "Detalle del análisis léxico:\n")

        for token in result_info['tokens']:
            output_text.insert("end", f"Línea: {token.lineno}, Tipo: {token.type}, Valor: {token.value}\n")

        output_text.insert("end", "Árbol sintáctico:\n")
        root_node = Node("Expression")
        Node(f"Number: {result_info['result']}", parent=root_node)
        Node(f"Conversion: {result_info['actual_conversion']}", parent=root_node)

        tree_str = display_tree_textually(root_node)
        output_text.insert("end", f"{tree_str}\n\n")

    output_text.config(state="disabled")

# Alternativa 2: Visualizar con networkx y matplotlib
def plot_tree_with_networkx(root_node):
    G = nx.DiGraph()

    def add_edges(node):
        for child in node.children:
            G.add_edge(node.name, child.name)
            add_edges(child)

    add_edges(root_node)

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=10, font_weight="bold")
    plt.show()

def show_results_networkx():
    input_strings = read_input_file("./input.txt")
    conversion_results = process_conversions(input_strings)
    output_text.config(state="normal")
    output_text.delete("1.0", "end")

    for result_info in conversion_results:
        output_text.insert("end", f"Cadena: {result_info['input_string']} => Salida: {result_info['result']}\n")
        output_text.insert("end", "Detalle del análisis léxico:\n")

        for token in result_info['tokens']:
            output_text.insert("end", f"Línea: {token.lineno}, Tipo: {token.type}, Valor: {token.value}\n")

        output_text.insert("end", "Árbol sintáctico:\n")
        root_node = Node("Expression")
        Node(f"Number: {result_info['result']}", parent=root_node)
        Node(f"Conversion: {result_info['actual_conversion']}", parent=root_node)

        plot_tree_with_networkx(root_node)

    output_text.config(state="disabled")

def show_results_dot():
    input_strings = read_input_file("./input.txt")
    conversion_results = process_conversions(input_strings)
    output_text.config(state="normal")
    output_text.delete("1.0", "end")

    for result_info in conversion_results:
        output_text.insert("end", f"Cadena: {result_info['input_string']} => Salida: {result_info['result']}\n")
        output_text.insert("end", "Detalle del análisis léxico:\n")

        for token in result_info['tokens']:
            output_text.insert("end", f"Línea: {token.lineno}, Tipo: {token.type}, Valor: {token.value}\n")

        output_text.insert("end", "Árbol sintáctico:\n")
        root_node = Node("Expression")
        Node(f"Number: {result_info['result']}", parent=root_node)
        Node(f"Conversion: {result_info['actual_conversion']}", parent=root_node)

        dot_filename = f"tree_{result_info['actual_conversion']}.dot"
        save_tree_as_dot(root_node, dot_filename)
        output_text.insert("end", f"Árbol guardado en: {dot_filename}\n\n")

    output_text.config(state="disabled")

# Configuración de la interfaz de Tkinter
root = tk.Tk()
root.title("Conversor desde Archivo")

input_label = tk.Label(root, text="Resultados de Conversión:")
input_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

scrollbar = tk.Scrollbar(root)
output_text = scrolledtext.ScrolledText(root, height=20, width=80)
output_text.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
scrollbar.config(command=output_text.yview)

# Botones para mostrar resultados con las diferentes opciones
textual_button = tk.Button(root, text="Mostrar en Texto (ASCII)", command=show_results_textual)
textual_button.grid(row=2, column=0, padx=10, pady=10)

networkx_button = tk.Button(root, text="Mostrar Gráficamente (networkx)", command=show_results_networkx)
networkx_button.grid(row=2, column=1, padx=10, pady=10)

root.mainloop()
