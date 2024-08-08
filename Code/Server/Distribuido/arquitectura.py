
"""Esqueleto del programa"""


class Beliefs:
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
    def __init__(self):
        self.options = []

    def add_option(self, option):
        # Agrega opciones
        if isinstance(option, dict):
            self.options.append(option)

    def get(self):
        return self.options

    def __str__(self):
        #  imprime los beliefs
        return f"Options({self.options})"


class Desires:
    def __init__(self):
        self.desires = {}

    def add_desire(self, key, value):
        # Agrega deseos y busca conflictos con los beliefs actuales, y los resuelve (este es el BRF)
        self.desires[key] = value

    def remove_desire(self, key):
        # remueve deseos de la lista
        self.desires.pop(key)

    def get(self, key):
        # Para consultar los desires actuales
        return self.desires.get(key, None)

    def get_allD(self):

        return self.desires

    def __str__(self):
        #  imprime los desires
        return f"Desires({self.desires})"


class Intentions:
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
        return self.intentions.get(key, None)

    def get_allI(self):

        return self.intentions

    def __str__(self):
        #  imprime los intentions
        return f"Intentions({self.intentions})"


class Environment:
    def __init__(self):
        self.buddy_here = False
        self.buddy_knows = False
        self.buddy_finish1 = False
        self.buddy_finish2 = False


