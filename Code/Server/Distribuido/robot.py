import math
import sys
from pathlib import Path

current_dir = Path(__file__).parent.absolute()
server_dir = current_dir.parent
server_dir_2 = current_dir.parent / "Server"
print(server_dir)
sys.path.append(str(server_dir))
sys.path.append(str(server_dir_2))

import time
from enum import Enum

from Servo import Servo
from Control import Control
from Buzzer import Buzzer
from ADC import ADC
from Ultrasonic import Ultrasonic as U

from camera import CameraSingletonFactory as C
from camera import ImageProcessor

class Camera:
    
    def __init__(self, res = (640, 480)):
        self.camera = C.get_camera("RGB888", res)
    
    def capture_image(self):
        return self.camera.capture_image_as_array()
    
    def get_video_frames(self):
        return self.camera.get_video_frames()
    
    def save_image(self, filename="image.jpg"):
        image_array = self.capture_image()
        ImageProcessor.save_image(image_array, filename)

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
            cls._isinstance.ultrasonic = U()
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
    
    def play_victory(self):
        self.play_note(0.05)
        self.play_note(0.05)
        self.play_note(0.05)
        self.play_note(0.075)
        time.sleep(0.1)

class Ctrl:
    SPEED_CAP = "7"

    def __init__(self):
        self.c = Control()
        self.s = Servo()
        self.u = Ultrasonic()
    
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
    
    def avanzar(self, cm: str):
        print(f"Avanzando {cm} cm")
        cm = float(cm)
        move_cap = 7.5
        x, y, speed, angle = "0", "27", self.SPEED_CAP, "0"
        
        data = {}
        n = math.floor(cm / move_cap)
        r = cm % move_cap

        print(f"n: {n}, r: {r}")
        for _ in range(n):
            # data=['CMD_MOVE', '1', '0', '25', '10', '0']
            data=["CMD_MOVE", '1', x, y, speed, angle]
            print(data)
            self.c.run(data)
        print("Se ejecuto el for de avanzar")
        
        self.stop()
        
        return data
    
    def detectar_obstaculo(self, threshold: float=30.0):
        threshold = float(threshold)
        if float(self.u.get_distance()) < threshold:
            return True
        return False
    
    def avanzar_hasta_obstaculo(self, threshold: float = 30.0, cont_verify: int = 5):
        print("\n\nAvanzando...")
        distance = self.u.get_distance()

        # Primer bucle: espera a obtener una lectura de distancia no cero
        while distance == 0:
            distance = self.u.get_distance()
            print("Distance: ", distance)

        # Segundo bucle: avanza hasta que se detecte un obstáculo o la distancia sea 0 de nuevo
        while distance >= threshold and distance != 0:
            print(f"\t Distancia actual: {distance} vs Umbral: {threshold}")
            if distance < threshold:
                print("Obstáculo detectado a menos de", threshold, "unidades")
                return True
            self.avanzar('7.5')
            distance = self.u.get_distance()

        print("Finalizado, no se detectaron obstáculos dentro del umbral")
        return False

    
    def girar(self, grados_f: str):
        move_cap = 45
        grados = abs(float(grados_f))

        if float(grados_f) >= 0:
            x, y, speed, angle = "0", "0", self.SPEED_CAP, "14"
            n = math.floor(grados / move_cap)
            r = abs(grados % move_cap)
        else:
            x, y, speed, angle = "0", "0", self.SPEED_CAP, "-14"
            n = math.ceil(grados / move_cap)
            r = -abs(grados % move_cap)

        data = {}
        print('ulti')
        print(f"n: {n}, r: {r}, grados{grados}, grados_f{grados_f}, angle {angle}")

        for _ in range(n):
            data=["CMD_MOVE", '1', x, y, speed, angle]
            print(data)
            self.c.run(data)
        
        if r != 0:
            correction = math.floor(14 * r/move_cap)
            if correction == 0:
                correction = 1
            print(f"Correción: {correction}, r: {r}")
            data=["CMD_MOVE", '1', x, y, speed, str(int(correction))]
            print(data)
            self.c.run(data)
        
        self.stop()
        
        return data

    def move(self, x:str = '0', y:str = '0', speed:str = '0', angle:str = '0'):
        print(f"Moving to x={x}, y={y}, speed={speed}, angle={angle}")
        #self.__comprobe_restrictions(x, y, speed, angle)
        
        data = [
            Orders.MOVE.value,
            GaitMode.MODE_1.value,
            x, y, speed, angle
            ]
        #print("Data: ", data)
        #data=['CMD_RELAX']
        self.c.run(data)
        #self.stop()

    def stop(self):
        data = [
            Orders.RELAX.value
            ]
        self.c.run(data)
    
    def handle_attitude_command(self, r, p, y):
        """Adjust the robot's attitude based on roll (r), pitch (p), and yaw (y) values."""
        r = self.c.restriction(int(r), -15, 15)
        p = self.c.restriction(int(p), -15, 15)
        y = self.c.restriction(int(y), -15, 15)
        point = self.c.postureBalance(r, p, y)
        self.c.coordinateTransformation(point)
        self.c.setLegAngle()

    def handle_position_command(self, x, y, z):
        """Adjust the robot's position based on coordinates x, y, z."""
        x = self.c.restriction(int(x), -40, 40)
        y = self.c.restriction(int(y), -40, 40)
        z = self.c.restriction(int(z), -20, 20)
        self.c.posittion(x, y, z)

    def handle_head_command(self, x, y):
        """Adjust the robot's head based on coordinates x, y."""
        self.s.setServoAngle(int(x), int(y))

    def move(self, x='0', y='0', speed='0', angle='0'):
        if speed >= self.SPEED_CAP:
            speed = self.SPEED_CAP
        print(f"Moving to x={x}, y={y}, speed={speed}, angle={angle}")
        data = [Orders.MOVE.value, GaitMode.MODE_1.value, x, y, speed, angle]
        print("Data: ", data)
        self.c.run(data)
        self.stop()

    def stop(self):
        data = [Orders.MOVE.value, GaitMode.MODE_1.value, '0', '0', '0', '0']
        self.c.run(data)

    def head(self, x='0', y='0'):
        self.handle_head_command(x, y)

    def position(self, x='0', y='0', z='0'):
        self.handle_position_command(x, y, z)

    def attitude(self, r='0', p='0', y='0'):
        self.handle_attitude_command(r=r, p=p, y=y)

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
    
if __name__ == "__main__":
    # Initialize the controller
    ctrl = Ctrl()

    # Example usage of head command
    print("Testing head movement...")
    ctrl.head(x='0', y='90')  # Adjust the robot's head to 90 degrees horizontal and 90 degrees vertical
    time.sleep(1)  # Pause to observe the action
    print("Testing head movement...")
    time.sleep(1)
    ctrl.head(x='0', y='0')  # Adjust the robot's head to 90 degrees horizontal and 90 degrees vertical
    print("Testing head movement...")
    time.sleep(1)
    for i in range(0,90,15):
        ctrl.head(x='0', y=str(i))
    print("Testing head movement...")
    time.sleep(1)
    for i in range(0,90,15):
        ctrl.head(x="1", y=str(i))
    print("Testing head movement...")
    time.sleep(1)

    # Example usage of position command
    print("Changing position...")
    ctrl.positions(x='20', y='15', z='5')  # Adjust the robot's position
    time.sleep(1)  # Pause to observe the action

    # Example usage of attitude command
    print("Adjusting attitude...")
    ctrl.attitude(r='10', p='5', y='3')  # Adjust the robot's roll, pitch, and yaw
    time.sleep(1)  # Pause to observe the action

    print("All commands executed.")