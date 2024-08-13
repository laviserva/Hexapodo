#from Bailes import bailes
from Distribuido.arquitectura import BDIAgent, Environment, Beliefs, Intentions, BDI_Actions
if __name__ == '__main__':
    """b = bailes()
    
    b.baile_1()"""

    # Inicializando el agente y el entorno de la arquitectura
    h1 = BDIAgent(completions=0, energy=20000)
    env = Environment()
    print("[INFO] Agente creado")
    print(f"[INFO] BDI_Actions.ACOMPAÑADO: {BDI_Actions.ACOMPAÑADO}")
    print(f"[INFO] h1.beliefs: {h1.beliefs.beliefs}")
    comunicación = False

    while h1.max_completions > h1.completes and h1.max_tries > h1.tries and h1.energy > 0:
        if not h1.beliefs.beliefs[BDI_Actions.ACOMPAÑADO] and not comunicación:
            print(f"[INFO] El agente no está acompañado!")
            print(f"[COMUNICACIÓN] Buscando a alguien para balar el pasito perrón")
            comunicación = True # supongamos que se estableció la comunicación
            # Establecer conexión
            env.buddy_here = True
            print(f"[COMUNICACIÓN] Comunicación establecida exitosamente con otro agente")
        if not comunicación:
            print(f"[ERROR] No se pudo establecer la comunicación con nadie")
            print(f"[ERROR] El agente no puede bailar solo")
            exit()
        rutina = "exapodo.obener_rutina()"
        
        h1.tries = 3

    """while h1.max_completions > h1.completes and h1.max_tries > h1.tries and h1.energy > 0:
        print(f"\n[INFO] Completions: {h1.completes}")
        if not BDI_Actions.ACOMPAÑADO in h1.beliefs.beliefs.keys():
            print(f"\n[ERROR] Error en las creencias del agente no sabe si está acompañado o no")
            print(f"[ERROR] Por favor revise las creencias del agente para asegurarse de que estén completas")
            exit()
        if not h1.beliefs.beliefs[BDI_Actions.ACOMPAÑADO] and not comunicación:
            print(f"[INFO] El agente no está acompañado!")
            print(f"[COMUNICACIÓN] Buscando a alguien para balar el pasito perrón")
            comunicación = True # supongamos que se estableció la comunicación
            # Establecer conexión
            env.buddy_here = True
            print(f"[COMUNICACIÓN] Comunicación establecida exitosamente con otro agente")
        if not comunicación:
            print(f"[ERROR] No se pudo establecer la comunicación con nadie")
            print(f"[ERROR] El agente no puede bailar solo")
            exit()
        rutina = "exapodo.obener_rutina()"

        h1.tries = 3"""
