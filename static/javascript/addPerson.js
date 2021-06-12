var n = [];

function pushData(){
  inputText = document.getElementById('addNew').value;
  n.push(inputText); // This does nothing, except keep an array internally.

  document.querySelector('#lists ul').innerHTML += "<li>" + inputText + "</li>";
}