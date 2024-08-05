import time
from Control import Control
from enum import Enum
import numpy as np
class Command(Enum):
    MOVE = 'CMD_MOVE'
    POSITION = 'CMD_POSITION'
    POSTURA = 'CMD_ATTITUDE'
    RELAX= 'CMD_RELAX'

class GaitMode(Enum):
    MODE_1 = '1'
    MODE_2 = '2'

class bailes:
    def __init__(self):
        self.ctrl = Control()
        self.data = [] 
    
    def altura(self):
        self.ctrl.posittion(0,0,40)
    
    
    def move(self, x:str = '0', y:str = '0', speed:str = '0', angle:str = '0'):
        self.__comprobe_restrictions(x, y, speed, angle)
        data = [
            Command.MOVE.value,
            GaitMode.MODE_1.value,
            x, y, speed, angle
            ]
    
    
    def giro_cabeza(self):
          self.c.servo.setServoAngle(0,90)
          time.sleep(0.2)
          for i in range(11):
              angulo = 45 + (i * 10 if i != 0 else 0)
              self.c.servo.setServoAngle(0,angulo)                    
              time.sleep(0.2)
          for i in range(11):
              angulo = 135 - (i * 10 if i != 0 else 0)
              self.c.servo.setServoAngle(0,angulo)                    
              time.sleep(0.2)
          self.c.servo.setServoAngle(0,94)    
    
    
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
          ###pata derecha delantera hacia adelante
          x = np.arange(90,140,2)
          y = np.arange(90,50,-2)
          z = np.arange(140,90,-2)
          for i in x:# pata se eleva para moverse
              #print(i)
              self.c.servo.setServoAngle(14,i)
              time.sleep(0.01)
          for i in y:# pata se mueve hacia adelante
              #print(i)
              self.c.servo.setServoAngle(15,i)
              time.sleep(0.01)  
          for i in z: # pata se hacienta en suelo
              #print(i)
              self.c.servo.setServoAngle(14,i)
              time.sleep(0.01)
    def pata_izquierda_del_adelante(self):
         ####pata izquierda delantera hacia delante
          x = np.arange(90,50,-2)
          y = np.arange(90,130,2)
          z = np.arange(50,90.2)
          for i in x: # pata se eleva para moverse
              self.c.servo.setServoAngle(17,i)
              time.sleep(0.01)
          for i in y: # pata se mueve hacia adelante   
              self.c.servo.setServoAngle(16,i)
              time.sleep(0.01)
          for i in z: # pata se hacienta en suelo   
              self.c.servo.setServoAngle(17,i)
              time.sleep(0.01)
    def pata_central_derecha_adelante(self):
          ####pata central derecha hacia adelante
          x = np.arange(90,140,2)
          y = np.arange(90,50,-2)
          z = np.arange(140,90,-2)
          for i in x:  # pata se eleva para moverse
              self.c.servo.setServoAngle(11,i)
              time.sleep(0.01)
          for i in y:  # pata se mueve hacia adelante
              self.c.servo.setServoAngle(12,i)
              time.sleep(0.01)    
          for i in z:  # pata se hacienta en suelo
              self.c.servo.setServoAngle(11,90)
              time.sleep(0.01)
    def pata_central_izquierda_adelante(self):
     ####pata central izquierda hacia adelante
          x = np.arange(90,50,-2)
          y = np.arange(90,150,2)
          z = np.arange(50,90,2)
          for i in x: # pata se eleva para moverse
              self.c.servo.setServoAngle(20,i)
              time.sleep(0.01)
          for i in y: # pata se mueve hacia adelante
              self.c.servo.setServoAngle(19,i)
              time.sleep(0.01)
          for i in z: # pata se hacienta en suelo    
              self.c.servo.setServoAngle(20,i)
              time.sleep(0.01)
    def pata_del_derecha_levantar(self):
         ####levantamiento de pata delantera derecha
          x = np.arange(90,140,2)
          y = np.arange(90,50,-2)
          z = np.arange(90,0,-2)
          for i in x: # pata se eleva  
              self.c.servo.setServoAngle(14,i)
              time.sleep(0.01)
          for i in y: # pata se va hacia adelante
              self.c.servo.setServoAngle(15,i)
              time.sleep(0.01)
          for i in z: # pata se extira
              self.c.servo.setServoAngle(13,i)
              time.sleep(0.01)
    def pata_del_izquierda_levantar(self):
          ####levantamiento de pata delantera izquierda
          x = np.arange(90,50,-2)
          y = np.arange(90,130,2)
          z = np.arange(90,200,2)
          for i in x: # pata se eleva
              self.c.servo.setServoAngle(17,i)
              time.sleep(0.01)
          for i in y: # pata se va hacia adelante
              self.c.servo.setServoAngle(16,i)
              time.sleep(0.01)
          for i in z: # pata se extira
              self.c.servo.setServoAngle(18,i)
              time.sleep(0.01)
    
    def baile_1(self): #Es un movimiento circular en el plano x,y, ademas de moverser formando un onda en el ejes z
          r=40
          theta= np.linspace(0,2* np.pi*2,100)
          self.altura()
          for t in theta:
 
            x = r*np.cos(t)
            y = r*np.sin(t)
            z = r/3*np.cos(-t*3)
            
            print("sexo")
            self.c.posittion(x,y,z)
   
          print("fin")    
    
    
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
   
        for i in range(1):
            self.altura()
            self.avance_en_diagonal_adelante_derecha()
            self.avance_en_diagonal_atras_izquierda()
            self.giro_cabeza()
            self.avance_en_diagonal_adelante_izquierda()
            self.avance_en_diagonal_atras_derecha()
            self.giro_cabeza()
        self.altura() 
        print("fin")  
    
    
    def baile_4(self): # Estes baile consiste de movimiento de la parte trasera del robot
          self.altura()
          punto=self.c.postureBalance(0,0,0)
          self.c.coordinateTransformation(punto)
          self.c.setLegAngle()
          for i in range(4):
              
              time.sleep(0.2)        
              punto=self.c.postureBalance(0,15,15)
              self.c.coordinateTransformation(punto)
              self.c.setLegAngle()
              time.sleep(0.2)
              punto=self.c.postureBalance(0,15,-15)
              self.c.coordinateTransformation(punto)
              self.c.setLegAngle()
              time.sleep(0.2)
          punto=self.c.postureBalance(0,0,0)
          self.c.coordinateTransformation(punto)
          self.c.setLegAngle()
          print("fin")
    
    
    def baile_5 (self):
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
          print("fin")       