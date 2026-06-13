import time, random, os
from mapa import Mapa 
from entidades import Enemigo, Proyectil

class MotorJuego:
    def __init__(self, mapa, jugador, enemigos):
        self.mapa_sala1 = mapa 
        self.mapa_sala2 = Mapa(mapa.ancho, mapa.alto) 
        self.jugador = jugador
        self.enemigos_sala1 = enemigos 
        self.enemigos_sala2 = [] 
        self.jugando = True 
        self.sala_actual = 1 
        self.proyectiles = [] 
        
    def enemigos_actuales(self):
        return self.enemigos_sala1 if self.sala_actual == 1 else self.enemigos_sala2

    def obtener_enemigo_en(self, x, y):
            for enemigo in self.enemigos_actuales():
                if enemigo.x == x and enemigo.y == y and enemigo.esta_viva:
                    return enemigo
            return None

    def iniciar(self):
        while self.jugando: 
            self._dibujar_escena() 
            mapa_act = self.mapa_sala1 if self.sala_actual == 1 else self.mapa_sala2

            entidades_activas = [self.jugador] + self.proyectiles + self.enemigos_actuales() 
            
            for entidad in entidades_activas:
                if entidad.esta_viva:
                    entidad.actuar(mapa_act, self) #Aquí ocurre el Polimorfismo. El motor no sabe qué es entidad, solo sabe que tiene un método llamado actuar.

            self.proyectiles = [p for p in self.proyectiles if p.esta_viva]
            
            self._actualizar_logica() 
            self._verificar_estado() 
            time.sleep(0.30) 

    def _dibujar_escena(self):
            os.system('cls' if os.name == 'nt' else 'clear') # Limpiamos la consola
            
            entidades_s1 = self.enemigos_sala1[:]
            entidades_s2 = self.enemigos_sala2[:] # Preparamos que vamos a dibujar en cada sala
            
            if self.sala_actual == 1:
                entidades_s1.append(self.jugador)
                entidades_s1.extend(self.proyectiles)   # Agrega al jugador y las balas solo a la sala en la que estamos, para que no se dibuje dos veces.
            else:
                entidades_s2.append(self.jugador)
                entidades_s2.extend(self.proyectiles)

            filas1 = self.mapa_sala1.crear_mapa(entidades_s1) # El mapa genera una representacion de si mismo ya con los caracteres correspondientes 
            filas2 = self.mapa_sala2.crear_mapa(entidades_s2)

            print(" SALA 1 ".center(self.mapa_sala1.ancho * 2) + "   " + " SALA 2 ".center(self.mapa_sala2.ancho * 2))
            for f1, f2 in zip(filas1, filas2): #Emparejamos el primer elemento de cada iterable, luego el segundo, y así sucesivamente, lo que permite procesar múltiples secuencias en paralelo
                
                lista_f1 = list(f1)
                if lista_f1[0] == " ": lista_f1[0] = "#"
                f1_cerrada = "".join(lista_f1)
                
                lista_f2 = list(f2)
                if lista_f2[-2] == " ": lista_f2[-2] = "#"
                f2_cerrada = "".join(lista_f2)

                print(f1_cerrada + " | " + f2_cerrada)
            
            print(f"\n HP: {self.jugador.vida} | Sala: {self.sala_actual} | Puerta: {'ABIERTA' if self.mapa_sala1.puerta_abierta else 'CERRADA'}") # Imprime la vida restante, la sala actual y el estado de la puerta.
            print("Controles: WASD para mover, IJKL para disparar, Q para salir.")
            
    def _actualizar_logica(self):
        if self.sala_actual == 1:
            if not any(e.esta_viva for e in self.enemigos_sala1): 
                self.mapa_sala1.puerta_abierta = True
                self.mapa_sala2.puerta_abierta = True 

        #Deteccion de cambio de sala
        if self.sala_actual == 1 and self.jugador.x >= self.mapa_sala1.ancho - 1:
            if self.mapa_sala1.puerta_abierta:
                self.sala_actual = 2
                self.jugador.x = 1 
                self.jugador.y = self.mapa_sala2.alto // 2
        
                if not self.enemigos_sala2: 
                    self.enemigos_sala2 = self.generar_enemigos_aleatorios(3, 2)
            else:
                self.jugador.x = self.mapa_sala1.ancho - 2 # Si esta cerrada,empujamos al jugador a la posicion anterior (antes de la puerta)

    def generar_enemigos_aleatorios(self, cantidad, sala):
        nuevos = []
        for _ in range(cantidad):
            rx = random.randint(5, self.mapa_sala1.ancho - 3) #Elige coordenadas al azar evitando las paredes (ancho-3).
            ry = random.randint(5, self.mapa_sala1.alto - 3)
            
            if sala == 1: # Creamos instancias diferentes según la sala (Dificultad progresiva).
                nuevos.append(Enemigo("Orco", rx, ry, 40, 10, 5))
            else:
                nuevos.append(Enemigo("Elite", rx, ry, 60, 15, 7))
        return nuevos

    def _verificar_estado(self):
        if not self.jugador.esta_viva:
            print("\n¡HAS MUERTO! GAME OVER")
            self.jugando = False
            
        if self.sala_actual == 2:
            if not any(e.esta_viva for e in self.enemigos_sala2):
                self._dibujar_escena() 
                print("\n" + "="*30)
                print("¡VICTORIA! Has despejado el Iceforge.")
                print("="*30)
                self.jugando = False