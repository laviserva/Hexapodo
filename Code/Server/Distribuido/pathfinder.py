import ast
import cv2
import numpy as np
import networkx as nx
import enum

class Accion(enum.Enum):
    MOVER = ["ctrl-avanzar", "45"]
    GIRAR = ["ctrl-girar", "90"]
    GIRAR_neg = ["ctrl-girar", "-90"]

class Direccion(enum.Enum):
    NORTE = "Norte"
    SUR = "Sur"
    ESTE = "Este"
    OESTE = "Oeste"

def agregar_aristas(G):
    G.add_edge('(0, 0)', '(1, 0)')
    G.add_edge('(0, 0)', '(0, 1)')
    G.add_edge('(1, 0)', '(2, 0)')
    G.add_edge('(1, 0)', '(1, 1)')
    G.add_edge('(2, 0)', '(3, 0)')
    G.add_edge('(2, 0)', '(2, 1)')
    G.add_edge('(3, 0)', '(3, 1)')
    G.add_edge('(0, 1)', '(1, 1)')
    G.add_edge('(0, 1)', '(0, 2)')
    G.add_edge('(1, 1)', '(2, 1)')
    G.add_edge('(1, 1)', '(1, 2)')
    G.add_edge('(2, 1)', '(3, 1)')
    G.add_edge('(2, 1)', '(2, 2)')
    G.add_edge('(3, 1)', '(3, 2)')
    G.add_edge('(0, 2)', '(1, 2)')
    G.add_edge('(0, 2)', '(0, 3)')
    G.add_edge('(1, 2)', '(2, 2)')
    G.add_edge('(1, 2)', '(1, 3)')
    G.add_edge('(2, 2)', '(3, 2)')
    G.add_edge('(2, 2)', '(2, 3)')
    G.add_edge('(3, 2)', '(3, 3)')
    G.add_edge('(0, 3)', '(1, 3)')
    G.add_edge('(1, 3)', '(2, 3)')
    G.add_edge('(3, 3)', '(2, 3)')

def agregar_obstaculo(G, coordenadas):
    for coordenada in coordenadas:
        G.remove_node(str(coordenada))

def girar_imagen(imagen, angulo):
    alto, ancho = imagen.shape[:2]
    centro = (ancho / 2, alto / 2)
    matriz_rotacion = cv2.getRotationMatrix2D(centro, angulo, 1.0)
    imagen_rotada = cv2.warpAffine(imagen, matriz_rotacion, (ancho, alto))
    return imagen_rotada

def tomar_foto_y_ajustarla(index, x, y, ancho, alto, angulo):
    # Índice de la cámara que deseas usar
    camera_index = index
    # Inicializar la cámara
    cap = cv2.VideoCapture(camera_index)
    # Verificar si la cámara se abrió correctamente
    if not cap.isOpened():
        print("Error al abrir la cámara")
        exit()
    # Capturar un fotograma desde la cámara
    ret, frame = cap.read()
    # Verificar si el fotograma se capturó correctamente
    if not ret:
        print("Error al capturar el fotograma")
        exit()
    # Guardar el fotograma como una imagen
    cv2.imwrite("foto.jpg", frame)
    # Liberar la cámara
    cap.release()
    # Mostrar un mensaje de éxito
    print("¡Foto tomada correctamente desde la cámara", camera_index, "!")
    # Cargar la imagen
    imagen_original = cv2.imread("foto.jpg")
    imagen = girar_imagen(imagen_original, angulo)
    # Recortar la región de interés
    region_recortada = imagen[y:y+alto, x:x+ancho]
    # Mostrar la imagen original y la región recortada
    # cv2.imshow("Imagen Original", imagen)
    # cv2.imshow("Region Recortada", region_recortada)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite("foto_recortada.jpg", region_recortada)

