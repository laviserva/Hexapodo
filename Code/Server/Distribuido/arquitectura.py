
"""Esqueleto del programa"""


class Beliefs:
    # Clase Beliefs
    def __init__(self, initial_beliefs=None):
        if initial_beliefs is None:
            initial_beliefs = {}
        self.beliefs = initial_beliefs

    def add_belief(self, key, value):
        # Agrega beliefs y busca conflictos con los beliefs actuales, y los resuelve (este es el BRF)
        if key in self.beliefs:
            self.resolve_conflict(key, value)
        else:
            self.beliefs[key] = value

    def resolve_conflict(self, key, new_value):
        # Aquí se implementa parte de la BRF, busca conflictos con las creencias actuales al momento de agregar nuevas
        current_value = self.beliefs[key]
        if new_value != current_value:
            self.beliefs[key] = new_value

    def get(self, key):
        # Para consultar los beliefs actuales
        return self.beliefs.get(key, None)

    def __str__(self):
        #  imprime los beliefs
        return f"Beliefs({self.beliefs})"


class Options:
    # Clase opciones
    def __init__(self):
        self.options = []

    def add_option(self, option):
        # Agrega opciones
        if isinstance(option, dict):
            self.options.append(option)

    def get(self):
        # extrae las opciones del objeto
        return self.options

    def __str__(self):
        #  imprime las opciones
        return f"Options({self.options})"


class Desires:
    # Clase deseos
    def __init__(self):
        self.desires = {}

    def add_desire(self, key, value):
        # Agrega deseos
        self.desires[key] = value

    def remove_desire(self, key):
        # remueve deseos
        self.desires.pop(key)

    def get(self, key):
        # Para consultar alguno de los deseos actuales
        return self.desires.get(key, None)

    def get_allD(self):
        # Para consultar todos los deseos
        return self.desires

    def __str__(self):
        #  imprime los deseos
        return f"Desires({self.desires})"


class Intentions:
    # Clase intenciones, puede tener iniciones iniciales pero generalmente inicia vacía
    def __init__(self, initial_intentions=None):
        if initial_intentions is None:
            initial_intentions = {}
        self.intentions = initial_intentions

    def add_intention(self, key, value):
        # Agrega intención
        self.intentions[key] = value

    def remove_intention(self, key):
        # Remueve intención
        self.intentions.pop(key)

    def get(self, key):
        # Obtiene una intención particular
        return self.intentions.get(key, None)

    def get_allI(self):
        # Obtiene todas las intenciones
        return self.intentions

    def __str__(self):
        #  imprime las intenciones
        return f"Intentions({self.intentions})"


class Environment:
    # El entorno está compuesto por 4 variables que determinan el estado del sistema (que incluya a ambos robots
    # estas variables son: tengo un compañero, ambos sabemos la rutina, ambos terminamos la primer parte de la rutina
    # y ambos terminamos la segunda parte de la rutina. Estas variabls deben ser modificadas conforme los robots
    # realizan acciones, cada acción puede modificar alguna de estas variables o bien, algun estado interno
    def __init__(self):
        self.buddy_here = False
        self.buddy_knows = False
        self.buddy_finish1 = False
        self.buddy_finish2 = False


