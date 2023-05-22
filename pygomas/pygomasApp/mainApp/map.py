from mainApp.box import Box;
import os
class Map:

    def __init__(self):
        self.map = []
        for y in range(32):
            fila = []
            for x in range(32):
                if x == 0 or x == 31 or y == 0 or y == 31:
                    box = Box(True, False, False, False)
                    box.set_has_wall(True)
                    fila.append(box)
                else:
                    box = Box(False, False, False, False)
                    fila.append(box)
            self.map.append(fila)

    def get_map(self):
        return self.map
    
    def getBox(self, x, y):
        return self.get_map()[x][y]
    
    def clearBox(self, x, y):
        newBox = self.getBox(x, y)
        newBox.clear()
        self.map[x][y] = newBox

    def setWallToBox(self, x, y):
        newBox = self.getBox(x,y)
        newBox.clear()
        newBox.set_has_wall(True)
        self.map[x][y] = newBox

    def setFlagToBox(self, x, y):
        newBox = self.getBox(x,y)
        newBox.clear()
        newBox.set_has_flag(True)
        self.map[x][y] = newBox   
    
    def setAxisToBox(self, x, y):
        newBox = self.getBox(x,y)
        newBox.clear()
        newBox.set_has_axisSpawn(True)
        self.map[x][y] = newBox 
        
    
    def setAlliedToBox(self, x, y):
        newBox = self.getBox(x,y)
        newBox.clear()
        newBox.set_has_alliedSpawn(True)
        self.map[x][y] = newBox 

    def get_alliedSpawn_coords(self):
        
        upper_left_x = 32
        upper_left_y = 32
        lower_right_x = 0
        lower_right_y = 0

        for x in range(32):
            for y in range(32):
                if self.map[x][y].get_has_alliedSpawn():
                    upper_left_x = min(upper_left_x, x)
                    upper_left_y = min(upper_left_y, y)
                    lower_right_x = max(lower_right_x, x)
                    lower_right_y = max(lower_right_y, y)

        return (upper_left_x, upper_left_y), (lower_right_x, lower_right_y)   

    def get_axisSpawn_coords(self):
        
        upper_left_x = 32
        upper_left_y = 32
        lower_right_x = 0
        lower_right_y = 0

        for x in range(32):
            for y in range(32):
                if self.map[x][y].get_has_axisSpawn():
                    upper_left_x =  min(upper_left_x, x)
                    upper_left_y =  min(upper_left_y, y)
                    lower_right_x = max(lower_right_x, x)
                    lower_right_y = max(lower_right_y, y)

        return (upper_left_x, upper_left_y), (lower_right_x, lower_right_y)  
    
    def get_flag_coords(self):
       
        for row_idx, row in enumerate(self.map):
            for col_idx, box in enumerate(row):
                if box.get_has_flag():
                    return (col_idx, row_idx)

        return None
                
    def createTxt(self, map_name):
        alliedSpawnCoords = self.get_alliedSpawn_coords()
        axisSpawnCoords = self.get_axisSpawn_coords()
        flagCoords = self.get_flag_coords()
        matrix = self.get_map()
        
        dir_path = "../maps/" + map_name
        os.makedirs(dir_path, exist_ok=True)
        new_map = open(os.path.join(dir_path, map_name + '_cost.txt'), 'w')

        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j].get_has_wall():
                    new_map.write("*")
                else:
                    new_map.write(" ")
            new_map.write("\n")

        config = open(os.path.join(dir_path, map_name + '.txt'), 'w')
        config.write("[pGomas]\n")
        config.write("pGomas_OBJECTIVE: " + str(flagCoords[0]) + " " + str(flagCoords[1]) + "\n")
        config.write("pGomas_SPAWN_ALLIED: " + str(alliedSpawnCoords[0][1]) + " " + str(alliedSpawnCoords[0][0]) + " " + str(alliedSpawnCoords[1][1]) + " " + str(alliedSpawnCoords[1][0]) + "\n")
        config.write("pGomas_SPAWN_AXIS: " + str(axisSpawnCoords[0][1]) + " " + str(axisSpawnCoords[0][0]) + " " + str(axisSpawnCoords[1][1]) + " " + str(axisSpawnCoords[1][0]) + "\n")
        config.write("pGomas_COST_MAP: 32 32 " + map_name + "_cost.txt\n")
        config.write("[pGomas]")


    def loadMap(self, map_name):
        with open(f"../maps/{map_name}/{map_name}_cost.txt") as f:
            lines = f.readlines()
            for y, line in enumerate(lines):
                for x, char in enumerate(line.strip()):
                    if char == "*":
                        self.setWallToBox(y,x)
                    else:
                        self.clearBox(y,x)

        with open(f"../maps/{map_name}/{map_name}.txt") as f:
            lines = f.readlines()
            for line in lines:
                if line.strip().startswith("pGomas_OBJECTIVE"):
                    obj_coords = line.strip().split(": ")[1].split()
                    obj_x, obj_y = int(obj_coords[0]), int(obj_coords[1])
                    self.setFlagToBox(obj_y, obj_x)

                if line.strip().startswith("pGomas_SPAWN_ALLIED"):
                    coords = line.strip().split(": ")[1].split()
                    x1, y1, x2, y2 = int(coords[1]), int(coords[0]), int(coords[3]), int(coords[2])
                    for x in range(x1, x2+1):
                        for y in range(y1, y2+1):
                            self.setAlliedToBox(x, y)
                
                if line.strip().startswith("pGomas_SPAWN_AXIS"):
                    coords = line.strip().split(": ")[1].split()
                    x1, y1, x2, y2 = int(coords[1]), int(coords[0]), int(coords[3]), int(coords[2])
                    for x in range(x1, x2+1):
                        for y in range(y1, y2+1):
                            self.setAxisToBox(x, y)

                    



            


                        
       
                
        

        

    

