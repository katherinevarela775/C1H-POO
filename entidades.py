import msvcrt
from abc import ABC, abstractmethod 

class Entidad(ABC):
    def __init__(self, nombre, x, y,dx ,dy , vida, fuerza): 
        self.nombre = nombre
        self.x, self.y = x, y
        self._vida = vida
        self._fuerza = fuerza 
        self.dx = dx 
        self.dy = dy 
    
  
    @property #getter: interaccion de manera controlada
    def fuerza(self): # Método para leer la fuerza protegida.
        return self._fuerza 

    @property 
    def esta_viva(self): return self._vida > 0 

    def recibir_danio(self, cantidad):  #setter: interaccion de manera controlada
        self._vida = max(0, self._vida - cantidad) # Resta vida pero asegura que el mínimo sea 0.

    def atacar(self, objetivo):
        if objetivo and objetivo.esta_viva: 
            objetivo.recibir_danio(self._fuerza) # el mismo método atacar() funciona para cualquier entidad que implemente recibir_danio(), ya sea un jugador, un enemigo o incluso una trampa.
            
    @property # Permite leer la vida actual desde fuera (ej: para la interfaz).
    def vida(self):
        return self._vida


    def mover(self, dx, dy, mapa): 
        if mapa.es_caminable(self.x + dx, self.y + dy): 
            self.x += dx 
            self.y += dy
            
    @abstractmethod # Obliga a los hijos a tener este método.
    def actuar(self, mapa, motor=None): pass 

class Jugador(Entidad): 
    def __init__(self, nombre, x, y, vida, fuerza): 
        super().__init__(nombre, x, y, 0, 0, vida, fuerza) 
        
    def actuar(self, mapa, motor=None): 
        if msvcrt.kbhit():
            tecla = msvcrt.getch().decode('utf-8').lower()

            teclas_mov = {'w': (0, -1), 's': (0, 1), 'a': (-1, 0), 'd': (1, 0)} # Diccionario de vectores.
            teclas_disparo = {'i': (0, -1), 'k': (0, 1), 'j': (-1, 0), 'l': (1, 0)} # Mapeo de ataque.

            if tecla in teclas_mov: 
                dx, dy = teclas_mov[tecla]
                self.mover(dx, dy, mapa) # Llama al método heredado de Entidad.
                
            elif tecla in teclas_disparo: 
                dx, dy = teclas_disparo[tecla]
                nueva_bala = Proyectil(self.x + dx, self.y + dy, dx, dy, self._fuerza) # Crea un objeto nuevo de la clase Proyectil.
                motor.proyectiles.append(nueva_bala) # Añade el objeto a la lista del motor.
            
            elif tecla == 'q':
                    motor.jugando = False
