
document.addEventListener("DOMContentLoaded", function() {
    
    var alliedList = document.getElementById("alliedList").dataset.valor;
    var axisList = document.getElementById("axisList").dataset.valor;
    var firstLoad = document.getElementById("main").dataset.valor;
    
    if(firstLoad === 'true'){
        console.log("Primera carga, guardamos listas iniciales...")
        localStorage.setItem("axisList", axisList);
        localStorage.setItem("alliedList", alliedList);
    }
    else{
        console.log("Segunda carga, se actualizan las listas...");

        var firstListAxis = localStorage.getItem("axisList");
        var firstListAllied = localStorage.getItem("alliedList");
        
        actualizarEstado(compareList(firstListAxis, axisList));
        actualizarEstado(compareList(firstListAllied,alliedList));
    }
  });

  function actualizarEstado(deadList){
    var spanElement;
    var parent;
    var imgElement;

    for(var i = 0; i < deadList.length; i++){
      spanElement = document.getElementById(deadList[i]);
      parent = spanElement.parentNode.parentNode;
      imgElement = parent.firstElementChild.querySelector("img");
      imgElement.src = "/static/icons/dead.png";

    }
  }

  function compareList(originalList, modifiedList) {
    

    if(modifiedList == '[]'){
      return originalList
    }
    else{
        var originalListArray = originalList.match(/'([^']+)'/g).map(function(item) {
          return item.slice(1, -1);
        });
        var modifiedListArray = modifiedList.match(/'([^']+)'/g).map(function(item) {
          return item.slice(1, -1);
        });
        
        var deadSoldiers = [];

        for (var i = 0; i < originalListArray.length; i++) {
          var elemento = originalListArray[i];
          if (!modifiedListArray.includes(elemento)) {
            deadSoldiers.push(elemento);
          }
        }
        return deadSoldiers;
    }
  }
  
  
  
  
  