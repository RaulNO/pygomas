from django.shortcuts import render, redirect
from mainApp.functions import *
from mainApp.executeGame import ExecuteGame;

def main(request):

    if(request.method == 'GET'):
        global executeGame 
        if executeGame is None:
            print("Inicializamos executeGame")
            executeGame = ExecuteGame()
        return render(request,'index.html')
    
def managerConfig(request):
    
    if(request.method == "GET"):
        options = rellenarMapSelect(executeGame)
        return render(request, 'managerConfig.html', {"options": options})
    
def agentConfig(request):
    if(request.method == "GET"):
        return render(request, 'agentConfig.html')
    else:
        if(request.POST.get("saveNumberOfPlayers")=="saveButton"):
            number = request.POST.get("players")
            playerNumber = [i for i in range(int(number))]
            context = {'playerNumber': playerNumber, 'number': number}
            return render(request, 'agentConfig.html', context)
        else:
            createJSONAgents(request, executeGame)
            return redirect("/")

def partidaEnCurso(request):
    empezarJuego(executeGame)
    return render(request, 'jugando.html')







    
   
    

