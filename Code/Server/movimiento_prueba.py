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
    
#####################################################    
    
    def baile_1(self):
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
    
    
    
          
          
####################################################                
    def baile_2(self):
          x = "30"
          y = "0"
          z = "0"
          speed = "10"
          angle = "0"
          ctrl.altura()
          ctrl.move(x, y, speed, angle)
          ctrl.move(x, y, speed, angle)
          ctrl.move(x, y, speed, angle)
          ctrl.move(x, y, speed, angle)
          ctrl.move("-30",y,speed, angle)
          ctrl.move("-30",y,speed, angle)
          ctrl.move("-30",y,speed, angle)
          ctrl.move("-30",y,speed, angle)


#####################################################    
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
#######################################################    
    
    def  baile_3(self):
   
        for i in range(1):
            self.altura()
            ctrl.move("-20","20","10","0")
            ctrl.move("-20","20","10","0")
            ctrl.move("-20","20","10","0")
            ctrl.move("20","-20","10","0")
            ctrl.move("20","-20","10","0")
            ctrl.move("20","-20","10","0")
            self.giro_cabeza()
            ctrl.move("20","20","10","0")
            ctrl.move("20","20","10","0")
            ctrl.move("20","20","10","0")
            ctrl.move("-20","-20","10","0")
            ctrl.move("-20","-20","10","0")
            ctrl.move("-20","-20","10","0")
            self.giro_cabeza()
        self.altura()
        
#####################################################        
    def baile_4(self):
          #self.altura()
          #self.c.posittion(0,-40,20)
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
################################################
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








###################################################                
    def altura(self):
          self.c.posittion(0,0,40)

##################################################
          
    def pata_derecha_del_adelante(self):  
          ###pata derecha delantera hacia adelante
          ctrl.c.servo.setServoAngle(14,140)
          time.sleep(0.2)
          ctrl.c.servo.setServoAngle(15,50)
          time.sleep(0.2)
          ctrl.c.servo.setServoAngle(14,90)
          time.sleep(0.2)

###################################################

    def pata_izquierda_del_adelante(self):
         ####pata izquierda delantera hacia delante
          ctrl.c.servo.setServoAngle(17,50)
          time.sleep(0.5)
          ctrl.c.servo.setServoAngle(16,130)
          time.sleep(0.5)
          ctrl.c.servo.setServoAngle(17,90)

##################################################

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




if __name__ == '__main__':
    ctrl = Ctrl()
    buzzer = Sound()
    ##buzzer.play()
    #ctrl.baile_1()
    #ctrl.baile_2()
    # Play the first few notes of a familiar song (replace with the actual sequence)
    #control = Control()
    #control.servo.setServoAngle(0,90)
    ctrl.altura()
    #time.sleep(2)
    
    
    #ctrl.baile_1()
    #ctrl.baile_2()
    #ctrl.baile_3()
    #ctrl.baile_4()
    #time.sleep(1.4)
    
    ctrl.baile_5()
    #ctrl.altura()

    ####patas izquierdas
    #ctrl.c.servo.setServoAngle(17,70)
    #time.sleep(0.1)
    #ctrl.c.servo.setServoAngle(16,140)
    #ctrl.c.servo.setServoAngle(20,300)
    #time.sleep(0.1)
    #ctrl.c.servo.setServoAngle(19,130)
    ###########
    #ctrl.c.servo.setServoAngle(14,260)
    #time.sleep(0.1)
    #ctrl.c.servo.setServoAngle(15,60)
    #ctrl.altura()
    #ctrl.c.servo.setServoAngle(12,30)
    #ctrl.c.servo.setServoAngle(11,160)
    #ctrl.c.servo.setServoAngle(10,0)
    #ctrl.c.servo.setServoAngle(19,130)
    #ctrl.c.servo.setServoAngle(20,340)
    #ctrl.c.servo.setServoAngle(21,180)
    #time.sleep(1.4)

    #ctrl.altura()
    #x = "30"
    #y = "0"
    #z = "0"
    #speed = "10"
    #angle = "0"
    #ctrl.altura()
    #ctrl.move(x, y, speed, angle)
    #ctrl.move(x, y, speed, angle)
    #ctrl.move(x, y, speed, angle)
    #ctrl.move(x, y, speed, angle)
    #ctrl.move("-30",y,speed, angle)
    #ctrl.move("-30",y,speed, angle)
    #ctrl.move("-30",y,speed, angle)
    #ctrl.move("-30",y,speed, angle)
    
    ##ctrl.relajar()
    ##ctrl.relajar()
    ##ctrl.inlinacion()


    ##ctrl.position("10","0","0")
    ##ctrl.position("20","0","0")
    ##ctrl.position("40","-2","20")
