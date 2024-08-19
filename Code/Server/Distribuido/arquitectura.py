from typing import Dict, List, Optional

class BDI_Actions:
    ABORTAR = "abortar"
    ACOMPAÑADO = "acompañado"
    BUSCAR_COMP = "buscar_compañero"
    COMP_ENTERADO = "compañero_enterado"
    EJECUTAR_SUB1 = "ejecutar_subrutina1"
    EJECUTAR_SUB2 = "ejecutar_subrutina2"
    ENVIAR_CONF = "enviar_confirmacion"
    ESTABLECER_CONSENSO = "establecer_consenso"
    HE_TERMINADO = "he_terminado"
    PUEDO_TERMINAR = "puedo_terminar"
    TERMINA_PART1 = "terminamos_parte1"
    TERMINA_PART2 = "terminamos_parte2"

class Beliefs:
    """
    Inicializa los beliefs del agente.
    
    :param initial_beliefs: Diccionario opcional de creencias iniciales. Cada clave es una string y el valor es un booleano.
    """
    def __init__(self, initial_beliefs: Optional[Dict[str, bool]] = None) -> None:
        if initial_beliefs is None:
            initial_beliefs = {}
        self.beliefs: Dict[str, bool] = initial_beliefs

    def add_belief(self, key: str, value: bool) -> None:
        """
        Agrega una creencia, resolviendo conflictos si es necesario.
        
        :param key: Clave de la creencia.
        :param value: Valor de la creencia.
        """
        if key in self.beliefs:
            self.resolve_conflict(key, value)
        else:
            self.beliefs[key] = value

    def resolve_conflict(self, key: str, new_value: bool) -> None:
        """
        Resuelve conflictos con las creencias actuales al agregar una nueva.
        
        :param key: Clave de la creencia en conflicto.
        :param new_value: Nuevo valor de la creencia.
        """
        current_value = self.beliefs[key]
        if new_value != current_value:
            self.beliefs[key] = new_value

    def get(self, key: str) -> Optional[bool]:
        """
        Obtiene el valor de una creencia específica.
        
        :param key: Clave de la creencia.
        :return: Valor de la creencia o None si no existe.
        """
        # Para consultar los beliefs actuales
        return self.beliefs.get(key, None)

    def __str__(self) -> str:
        """
        Representación en cadena de los beliefs.
        
        :return: Cadena que representa los beliefs.
        """
        return f"Beliefs({self.beliefs})"

class Options:
    # Clase opciones
    def __init__(self) -> None:
        """
        Inicializa las opciones del agente.
        """
        self.options: List[Dict[str, object]] = []

    def add_option(self, option: Dict[str, object]) -> None:
        """
        Agrega una opción.
        
        :param option: Diccionario que representa la opción. Cada opción debe ser un diccionario con claves 'name', 'priority', y 'condition'.
        """
        if isinstance(option, dict):
            self.options.append(option)

    def get(self) -> List[Dict[str, object]]:
        """
        Obtiene las opciones.
        
        :return: Lista de opciones.
        """
        return self.options

    def __str__(self) -> str:
        """
        Representación en cadena de las opciones.
        
        :return: Cadena que representa las opciones.
        """
        return f"Options({self.options})"

class Desires:
    # Clase deseos
    def __init__(self) -> None:
        """
        Inicializa los deseos del agente.
        """
        self.desires: Dict[str, int] = {}

    def add_desire(self, key: str, value: int) -> None:
        """
        Agrega un deseo.
        
        :param key: Clave del deseo.
        :param value: Valor del deseo.
        """
        self.desires[key] = value

    def remove_desire(self, key: str) -> None:
        """
        Remueve un deseo.
        
        :param key: Clave del deseo.
        """
        self.desires.pop(key)

    def get(self, key: str) -> Optional[int]:
        """
        Obtiene el valor de un deseo específico.
        
        :param key: Clave del deseo.
        :return: Valor del deseo o None si no existe.
        """
        return self.desires.get(key, None)

    def get_allD(self) -> Dict[str, int]:
        """
        Obtiene todos los deseos.
        
        :return: Diccionario de deseos. Cada clave es una string y el valor es un entero.
        """
        return self.desires

    def __str__(self) -> str:
        """
        Representación en cadena de los deseos.
        
        :return: Cadena que representa los deseos.
        """
        return f"Desires({self.desires})"

