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
        if speed <= 1 or speed >= 10:
            raise ValueError(f"Argumento speed={speed} debe de estar en el intervalo 1 <= x <= 10")
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
          Command.POSITION.value
          data = ["CMD_POSITION","1","0","10","0","0"]
          r=40
          theta= np.linspace(0,2* np.pi*2,100)
          for t in theta:
 
            x = r*np.cos(t)
            y = r*np.sin(t)
            z = r/3*np.cos(-t*3)
            
            print("sexo")
            self.c.posittion(x,y,z)
            #time.sleep(0.1) 
          #self.c.posittion(30,-30,0)
          #self.c.posittion(30,-30,0)  
          print("fin")
    def inlinacion(self):
          Command.POSTURA.value
          data = ["CMD_ATTITUDE","0","-15","0"]
          print("reverancia")
          r = 0
          p = 0
          y = 10
          self.c.postureBalance(r,p,y)
    def relajar(self):
          Command.RELAX.value
          self.c.relax(True)
          print("relajado")

if __name__ == '__main__':
    ctrl = Ctrl()
    buzzer = Sound()
    ##buzzer.play()
    
    # Play the first few notes of a familiar song (replace with the actual sequence)
    

    x = "20"
    y = "20"
    z = "30"
    speed = "7"
    angle = "0"
    ctrl.baile_1()
    ##ctrl.relajar()
    ctrl.inlinacion()
    ##ctrl.move(x, y, speed, angle)
    ##ctrl.position(x,y,z)
    ##ctrl.position("10","0","0")
    ##ctrl.position("20","0","0")
    ##ctrl.position("40","-2","20")
