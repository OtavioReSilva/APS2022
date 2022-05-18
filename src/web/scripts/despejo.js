window.onload = myF;
eel.expose(closeDespejoScreen);
function closeDespejoScreen() {
  window.close();
}

function irParaAnalytics() {
  eel.openPage("despejo.html", "dashboard.html");
}

function irParaUsuarios() {
  eel.openPage("despejo.html", "cadastro.html");
}

function irParaChat() {
  eel.openPage("despejo.html", "chat.html");
}

function cadastrarDespejo() {
  const empresa = document.getElementById("empresa").value;
  const cnpj = document.getElementById("cnpj").value;
  const tipo = document.getElementById("tipo").value;
  const quantidade = document.getElementById("quantidade").value;
  const regiao = document.getElementById("regiao").value

      eel.CadastroDespejo(empresa, cnpj, tipo, quantidade, regiao)()
      .then((result) => {
       
      });
  }

function myF() {
  var x = document.getElementById("empresa");
  var option = document.createElement("option");
  
  eel.CadastroDespejo(empresa, cnpj, tipo, quantidade, regiao)()
      .then((result) => {
        if (result == 'CONFIRMED USER') {
          eel.openPage("login.html", "chat.html");
        } else if (result == 'USER IS ALREADY CONNECTED') {
          alert("Usuário já conectado!");
        } else if (result == 'USER DOES NOT EXIST') {
          alert("Usuário não existe!");
        }
      });
  option.value = "hand";
  option.text = "Hand";
  x.add(option);
}
