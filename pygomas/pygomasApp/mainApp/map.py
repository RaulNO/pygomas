from mainApp.box import Box;

class Map:
    
    def __init__(self):
        self.map = []
        # Creamos una matriz de 32x32 y llenamos los bordes con paredes
        for i in range(32):
            fila = []
            for j in range(32):
                if i == 0 or i == 31 or j == 0 or j == 31:
                    box = Box()
                    box.set_has_wall(True)
                    fila.append(box)
                else:
                    box = Box()
                    fila.append(box)
            self.map.append(fila)

    

