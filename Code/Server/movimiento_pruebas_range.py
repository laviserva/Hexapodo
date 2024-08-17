from enum import Enum, auto
import time
from Control import Control
from Buzzer import Buzzer
import numpy as np
class Command(Enum):
    MOVE = 'CMD_MOVE'
    POSITION = 'CMD_POSITION'
    POSTURA = 'CMD_ATTITUDE'
    RELAX= 'CMD_RELAX'
class GaitMode(Enum):
    MODE_1 = '1'
    MODE_2 = '2'

class Sound:
    def __init__(self) -> None:
        self.buzzer = Buzzer()
    
    def play_note(self, duration):
        self.buzzer.run('1')
        time.sleep(duration)
        self.buzzer.run('0')
        time.sleep(duration)
    
    def play(self):
        self.play_note(0.1)
        self.play_note(0.1)
        self.play_note(0.1)
        self.play_note(0.1)
        self.play_note(0.3)
        self.play_note(0.3)
        self.play_note(0.2)
        time.sleep(0.2)
        self.play_note(0.1)
        self.play_note(0.1)
        self.play_note(0.1)
        self.play_note(0.1)
        self.play_note(0.3)
        self.play_note(0.3)
        self.play_note(0.1)
        time.sleep(0.05)
        self.play_note(0.1)
        self.play_note(0.1)



