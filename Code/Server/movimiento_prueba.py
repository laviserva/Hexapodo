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
    def  baile_3(self):
   
        for i in range(2):
            self.altura()
            ctrl.move("20","20","10","0")
            ctrl.move("20","20","10","0")
            self.giro_cabeza()
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
                
    def altura(self):
          self.c.posittion(0,0,20)

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

    #ctrl.baile_1()
    #ctrl.baile_2()
    #ctrl.baile_3()
    ctrl.baile_4()
    #time.sleep(1.4)
    #ctrl.c.servo.setServoAngle(14,160)
    #ctrl.c.servo.setServoAngle(13,0)

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