class Intentions:
    # Clase intenciones, puede tener iniciones iniciales pero generalmente inicia vacía
    def __init__(self, initial_intentions: Optional[Dict[str, int]] = None) -> None:
        """
        Inicializa las intenciones del agente.
        
        :param initial_intentions: Diccionario opcional de intenciones iniciales. Cada clave es una string y el valor es un entero.
        """
        if initial_intentions is None:
            initial_intentions = {}
        self.intentions: Dict[str, int] = initial_intentions

    def add_intention(self, key: str, value: int) -> None:
        """
        Agrega una intención.
        
        :param key: Clave de la intención.
        :param value: Valor de la intención.
        """
        self.intentions[key] = value

    def remove_intention(self, key: str) -> None:
        """
        Remueve una intención.
        
        :param key: Clave de la intención.
        """
        self.intentions.pop(key)

    def get(self, key: str) -> Optional[int]:
        """
        Obtiene el valor de una intención específica.
        
        :param key: Clave de la intención.
        :return: Valor de la intención o None si no existe.
        """
        return self.intentions.get(key, None)

    def get_allI(self) -> Dict[str, int]:
        """
        Obtiene todas las intenciones.
        
        :return: Diccionario de intenciones. Cada clave es una string y el valor es un entero.
        """
        return self.intentions

    def __str__(self) -> str:
        """
        Representación en cadena de las intenciones.
        
        :return: Cadena que representa las intenciones.
        """
        return f"Intentions({self.intentions})"

class Environment:
    def __init__(self) -> None:
        """
        Inicializa el entorno con valores predeterminados.
        """
        self.buddy_here: bool = False
        self.buddy_knows: bool = False
        self.buddy_finish1: bool = False
        self.buddy_finish2: bool = False