class BDIAgent:
    def __init__(self, completions=0, energy=20000):
        self.beliefs = Beliefs({"acompañado": False, "puedo_terminar": True})
        self.completes = completions
        self.energy = energy
        self.leader = False
        self.enough_batt = True
        self.tries = 0
        self.all_ok = True
        self.options = Options()
        self.desires = Desires()
        self.intentions = Intentions()

    def percieve(self, environment):
        # Aquí se percibe el entorno y utiliza el BRF para actualizar la lista de beliefs

        if environment.buddy_here is True:
            self.beliefs.add_belief("acompañado", True)
        if environment.buddy_knows is True:
            self.beliefs.add_belief("compañero_enterado", True)
        if environment.buddy_finish1 is True:
            self.beliefs.add_belief("terminamos_parte1", True)
        if environment.buddy_finish2 is True:
            self.beliefs.add_belief("terminamos_parte2", True)

    def genbeliefs_fromstates(self):
        # Aquí mira los estados internos y utiliza el BRF para actualizar la lista de beliefs
        if self.tries == 3 or self.all_ok is False:
            self.beliefs = Beliefs({"acompañado": False, "puedo_terminar": True})
        if self.enough_batt is False:
            self.beliefs.add_belief("puedo_terminar", False)
        if self.completes == 3:
            self.beliefs.add_belief("he_terminado", True)

    def generate_options(self, beliefs):
        # Se generan las opciones (sin evaluar) con base en la lista de beliefs

        # Cada opción tiene asociada una prioridad y una lista de conflictos
        if beliefs.get("acompañado") is True:
            self.options.add_option({"name": "establecer_consenso", "priority": 5,
                                     "conflicts": ["terminar_programa",
                                                   "abortar",
                                                   "ejecutar_subrutina1",
                                                   "ejecutar_subrutina2",
                                                   "buscar_compañero",
                                                   "enviar_confirmacion"]})
        else:
            self.options.add_option({"name": "buscar_compañero", "priority": 4,
                                     "conflicts": ["terminar_programa",
                                                   "abortar",
                                                   "ejecutar_subrutina1",
                                                   "ejecutar_subrutina2",
                                                   "establecer_consenso",
                                                   "enviar_confirmacion"]})

        if beliefs.get("puedo_terminar") is False:
            self.options.add_option({"name": "abortar", "priority": 10,
                                     "conflicts": ["terminar_programa",
                                                   "ejecutar_subrutina1",
                                                   "ejecutar_subrutina2",
                                                   "buscar_compañero",
                                                   "establecer_consenso",
                                                   "enviar_confirmacion"]})

        if beliefs.get("compañero_enterado") is True:
            self.options.add_option({"name": "ejecutar_subrutina1", "priority": 7,
                                     "conflicts": ["terminar_programa",
                                                   "abortar",
                                                   "ejecutar_subrutina2",
                                                   "buscar_compañero",
                                                   "establecer_consenso"]})

            self.options.add_option({"name": "enviar_confirmacion", "priority": 6,
                                     "conflicts": ["terminar_programa",
                                                   "abortar",
                                                   "buscar_compañero",
                                                   "establecer_consenso"]})

        if beliefs.get("terminamos_parte1") is True:
            self.options.add_option({"name": "ejecutar_subrutina2", "priority": 8,
                                     "conflicts": ["terminar_programa",
                                                   "abortar",
                                                   "ejecutar_subrutina1",
                                                   "buscar_compañero",
                                                   "establecer_consenso",
                                                   "reinicia_todo"]})
            self.options.add_option({"name": "enviar_confirmacion", "priority": 6,
                                     "conflicts": ["terminar_programa",
                                                   "abortar",
                                                   "buscar_compañero",
                                                   "establecer_consenso",
                                                   "reinicia_todo"]})

        if beliefs.get("terminamos_parte2") is True:
            self.options.add_option({"name": "reinicia_todo", "priority": 9,
                                     "conflicts": ["ejecutar_subrutina1",
                                                   "ejecutar_subrutina2",
                                                   "terminar_programa",
                                                   "abortar",
                                                   "establecer_consenso",
                                                   "enviar_confirmacion"]})

        if beliefs.get("he_terminado") is True:
            self.options.add_option({"name": "terminar_programa", "priority": 10,
                                     "conflicts": ["ejecutar_subrutina1",
                                                   "ejecutar_subrutina2",
                                                   "buscar_compañero",
                                                   "establecer_consenso",
                                                   "enviar_confirmacion",
                                                   "reinicia_todo"]})

    def deliberate(self, options):
        current_options = options.get()  # extrae el diccionario contenido en el objeto

        name_conf = {option["name"]: option["conflicts"] for option in current_options}  # nombre-conflicto
        name_prio = {option["name"]: option["priority"] for option in current_options}  # nombre-prioridad
        for option in current_options:
            self.desires.add_desire(option["name"], option["priority"])

        for option in name_conf.keys():
            for conflict in name_conf.values():
                if option in conflict:
                    key_conflict = next((k for k, v in name_conf.items() if v == conflict), None)

                    value1 = name_prio.get(option)
                    value2 = name_prio.get(key_conflict)
                    # if env.buddy_finish2 is True and option == "reinicia_todo":
                    #    print("_____________")
                    #    print(key_conflict)
                    #    print("_____________")
                    #    print(value1)
                    #    print(value2)
                    if self.desires.get(option) and value1 < value2:
                        self.desires.remove_desire(option)

            # print("-----------")
        # print(name_conf.keys())

        # print(self.desires)

    def filter(self, desires, intentions):
        current_desires = desires.get_allD()
        current_intentions = intentions.get_allI()

        intention_keys = list(current_intentions.keys())  # Crea una lista de claves

        # Primero, elimina las intenciones conflictivas
        for des_name, des_prio in current_desires.items():
            for intention in intention_keys:
                if intention in current_intentions:  # Verifica que la intención existe
                    priority = current_intentions[intention]
                    if des_prio > priority and self.intentions.get(intention):
                        self.intentions.remove_intention(intention)

        # Luego, agrega nuevas intenciones
        for des_name, des_prio in current_desires.items():
            if des_name not in current_intentions:
                self.intentions.add_intention(des_name, des_prio)
        self.desires = Desires()
        self.options = Options()

    def bdi_cycle(self, envi):
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

    h1 = BDIAgent(0, 20000)
    env = Environment()

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
