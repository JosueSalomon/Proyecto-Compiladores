# Importación de las bibliotecas necesarias
import tkinter as tk  # Biblioteca para crear la interfaz gráfica
import ply.lex as lex  # Biblioteca para análisis léxico
import ply.yacc as yacc  # Biblioteca para análisis sintáctico
import re  # Biblioteca para expresiones regulares
import random  # Biblioteca para generar valores aleatorios
from anytree import Node, RenderTree, AsciiStyle  # Biblioteca para manipular y visualizar árboles
from treelib import Node as TreeNode, Tree  # Biblioteca alternativa para manipular árboles
import matplotlib.pyplot as plt  # Biblioteca para visualización de gráficos
from anytree.exporter import UniqueDotExporter, DotExporter  # Exportadores para árboles en formato DOT
from tkinter import scrolledtext  # Componente de texto con desplazamiento en Tkinter
from PIL import Image, ImageTk  # Biblioteca para manipular imágenes
import networkx as nx  # Biblioteca para manipular y visualizar grafos

# Definición de los tokens para el analizador léxico
tokens = [
    'NUMBER',  # Números enteros
    'CONVERSION',  # Tipos de conversión (Hexadecimal, Octal, etc.)
    'END'  # Fin de la expresión ('$')
]

# Expresiones regulares para reconocer los tokens de conversión y fin
t_CONVERSION = r'Hexadecimal|Octal|Binario|Romano|Duodecimal|Aleatorio|Maya'
t_END = r'\$'

# Expresión regular para reconocer números
def t_NUMBER(t):
    r'\d+'  # Reconoce dígitos (números enteros)
    t.value = int(t.value)  # Convierte el valor a entero
    t.lexer.lineno = t.lineno  # Registra el número de línea
    return t

# Ignorar espacios en blanco y saltos de línea
t_ignore = ' \t\n'

# Manejo de errores léxicos
def t_error(t):
    print("Error léxico: Caracter no válido '%s'" % t.value[0])
    t.lexer.skip(1)

# Construcción del analizador léxico
lexer = lex.lex()

# Definición de la gramática para el analizador sintáctico
def p_expression(p):
    '''expression : NUMBER CONVERSION END'''
    p[0] = (p[1], p[2])  # Almacena el número y el tipo de conversión

# Manejo de errores sintácticos
def p_error(p):
    print("Error sintáctico en la entrada")

# Construcción del analizador sintáctico
parser = yacc.yacc()

# Función para convertir de decimal a romano
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

# Función para convertir de decimal a binario
def decimal_to_bin(n):
    return bin(n)[2:]  # Elimina el prefijo '0b'

# Función para convertir de decimal a octal
def decimal_to_oct(n):
    return oct(n)[2:]  # Elimina el prefijo '0o'

# Función para convertir de decimal a hexadecimal
def decimal_to_hex(n):
    return hex(n)[2:].upper()  # Elimina el prefijo '0x' y convierte a mayúsculas

# Función para convertir de decimal a duodecimal
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

# Función para convertir de decimal a la numeración maya
def decimal_to_mayan(n):
    if n == 0:
        return "0"  # Concha para cero
    
    mayan_digits = []
    while n > 0:
        remainder = n % 20
        mayan_digits.append(remainder)
        n //= 20

    # Convertir los dígitos a una representación textual en maya
    def value_to_mayan_string(value):
        if value == 0:
            return "0"  # Concha para cero
        result = []
        bars = value // 5
        points = value % 5
        
        result.extend(['.' * points])  # Puntos
        result.extend(['|' * bars])  # Barras
        return ''.join(result)

    mayan_representation = [value_to_mayan_string(value) for value in reversed(mayan_digits)]
    return ' '.join(mayan_representation)

# Función para realizar la conversión según el tipo especificado
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
    elif conversion == 'Maya':
        return decimal_to_mayan(number), conversion
    elif conversion == 'Aleatorio':
        conversion_options = ['Binario', 'Octal', 'Hexadecimal', 'Romano', 'Duodecimal', 'Maya']
        chosen_conversion = random.choice(conversion_options)  # Elige una conversión aleatoria
        result = do_conversion(number, chosen_conversion)
        return result, chosen_conversion

# Función para leer las cadenas de un archivo de entrada
def read_input_file(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
        return [line.strip() for line in lines]  # Elimina espacios en blanco y saltos de línea
    except Exception as e:
        print("Error al leer el archivo:", e)
        return []

# Función para procesar las conversiones de las cadenas de entrada
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

# Alternativa 1: Mostrar árbol en formato de texto (ASCII)
def display_tree_textually(root_node):
    tree_str = ""
    for pre, _, node in RenderTree(root_node, style=AsciiStyle()):
        tree_str += f"{pre}{node.name}\n"
    return tree_str

# Mostrar los resultados en la interfaz de usuario en formato de texto (ASCII)
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

# Alternativa 2: Visualizar árbol sintáctico usando networkx y matplotlib
def plot_tree_with_networkx(root_node):
    G = nx.DiGraph()  # Crear un grafo dirigido

    def add_edges(node):
        for child in node.children:
            G.add_edge(node.name, child.name)  # Añadir aristas del nodo padre al hijo
            add_edges(child)  # Recursión para los nodos hijos

    add_edges(root_node)

    pos = nx.spring_layout(G)  # Disposición de nodos en el gráfico
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=10, font_weight="bold")
    plt.show()

# Mostrar los resultados en la interfaz de usuario con visualización de grafos (networkx)
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

# Configuración de la interfaz gráfica de usuario (GUI) utilizando Tkinter
root = tk.Tk()
root.title("Conversor desde Archivo")  # Título de la ventana

# Etiqueta para los resultados de conversión
input_label = tk.Label(root, text="Resultados de Conversión:")
input_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

# Área de texto con desplazamiento para mostrar los resultados
scrollbar = tk.Scrollbar(root)
output_text = scrolledtext.ScrolledText(root, height=20, width=80)
output_text.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
scrollbar.config(command=output_text.yview)

# Botones para mostrar los resultados con las diferentes opciones
textual_button = tk.Button(root, text="Mostrar en Texto (ASCII)", command=show_results_textual)
textual_button.grid(row=2, column=0, padx=10, pady=10)

networkx_button = tk.Button(root, text="Mostrar Gráficamente (networkx)", command=show_results_networkx)
networkx_button.grid(row=2, column=1, padx=10, pady=10)

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()