def detectar_objetos(imagen):
    # Convertir la imagen a formato HSV (Hue, Saturation, Value)
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

    # Definir los rangos de color para el rojo, verde y azul en formato HSV
    rango_rojo_bajo = np.array([0, 100, 100])
    rango_rojo_alto = np.array([10, 255, 255])
    rango_verde_bajo = np.array([40, 100, 100])  # Rango de tonos de verde
    rango_verde_alto = np.array([80, 255, 255])  # Rango de tonos de verde
    rango_azul_bajo = np.array([100, 100, 100])
    rango_azul_alto = np.array([130, 255, 255])

    # Aplicar las máscaras para detectar objetos rojos, verdes y azules
    mascara_roja = cv2.inRange(hsv, rango_rojo_bajo, rango_rojo_alto)
    mascara_verde = cv2.inRange(hsv, rango_verde_bajo, rango_verde_alto)
    mascara_azul = cv2.inRange(hsv, rango_azul_bajo, rango_azul_alto)

    # Encontrar contornos de los objetos detectados
    contornos_rojos, _ = cv2.findContours(mascara_roja, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contornos_verdes, _ = cv2.findContours(mascara_verde, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contornos_azules, _ = cv2.findContours(mascara_azul, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Lista para almacenar las posiciones de los objetos rojos, verdes y azules
    posiciones_rojas = []
    posiciones_verdes = []
    posiciones_azules = []

    # Iterar sobre los contornos y encontrar las posiciones
    for contorno in contornos_rojos:
        area = cv2.contourArea(contorno)
        if area > 100:  # Filtrar contornos pequeños para evitar falsos positivos
            x, y, w, h = cv2.boundingRect(contorno)
            posiciones_rojas.append((x, y))

    for contorno in contornos_verdes:
        area = cv2.contourArea(contorno)
        if area > 100:  # Filtrar contornos pequeños para evitar falsos positivos
            x, y, w, h = cv2.boundingRect(contorno)
            posiciones_verdes.append((x, y))

    for contorno in contornos_azules:
        area = cv2.contourArea(contorno)
        if area > 100:  # Filtrar contornos pequeños para evitar falsos positivos
            x, y, w, h = cv2.boundingRect(contorno)
            posiciones_azules.append((x, y))

    return posiciones_rojas, posiciones_verdes, posiciones_azules

def transformar_coordenadas(coordenadas):
    coordenadas_transformadas = []
    
    for x, y in coordenadas:
        # Transformación para x
        if 19 < x <= 106:
            x_transformado = 0
        elif 114 < x <= 208:
            x_transformado = 1
        elif 212 < x <= 305:
            x_transformado = 2
        elif 313 < x <= 406:
            x_transformado = 3
        else:
            x_transformado = None  # Si no está en ningún rango
        
        # Transformación para y
        if 10 < y <= 102:
            y_transformado = 0
        elif 108 < y <= 196:
            y_transformado = 1
        elif 204 < y <= 286:
            y_transformado = 2
        elif 296 < y <= 381:
            y_transformado = 3
        else:
            y_transformado = None  # Si no está en ningún rango
        
        # Si ambas coordenadas están en un rango válido
        if x_transformado is not None and y_transformado is not None:
            coordenadas_transformadas.append((x_transformado, y_transformado))
    
    return coordenadas_transformadas

def girar_hacia(orientacion_actual, orientacion_deseada):
    direcciones = [Direccion.NORTE, Direccion.ESTE, Direccion.SUR, Direccion.OESTE]
    indice_actual = direcciones.index(orientacion_actual)
    indice_deseado = direcciones.index(orientacion_deseada)

    derecha = (indice_deseado - indice_actual) % 4
    izquierda = (indice_actual - indice_deseado) % 4

    if derecha < izquierda:
        for _ in range(derecha):
            orientacion_actual, accion = girar_derecha(orientacion_actual)
        return orientacion_actual, accion
    else:
        for _ in range(izquierda):
            orientacion_actual, accion = girar_izquierda(orientacion_actual)
        return orientacion_actual, accion

def girar_derecha(orientacion):
    direcciones = [Direccion.NORTE, Direccion.ESTE, Direccion.SUR, Direccion.OESTE]
    nueva_orientacion = direcciones[(direcciones.index(orientacion) + 1) % 4]
    return nueva_orientacion, Accion.GIRAR.value

def girar_izquierda(orientacion):
    direcciones = [Direccion.NORTE, Direccion.ESTE, Direccion.SUR, Direccion.OESTE]
    nueva_orientacion = direcciones[(direcciones.index(orientacion) - 1) % 4]
    return nueva_orientacion, Accion.GIRAR_neg.value

def avanzar(posicion, orientacion):
    if orientacion == Direccion.NORTE:
        return (posicion[0], posicion[1] - 1), Accion.MOVER.value
    elif orientacion == Direccion.SUR:
        return (posicion[0], posicion[1] + 1), Accion.MOVER.value
    elif orientacion == Direccion.ESTE:
        return (posicion[0] + 1, posicion[1]), Accion.MOVER.value
    elif orientacion == Direccion.OESTE:
        return (posicion[0] - 1, posicion[1]), Accion.MOVER.value

def to_command(posiciones_camino):
    orientacion_actual = Direccion.ESTE
    posicion_actual = posiciones_camino[0]
    movimientos = []

    for i in range(len(posiciones_camino) - 1):
        proxima_posicion = posiciones_camino[i + 1]

        # Determinar la orientación necesaria
        if proxima_posicion[0] == posicion_actual[0]:
            if proxima_posicion[1] > posicion_actual[1]:
                orientacion_deseada = Direccion.SUR
            else:
                orientacion_deseada = Direccion.NORTE
        else:
            if proxima_posicion[0] > posicion_actual[0]:
                orientacion_deseada = Direccion.ESTE
            else:
                orientacion_deseada = Direccion.OESTE

        # Ajustar orientación de manera eficiente
        if orientacion_actual != orientacion_deseada:
            orientacion_actual, accion = girar_hacia(orientacion_actual, orientacion_deseada)
            movimientos.append(accion)

        # Avanzar hasta alcanzar la posición deseada
        while posicion_actual != proxima_posicion:
            posicion_actual, accion = avanzar(posicion_actual, orientacion_actual)
            movimientos.append(accion)

    print("Movimientos registrados:", movimientos)
    out = {}
    for i, mov in enumerate(movimientos):
        out[i+1] = mov
    return out

def pathfind(camera=1):
    tomar_foto_y_ajustarla(camera, 73, 38, 416, 390, 3)

    # Leer la imagen del grid con objetos rojos, verdes y azules
    imagen = cv2.imread('foto_recortada.jpg')

    # Obtener las posiciones de los objetos rojos, verdes y azules en pixeles
    posiciones_rojas, posiciones_verdes, posiciones_azules = detectar_objetos(imagen)

    # Mostrar las coordenadas de los objetos rojos, verdes y azules
    coordenadas_rojos = transformar_coordenadas(posiciones_rojas)
    coordenadas_verdes = transformar_coordenadas(posiciones_verdes)
    coordenadas_azules = transformar_coordenadas(posiciones_azules)

    print("Coordenadas de la Araña:", coordenadas_rojos)
    print("Coordenadas obstaculos:", coordenadas_verdes)
    print("Coordenadas del objetivo:", coordenadas_azules)

    # Crar Grafo y agregar Aristas
    G = nx.Graph()
    agregar_aristas(G)

    print("Tipo de variable objetivo")

    agregar_obstaculo(G, coordenadas_verdes)
    coordenadas_araña = str(coordenadas_rojos[0])
    coordenadas_objetivo = str(coordenadas_azules[0])
    camino = nx.dijkstra_path(G, coordenadas_araña, coordenadas_objetivo)
    print("Camino a seguir:", camino)
    return camino

if __name__ == "__main__":
    data = pathfind(camera=2)
    data = []
    data = [ast.literal_eval(item) for item in data]
    data = to_command(data)
    print("[Servidor]: Datos procesados:", data)