class Ctrl:
    def __init__(self):
        self.c = Control()
        self.data = []
    
    def __comprobe_restrictions(self, x: str, y: str, speed: str, angle: str):
        x = int(x)
        y = int(y)
        speed = int(speed)
        angle = int(angle)

        if x <= -35 or x >= 35:
            raise ValueError(f"Argumento x={x} debe de estar en el intervalo -35 <= x <= 35")
        if y <= -35 or y >= 35:
            raise ValueError(f"Argumento y={y} debe de estar en el intervalo -35 <= x <= 35")
        if angle <= -35 or angle >= 35:
            raise ValueError(f"Argumento angle={angle} debe de estar en el intervalo -35 <= x <= 35")

    def move(self, x:str = '0', y:str = '0', speed:str = '0', angle:str = '0'):
        self.__comprobe_restrictions(x, y, speed, angle)
        data = [
            Command.MOVE.value,
            GaitMode.MODE_1.value,
            x, y, speed, angle
            ]
        
        self.c.run(data)
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
    def baile_2(self):  #Es un movimiento lateral de izquierda a derecha 
          speed = "10"
          angle = "0"
          ctrl.altura()
          ctrl.move("30","0", speed, angle)
          ctrl.move("30","0", speed, angle)
          ctrl.move("30","0", speed, angle)
          ctrl.move("30","0", speed, angle)
          ctrl.move("-30","0",speed, angle)
          ctrl.move("-30","0",speed, angle)
          ctrl.move("-30","0",speed, angle)
          ctrl.move("-30","0",speed, angle)    
          print("fin")
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
    def  baile_3(self): #Es un movimiento en diagonal hacia adelante y atras en ambos lados izquierda y derecha en cada retorno al punto inicial se mueve el cuello de  robot
   
        for i in range(1):
            self.altura()
            self.avance_en_diagonal_adelante_derecha()
            ##avance en diagonal hacia la derecha adelante
            #ctrl.move("-20","20","10","0")
            #ctrl.move("-20","20","10","0")
            #ctrl.move("-20","20","10","0")
            self.avance_en_diagonal_atras_izquierda()
            ##avance en diagonal hacia atras a la izquierda
            #ctrl.move("20","-20","10","0")
            #ctrl.move("20","-20","10","0")
            #ctrl.move("20","-20","10","0")
            self.giro_cabeza()
            self.avance_en_diagonal_adelante_izquierda()
            ##avance en diagonal hacia la izquierda
            #ctrl.move("20","20","10","0")
            #ctrl.move("20","20","10","0")
            #ctrl.move("20","20","10","0")
            self.avance_en_diagonal_atras_derecha()
            ##avance en diagonal hacia atras ala derecha
            #ctrl.move("-20","-20","10","0")
            #ctrl.move("-20","-20","10","0")
            #ctrl.move("-20","-20","10","0")
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
          #ctrl.c.servo.setServoAngle(14,140)
          #time.sleep(0.5)
          #ctrl.c.servo.setServoAngle(15,50)
          #time.sleep(0.5)
          #ctrl.c.servo.setServoAngle(14,90)
          #time.sleep(0.5)
          ####pata izquierda delantera hacia delante
          self.pata_izquierda_del_adelante()
          #ctrl.c.servo.setServoAngle(17,50)
          #time.sleep(0.5)
          #ctrl.c.servo.setServoAngle(16,130)
          #time.sleep(0.5)
          #ctrl.c.servo.setServoAngle(17,90)
          ####pata central derecha hacia adelante
          self.pata_central_derecha_adelante()
          #ctrl.c.servo.setServoAngle(11,140)
          #time.sleep(0.5)
          #ctrl.c.servo.setServoAngle(12,30)
          #time.sleep(0.5)
          #ctrl.c.servo.setServoAngle(11,90)
          #time.sleep(0.5)
          ####pata central izquierda hacia adelante
          self.pata_central_izquierda_adelante()
          #ctrl.c.servo.setServoAngle(20,50)
          #time.sleep(0.5)
          #ctrl.c.servo.setServoAngle(19,150)
          #time.sleep(0.5)
          #ctrl.c.servo.setServoAngle(20,90)
          #time.sleep(0.5)
        ####levantamiento de pata delantera derecha
          self.pata_del_derecha_levantar()
        
          #ctrl.c.servo.setServoAngle(14,140)
          #time.sleep(0.1)
          #ctrl.c.servo.setServoAngle(15,50)
          #time.sleep(0.1)
          #ctrl.c.servo.setServoAngle(13,0)
        ####levantamiento de pata delantera izquierda
          self.pata_del_izquierda_levantar()
          #ctrl.c.servo.setServoAngle(17,50)
          #time.sleep(0.1)
          #ctrl.c.servo.setServoAngle(16,130)
          #time.sleep(0.1)
          #ctrl.c.servo.setServoAngle(18,180)
          #time.sleep(3)
          print("fin")                
    def altura(self):
          self.c.posittion(0,0,40)
          print("posicion de en alto")          
    def pata_derecha_del_adelante(self):  
          ###pata derecha delantera hacia adelante
          x = np.arange(90,140,10)
          y = np.arange(90,50,-10)
          z = np.arange(140,90,-10)
          #ctrl.c.servo.setServoAngle(14,140)
          #time.sleep(0.2)
          for i in x:
              print(i)
              ctrl.c.servo.setServoAngle(14,140)
              time.sleep(0.2)
          #ctrl.c.servo.setServoAngle(15,50)
          #time.sleep(0.2)
          for i in y:
              print(i)
              ctrl.c.servo.setServoAngle(15,i)
              time.sleep(0.2)  
          #ctrl.c.servo.setServoAngle(14,90)
          #time.sleep(0.2)
          for i in z:
              print(i)
              ctrl.c.servo.setServoAngle(14,i)
              time.sleep(0.2)
    def pata_izquierda_del_adelante(self):
         ####pata izquierda delantera hacia delante
          ctrl.c.servo.setServoAngle(17,50)
          time.sleep(0.5)
          ctrl.c.servo.setServoAngle(16,130)
          time.sleep(0.5)
          ctrl.c.servo.setServoAngle(17,90)
    def pata_central_derecha_adelante(self):
          ####pata central derecha hacia adelante
          ctrl.c.servo.setServoAngle(11,140)
          time.sleep(0.5)
          ctrl.c.servo.setServoAngle(12,30)
          time.sleep(0.5)
          ctrl.c.servo.setServoAngle(11,90)
          time.sleep(0.5)
    def pata_central_izquierda_adelante(self):
     ####pata central izquierda hacia adelante
          ctrl.c.servo.setServoAngle(20,50)
          time.sleep(0.5)
          ctrl.c.servo.setServoAngle(19,150)
          time.sleep(0.5)
          ctrl.c.servo.setServoAngle(20,90)
          time.sleep(0.5)
    def pata_del_derecha_levantar(sefl):
         ####levantamiento de pata delantera derecha
          ctrl.c.servo.setServoAngle(14,140)
          time.sleep(0.1)
          ctrl.c.servo.setServoAngle(15,50)
          time.sleep(0.1)
          ctrl.c.servo.setServoAngle(13,0)
    def pata_del_izquierda_levantar(self):
          ####levantamiento de pata delantera izquierda
          ctrl.c.servo.setServoAngle(17,50)
          time.sleep(0.1)
          ctrl.c.servo.setServoAngle(16,130)
          time.sleep(0.1)
          ctrl.c.servo.setServoAngle(18,180)
          time.sleep(3)
    def avance_en_diagonal_adelante_derecha(self):
    ##avance en diagonal hacia la derecha adelante
        ctrl.move("-20","20","10","0")
        ctrl.move("-20","20","10","0")
        ctrl.move("-20","20","10","0")
    def avance_en_diagonal_atras_izquierda(self):
    ##avance en diagonal hacia atras a la izquierda
        ctrl.move("20","-20","10","0")
        ctrl.move("20","-20","10","0")
        ctrl.move("20","-20","10","0")
    def avance_en_diagonal_adelante_izquierda(self):
    ##avance en diagonal hacia la izquierda
        ctrl.move("20","20","10","0")
        ctrl.move("20","20","10","0")
        ctrl.move("20","20","10","0")
    def avance_en_diagonal_atras_derecha(self):
     ##avance en diagonal hacia atras ala derecha
        ctrl.move("-20","-20","10","0")
        ctrl.move("-20","-20","10","0")
        ctrl.move("-20","-20","10","0")    
        


if __name__ == '__main__':
    ctrl = Ctrl()
    buzzer = Sound()
    ##buzzer.play()
    # Play the first few notes of a familiar song (replace with the actual sequence)
    #control = Control()
    #control.servo.setServoAngle(0,90)
    #ctrl.altura()
    #time.sleep(2)
    #ctrl.baile_1()
    #ctrl.baile_2()
    #ctrl.baile_3()
    #ctrl.baile_4()
    #time.sleep(1.4)
    #ctrl.baile_5()
    #ctrl.altura()
    ctrl.pata_derecha_del_adelante()
    

    
