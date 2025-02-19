from django.shortcuts import render, redirect
import os
import json
import fileinput
import subprocess
import time


def rellenarMapSelect():
    # Obtener nombres de los archivos en la carpeta "maps"
    maps_dir = os.listdir("maps")
    return maps_dir
def obtainTroopsFiles():
    # Obtener nombres de los archivos en la carpeta "troopsJSON"
    troops_files = os.listdir("troopsJSON")
    return troops_files

def obtenerSaves(): 
    saves = os.listdir("saves")
    return saves

def modifyJSON(JSONfile, dataGame):
    print('JSONFILE is: ' + str(JSONfile))
    with open ("troopsJSON/"+JSONfile, 'r') as file:
        data = json.load(file)
    data["manager"] = dataGame['MANAGER']
    data["service"] = dataGame['SERVICE']

    with open("troopsJSON/"+JSONfile, 'w') as file:
        json.dump(data, file, indent = 4)

def launchLocal(save,agent):
    print("Lanzando " + agent + ".............")
    ##Save config
    params = getDataGame(save)
    
    server = params["SERVER"]
    map_name = params["MAP_NAME"]
    numPlayers = params["NUM_PLAYERS"]
    agents = params["AGENTS"]
    manager = params["MANAGER"]
    service = params["SERVICE"]
    port = params["PORT"]
    LimitTime = params["TIME"]
    current_dir = os.getcwd()
    maps_path = os.path.join(current_dir, 'maps')

    if (agent == 'manager'):
        comandoManager = 'pygomas manager -j ' + manager + '@' +server+ ' -m '+ map_name +' -mp ' + maps_path + ' -sj ' + service + '@' + server + ' -np ' + str(numPlayers) + ' --port ' + port + ' -t ' + LimitTime
        subprocess.Popen(['cmd.exe', '/k', comandoManager])
        time.sleep(5)

    if (agent == 'render'): 
       comandoVista = 'pygomas render --maps maps --ip ' + server
       subprocess.Popen(['cmd.exe', '/k', comandoVista])  
       
    if (agent == 'soldiers'):
        print("Se van a lanzar los soldiers...")
        comandoAgentes = 'cd troopsJSON & pygomas run -g ' + agents + '.json -mp ../maps/ & cd ..'  
        subprocess.Popen(['cmd.exe', '/k', comandoAgentes])
        time.sleep(3)

def launchManagerOnline(formData):
    manager = formData.get("NombreManager")
    server = formData.get("NombreServer")
    map_name = formData.get("map_name")
    service = formData.get("NombreServicio")
    numPlayers = formData.get("Njugadores")
    port = formData.get("Puerto")
    LimitTime = formData.get("matchTime")
    current_dir = os.getcwd()
    maps_path = os.path.join(current_dir, 'maps')
    
    comandoManager = 'pygomas manager -j ' + manager + '@' +server+ ' -m '+ map_name + ' -mp ' + str(maps_path) + ' -sj ' + service + '@' + server + ' -np ' + str(numPlayers) + ' --port ' + port + ' -t ' + LimitTime
    subprocess.Popen(['cmd.exe', '/k', comandoManager])

def launchSoldierOnline():
    comandoAgentes = 'cd troopsJSON & pygomas run -g temp.json -mp ../maps & cd ..'  
    subprocess.Popen(['cmd.exe', '/k', comandoAgentes])   

def launchRenderOnline(formData):
    name = formData.get("NombreServer")
    comandoVista = 'pygomas render --maps maps --ip ' + name
    subprocess.Popen(['cmd.exe', '/k', comandoVista])  
  
def createConfigFolder(configName):
    print("CREANDO PARTIDA...")
    currentPath = os.path.dirname(os.path.abspath(__file__))
    relativePath = os.path.join(currentPath, "saves", configName)
    if not os.path.exists(relativePath):
        os.makedirs(relativePath)
    filePath = os.path.join(relativePath, f"{configName}_config.txt")
    with open(filePath, 'w') as f:
        f.write("SERVER: desktop-5hmpkhv\n")
        f.write("MAP_NAME: default\n")
        f.write("NUM_PLAYERS: 6\n")
        f.write("AGENTS: default\n")
        f.write("MANAGER: cmanager\n")
        f.write("SERVICE: cservice\n")
        f.write("PORT: 8001\n")
        f.write("TIME: 300\n")

