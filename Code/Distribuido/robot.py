import sys
from pathlib import Path

current_dir = Path(__file__).parent.absolute()
server_dir = current_dir.parent
print(server_dir)
sys.path.append(str(server_dir))

import time
from enum import Enum

from Control import Control
from Buzzer import Buzzer
from ADC import ADC
from Ultrasonic import Ultrasonic

class Battery:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Battery, cls).__new__(cls)
            cls._instance.adc = ADC()
        return cls._instance

    def get_power(self) -> tuple[float, float]:
        return self.adc.batteryPower()
    
    def __str__(self):
        return f"[Voltaje]: {self.get_power():.2f}"
    
    def __gt__(self, other: float):
        s1, s2 = self.get_power()
        return s1 > other, s2 > other
    
    def __lt__(self, other: float):
        s1, s2 = self.get_power()
        return s1 < other, s2 < other
    
    def __ge__(self, other: float):
        s1, s2 = self.get_power()
        return s1 >= other, s2 >= other
    
    def __le__(self, other: float):
        s1, s2 = self.get_power()
        return s1 <= other, s2 <= other

class Ultrasonic:
    _isinstance = None

    def __new__(cls):
        if cls._isinstance is None:
            cls._isinstance = super(Ultrasonic, cls).__new__(cls)
            cls._isinstance.ultrasonic = Ultrasonic()
        return cls._isinstance
    
    def get_distance(self) -> float:
        return self.ultrasonic.getDistance()
    
    def __str__(self):
        return f"[Distancia]: {self.get_distance():.2f}"
    
    def __gt__(self, other: float):
        return self.get_distance() > other
    
    def __lt__(self, other: float):
        return self.get_distance() < other
    
    def __ge__(self, other: float):
        return self.get_distance() >= other
    
    def __le__(self, other: float):
        return self.get_distance() <= other

class Orders(Enum):
    MOVE = 'CMD_MOVE'
    BALANCE = 'CMD_BALANCE'
    HEAD = 'CMD_HEAD'
    POSITIONS = 'CMD_POSITIONS'
    ATTITUDE = 'CMD_ATTITUDE'
    RELAX = 'CMD_RELAX'

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
    
    def __comprobe_restrictions(self, x: str, y: str, speed: str, angle: str):
        x = int(x)
        y = int(y)
        speed = int(speed)
        angle = int(angle)

        if x <= -35 or x >= 35:
            raise ValueError(f"Argumento x={x} debe de estar en el intervalo -35 <= x <= 35")
        if y <= -35 or y >= 35:
            raise ValueError(f"Argumento y={y} debe de estar en el intervalo -35 <= x <= 35")
        if speed < 1 or speed > 10:
            raise ValueError(f"Argumento speed={speed} debe de estar en el intervalo 1 <= x <= 10")
        if angle <= -35 or angle >= 35:
            raise ValueError(f"Argumento angle={angle} debe de estar en el intervalo -35 <= x <= 35")

    def move(self, x:str = '0', y:str = '0', speed:str = '0', angle:str = '0'):
        print(f"Moving to x={x}, y={y}, speed={speed}, angle={angle}")
        #self.__comprobe_restrictions(x, y, speed, angle)
        
        data = [
            Orders.MOVE.value,
            GaitMode.MODE_1.value,
            x, y, speed, angle
            ]
        print("Data: ", data)
        # data=['CMD_MOVE', '1', '0', '25', '10', '0']
        self.c.run(data)
        self.stop()

    def stop(self):
        data = [
            Orders.MOVE.value,
            GaitMode.MODE_1.value,
            '0', '0', '0', '0'
            ]
        self.c.run(data)
    
    def balance(self):
        data = [
            Orders.BALANCE.value,
            GaitMode.MODE_1.value
            ]
        self.c.run(data)

    def head(self, x:str = '0', y:str = '0'):
        # CMD_HEAD#1#90 # Horizontal
        # CMD_HEAD#0#90 # Vertical
        data = [
            Orders.HEAD.value,
            x, y
            ]
        self.c.run(data)

    def positions(self, x:str = '0', y:str = '0', z:str = '0'):
        # CMD_POSITION#22#14#0
        data = [
            Orders.POSITIONS.value,
            x, y, z
            ]
        self.c.run(data)
    
    def attitude(self, x:str = '0', y:str = '0', z:str = '0'):
        # CMD_ATTITUDE#0#0#0
        data = [
            Orders.ATTITUDE.value,
            x, y, z
            ]
        self.c.run(data)




class Commands_available:
    def __init__(self):
        self.__init_commands([Ctrl, Sound])
    
    def __init_commands(self, classes):
        for class_ in classes:
            for method_name in dir(class_):
                if not method_name.startswith('_') and callable(getattr(class_, method_name)):
                    setattr(self, f"{class_.__name__.lower()}-{method_name}", getattr(class_(), method_name))
    
    def get_commands(self):
        out = dir(self)
        out.pop(out.index('get_commands'))
        out.pop(out.index('prepare_command'))
        return [x for x in out if (not x.startswith('_'))]
    
    def prepare_command(self, command: str):
        return command.replace('-', '.')