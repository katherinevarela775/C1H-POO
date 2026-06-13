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