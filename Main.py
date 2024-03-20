import xml.etree.ElementTree as ET

import subprocess
from os import startfile


class NodoPatron:
    def __init__(self, codigo, patron):
        self.codigo = codigo
        self.patron = patron
        self.siguiente = None

class NodoPiso:
    def __init__(self, nombre, R, C, F, S):
        self.nombre = nombre
        self.R = R
        self.C = C
        self.F = F
        self.S = S
        self.patrones = ListaEnlazadaPatrones()
        self.siguiente = None

    def agregar_patron(self, codigo, patron):
        self.patrones.agregar_nodo(NodoPatron(codigo, patron))

class ListaEnlazadaPatrones:
    def __init__(self):
        self.cabeza = None

    def agregar_nodo(self, nodo_patron):
        nodo_patron.siguiente = self.cabeza
        self.cabeza = nodo_patron

    def mostrar_patrones(self):
        actual = self.cabeza
        while actual:
            print(f"Código: {actual.codigo}, Patrón: {actual.patron}")
            actual = actual.siguiente

    def buscar_por_patron(self, codigo_patron):
        actual = self.cabeza
        while actual:
            if actual.codigo == codigo_patron:
                return actual.patron
            actual = actual.siguiente
        return None

    def mostrar_patron(self, codigo_patron):
        patron = self.buscar_por_patron(codigo_patron)
        if patron:
            return patron
        else:
            return None

class ListaEnlazadaPisos:
    def __init__(self):
        self.cabeza = None

    def agregar_nodo(self, nodo_piso):
        if self.cabeza is None:
            self.cabeza = nodo_piso
            return
        
        if nodo_piso.nombre < self.cabeza.nombre:
            nodo_piso.siguiente = self.cabeza
            self.cabeza = nodo_piso
            return
        
        prev = None
        current = self.cabeza
        while current and current.nombre < nodo_piso.nombre:
            prev = current
            current = current.siguiente
        
        prev.siguiente = nodo_piso
        nodo_piso.siguiente = current

    def mostrar_pisos(self):
        actual = self.cabeza
        while actual:
            print(f"Nombre: {actual.nombre}")
            print(f"R: {actual.R}")
            print(f"C: {actual.C}")
            print(f"F: {actual.F}")
            print(f"S: {actual.S}")
            print("Patrones:")
            actual.patrones.mostrar_patrones()
            print()
            actual = actual.siguiente

    def buscar_por_piso(self, nombre_piso):
        actual = self.cabeza
        while actual:
            if actual.nombre == nombre_piso:
                return actual
            actual = actual.siguiente
        return None

    def mostrar_piso(self, nombre_piso):
        piso = self.buscar_por_piso(nombre_piso)
        if piso:
            print(f"\nMostrar información del piso '{nombre_piso}':")
            print(f"Nombre: {piso.nombre}")
            print(f"R: {piso.R}")
            print(f"C: {piso.C}")
            print(f"F: {piso.F}")
            print(f"S: {piso.S}")
            print("Patrones:")
            piso.patrones.mostrar_patrones()
        else:
            print(f"\nPiso '{nombre_piso}' no encontrado.")

  
    def graficarPatron(self, piso, codigoPatron, nombreArchivo):
        pisoEncontrado= self.buscar_por_piso(piso)
        if pisoEncontrado:
            R=int(pisoEncontrado.R)
            C=int(pisoEncontrado.C)
            F=pisoEncontrado.F 
            S=pisoEncontrado.S

            patronEncontrado=pisoEncontrado.patrones.mostrar_patron(codigoPatron)
          
            fullNameTxt = nombreArchivo+".dot"

            fullNameImg = nombreArchivo+".jpg"

            if ((R*C)==len(patronEncontrado)):
                cont=0

                try:
                    f = open(fullNameTxt, "w")
                    f.write("digraph TablaBasica{\n")
                    f.write("node [shape=plaintext];\n")
                    f.write("Tabla1 [label=<\n")
                    f.write(' <table border="1" cellspacing="0">\n')

                  
                    for y in range(0,R, 1):
                        f.write("<tr>\n")
                       
                        for x in range(0,C,1):
                            if patronEncontrado[cont]=="B":
                                f.write("<td>     </td>\n")
                            if patronEncontrado[cont]=="N":
                                f.write('<td bgcolor="black">     </td>\n')
                            cont+=1
                        f.write("</tr>\n")

                    f.write("</table>>];\n")
                    f.write("}")
                    f.close()
                    
                    command = ['dot', '-Tjpg', fullNameTxt, '-o', fullNameImg]
                    
                    subprocess.call(command)
                    
                    startfile(fullNameImg)
                except :        
                    print("Error: .")
                    f.close()

            else:
                print("dimensiones incorrectas")
        else:
            print("No se pudo crear la grafica, piso o patron no encontrado")


lista_pisos = ListaEnlazadaPisos()

piso_ejemplo01 = NodoPiso("dormitorio", 2, 4, 1, 1)
piso_ejemplo01.agregar_patron("coddo", "BNBNBBBN")
piso_ejemplo01.agregar_patron("cod12", "NBNBBBBB")

piso_ejemplo02 = NodoPiso("sala", 3, 3, 1, 1)
piso_ejemplo02.agregar_patron("codsa", "BNNNBNBBB")
piso_ejemplo02.agregar_patron("cod22", "BBBNBBBN")