class BDIAgent:
    # Agente principal, ambos robots son instancias de esta clase
    def __init__(self, completions: int = 0, energy: int = 20000, max_completions: int = 3, max_tries: int = 3) -> None:
        """
        Inicializa el agente BDI.
        
        :param completions: Cantidad de rutinas completadas exitosamente.
        :param energy: Energía disponible del agente.
        """
        self.beliefs = Beliefs({
            BDI_Actions.ACOMPAÑADO: False,
            BDI_Actions.PUEDO_TERMINAR: True
        })  # base de creencias del agente
        self.completes: int = completions  # Cantidad de rutinas completadas exitosamente
        self.max_completions: int = max_completions  # Cantidad máxima de rutinas a completar
        self.energy: int = energy  # Energía disponible del agente
        self.leader: bool = False  # Indica si el agente es lider
        self.enough_batt: bool = True  # I indica si la batería es suficiente para terminar su tarea
        self.tries: int = 0  # intentos en recibir rutina o en recibir ACK de recepción de rutina
        self.max_tries: int = max_tries  # cantidad máxima de intentos
        self.all_ok: bool = True  # Indica si all está bien para poder proseguir, si no es así entonces debe abortar
        # lo que hace actualmente con el robot actual
        self.options: Options = Options()  # base de opciones del agente
        self.desires: Desires = Desires()  # base de deseos del agente
        self.intentions: Intentions = Intentions()  # base de intenciones del agente

    def percieve(self, environment) -> None:
        """
        Percibe el entorno y actualiza las creencias del agente en base al estado del entorno.
        
        :param environment: Instancia de la clase Environment que representa el estado actual del entorno.
        """
        environmental_beliefs = {
            BDI_Actions.ACOMPAÑADO: environment.buddy_here,
            BDI_Actions.COMP_ENTERADO: environment.buddy_knows,
            BDI_Actions.TERMINA_PART1: environment.buddy_finish1,
            BDI_Actions.TERMINA_PART2: environment.buddy_finish2,
        }
        for belief, value in environmental_beliefs.items():
            self.beliefs.add_belief(belief, value)

    def genbeliefs_fromstates(self) -> None:
        """
        Genera creencias a partir de los estados internos del agente y actualiza las creencias.
        """
        state_beliefs = {
            BDI_Actions.ACOMPAÑADO: False if self.tries == self.max_tries or not self.all_ok else None,
            BDI_Actions.PUEDO_TERMINAR: False if not self.enough_batt else True,
            BDI_Actions.HE_TERMINADO: True if self.completes == self.max_completions else None,
        }
        for belief, value in state_beliefs.items():
            if value is not None:
                self.beliefs.add_belief(belief, value)

    def generate_options(self, beliefs: Beliefs) -> Options:
        """
        Genera opciones basadas en las creencias del agente.
        
        :param beliefs: Instancia de la clase Beliefs que contiene las creencias actuales del agente.
        :return: Instancia de la clase Options con las opciones generadas basadas en las creencias.
        """
        options = [
            {"name": BDI_Actions.ESTABLECER_CONSENSO, "priority": 5, "condition": beliefs.get(BDI_Actions.ACOMPAÑADO)},
            {"name": BDI_Actions.BUSCAR_COMP, "priority": 4, "condition": not beliefs.get(BDI_Actions.ACOMPAÑADO)},
            {"name": BDI_Actions.ABORTAR, "priority": 10, "condition": not beliefs.get(BDI_Actions.PUEDO_TERMINAR)},
            {"name": BDI_Actions.EJECUTAR_SUB1, "priority": 7, "condition": beliefs.get(BDI_Actions.COMP_ENTERADO)},
            {"name": BDI_Actions.ENVIAR_CONF, "priority": 6, "condition": beliefs.get(BDI_Actions.COMP_ENTERADO)},
            {"name": BDI_Actions.EJECUTAR_SUB2, "priority": 8, "condition": beliefs.get(BDI_Actions.TERMINA_PART1)},
            {"name": BDI_Actions.ABORTAR, "priority": 9, "condition": beliefs.get(BDI_Actions.TERMINA_PART2)},
            {"name": BDI_Actions.HE_TERMINADO, "priority": 10, "condition": beliefs.get(BDI_Actions.HE_TERMINADO)},
        ]

        conflicts = {
            BDI_Actions.ESTABLECER_CONSENSO: [BDI_Actions.HE_TERMINADO, BDI_Actions.ABORTAR, BDI_Actions.EJECUTAR_SUB1, BDI_Actions.ABORTAR, BDI_Actions.BUSCAR_COMP, BDI_Actions.ENVIAR_CONF],
            BDI_Actions.BUSCAR_COMP: [BDI_Actions.HE_TERMINADO, BDI_Actions.ABORTAR, BDI_Actions.EJECUTAR_SUB1, BDI_Actions.ABORTAR, BDI_Actions.ESTABLECER_CONSENSO, BDI_Actions.ENVIAR_CONF],
            BDI_Actions.ABORTAR: [BDI_Actions.HE_TERMINADO, BDI_Actions.EJECUTAR_SUB1, BDI_Actions.EJECUTAR_SUB2, BDI_Actions.ESTABLECER_CONSENSO, BDI_Actions.BUSCAR_COMP, BDI_Actions.ENVIAR_CONF],
            BDI_Actions.EJECUTAR_SUB1: [BDI_Actions.HE_TERMINADO, BDI_Actions.BUSCAR_COMP, BDI_Actions.ESTABLECER_CONSENSO, BDI_Actions.ABORTAR, BDI_Actions.ENVIAR_CONF, BDI_Actions.EJECUTAR_SUB2],
            BDI_Actions.EJECUTAR_SUB2: [BDI_Actions.HE_TERMINADO, BDI_Actions.BUSCAR_COMP, BDI_Actions.ESTABLECER_CONSENSO, BDI_Actions.ABORTAR, BDI_Actions.ENVIAR_CONF, BDI_Actions.EJECUTAR_SUB1],
            BDI_Actions.ENVIAR_CONF: [BDI_Actions.HE_TERMINADO, BDI_Actions.BUSCAR_COMP, BDI_Actions.ESTABLECER_CONSENSO, BDI_Actions.ABORTAR, BDI_Actions.EJECUTAR_SUB1, BDI_Actions.EJECUTAR_SUB2],
            BDI_Actions.TERMINA_PART1: [BDI_Actions.ABORTAR, BDI_Actions.HE_TERMINADO, BDI_Actions.EJECUTAR_SUB1, BDI_Actions.EJECUTAR_SUB2, BDI_Actions.ESTABLECER_CONSENSO, BDI_Actions.BUSCAR_COMP, BDI_Actions.ENVIAR_CONF],
            BDI_Actions.TERMINA_PART2: [BDI_Actions.HE_TERMINADO, BDI_Actions.ABORTAR, BDI_Actions.EJECUTAR_SUB1, BDI_Actions.EJECUTAR_SUB2, BDI_Actions.ESTABLECER_CONSENSO, BDI_Actions.BUSCAR_COMP, BDI_Actions.ENVIAR_CONF],
            BDI_Actions.HE_TERMINADO: [BDI_Actions.ABORTAR, BDI_Actions.EJECUTAR_SUB1, BDI_Actions.EJECUTAR_SUB2, BDI_Actions.ESTABLECER_CONSENSO, BDI_Actions.BUSCAR_COMP, BDI_Actions.ENVIAR_CONF],
        }

        for option in options:
            if option["condition"]:
                self.options.add_option({
                    "name": option["name"],
                    "priority": option["priority"],
                    "conflicts": conflicts[option["name"]]
                })

        return self.options  # Devuelve las opciones generadas

    def deliberate(self, options: Options) -> Desires:
        """
        Realiza la deliberación para identificar y priorizar deseos basados en las opciones generadas y sus conflictos.
        
        :param options: Instancia de la clase Options que contiene las opciones generadas.
        :return: Instancia de la clase Desires con los deseos priorizados.
        """
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
        return self.desires

    def filter_(self, desires: Desires, intentions: Intentions) -> Intentions:
        """
        Filtra los deseos recientes con las intenciones actuales y genera nuevas intenciones.

        :param desires: Instancia de la clase Desires que contiene los deseos generados.
        :param intentions: Instancia de la clase Intentions que contiene las intenciones actuales.
        :return: Instancia de la clase Intentions con las intenciones actualizadas.
        """
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
        return self.intentions

    def bdi_cycle(self, envi: object) -> Dict[str, object]:
        """
        Ejecuta un ciclo BDI completo: percibe el entorno, genera creencias, opciones, deseos e intenciones, y devuelve
        el estado actual del agente.

        :param envi: Objeto que representa el entorno percibido por el agente.
        :return: Diccionario con las creencias, deseos e intenciones actuales del agente.
        """
        self.percieve(envi)
        self.genbeliefs_fromstates()
        self.generate_options(beliefs=self.beliefs)
        # print(self.options)
        self.deliberate(self.options)
        self.filter_(self.desires, self.intentions)
        print(self.intentions)
        return {
            'beliefs': self.beliefs,
            'desires': self.desires,
            'intentions': self.intentions
        }

