class Mapa: 
    def __init__(self, ancho, alto): 
        self.ancho, self.alto = ancho, alto 
        self.puerta_abierta = False 

    def es_caminable(self, x, y):
        if x == 0 or x == self.ancho - 1 or y == 0 or y == self.alto - 1: #Detecta si la posición es el borde del mapa (donde van los muros #).
            if (x == self.ancho - 1 or x == 0) and y == self.alto // 2: # Verifica si es la puerta
                return True
            return False 
        return True 

    def crear_mapa (self, entidades): 
            filas = []
            for y in range(self.alto):
                fila_str = ""
                for x in range(self.ancho): 
                    if x == 0 or x == self.ancho - 1 or y == 0 or y == self.alto - 1: # Si es el borde, revisamos si es la puerta
                        if (x == self.ancho - 1 or x == 0) and y == self.alto // 2:
                            char = " " # Puerta abierta
                        else:
                            char = "#" #Muro
                    else:
                        char = "." #Suelo

                    char_entidad = None
                    for e in entidades:
                        if e.x == x and e.y == y and e.esta_viva: #Si la entidad está viva y coincide con la coordenada actual
                            if e.nombre == "Heroe":
                                char_entidad = "H"
                                break # Si encontramos al heroe, no buscamos más en este píxel
                            elif e.nombre == "Bala":
                                char_entidad = "*"
                            else:
                                char_entidad = e.nombre[0] # Usa la inicial (Ej: 'O' para Orco)
                    
                    if char_entidad:
                        char = char_entidad # El personaje "tapa" al suelo
                    
                    fila_str += char + " " # Añadimos el carácter y un espacio (para que no se vea tan apretado)
                
                filas.append(fila_str)
            return filas