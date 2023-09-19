
document.addEventListener("DOMContentLoaded", function() {

  var InitAlliedList = document.getElementById("alliedList").dataset.valor;
  var InitAxisList = document.getElementById("axisList").dataset.valor;

  var intervalId = setInterval(function(){
    $.ajax({
        url: '/pygomas/getAgentList',
        type: 'GET',
        dataType: 'json',
        headers: {
            'Accept': 'application/json'     
        }, 
      success: function(data) {
        console.log(data);
        
        var axisSoldiersList = JSON.stringify(data.axisSoldiers).replace(/"/g, "'");
        var alliedSoldiersList = JSON.stringify(data.alliedSoldiers).replace(/"/g, "'");
        
        console.log(axisSoldiersList);
        console.log(alliedSoldiersList);

        if (data.finishedGame) {
          console.log("Detenemos el AJAX");
          clearInterval(intervalId);
        }

        actualizarEstado(compareList(InitAlliedList, alliedSoldiersList ));
        actualizarEstado(compareList(InitAxisList, axisSoldiersList));

      },
      error: function(xhr, status, error) {
        console.error(error);
      }
    });
  }, 1000);
    
});

  function actualizarEstado(deadList){
    var spanElement;
    var parent;
    var imgElement;

    for(var i = 0; i < deadList.length; i++){
      console.log("ELEMENTO " + deadList[i])
      spanElement = document.getElementById(deadList[i]);
      parent = spanElement.parentNode.parentNode;
      imgElement = parent.firstElementChild.querySelector("img");
      imgElement.src = "/static/icons/dead.png";
    }
  }

  function compareList(originalList, modifiedList) {
  
    var originalArray = originalList.replace(/\s/g, "").slice(1, -1).split(",");
    var modifiedArray = modifiedList.replace(/\s/g, "").slice(1, -1).split(",");
    console.log("modified" + modifiedArray)
    console.log("original" + originalArray)
    var difference = originalArray.filter((element) => !modifiedArray.includes(element));

    var deadList = difference.map(item => item.replace(/'/g, ''));

    console.log(deadList);

    return deadList;
  }
  
  
  
  
  
  
  
  