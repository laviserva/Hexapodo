
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
        if isinstance(option, dict):
            self.options.append(option)

    def get(self):
        return self.options


class Environment:
    def __init__(self, restart=False):
        self.buddy_here = False
        self.buddy_knows = False
        self.buddy_finish1 = False
        self.buddy_finish2 = False

        if restart is True:
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

    def percieve(self, environment):
        # Aquí se percibe el entorno y utiliza el BRF para actualizar la lista de beliefs

        if environment.buddy_here is True:
            self.beliefs.add_belief("acompañado", True)
        if environment.buddy_knows is True:
            self.beliefs.add_belief("compa_enterado", True)
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
            self.beliefs.add_belief("he terminado", True)

    def generate_options(self):
        # Se generan las opciones (no se evalúan aún) con base en la lista de beliefs
        options = []
        if "acompañado" in self.beliefs.get("acompañado") is True:
            options.append({"name": "establecer_consenso", "conflicts": ["temrinar_programa", "stop"]})
        else:
            options.append({"name": "buscar_compañero", "conflicts": ["stop"]})

        if self.beliefs.get("puedo_terminar") is False:
            options.append({"name": "stop", "conflicts": ["ejecutar_subrutina1", "ejecutar_subrutina2",
                                                          "buscar_compañero", "establecer_consenso"]})

        if self.beliefs.get("compañero_enterado") is True:
            options.append({"name": "ejecutar_subrutina1", "conflicts": ["stop"]})

        if self.beliefs.get("terminamos_parte1") is True:
            options.append({"name": "ejecutar_subrutina2", "conflicts": ["stop"]})

        if self.beliefs.get("terminamos_parte2") is True:
            options.append({"name": "buscar_compañero", "conflicts": ["terminar_programa", "stop"]})

        if self.beliefs.get("puedo terminar") is False:
            options.append({"name": "terminar_programa", "conflicts": ["ejecutar_subrutina1", "ejecutar_subrutina2",
                                                                        "buscar_compañero", "establecer_consenso"]})
        return options


if __name__ == "__main__":

    h1 = BDIAgent(0, 20000)
    env = Environment()
    h1.percieve(env)
    print(h1.beliefs)
    env.buddy_here = True
    h1.percieve(env)
    print(h1.generate_options())
