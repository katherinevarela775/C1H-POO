from entidades import Jugador # Importamos las clases
from mapa import Mapa
from juego import MotorJuego

def main():
    try:
        mi_mapa = Mapa(16, 16) # Instanciamos el mapa con un tamaño específico 
        
        hero = Jugador("Héroe", 2, 2, 200, 20) # Creamos al jugador con su nombre, posición inicial (2,2), vida y fuerza.
        
        engine = MotorJuego(mi_mapa, hero, []) 
        engine.enemigos_sala1 = engine.generar_enemigos_aleatorios(cantidad=4, sala=1) #Llamas a la función que creaste en el motor para poblar la primera sala. 
        engine.iniciar() #Llamas al método que contiene el while True. A partir de esta línea, el control del programa pasa totalmente al archivo juego.py.
        
    except KeyboardInterrupt: #Captura el comando Ctrl+C.
        print("\n\nSaliendo del juego...")

if __name__ == "__main__": #Verificación de ejecución directa. "Si este archivo se está ejecutando directamente (y no siendo importado por otro), entonces corre el juego".
    main()