import time
from Control import Control
from enum import Enum
import numpy as np

def bazier_curve(p_0, p_1, p_2, t):
    return (1-t)**2 * p_0 + 2 * (1-t) * t * p_1 + t**2 * p_2

class Command(Enum):
    MOVE = 'CMD_MOVE'
    POSITION = 'CMD_POSITION'
    POSTURA = 'CMD_ATTITUDE'
    RELAX= 'CMD_RELAX'

class GaitMode(Enum):
    MODE_1 = '1'
    MODE_2 = '2'

class bailes:
    def __init__(self, use_bazier = False):
        self.ctrl = Control()
        self.data = [] 
        self.use_bazier = use_bazier
    
    def altura(self):
        self.ctrl.posittion(0,0,40)
    
    def move(self, x:str = '0', y:str = '0', speed:str = '0', angle:str = '0'):
        #self.__comprobe_restrictions(x, y, speed, angle)
        data = [
            Command.MOVE.value,
            GaitMode.MODE_1.value,
            x, y, speed, angle
            ]
        self.ctrl.run(data)
    
    def giro_cabeza(self):
        p_0 = 45
        p_2 = 135
        p_1 = (p_0 + p_2) / 2  # Punto de control para la curva de Bézier
        steps = 11  # Número de pasos para la interpolación

        if self.use_bezier:
            t_values = np.linspace(0, 1, steps)
            angles = bazier_curve(p_0, p_1, p_2, t_values)
        else:
            angles = np.linspace(p_0, p_2, steps)
        
        # Giro de la cabeza con Bézier o lineal
        self.ctrl.servo.setServoAngle(0, 90)
        time.sleep(0.2)

        for angulo in angles:
            self.ctrl.servo.setServoAngle(0, angulo)
            time.sleep(0.2)

        # Retornar la cabeza a la posición central
        self.ctrl.servo.setServoAngle(0, 94)   
    
    
    def avance_en_diagonal_adelante_derecha(self):
        """Avance en diagonal hacia la derecha adelante"""
        steps = 3
        dx, dy, speed, angle = "-20", "20", "10", "0"
        
        for _ in range(steps):
            self.move(dx, dy, speed, angle)

    def avance_en_diagonal_atras_izquierda(self):
        """Avance en diagonal hacia atrás a la izquierda"""
        steps = 3
        dx, dy, speed, angle = "20", "-20", "10", "0"
        
        for _ in range(steps):
            self.move(dx, dy, speed, angle)

    def avance_en_diagonal_adelante_izquierda(self):
        """Avance en diagonal hacia la izquierda adelante"""
        steps = 3
        dx, dy, speed, angle = "20", "20", "10", "0"
        
        for _ in range(steps):
            self.move(dx, dy, speed, angle)

    def avance_en_diagonal_atras_derecha(self):
        """Avance en diagonal hacia atrás a la derecha"""
        steps = 3
        dx, dy, speed, angle = "-20", "-20", "10", "0"
        
        for _ in range(steps):
            self.move(dx, dy, speed, angle)

    def pata_derecha_del_adelante(self):  
        x_p0, x_p2 = 90, 140
        y_p0, y_p2 = 90, 50
        z_p0, z_p2 = 140, 90
        x_p1 = (x_p0 + x_p2) / 2
        y_p1 = (y_p0 + y_p2) / 2
        z_p1 = (z_p0 + z_p2) / 2

        steps = 25  # Cantidad de pasos en el movimiento

        t_values = np.linspace(0, 1, steps)

        # Curvas de Bézier o lineales para cada eje
        if self.use_bezier:
            x_curve = bazier_curve(x_p0, x_p1, x_p2, t_values)
            y_curve = bazier_curve(y_p0, y_p1, y_p2, t_values)
            z_curve = bazier_curve(z_p0, z_p1, z_p2, t_values)
        else:
            x_curve = np.linspace(x_p0, x_p2, steps)
            y_curve = np.linspace(y_p0, y_p2, steps)
            z_curve = np.linspace(z_p0, z_p2, steps)

        # Movimiento de la pata en el eje x (elevación)
        for i in range(len(x_curve)):
            self.ctrl.servo.setServoAngle(14, x_curve[i])
            time.sleep(0.01)

        # Movimiento de la pata en el eje y (avance)
        for i in range(len(y_curve)):
            self.ctrl.servo.setServoAngle(15, y_curve[i])
            time.sleep(0.01)

        # Movimiento de la pata en el eje z (asentamiento)
        for i in range(len(z_curve)):
            self.ctrl.servo.setServoAngle(14, z_curve[i])
            time.sleep(0.01)
            
    def pata_izquierda_del_adelante(self):
        ####pata izquierda delantera hacia delante
        x_p0, x_p2 = 90, 50
        y_p0, y_p2 = 90, 130
        z_p0, z_p2 = 50, 90
        x_p1 = (x_p0 + x_p2) / 2
        y_p1 = (y_p0 + y_p2) / 2
        z_p1 = (z_p0 + z_p2) / 2

        steps = 25
        t_values = np.linspace(0, 1, steps)

        if self.use_bezier:
            x_curve = bazier_curve(x_p0, x_p1, x_p2, t_values)
            y_curve = bazier_curve(y_p0, y_p1, y_p2, t_values)
            z_curve = bazier_curve(z_p0, z_p1, z_p2, t_values)
        else:
            x_curve = np.linspace(x_p0, x_p2, steps)
            y_curve = np.linspace(y_p0, y_p2, steps)
            z_curve = np.linspace(z_p0, z_p2, steps)

        for i in range(len(x_curve)):  # Elevación
            self.ctrl.servo.setServoAngle(17, x_curve[i])
            time.sleep(0.01)

        for i in range(len(y_curve)):  # Avance
            self.ctrl.servo.setServoAngle(16, y_curve[i])
            time.sleep(0.01)

        for i in range(len(z_curve)):  # Asentamiento
            self.ctrl.servo.setServoAngle(17, z_curve[i])
            time.sleep(0.01)
    def pata_central_derecha_adelante(self):
        ####pata central derecha hacia adelante
        x_p0, x_p2 = 90, 140
        y_p0, y_p2 = 90, 50
        z_p0, z_p2 = 140, 90
        x_p1 = (x_p0 + x_p2) / 2
        y_p1 = (y_p0 + y_p2) / 2
        z_p1 = (z_p0 + z_p2) / 2

        steps = 25
        t_values = np.linspace(0, 1, steps)

        if self.use_bezier:
            x_curve = bazier_curve(x_p0, x_p1, x_p2, t_values)
            y_curve = bazier_curve(y_p0, y_p1, y_p2, t_values)
            z_curve = bazier_curve(z_p0, z_p1, z_p2, t_values)
        else:
            x_curve = np.linspace(x_p0, x_p2, steps)
            y_curve = np.linspace(y_p0, y_p2, steps)
            z_curve = np.linspace(z_p0, z_p2, steps)

        for i in range(len(x_curve)):  # Elevación
            self.ctrl.servo.setServoAngle(11, x_curve[i])
            time.sleep(0.01)

        for i in range(len(y_curve)):  # Avance
            self.ctrl.servo.setServoAngle(12, y_curve[i])
            time.sleep(0.01)

        for i in range(len(z_curve)):  # Asentamiento
            self.ctrl.servo.setServoAngle(11, z_curve[i])
            time.sleep(0.01)

    def pata_central_izquierda_adelante(self):
        x_p0, x_p2 = 90, 50
        y_p0, y_p2 = 90, 150
        z_p0, z_p2 = 50, 90
        x_p1 = (x_p0 + x_p2) / 2
        y_p1 = (y_p0 + y_p2) / 2
        z_p1 = (z_p0 + z_p2) / 2

        steps = 25
        t_values = np.linspace(0, 1, steps)

        if self.use_bezier:
            x_curve = bazier_curve(x_p0, x_p1, x_p2, t_values)
            y_curve = bazier_curve(y_p0, y_p1, y_p2, t_values)
            z_curve = bazier_curve(z_p0, z_p1, z_p2, t_values)
        else:
            x_curve = np.linspace(x_p0, x_p2, steps)
            y_curve = np.linspace(y_p0, y_p2, steps)
            z_curve = np.linspace(z_p0, z_p2, steps)

        for i in range(len(x_curve)):  # Elevación
            self.ctrl.servo.setServoAngle(20, x_curve[i])
            time.sleep(0.01)

        for i in range(len(y_curve)):  # Avance
            self.ctrl.servo.setServoAngle(19, y_curve[i])
            time.sleep(0.01)

        for i in range(len(z_curve)):  # Asentamiento
            self.ctrl.servo.setServoAngle(20, z_curve[i])
            time.sleep(0.01)

    def pata_del_derecha_levantar(self):
        x_p0, x_p2 = 90, 140
        y_p0, y_p2 = 90, 50
        z_p0, z_p2 = 90, 0
        x_p1 = (x_p0 + x_p2) / 2
        y_p1 = (y_p0 + y_p2) / 2
        z_p1 = (z_p0 + z_p2) / 2

        steps = 25
        t_values = np.linspace(0, 1, steps)

        if self.use_bezier:
            x_curve = bazier_curve(x_p0, x_p1, x_p2, t_values)
            y_curve = bazier_curve(y_p0, y_p1, y_p2, t_values)
            z_curve = bazier_curve(z_p0, z_p1, z_p2, t_values)
        else:
            x_curve = np.linspace(x_p0, x_p2, steps)
            y_curve = np.linspace(y_p0, y_p2, steps)
            z_curve = np.linspace(z_p0, z_p2, steps)

        for i in range(len(x_curve)):  # Elevación
            self.ctrl.servo.setServoAngle(14, x_curve[i])
            time.sleep(0.01)

        for i in range(len(y_curve)):  # Avance
            self.ctrl.servo.setServoAngle(15, y_curve[i])
            time.sleep(0.01)

        for i in range(len(z_curve)):  # Extensión
            self.ctrl.servo.setServoAngle(13, z_curve[i])
            time.sleep(0.01)

    def pata_del_izquierda_levantar(self):
        x_p0, x_p2 = 90, 50
        y_p0, y_p2 = 90, 130
        z_p0, z_p2 = 90, 200
        x_p1 = (x_p0 + x_p2) / 2
        y_p1 = (y_p0 + y_p2) / 2
        z_p1 = (z_p0 + z_p2) / 2

        steps = 25
        t_values = np.linspace(0, 1, steps)

        if self.use_bezier:
            x_curve = bazier_curve(x_p0, x_p1, x_p2, t_values)
            y_curve = bazier_curve(y_p0, y_p1, y_p2, t_values)
            z_curve = bazier_curve(z_p0, z_p1, z_p2, t_values)
        else:
            x_curve = np.linspace(x_p0, x_p2, steps)
            y_curve = np.linspace(y_p0, y_p2, steps)
            z_curve = np.linspace(z_p0, z_p2, steps)

        for i in range(len(x_curve)):  # Elevación
            self.ctrl.servo.setServoAngle(17, x_curve[i])
            time.sleep(0.01)

        for i in range(len(y_curve)):  # Avance
            self.ctrl.servo.setServoAngle(16, y_curve[i])
            time.sleep(0.01)

        for i in range(len(z_curve)):  # Extensión
            self.ctrl.servo.setServoAngle(18, z_curve[i])
            time.sleep(0.01)
        
    def baile_1(self): #Es un movimiento circular en el plano x,y, ademas de moverser formando un onda en el ejes z
          r=40
          p_0 = 0
          p_2 = 2* np.pi*2
          p_1 = (p_0 + p_2) // 2
          steps = 100

          if self.use_bezier:
            # Generamos una serie de valores t linealmente espaciados entre 0 y 1
            t_values = np.linspace(0, 1, steps)
            
            # Calculamos los valores de theta usando la curva de Bézier vectorizada
            theta = bazier_curve(p_0, p_1, p_2, t_values)
          else:
            # Si no se usa Bézier, generamos 'theta' de forma lineal
            theta = np.linspace(p_0, p_2, steps)

          self.altura()
          for t in theta:
 
            x = r*np.cos(t)
            y = r*np.sin(t)
            z = r/3*np.cos(-t*3)
            self.ctrl.posittion(x,y,z)
          self.altura()  
    
    
    def baile_2(self):  # Es un movimiento lateral de izquierda a derecha
        speed = "10"
        angle = "0"
        steps = 4
        distance = "30"

        self.altura()
        # Movimiento hacia la derecha
        for _ in range(steps):
            self.move(distance, "0", speed, angle)
        
        # Movimiento hacia la izquierda
        for _ in range(steps):
            self.move(f"-{distance}", "0", speed, angle)

        self.altura()

    
    
    def  baile_3(self): #Es un movimiento en diagonal hacia adelante y atras en ambos lados izquierda y derecha en cada retorno al punto inicial se mueve el cuello de  robot
        self.altura()
        for i in range(1):
            self.altura()
            self.avance_en_diagonal_adelante_derecha()
            self.avance_en_diagonal_atras_izquierda()
            self.giro_cabeza()
            self.avance_en_diagonal_adelante_izquierda()
            self.avance_en_diagonal_atras_derecha()
            self.giro_cabeza()
        self.altura() 
    
    
    def baile_4(self): # Estes baile consiste de movimiento de la parte trasera del robot
          self.altura()
          punto=self.ctrl.postureBalance(0,0,0)
          self.ctrl.coordinateTransformation(punto)
          self.ctrl.setLegAngle()

          for i in range(4):
              time.sleep(0.2)        
              punto=self.ctrl.postureBalance(0,15,15)
              self.ctrl.coordinateTransformation(punto)
              self.ctrl.setLegAngle()
              time.sleep(0.2)
              punto=self.ctrl.postureBalance(0,15,-15)
              self.ctrl.coordinateTransformation(punto)
              self.ctrl.setLegAngle()
              time.sleep(0.2)
          punto=self.ctrl.postureBalance(0,0,0)
          self.ctrl.coordinateTransformation(punto)
          self.ctrl.setLegAngle()
          self.altura()
    
    def baile_5 (self):
          self.altura()
          ###movimiento de patas delanteras para estabilizar con 4 piernas
          ###pata derecha delantera hacia adelante
          self.pata_derecha_del_adelante()
          ####pata izquierda delantera hacia delante
          self.pata_izquierda_del_adelante()
          ####pata central derecha hacia adelante
          self.pata_central_derecha_adelante()
          ####pata central izquierda hacia adelante
          self.pata_central_izquierda_adelante()
          ###levantamiento de pata delantera derecha
          self.pata_del_derecha_levantar()
          self.pata_del_izquierda_levantar()
          self.altura()