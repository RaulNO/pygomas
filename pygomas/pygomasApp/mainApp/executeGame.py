import json
import subprocess
import time


class ExecuteGame:

    def __init__(self):
        self.agents = "ejemplo.json"
        self.numPlayers = 4
        self.map = "map_01"
    
    def get_agents(self):
        return self.agents
    
    def set_agents(self, agents):
        self.agents = agents
        
    def get_numPlayers(self):
        return self.numPlayers
    
    def set_numPlayers(self, numPlayers):
        self.numPlayers = numPlayers
        
    def get_map(self):
        return self.map
    
    def set_map(self, map):
        self.map = map

    def createJSON (self, json_data): 
        json_string = json.dumps(json_data)
        with open('../../ejemplos/archivo.json', 'w') as archivo:
            archivo.write(json_string)
        self.set_agents("archivo.json")
        return "archivo.json"
    
    def execute(self):
        print (self.get_agents())
        print (self.get_numPlayers())
        print (self.get_map())
        comandoManager = 'pygomas manager -j manager@desktop-5hmpkhv -m '+ self.get_map()+' -sj service@desktop-5hmpkhv -np ' + str(self.get_numPlayers()) 
        comandoVista = 'pygomas render'
        comandoAgentes = 'cd ../../ejemplos & pygomas run -g' + self.get_agents()

        subprocess.Popen(['cmd.exe', '/k', comandoManager])
        time.sleep(20)
        subprocess.Popen(['cmd.exe', '/k', comandoAgentes])
        subprocess.Popen(['cmd.exe', '/k', comandoVista])

        print("GAME FINISHED")

        self =  ExecuteGame()