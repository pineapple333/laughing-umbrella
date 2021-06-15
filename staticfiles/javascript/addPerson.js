var n = [];

function pushData(){
  inputText = document.getElementById('addNew').value;
  n.push(inputText);
  document.querySelector('#lists ul').innerHTML += "<li>" + inputText + "</li>";
}