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
    'NUMBER',      # Números enteros
    'CONVERSION',  # Tipos de conversión (Hexadecimal, Octal, etc.)
    'END'          # Fin de la expresión ('$')
]

# Expresiones regulares para reconocer los tokens de conversión y fin
t_CONVERSION = r'Hexadecimal|Octal|Binario|Romano|Aleatorio|Maya'
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
    print(f"Error léxico: Caracter no válido '{t.value[0]}'")
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
def convertir_decimal_a_romano(n):
    valores = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    simbolos = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    resultado = ''
    i = 0
    while n > 0:
        for _ in range(n // valores[i]):
            resultado += simbolos[i]
            n -= valores[i]
        i += 1
    return resultado

# Función para convertir de decimal a binario
def convertir_decimal_a_binario(n):
    return bin(n)[2:]  # Elimina el prefijo '0b'

# Función para convertir de decimal a octal
def convertir_decimal_a_octal(n):
    return oct(n)[2:]  # Elimina el prefijo '0o'

# Función para convertir de decimal a hexadecimal
def convertir_decimal_a_hexadecimal(n):
    return hex(n)[2:].upper()  # Elimina el prefijo '0x' y convierte a mayúsculas

# Función para convertir de decimal a la numeración maya
def convertir_decimal_a_maya(n):
    if n == 0:
        return "0"  # Concha se le agrega un cero
    
    mayan_digits = []
    while n > 0:
        remainder = n % 20
        mayan_digits.append(remainder)
        n //= 20

    # Convertir los dígitos a una representación textual en maya
    def value_to_mayan_string(value):
        if value == 0:
            return "0"  # Concha se le agrega un cero
        result = []
        bars = value // 5
        points = value % 5
        
        result.extend(['.' * points])  # Puntos
        result.extend(['|' * bars])  # Barras
        return ''.join(result)

    mayan_representation = [value_to_mayan_string(value) for value in reversed(mayan_digits)]
    return ' '.join(mayan_representation)

# Función para realizar la conversión según el tipo especificado
def realizar_conversion(numero, tipo_conversion):
    conversiones = {
        'Binario': convertir_decimal_a_binario,
        'Octal': convertir_decimal_a_octal,
        'Hexadecimal': convertir_decimal_a_hexadecimal,
        'Romano': convertir_decimal_a_romano,
        'Maya': convertir_decimal_a_maya
    }

    if tipo_conversion == 'Aleatorio':
        tipo_conversion = random.choice(list(conversiones.keys()))
    
    return conversiones[tipo_conversion](numero), tipo_conversion

# Función para leer las cadenas de un archivo de entrada
def leer_archivo_entrada(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as archivo:
            lineas = archivo.readlines()
        return [linea.strip() for linea in lineas] # Elimina espacios en blanco y saltos de línea
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return []

# Función para procesar las conversiones de las cadenas de entrada
def procesar_conversiones(cadenas_entrada):
    resultados = []
    for cadena in cadenas_entrada:
        lexer.input(cadena)
        tokens = []
        while True:
            tok = lexer.token()
            if not tok:
                break
            tokens.append(tok)
        try:
            parsed_data = parser.parse(cadena)
            numero, conversion = parsed_data
            resultado, conversion_real = realizar_conversion(numero, conversion)
            info_resultado = {
                "cadena_entrada": cadena,
                "resultado": resultado,
                "tokens": tokens,
                "conversion_real": conversion_real
            }
            resultados.append(info_resultado)
        except Exception as e:
            print(f"Error: {e}")
    return resultados

# Alternativa 1: Mostrar árbol en formato de texto (ASCII)
def mostrar_arbol_texto(raiz_nodo):
    arbol_str = ""
    for pre, _, nodo in RenderTree(raiz_nodo, style=AsciiStyle()):
        arbol_str += f"{pre}{nodo.name}\n"
    return arbol_str

# Mostrar los resultados en la interfaz de usuario en formato de texto (ASCII)
def mostrar_resultados_texto():
    cadenas_entrada = leer_archivo_entrada("./input.txt")
    resultados_conversion = procesar_conversiones(cadenas_entrada)
    output_text.config(state="normal")
    output_text.delete("1.0", "end")

    for info_resultado in resultados_conversion:
        output_text.insert("end", f"Cadena: {info_resultado['cadena_entrada']} => Salida: {info_resultado['resultado']}\n")
        output_text.insert("end", "Detalle del análisis léxico:\n")

        for token in info_resultado['tokens']:
            output_text.insert("end", f"Línea: {token.lineno}, Tipo: {token.type}, Valor: {token.value}\n")

        output_text.insert("end", "Árbol sintáctico:\n")
        raiz_nodo = Node("Expression")
        Node(f"Number: {info_resultado['resultado']}", parent=raiz_nodo)
        Node(f"Conversion: {info_resultado['conversion_real']}", parent=raiz_nodo)

        arbol_str = mostrar_arbol_texto(raiz_nodo)
        output_text.insert("end", f"{arbol_str}\n\n")

    output_text.config(state="disabled")

# Función personalizada para disposición jerárquica en NetworkX
def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    pos = _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)
    return pos

def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None, parsed=None):
    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    if parsed is None:
        parsed = set()
    parsed.add(root)
    neighbors = list(G.neighbors(root))
    if not isinstance(G, nx.DiGraph) and parent is not None:
        neighbors.remove(parent)  # Remove the parent to prevent cycles

    if len(neighbors) != 0:
        dx = width / len(neighbors)
        nextx = xcenter - width / 2 - dx / 2
        for neighbor in neighbors:
            nextx += dx
            pos = _hierarchy_pos(G, neighbor, width=dx, vert_gap=vert_gap, vert_loc=vert_loc-vert_gap, 
                                 xcenter=nextx, pos=pos, parent=root, parsed=parsed)
    return pos

