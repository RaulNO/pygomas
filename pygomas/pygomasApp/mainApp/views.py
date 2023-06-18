
from django.shortcuts import render, redirect
from mainApp.functions import *
from mainApp.executeGame import ExecuteGame;
from mainApp.map import Map;
from django.utils.translation import gettext_lazy as _
from spade.agent import Agent

    
           

def launcher(request):
    global mainSave
    dataGame = getDataGame(mainSave)
    context = {
            "data_game": dataGame,
            "mainSave" : mainSave
        }
    if(request.method == 'GET'):
        
        return render(request, 'launcher.html', context)
    elif(request.method == 'POST'):
        
        manager = request.POST.get('manager')
        soldiers = request.POST.get('soldiers')
        renderI = request.POST.get('render')
    
        if(manager is not None and manager != ""):
            launchLocal(mainSave,manager)
        if(soldiers is not None and soldiers != ""):
            launchLocal(mainSave,soldiers)    
        if(renderI is not None and renderI != ""):
            launchLocal(mainSave, renderI)
        
        return render(request, 'launcher.html', context)
        

        
def createMap(request):
    global mainSave
    global map
    
    if request.method == 'POST':
        if(request.POST.get("action-button")=="saveMap"):
            map_name =  request.POST.get("map_name")
            map = buildMap(map, request.POST)
            map.createTxt(map_name)
            mapOptions = rellenarMapSelect()
            context = {
                'options': mapOptions,
                'map': map.get_map(),
                'map_name': request.POST.get("map_name")
            }

            return render(request, 'mapEditor.html', context)   

        elif(request.POST.get("action-button")=="loadMap"):
            map.loadMap(request.POST.get("select-map"))  
            mapOptions = rellenarMapSelect()
            context = {
                'options': mapOptions,
                'map': map.get_map(),
                'map_name': request.POST.get("select-map")
            }
            return render(request, 'mapEditor.html', context)   
        
        elif(request.POST.get("action-button")=="assignMap"):
            map_name =  request.POST.get("map_name")
            map = buildMap(map, request.POST)
            map.createTxt(map_name)
            assignMap(mainSave, map_name)
            return redirect("/pygomas/menu")  
       
    else:
        mapOptions = rellenarMapSelect()
        context = {
            'map': map.get_map(),
            'options': mapOptions
        }
        return render(request, 'mapEditor.html', context)



    
def onlinemode(request):
    return render(request, 'onlinemode.html')

def sendManager(request):
    mapOptions = rellenarMapSelect()
    context = {
            'options': mapOptions
        }
    if(request.method == 'GET'):
        return render(request, 'sendManager.html', context)
    else:
        launchManagerOnline(request)
        return render(request, 'sendManager.html')

def sendSoldier(request):
    
    if(request.method == 'GET'):
        return render(request, 'sendSoldier.html')
    else:
        createJson(request)
        launchSoldierOnline()
        return render(request, 'sendSoldier.html')

def sendRender(request):
    if(request.method == 'GET'):
        return render(request, 'sendRender.html')
    else:
        launchRenderOnline(request)
        return render(request, 'sendRender.html')



    
   
    

