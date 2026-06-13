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

class Proyectil(Entidad): 
    def __init__(self, x, y, dx, dy, fuerza): 
        super().__init__("Bala", x, y, dx, dy, 1, fuerza)  
        
    def actuar(self, mapa, motor): 
        objetivo_inmediato = motor.obtener_enemigo_en(self.x, self.y) #Verifica si hay un enemigo en su pos. actual
        
        if objetivo_inmediato: 
            objetivo_inmediato.recibir_danio(self._fuerza) # El proyectil daño al enemigo.
            self._vida = 0 # 9. El proyectil se destruye a sí mismo 
            return 

        self.x += self.dx # Si no chocó, avanza según su dirección almacenada.
        self.y += self.dy
        
        if not mapa.es_caminable(self.x, self.y): # Verificamos si el nuevo lugar es caminable. Si no lo es, el proyectil se destruye.
            self._vida = 0
            return

        objetivo_final = motor.obtener_enemigo_en(self.x, self.y)
        
        if objetivo_final:
            objetivo_final.recibir_danio(self._fuerza) 
            self._vida = 0
            #Aunque la función termine, el objeto sigue existiendo en la memoria, Cuando el bucle principal vuelva a ejecutarse en el siguiente frame, volverá a llamar a proyectil.actuar().

class Enemigo(Entidad):  
    def __init__(self, nombre, x, y, vida, fuerza, rango_vision): # Constructor con atributo extra.
        super().__init__(nombre, x, y, 0, 0, vida, fuerza) 
        self.rango_vision = rango_vision # Que tan lejos ve este enemigo.

    def actuar(self, mapa, motor): 
        if not self.esta_viva: # Si está muerto, no hace nada.
                    return

        jugador = motor.jugador # Obtiene la referencia del Jugador.
        distancia = abs(self.x - jugador.x) + abs(self.y - jugador.y)
        
        if distancia == 1:
            self.atacar(jugador) # si el jugador esta a lado lo ataca.
    
        elif 1 < distancia <= self.rango_vision:
            dx = 1 if self.x < jugador.x else -1 if self.x > jugador.x else 0 #derecha (+1) izquierda (-1).
            dy = 1 if self.y < jugador.y else -1 if self.y > jugador.y else 0 # subir (-1) bajar (+1).
            
            nueva_x = self.x + dx # Calcula posición destino.
            nueva_y = self.y + dy

            ocupado_por_jugador = (nueva_x == jugador.x and nueva_y == jugador.y) # Verificaciones técnicas para no encimarse.
            otro_enemigo = motor.obtener_enemigo_en(nueva_x, nueva_y)
            
            if not ocupado_por_jugador and otro_enemigo is None: # Si el camino esta libre se mueve hacia el jugador.
                self.mover(dx, dy, mapa)

            ocupado_por_jugador = (nueva_x == jugador.x and nueva_y == jugador.y)
            
            otro_enemigo = motor.obtener_enemigo_en(nueva_x, nueva_y)
            
            if not ocupado_por_jugador and otro_enemigo is None:
                self.mover(dx, dy, mapa)