# Alternativa 2: Visualizar árbol sintáctico usando networkx y matplotlib
def mostrar_arbol_grafico(raiz_nodo):
    G = nx.DiGraph()  # Crear un grafo dirigido

    def agregar_aristas(nodo):
        for hijo in nodo.children:
            G.add_edge(nodo.name, hijo.name)  # Añadir aristas del nodo padre al hijo
            agregar_aristas(hijo)  # Recursión para los nodos hijos

    agregar_aristas(raiz_nodo)

    pos = hierarchy_pos(G, raiz_nodo.name)  # Disposición jerárquica de nodos
    nx.draw(G, pos, with_labels=True, node_size=10000, node_color="lightgreen", font_size=10, font_weight="bold", arrows=False)
    plt.show()

# Mostrar los resultados en la interfaz de usuario con visualización de grafos (networkx)
def mostrar_resultados_grafico():
    cadenas_entrada = leer_archivo_entrada("./input.txt")
    resultados_conversion = procesar_conversiones(cadenas_entrada)
    output_text.config(state="normal")
    output_text.delete("1.0", "end")

    for info_resultado in resultados_conversion:
        output_text.insert("end", f"Cadena: {info_resultado['cadena_entrada']} => Salida: {info_resultado['resultado']}\n")
        output_text.insert("end", "Detalle del análisis léxico:\n")

        for token in info_resultado['tokens']:
            output_text.insert("end", f"Línea: {token.lineno}, Tipo: {token.type}, Valor: {token.value}\n")

        output_text.insert("end", "Árbol sintáctico:\n")
        raiz_nodo = Node("Expression")
        Node(f"Number: {info_resultado['resultado']}", parent=raiz_nodo)
        Node(f"Conversion: {info_resultado['conversion_real']}", parent=raiz_nodo)

        mostrar_arbol_grafico(raiz_nodo)

    output_text.config(state="disabled")

# Configuración de la interfaz gráfica de usuario (GUI) utilizando Tkinter
root = tk.Tk()
root.title("Conversor desde Archivo") # Título de la ventana

# Etiqueta para los resultados de conversión
input_label = tk.Label(root, text="Resultados de Conversión:")
input_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

# Área de texto con desplazamiento para mostrar los resultados
scrollbar = tk.Scrollbar(root)
output_text = scrolledtext.ScrolledText(root, height=20, width=80)
output_text.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
scrollbar.config(command=output_text.yview)

# Botones para mostrar los resultados con las diferentes opciones
textual_button = tk.Button(root, text="Mostrar en Texto (ASCII)", command=mostrar_resultados_texto)
textual_button.grid(row=2, column=0, padx=10, pady=10)

networkx_button = tk.Button(root, text="Mostrar Gráficamente (networkx)", command=mostrar_resultados_grafico)
networkx_button.grid(row=2, column=1, padx=10, pady=10)

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()