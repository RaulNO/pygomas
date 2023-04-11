


class Box:

    def __init__(self, has_wall, has_AxisSpawn, has_AlliedSpawn, has_Flag):
        self.has_wall = has_wall
        self.has_AxisSpawn = has_AxisSpawn
        self.has_AlliedSpawn = has_AlliedSpawn
        self.has_Flag = has_Flag

    
    def get_has_wall(self):
        return self._has_wall

    def get_has_AxisSpawn(self):
        return self._has_AxisSpawn

    def get_has_AlliedSpawn(self):
        return self._has_AlliedSpawn

    def get_has_Flag(self):
        return self._has_Flag

    
    def set_has_wall(self, has_wall):
        self._has_wall = has_wall

    def set_has_AxisSpawn(self, has_AxisSpawn):
        self._has_AxisSpawn = has_AxisSpawn

    def set_has_AlliedSpawn(self, has_AlliedSpawn):
        self._has_AlliedSpawn = has_AlliedSpawn

    def set_has_Flag(self, has_Flag):
        self._has_Flag = has_Flag
 