if __name__ == "__main__":
    h1 = BDIAgent(completions=0, energy=20000)
    env = Environment()
    intenciones = h1.intentions.intentions

    # Establecer estado inicial del agente
    h1.all_ok = True
    h1.completes = 1
    h1.enough_batt = True

    # Ejecutar el ciclo BDI y guardar el resultado
    result1 = h1.bdi_cycle(env)

    # Establecer conexión
    env.buddy_here = True
    result2 = h1.bdi_cycle(env)

    # Compartir la rutina
    env.buddy_knows = True
    result3 = h1.bdi_cycle(env)

    # Terminar la primera parte de la rutina
    env.buddy_finish1 = True
    result4 = h1.bdi_cycle(env)

    # Terminar la segunda parte de la rutina
    env.buddy_finish2 = True
    result5 = h1.bdi_cycle(env)

    # Reiniciar el entorno y el estado del agente
    env = Environment()
    h1.beliefs = Beliefs({BDI_Actions.ACOMPAÑADO: False, BDI_Actions.PUEDO_TERMINAR: True})
    h1.intentions = Intentions()
    result6 = h1.bdi_cycle(env)

    # Ya no hay batería suficiente
    h1.enough_batt = False
    print("====================================")
    result7 = h1.bdi_cycle(env)
    print("====================================")
    print(intenciones)