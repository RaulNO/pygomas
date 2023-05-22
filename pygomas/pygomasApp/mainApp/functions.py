from django.shortcuts import render, redirect
import os
from mainApp.executeGame import ExecuteGame;
import json
import fileinput
import subprocess
import time


def rellenarMapSelect():
    # Obtener nombres de las carpetas en la carpeta "maps"
    maps_dir = os.listdir("../maps")
    return maps_dir

def obtenerSaves():
    saves = os.listdir("../saves")
    return saves

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
    

    if (agent == 'manager'):
        comandoManager = 'pygomas manager -j ' + manager + '@' +server+ ' -m '+ map_name +' -mp ../maps/ -sj ' + service + '@' + server + ' -np ' + str(numPlayers) + ' --port ' + port + ' -t ' + LimitTime
        subprocess.Popen(['cmd.exe', '/k', comandoManager])
        time.sleep(20)

    if (agent == 'render'): ##Se puede añadir puerto y direccion del manager
       comandoVista = 'pygomas render --maps ../maps/ --ip ' + server
       subprocess.Popen(['cmd.exe', '/k', comandoVista])  

    if (agent == 'soldiers'):
        comandoAgentes = 'cd ../../ejemplos & pygomas run -g' + agents + '.json -mp ../pygomas/maps'  
        subprocess.Popen(['cmd.exe', '/k', comandoAgentes])

def launchManagerOnline(request):
    manager = request.POST.get("NombreManager")
    server = request.POST.get("NombreServer")
    map_name = request.POST.get("mapName")
    service = request.POST.get("NombreServicio")
    numPlayers = request.POST.get("Njugadores")
    port = request.POST.get("Puerto")
    LimitTime = request.POST.get("matchTime")
    
    comandoManager = 'pygomas manager -j ' + manager + '@' +server+ ' -m '+ map_name +' -mp ../maps/ -sj ' + service + '@' + server + ' -np ' + str(numPlayers) + ' --port ' + port + ' -t ' + LimitTime
    subprocess.Popen(['cmd.exe', '/k', comandoManager])

def launchSoldierOnline():

    comandoAgentes = 'cd ../../ejemplos & pygomas run -g temp.json -mp ../pygomas/maps'  
    subprocess.Popen(['cmd.exe', '/k', comandoAgentes])   

def launchRenderOnline(request):
    name = request.POST.get("NombreServer")
    comandoVista = 'pygomas render --maps ../maps/ --ip ' + name
    subprocess.Popen(['cmd.exe', '/k', comandoVista])  
  
def createConfigFolder(configName):
    folderPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'saves', configName))
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    filePath = os.path.join(folderPath, f"{configName}_config.txt")
    with open(filePath, 'w') as f:
        f.write("SERVER: desktop-5hmpkhv\n")
        f.write("MAP_NAME: map_01\n")
        f.write("NUM_PLAYERS: 8\n")
        f.write("AGENTS: ejemplo1\n")
        f.write("MANAGER: cmanager\n")
        f.write("SERVICE: cservice\n")
        f.write("PORT: 8001\n")
        f.write("TIME: 60\n")

def createJSONAgents(request, executeGame):
    cont = 0
    AxisAgents = []
    AxisAgent = {}

    AlliedAgents = []
    AlliedAgent = {}

    numero = request.POST.get("players")
    for i in range(int(numero)):
        nameAX =  ""
        rankAX =  ""
        nameALL =  ""
        rankALL =  ""

        nameAX =  request.POST.get("AxisName"+str(i))
        rankAX =  request.POST.get("AxisRank"+str(i))
        nameALL =  request.POST.get("AlliedName"+str(i))
        rankALL =  request.POST.get("AlliedRank"+str(i))

        if(nameAX != None and nameAX != ""):
            AxisAgent = {
                "rank": rankAX,
                "name": nameAX,
                "password": "secret"
            } 
            cont+=1
            AxisAgents.append(AxisAgent)
        if(nameALL != None and nameALL != ""):    
            AlliedAgent = {
                "rank": rankALL,
                "name": nameALL,
                "password": "secret" 
            }
            cont+=1
            AlliedAgents.append(AlliedAgent)

    mainJSON = { "host": "desktop-5hmpkhv",
    "manager": "manager",
    "service": "service",
    "axis": AxisAgents,
    "allied": AlliedAgents
    }
    
    if(AlliedAgents != [] and AxisAgents != []):
        jsonFinal = executeGame.createJSON(mainJSON)
        print("Numplayers: " + str(cont))
        executeGame.set_agents(jsonFinal)
        executeGame.set_numPlayers(cont)

def createJson(request):
     host = request.POST.get("NombreServer")
     manager = request.POST.get("NombreManager")
     service = request.POST.get("NombreServicio")
     team = request.POST.get("team")
     soldierName = request.POST.get("soldierName")
     rank = request.POST.get("rank")
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
     with open('../../ejemplos/temp.json', 'w') as archivo:
         archivo.write(json_string)
        

def buildMap(map, request):

    for i in range(32):
        for j in range(32):
            boxContent = request.get(str(i) + '-' + str(j))
            
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
    folderPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'saves', save))

    config_file = os.path.join(folderPath, save + '_config.txt')

    with fileinput.FileInput(config_file, inplace=True) as file:
        for line in file:
            if line.startswith('MAP_NAME'):
                print('MAP_NAME: {}'.format(map_name))
            else:
                print(line, end='')

def getDataGame(save):
    print("SavE IS " + save)
    folderPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'saves', save))
    config_file = os.path.join(folderPath, save + '_config.txt') 

    with open(config_file, 'r') as f:
        lines = f.readlines()

    data = {}

    for line in lines:
        key, value = line.strip().split(': ')
        data[key] = value

    print(data)
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

def configurarManager(save, request):

    folderPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..', 'saves', save))

    config_file = os.path.join(folderPath, save + '_config.txt')

    with fileinput.FileInput(config_file, inplace=True) as file:
        for line in file:
            if line.startswith('SERVER'):
                print('SERVER: {}'.format(request.POST.get('NombreServer')))
            elif line.startswith('MANAGER'):
                print('MANAGER: {}'.format(request.POST.get('NombreManager')))
            elif line.startswith('SERVICE'):
                print('SERVICE: {}'.format(request.POST.get('NombreServicio')))
            elif line.startswith('PORT'):
                print('PORT: {}'.format(request.POST.get('Puerto')))
            elif line.startswith('NUM_PLAYERS'):
                print('NUM_PLAYERS: {}'.format(request.POST.get('Njugadores')))
            elif line.startswith('TIME'):
                print('TIME: {}'.format(request.POST.get('matchTime')))
            else:
                print(line, end='')
