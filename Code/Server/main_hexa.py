#from Bailes import bailes
from Distribuido.arquitectura import BDIAgent, Environment, Beliefs, Intentions, BDI_Actions
from Distribuido.Eleccion_de_lider import Liderazgo, role
from Distribuido.Generador_de_rutinas import crea_rutina
from Bailes import bailes
def participar_en_consenso():
    hexapodo_1 = Liderazgo(k_devices=2)
    print(f"[CONSENSO] Participando en el consenso")
    #       [CONSENSO]: ID        10      , status:    role.CANDIDATO  , líder:        None
    print(f"[CONSENSO]: ID {hexapodo_1.id}, status: {hexapodo_1.estado}, líder: {hexapodo_1.Lider}")
    print()

    # Aquí debe de haber una comunicación entre los robots para enviar y recibir los IDs
    # para comprobar y corregir los IDs. Lo que se tiene que enviar es
    # hexapodo_1.id
    # supongamos que tenemos...
    # enviar hexapodo_1.compartir_estado() a los demás hexápodos
    # esperar a recibir los estados de los demás hexápodos
    # Lo ideal seria tener un while desde el envío de los IDs hasta que se haga el consenso
    # y todos los hexápodos sepan que tienen distinto ID
    hexapodo_2_id = 10
    hexapodo_1.comprobar_y_corregir_UID([hexapodo_2_id])
    
    #       [CONSENSO]: ID        10      , status:    role.CANDIDATO  , líder:        (int)
    print(f"[CONSENSO]: ID {hexapodo_1.id}, status: {hexapodo_1.estado}, líder: {hexapodo_1.Lider}")
    print()

    # El consenso se hace de forma automática y sin comunicarse con los demás hexápodos
    # Supongamos que el hexapodo 2 tiene el siguiente estado:
    hexapodo_2_estado = {-1: role.CANDIDATO} # {id: rol}
    hexapodo_1.elegir_lider([hexapodo_2_estado])

    # Para este punto, ya se hizo el consenso.
    return hexapodo_1
def generar_rutina_de_baile():
    numero_bailes=6
    baile = crea_rutina(numero_bailes)
    mitad = len(baile)//2
    subrutina1=baile[:mitad]
    subrutina2=baile[mitad:]
    return subrutina1, subrutina2
def ejecutar_subrutina(subrurina):
    b=bailes()
    for baile in subrurina:
        metodo = getattr(b,baile)
        metodo()

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
        else:
            print(f"[INFO] El agente está acompañado")
            print(f"[CONSENSO] Participando en el consenso")
            hexapodo_1 = participar_en_consenso()
            if hexapodo_1.estado == role.LIDER:

                print(f"[BAILE] Generando rutina de baile")
                
                subrutina1, subrutina2 = generar_rutina_de_baile()
                print(subrutina1)
                print("xdSSS")
                print(subrutina2)


                print(f"[BAILE] Rutina de baile generada")
                print(f"[BAILE] transmitiendo rutiina de baile a los demás hexápodos")
                ... # Transmitir la rutina de baile a los demás hexápodos
                print(f"[BAILE] Rutina de baile transmitida exitosamente")
                # Esperar a que los demás hexápodos respondan con la confirmación de la rutina de baile
                print(f"[BAILE] Esperando confirmación de la rutina de baile")
                confirmacion_de_baile = True
                print(f"[BAILE] Confirmación de la rutina de baile recibida")
                if confirmacion_de_baile:
                    ejecutar_subrutina(subrutina1)
                    print(f"[BAILE] Bailando subrutina 1")
                    ...
                    print(f"[BAILE] Subrutina 1 completada, enviando confirmación a los demás hexápodos")
                    ...
                    print(f"[BAILE] Confirmación de la subrutina 1 enviada")
                    print(f"[BAILE] Esperando confirmación de la subrutina 1 de los demás hexápodos")
                    confirmacion_de_subrutina_1 = True
                    print(f"[BAILE] Confirmación de la subrutina 1 recibida")
                    print(f"[BAILE] Bailando subrutina 2")
                    ejecutar_subrutina(subrutina2)
                    ...
                    print(f"[BAILE] Subrutina 2 completada, enviando confirmación a los demás hexápodos")
                    ...
                    print(f"[BAILE] Confirmación de la subrutina 2 enviada")
                    print(f"[BAILE] Esperando confirmación de la subrutina 2 de los demás hexápodos")
                    confirmacion_de_subrutina_2 = True
                    print(f"[BAILE] Confirmación de la subrutina 2 recibida")


                    


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