def createJSONAgents(request, formData, dataGame): 
    AxisAgents = []
    AxisAgent = {}

    AlliedAgents = []
    AlliedAgent = {}

    numero = formData.get("players")

    for i in range(int(numero)):
        nameAX =  ""
        rankAX =  ""
        nameALL =  ""
        rankALL =  ""

        nameAX =  formData.get("AxisName"+str(i))
        rankAX =  formData.get("AxisRank"+str(i))
        nameALL =  formData.get("AlliedName"+str(i))
        rankALL =  formData.get("AlliedRank"+str(i))

        if(nameAX != None and nameAX != ""):
            AxisAgent = {
                "rank": rankAX,
                "name": nameAX,
                "password": "secret"
            } 
            AxisAgents.append(AxisAgent)
        if(nameALL != None and nameALL != ""):    
            AlliedAgent = {
                "rank": rankALL,
                "name": nameALL,
                "password": "secret" 
            }
            AlliedAgents.append(AlliedAgent)

    mainJSON = { "host": "desktop-5hmpkhv",
    "manager": dataGame['MANAGER'],
    "service": dataGame['SERVICE'],
    "axis": AxisAgents,
    "allied": AlliedAgents
    }
    
    if(AlliedAgents != [] and AxisAgents != []):
        json_string = json.dumps(mainJSON)
        file_name = formData.get("troopsName")
        path = os.path.join('troopsJSON', file_name+".json")
        with open(path, 'w') as archivo:
            archivo.write(json_string)
        

def createJson(formData):
     host = formData.get("NombreServer")
     manager = formData.get("NombreManager")
     service = formData.get("NombreServicio")
     team = formData.get("team")
     soldierName = formData.get("soldierName")
     rank = formData.get("rank")
     soldier = [{
         "rank": rank,
         "name": soldierName,
         "password" : "secret"
     }]
     jsonData = { 
        "host": host,
        "manager": manager,
        "service": service,
         team : soldier
    }
     
     json_string = json.dumps(jsonData)
     with open('troopsJSON/temp.json', 'w') as archivo:
         archivo.write(json_string)
        

def buildMap(map, formData):

    for i in range(32):
        for j in range(32):
            boxContent = formData.get(str(i) + '-' + str(j))
            
            if(boxContent == 'wall'):
                map.setWallToBox(i,j)
            elif(boxContent == 'flag'):
                map.setFlagToBox(i,j)
            elif(boxContent == 'axis'):
                map.setAxisToBox(i,j)
            elif(boxContent == 'allied'):
                map.setAlliedToBox(i,j)
            else:
                map.clearBox(i,j)
    
    return map

def assignMap(save, map_name):
    currentPath = os.path.dirname(os.path.abspath(__file__))
    relativePath = os.path.join(currentPath, "saves", save)

    config_file = os.path.join(relativePath, save + '_config.txt')

    with fileinput.FileInput(config_file, inplace=True) as file:
        for line in file:
            if line.startswith('MAP_NAME'):
                print('MAP_NAME: {}'.format(map_name))
            else:
                print(line, end='')

def assignTroops(save, troopsName):
    currentPath = os.path.dirname(os.path.abspath(__file__))
    relativePath = os.path.join(currentPath, "saves", save)

    config_file = os.path.join(relativePath, save + '_config.txt')

    with fileinput.FileInput(config_file, inplace=True) as file:
        for line in file:
            if line.startswith('AGENTS'):
                print('AGENTS: {}'.format(troopsName))
            else:
                print(line, end='')                

def getDataGame(save):
    currentPath = os.path.dirname(os.path.abspath(__file__))
    relativePath = os.path.join(currentPath, "saves", save)
    config_file = os.path.join(relativePath, save + '_config.txt') 

    with open(config_file, 'r') as f:
        lines = f.readlines()

    data = {}

    for line in lines:
        key, value = line.strip().split(': ')
        data[key] = value

    server = data['SERVER']
    map_name = data['MAP_NAME']
    num_players = int(data['NUM_PLAYERS'])
    agents = data['AGENTS']
    manager = data['MANAGER']
    service = data['SERVICE']
    port = data['PORT']
    time = data['TIME']
    ##server = data['SERVER']
    return{
        "SERVER" : server,
        "MAP_NAME" : map_name,
        "NUM_PLAYERS" : num_players,
        "AGENTS" : agents,
        "MANAGER" : manager,
        "SERVICE" : service,
        "PORT" : port,
        "TIME" : time
        ##"SERVER" : server
    }

def configurarManager(save, formData):

    currentPath = os.path.dirname(os.path.abspath(__file__))
    relativePath = os.path.join(currentPath, "saves", save)
    config_file = os.path.join(relativePath, save + '_config.txt')

    with fileinput.FileInput(config_file, inplace=True) as file:
        for line in file:
            if line.startswith('SERVER'):
                print('SERVER: {}'.format(formData.get('NombreServer')))
            elif line.startswith('MANAGER'):
                print('MANAGER: {}'.format(formData.get('NombreManager')))
            elif line.startswith('SERVICE'):
                print('SERVICE: {}'.format(formData.get('NombreServicio')))
            elif line.startswith('PORT'):
                print('PORT: {}'.format(formData.get('Puerto')))
            elif line.startswith('NUM_PLAYERS'):
                print('NUM_PLAYERS: {}'.format(formData.get('Njugadores')))
            elif line.startswith('TIME'):
                print('TIME: {}'.format(formData.get('matchTime')))
            else:
                print(line, end='')
