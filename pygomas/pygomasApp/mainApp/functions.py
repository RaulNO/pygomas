from django.shortcuts import render, redirect
import os
from mainApp.executeGame import ExecuteGame;
import json


def rellenarMapSelect(executeGame):
    # Obtener nombres de las carpetas en la carpeta "maps"
    maps_dir = os.listdir("D:\pygomas\pygomas\maps")
    return maps_dir

def empezarJuego(executeGame):
    executeGame.execute()

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
        executeGame.set_agents(jsonFinal)
        executeGame.set_numPlayers(cont)
    

   
  