piso_ejemplo03 = NodoPiso("comedor", 1, 5, 1000, 1)
piso_ejemplo03.agregar_patron("codco", "BNNNN")
piso_ejemplo03.agregar_patron("cod32", "NNNBB")

lista_pisos.agregar_nodo(piso_ejemplo01)
lista_pisos.agregar_nodo(piso_ejemplo02)
lista_pisos.agregar_nodo(piso_ejemplo03)


tree = ET.parse('entrada.xml')

root = tree.getroot()

for piso in root.findall('piso'):

    nombrePiso=piso.get('nombre')

    valorR=piso.find('R').text.strip()
    valorC=piso.find('C').text.strip()
    valorF=piso.find('F').text.strip()
    valorS=piso.find('S').text.strip()
    variable=NodoPiso(nombrePiso, valorR, valorC, valorF, valorS)

    for patron in piso.findall('.//patron'):
        codigo = patron.get('codigo')
        contenido = patron.text.strip()
        variable.agregar_patron(codigo, contenido)

    lista_pisos.agregar_nodo(variable)


def cambiar_patron(piso_nombre, codigo_patron_inicial, codigo_patron_final):
    piso_encontrado = lista_pisos.buscar_por_piso(piso_nombre)
    if piso_encontrado:
        patron_inicial = piso_encontrado.patrones.mostrar_patron(codigo_patron_inicial)
        patron_final = piso_encontrado.patrones.mostrar_patron(codigo_patron_final)
        if patron_inicial and patron_final and len(patron_inicial) == len(patron_final):
            costo_total = 0
            instrucciones = []

            for i in range(len(patron_inicial)):
                if patron_inicial[i] != patron_final[i]:
                    costo_total += 1  # Incrementar el costo por cada cambio

                    if patron_inicial[i] == 'B' and patron_final[i] == 'N':
                        instrucciones.append(f"Voltear azulejo {i + 1} (B -> N)")
                        # Actualizar el patrón inicial
                        patron_inicial = patron_inicial[:i] + 'N' + patron_inicial[i+1:]
                    elif patron_inicial[i] == 'N' and patron_final[i] == 'B':
                        instrucciones.append(f"Voltear azulejo {i + 1} (N -> B)")
                        # Actualizar el patrón inicial
                        patron_inicial = patron_inicial[:i] + 'B' + patron_inicial[i+1:]
                    else:
                        # Calcular el índice del azulejo cercano en el patrón final
                        indice_cercano = buscar_azulejo_cercano(patron_inicial, patron_final, i)
                        instrucciones.append(f"Intercambiar azulejo {indice_cercano + 1}")
                        costo_total += int(piso_encontrado.F)  # Incrementar el costo por voltear
                        # Actualizar el patrón inicial
                        patron_inicial = patron_inicial[:indice_cercano] + ('N' if patron_inicial[indice_cercano] == 'B' else 'B') + patron_inicial[indice_cercano+1:]

            print(f"Instrucciones para cambiar el patrón '{piso_encontrado.patrones.mostrar_patron(codigo_patron_inicial)}' al patrón '{piso_encontrado.patrones.mostrar_patron(codigo_patron_final)}':")
            for instruccion in instrucciones:
                print(instruccion)
            print(f"Costo total: {costo_total}")
        else:
            print("Los patrones deben tener la misma longitud.")
    else:
        print(f"No se encontró el piso '{piso_nombre}'.")


def buscar_azulejo_cercano(patron_actual, nuevo_patron, indice):

    for i in range(indice + 1, len(patron_actual)):
        if patron_actual[i] != nuevo_patron[i]:
            return i
    for i in range(indice - 1, -1, -1):
        if patron_actual[i] != nuevo_patron[i]:
            return i
    return -1


while True:
    print("============================================================")
    print("\nMenú:")
    print("1. Mostrar información de todos los pisos")
    print("2. Buscar por piso")
    print("3. Graficar patron")
    print("4. Cambiar patrón")
    print("5. Salir")
    print("============================================================")

    opcion = input("Ingrese el número de la opción deseada: ")

    if opcion == "1":
        lista_pisos.mostrar_pisos()
    elif opcion == "2":
        nombre_piso = input("Ingrese el nombre del piso: ")
        lista_pisos.mostrar_piso(nombre_piso)
    elif opcion == "3":
        nombre_piso = input("Ingrese el nombre del piso que desea graficar: ")
        piso_encontrado = lista_pisos.buscar_por_piso(nombre_piso)
        if piso_encontrado:
            print("Patrones disponibles para el piso '{}':\n".format(nombre_piso))
            piso_encontrado.patrones.mostrar_patrones()
            codigo_patron = input("\nIngrese el código del patrón que desea graficar: ")
            lista_pisos.graficarPatron(nombre_piso, codigo_patron, "imagen")

    elif opcion == "4":
        nombre_piso = input("Ingrese el nombre del piso: ")
        codigo_patron_inicial = input("Ingrese el código del patrón inicial: ")
        codigo_patron_final = input("Ingrese el código del patrón final: ")
        cambiar_patron(nombre_piso, codigo_patron_inicial, codigo_patron_final)

    elif opcion == "5":
        print("Saliendo del programa.")
        break
    else:
        print("Opción no válida. Por favor, ingrese un número válido.")