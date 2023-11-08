import random

class Casilla:
    def __init__(self, es_mina=False):
        self.es_mina = es_mina
        self.revelada = False
## Patron de diseño singleton para protejer el tablero de dos instancias en un mismo game
class Tablero:
    _instance = None
   
    def __new__(cls):
        if not cls._instance :
            nivel=""
            while True:
                try: 
                    selecccion = (input('Nivel principiante(p)  intermedio(m)  experto(e)\n Ingrese caracter: '))
                    if selecccion == "p" or selecccion == "m" or selecccion == "e":
                        nivel +=selecccion
                        break
                    EOFError
                except (ValueError):
                    print("Error Valor no valido, Ingrese nuevamente")
                except TypeError:
                    print("Error Valor no valido, Ingrese nuevamente")
            if nivel == "p":
                f,c,m=8,8,10
            elif nivel == "m":
                f,c,m=16,16,41
            else:
                f,c,m=16,30,100
            cls._instance=super(Tablero, cls).__new__(cls)
            cls._instance.filas,cls._instance.columnas,cls._instance.num_minas =f,c,m
            
            cls._instance.tablero = [[Casilla() for _ in range(c)] for _ in range(f)]
            cls._instance.colocar_minas()
            return cls._instance

    def colocar_minas(self):
        minas_colocadas = 0
        while minas_colocadas < self.num_minas:
            fila = random.randint(0, self.filas - 1)
            columna = random.randint(0, self.columnas - 1)
            if not self.tablero[fila][columna].es_mina:
                self.tablero[fila][columna].es_mina = True
                minas_colocadas += 1

    def mostrar_tablero(self, mostrar_minas=False):
        for fila in range(self.filas):
            for columna in range(self.columnas):
                casilla = self.tablero[fila][columna]
                if casilla.revelada or mostrar_minas:
                    if casilla.es_mina:
                        print('* |', end=' ')
                    else:
                        if self.contar_minas_vecinas(fila,columna) != 0 :
                            print(f"{self.contar_minas_vecinas(fila,columna)} |", end=' ')
                        else:
                            print("- |",end=" ")
                else:
                    print('X |', end=' ')
            print()

    def revelar_casilla(self, fila, columna):
        casilla = self.tablero[fila][columna]
        if casilla.revelada:
            return
        casilla.revelada = True
        if casilla.es_mina:
            return
        minas_vecinas = self.contar_minas_vecinas(fila, columna)
        if minas_vecinas == 0:
            for f in range(fila - 1, fila + 2):
                for c in range(columna - 1, columna + 2):
                    if 0 <= f < self.filas and 0 <= c < self.columnas:
                        self.revelar_casilla(f, c)

    def contar_minas_vecinas(self, fila, columna):
        minas_vecinas = 0
        for f in range(fila - 1, fila + 2):
            for c in range(columna - 1, columna + 2):
                if 0 <= f < self.filas and 0 <= c < self.columnas:
                    if self.tablero[f][c].es_mina:
                        minas_vecinas += 1
        return minas_vecinas

    def jugar(self):
        while True:
            self.mostrar_tablero()
            fila=0
            columna =0  
            valid = True          
            while valid:

                try: 
                    fila = int(input('Fila: '))
                    columna = int(input('Columna: '))
                    valid = False
                except (ValueError):
                    print("Error Valor no valido, Ingrese nuevamente")
                except TypeError:
                    print("Error Valor no valido, Ingrese nuevamente")
                             
            if 0 <= fila < self.filas and 0 <= columna < self.columnas:
                if self.tablero[fila][columna].es_mina:
                    print('¡Perdiste!')
                    self.mostrar_tablero(mostrar_minas=True)
                    break
                self.revelar_casilla(fila, columna)
                casillas_no_minadas = sum(1 for fila in self.tablero for casilla in fila if not casilla.es_mina and casilla.revelada)
                if casillas_no_minadas == (self.filas * self.columnas - self.num_minas):
                    print('¡Ganaste!')
                    self.mostrar_tablero(mostrar_minas=True)
                    break
            else:
                print('Coordenadas inválidas. Inténtalo de nuevo.')


if __name__ == '__main__':
    tablero = Tablero()
    tablero.jugar()