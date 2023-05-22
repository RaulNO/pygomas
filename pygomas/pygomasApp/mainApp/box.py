
class Box:

    def __init__(self, has_wall, has_AxisSpawn, has_AlliedSpawn, has_Flag):
        self.has_wall = has_wall
        self.has_axisSpawn = has_AxisSpawn
        self.has_alliedSpawn = has_AlliedSpawn
        self.has_flag = has_Flag

    ##Getters
    def get_has_wall(self):
        return self.has_wall

    def get_has_axisSpawn(self):
        return self.has_axisSpawn

    def get_has_alliedSpawn(self):
        return self.has_alliedSpawn

    def get_has_flag(self):
        return self.has_flag

    ##Setters
    def set_has_wall(self, has_wall):
        self.has_wall = has_wall

    def set_has_axisSpawn(self, has_AxisSpawn):
        self.has_axisSpawn = has_AxisSpawn
       
    def set_has_alliedSpawn(self, has_AlliedSpawn):
        self.has_alliedSpawn = has_AlliedSpawn

    def set_has_flag(self, has_Flag):
        self.has_flag = has_Flag
    
    def clear(self):
        self.set_has_alliedSpawn(False)
        self.set_has_axisSpawn(False)
        self.set_has_flag(False)
        self.set_has_wall(False)

    def toString(self):
        return "Wall? -> " + str(self.get_has_wall()) + " Flag? -> " + str(self.get_has_flag()) + " Allied --> " + str(self.get_has_alliedSpawn()) + " Axis --> " + str(self.get_has_axisSpawn());