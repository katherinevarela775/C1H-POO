# ⚔️ Desafío POO: Arcade Roguelike - The Iceforge (Python)

Este proyecto fue desarrollado como respuesta a un desafío académico cuyo objetivo principal era diseñar y programar un videojuego aplicando los pilares de la **Programación Orientada a Objetos (POO)** e implementando obligatoriamente el uso de una **Clase Base Abstracta**. 

Para resolverlo, opté por crear un videojuego interactivo en consola de tipo **Roguelike/Arcade**, donde el usuario controla a un héroe que debe explorar mazmorras, disparar proyectiles direccionales y erradicar amenazas automatizadas con dificultad escalable.

---

## 🛠️ Arquitectura de Software & Pilares POO

El proyecto destaca por estar completamente modularizado en archivos independientes (`mapa.py`, `entidades.py`, `juego.py` y `main.py`), lo que garantiza un código limpio, legible y escalable basado en los siguientes conceptos:

### 1. Abstracción y Clases Abstractas (`ABC`)
El corazón de los personajes es la clase `Entidad` (ubicada en `entidades.py`), la cual hereda de `ABC`. 
* **El Contrato:** Define el método `@abstractmethod def actuar(self, mapa, motor)`. Ninguna entidad genérica puede ser instanciada directamente. 
* **La Obligación:** Obliga a todas las clases hijas (`Jugador`, `Enemigo`, `Proyectil`) a implementar su propia lógica de comportamiento para poder existir en el mundo.

### 2. Encapsulamiento Avanzado (`@property`)
Para proteger la integridad de los datos internos y evitar modificaciones accidentales desde el exterior, se aplicó encapsulamiento estricto mediante atributos protegidos (ej. `self._vida`, `self._fuerza`) gestionados de forma controlada a través de decoradores:
* **Getters:** Permiten a la interfaz y al motor leer de forma segura el estado de salud (`vida`), la potencia de impacto (`fuerza`) o si la entidad `esta_viva`.
* **Setters Implícitos:** El método `recibir_danio` actúa como un regulador que aplica lógica matemática interna, asegurando por seguridad que la vida de ningún agente caiga por debajo de cero.

### 3. Polimorfismo Dinámico en el Game Loop
El `MotorJuego` coordina el ciclo de fotogramas (*Game Loop*) manejando una lista unificada de entidades activas. Al ejecutar el bucle, el motor invoca:
```python
for entidad in entidades_activas:
    if entidad.esta_viva:
        entidad.actuar(mapa_act, self)
```
* **La Magia:** El motor no tiene idea (ni le interesa saber) si el objeto en esa iteración es el Héroe, un Orco o una Bala. Gracias al polimorfismo, cada objeto responde de forma autónoma invocando sus propias físicas y reglas preprogramadas.

---

## 🕹️ Mecánicas Destacadas & Extras del Motor

* **📺 Renderizado Dual en Paralelo (Split-Screen):** El motor gráfico procesa e imprime la **Sala 1** y la **Sala 2** de forma simultánea lado a lado en la terminal utilizando la función `zip()`. Esto permite al usuario visualizar ambos mapas en paralelo mientras juega en tiempo real.
* **🧀 Dificultad Progresiva Procedimental:** El motor incluye un *spawner* aleatorio (`generar_enemigos_aleatorios`) con restricciones perimetrales para evitar que los enemigos aparezcan dentro de los muros. Además, escala los atributos de las entidades según la sala: la Sala 1 es custodiada por "Orcos" estándar, mientras que la Sala 2 se pobla automáticamente con enemigos "Elite" (con más vida, fuerza y rango de visión).
* **🎯 Balas de Alta Velocidad (Anti-Tunneling):** La clase `Proyectil` maneja un sistema de colisión predictivo bifásico (*objetivo inmediato* y *objetivo final*). Esto garantiza matemáticamente que una bala nunca "atraviese" o salte visualmente a un enemigo sin registrar el daño en fotogramas de alta velocidad.
* **⌨️ Controles Asincrónicos Direccionales:** A través de la librería nativa de Windows `msvcrt`, el juego captura pulsaciones de teclado instantáneas sin pausar el flujo de fotogramas:
  * `W`, `A`, `S`, `D` para mover físicamente al héroe (dejando un rastro visual de puntos `.`).
  * `I`, `J`, `K`, `L` para disparar proyectiles en las 4 direcciones cartesianas.

---

## ⚙️ Estructura del Repositorio y Ejecución

* `mapa.py`: Controla la matriz del terreno, límites perimetrales y estados de puertas.
* `entidades.py`: Contiene la clase abstracta `Entidad` y las subclases `Jugador`, `Enemigo` y `Proyectil`.
* `juego.py`: Alberga la clase `MotorJuego`, el renderizado con `zip()` y las mecánicas de salas.
* `main.py`: Inicializador del juego con setup de parámetros y control de excepciones para salidas limpias (`KeyboardInterrupt`).

Para ejecutar el videojuego, asegúrate de estar en una consola de Windows con Python 3 instalado y corre el script de arranque principal:
```bash
python main.py
```