class BDIAgent:
    # Agente principal, ambos robots son instancias de esta clase
    def __init__(self, completions=0, energy=20000):
        # Estados internos del agente, serán modificados en algunas ocasiones dependiendo de las acciones de los
        # agentes
        self.beliefs = Beliefs({"acompañado": False, "puedo_terminar": True})  # base de creencias del agente
        self.completes = completions  # Cantidad de rutinas completadas exitosamente
        self.energy = energy  # Energía disponible del agente
        self.leader = False  # Indica si el agente es lider
        self.enough_batt = True  # I indica si la batería es suficiente para terminar su tarea
        self.tries = 0  # intentos en recibir rutina o en recibir ACK de recepción de rutina
        self.all_ok = True  # Indica si all está bien para poder proseguir, si no es así entonces debe abortar
        # lo que hace actualmente con el robot actual
        self.options = Options()  # base de opciones del agente
        self.desires = Desires()  # base de deseos del agente
        self.intentions = Intentions()  # base de intenciones del agente

    def percieve(self, environment):
        # Aquí se percibe el entorno y utiliza el BRF para actualizar la lista de beliefs

        if environment.buddy_here is True:
            self.beliefs.add_belief("acompañado", True)  # Creo que estoy acompñado
        if environment.buddy_knows is True:
            self.beliefs.add_belief("compañero_enterado", True)  # Creo que (independientemente del lider)
        # ambos sabemos la rutina a ejecutar
        if environment.buddy_finish1 is True:
            self.beliefs.add_belief("terminamos_parte1", True)  # Creo que ambos terminamos la subrutina 1
        if environment.buddy_finish2 is True:
            self.beliefs.add_belief("terminamos_parte2", True)  # Creo que ambos terminamos la subrutina 2

    def genbeliefs_fromstates(self):
        # Aquí mira los estados internos y utiliza el BRF para actualizar la lista de beliefs

        if self.tries == 3 or self.all_ok is False:
            # Si intenté 3 veces enviar o recibir la lista sin éxito o no he recibido confirmación del otro robot
            self.beliefs = Beliefs({"acompañado": False, "puedo_terminar": True})  # Creo que ya no estoy acompañado

        if self.enough_batt is False:
            # si no tengo batería suficiente para completar mi objetivo
            self.beliefs.add_belief("puedo_terminar", False)  # Creo que ya no puedo acabar

        if self.completes == 3:
            # Si ya he completado 3 rutinas exitosamente
            self.beliefs.add_belief("he_terminado", True)  # Creo que he terminado mi labor

    def generate_options(self, beliefs):
        # Se generan las opciones (sin evaluar) con base en la lista de beliefs,
        # OJO: LAS OPCIONES SE REINICIAN EN CADA CICLO

        # Cada opción tiene asociada una prioridad y una lista de conflictos
        if beliefs.get("acompañado") is True:
            # Si creo que estoy acompañado, tengo la opción de establecer
            # consenso (determinar lider + generarr/recibir rutina)
            self.options.add_option({"name": "establecer_consenso", "priority": 5,
                                     "conflicts": ["terminar_programa",
                                                   "abortar",
                                                   "ejecutar_subrutina1",
                                                   "ejecutar_subrutina2",
                                                   "buscar_compañero",
                                                   "enviar_confirmacion"]})
        else:
            # Si creo que no estoy acompañado, tengo la opcíón de seguir buscando compañero
            self.options.add_option({"name": "buscar_compañero", "priority": 4,
                                     "conflicts": ["terminar_programa",
                                                   "abortar",
                                                   "ejecutar_subrutina1",
                                                   "ejecutar_subrutina2",
                                                   "establecer_consenso",
                                                   "enviar_confirmacion"]})

        if beliefs.get("puedo_terminar") is False:
            # Si creo que no puedo terminar, tengo la opción de abortar
            self.options.add_option({"name": "abortar", "priority": 10,
                                     "conflicts": ["terminar_programa",
                                                   "ejecutar_subrutina1",
                                                   "ejecutar_subrutina2",
                                                   "buscar_compañero",
                                                   "establecer_consenso",
                                                   "enviar_confirmacion"]})

        if beliefs.get("compañero_enterado") is True:
            # Si creo que ambos conocemos la rutina, tengo la opción de ejecutar subrutina 1
            self.options.add_option({"name": "ejecutar_subrutina1", "priority": 7,
                                     "conflicts": ["terminar_programa",
                                                   "abortar",
                                                   "ejecutar_subrutina2",
                                                   "buscar_compañero",
                                                   "establecer_consenso"]})
            # y también tengo la opción de confirmar que terminé la subrutina
            self.options.add_option({"name": "enviar_confirmacion", "priority": 6,
                                     "conflicts": ["terminar_programa",
                                                   "abortar",
                                                   "buscar_compañero",
                                                   "establecer_consenso"]})

        if beliefs.get("terminamos_parte1") is True:
            # Si creo que ambos terminamos la subrutina 1, tengo la opción de ejecutar la subrutina 2
            self.options.add_option({"name": "ejecutar_subrutina2", "priority": 8,
                                     "conflicts": ["terminar_programa",
                                                   "abortar",
                                                   "ejecutar_subrutina1",
                                                   "buscar_compañero",
                                                   "establecer_consenso",
                                                   "reinicia_todo"]})
            # Y también tengo la opción de confirmar que terminé la subrutina
            self.options.add_option({"name": "enviar_confirmacion", "priority": 6,
                                     "conflicts": ["terminar_programa",
                                                   "abortar",
                                                   "buscar_compañero",
                                                   "establecer_consenso",
                                                   "reinicia_todo"]})

        if beliefs.get("terminamos_parte2") is True:
            # Si creo que ambos terminamos la subrutina 2, tengo la opcíón de reiniciar
            self.options.add_option({"name": "reinicia_todo", "priority": 9,
                                     "conflicts": ["ejecutar_subrutina1",
                                                   "ejecutar_subrutina2",
                                                   "terminar_programa",
                                                   "abortar",
                                                   "establecer_consenso",
                                                   "enviar_confirmacion"]})

        if beliefs.get("he_terminado") is True:
            # Si creo que ya he completado tres rutinas exitosamente, tengo la opción de terminar el programa
            self.options.add_option({"name": "terminar_programa", "priority": 10,
                                     "conflicts": ["ejecutar_subrutina1",
                                                   "ejecutar_subrutina2",
                                                   "buscar_compañero",
                                                   "establecer_consenso",
                                                   "enviar_confirmacion",
                                                   "reinicia_todo"]})

    def deliberate(self, options):
        # aquí se realiza la deliberación, se analizan todos las opciones generados y se identifican conflictos entre
        # ellos (por medio de prioridad, las opciones de mayor prioridad desplazan a las de manos prioridad)

        current_options = options.get()  # extrae el diccionario contenido en el objeto y lo almacena en las opciones
        # Actuales

        name_conf = {option["name"]: option["conflicts"] for option in current_options}  # relación nombre-conflicto
        name_prio = {option["name"]: option["priority"] for option in current_options}  # relación nombre-prioridad

        for option in current_options:  # agrega las opciones a la base de deseos del agente, junto con su prioridad
            self.desires.add_desire(option["name"], option["priority"])

        for option in name_conf.keys():
            for conflict in name_conf.values():
                # Encuentra las otras opciones con las que la función actual tiene conflicto, luego remueve
                # la opción actual si tiene prioridad menor
                if option in conflict:
                    key_conflict = next((k for k, v in name_conf.items() if v == conflict), None)

                    value1 = name_prio.get(option)  # Prioridad de la opción actual
                    value2 = name_prio.get(key_conflict)  # Prioridad de la opción en conflicto
                    """ 
                    # if env.buddy_finish2 is True and option == "reinicia_todo":
                    #    print("_____________")
                    #    print(key_conflict)
                    #    print("_____________")
                    #    print(value1)
                    #    print(value2)
                    """
                    if self.desires.get(option) and value1 < value2:  # Si la prioridad de la opción actual
                        # es menor que la opción en conflicto
                        self.desires.remove_desire(option)  # Remueve la opción acual de la base de deseos
        self.options = Options()  # UNA VEZ GENERADOS LOS DESEOS, BORRA LAS OPCIONES
        """
            print("-----------")
        print(name_conf.keys())

        print(self.desires)
        """

    def filter(self, desires, intentions):
        # La función de filtro toma en consideración los deseos recien generados con las intenciones que ya están en
        # Memoria, y genera nuevas intenciones

        current_desires = desires.get_allD()  # Obtiene todos los deseos
        current_intentions = intentions.get_allI()  # Obtiene todas las intenciones

        intention_keys = list(current_intentions.keys())  # Crea una lista de claves

        # Primero, elimina las intenciones conflictivas
        for des_name, des_prio in current_desires.items():
            for intention in intention_keys:
                if intention in current_intentions:  # Verifica que la intención existe
                    priority = current_intentions[intention]  # obtiene su prioridad
                    if des_prio > priority and self.intentions.get(intention):  # Compara la prioridad de el deseo
                        # actual con la proridad de la intención actual
                        self.intentions.remove_intention(intention)  # si la prioridad del deseo actual es mayor,
                        # remueve la intención actual

        # Luego, agrega nuevas intenciones
        for des_name, des_prio in current_desires.items():
            if des_name not in current_intentions:  # Si el deseo actual no está ya presente como intención
                self.intentions.add_intention(des_name, des_prio)  # Agrega el deseo actual como intención
        self.desires = Desires()  # UNA VEZ GENERADAS LAS INTECIONES, BORRA LOS DESEOS


    def bdi_cycle(self, envi):
        # Aquí se define el ciclo BDI, el agente percibe el entorno y monitorea sus estados internos,
        # luego genera las creencias usando la BRF, enseguida genera
        # las opciones y delibera para obtener los deseos, a partir de los deseos hace un filtrado considerando las
        # intenciones actuales y modifica las intenciones del agente, eso es la salida del BDI
        self.percieve(envi)
        self.genbeliefs_fromstates()
        print(self.beliefs)
        self.generate_options(beliefs=self.beliefs)
        # print(h1.options)
        self.deliberate(self.options)
        print(h1.desires)
        self.filter(self.desires, self.intentions)
        print(h1.intentions)


if __name__ == "__main__":

    h1 = BDIAgent(0, 20000)  # Crea el agente
    env = Environment()  # Crea el entorno

    h1.all_ok = True
    h1.completes = 1
    h1.enough_batt = True

    h1.bdi_cycle(env)

    env.buddy_here = True

    h1.bdi_cycle(env)

    env.buddy_knows = True

    h1.bdi_cycle(env)

    env.buddy_finish1 = True

    h1.bdi_cycle(env)

    env.buddy_finish2 = True

    h1.bdi_cycle(env)

    env = Environment()
    h1.beliefs = Beliefs({"acompañado": False, "puedo_terminar": True})
    h1.intentions = Intentions()

    h1.bdi_cycle(env)

    h1.enough_batt = False

    h1.bdi_cycle(env)
