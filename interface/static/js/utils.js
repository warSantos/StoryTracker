function criarModal(documento) {

    card = document.createElement("w3-card-4");
    // Configurando o header com a classe do documento.
    classe = document.createElement("header");
    classe.innerHTML = documento.classe;
    classe.classList.add("w3-container");
    classe.classList.add("w3-blue");
    // Configurando o espaço com o título.
    titulo = document.createElement("p");
    titulo.innerHTML = documento.titulo;
    div_titulo = document.createElement("div");
    div_titulo.classList.add("w3-container");
    div_titulo.appendChild(titulo);
    // Configurando a barra de texto.
    rodape = document.createElement("footer");
    rodape.innerHTML = "Click to see the fulll text..."
    rodape.classList.add("w3-container");
    rodape.classList.add("w3-grey");
    // Adicionando os elementos no card.
    card.appendChild(classe);
    card.appendChild(div_titulo);
    card.appendChild(rodape);
    /*
    <div class="w3-card-4">
      <header class="w3-container w3-blue">
        <h1>Classe</h1>
      </header>
      <div class="w3-container">
        <p onclick="document.getElementById('id01').style.display='block'">Lorem ipsum...</p>
      </div>
      <footer class="w3-container w3-blue">
        <h5>Score: 0.78</h5>
      </footer>
  </div> 
    */
    return card;
}

function pageRanking() {

    var texto = document.getElementById("texto").value;
    var data = document.getElementById("data").value;
    $.ajax({
        url: "pageranking/",
        type: "POST",
        data: {
            data: data,
            texto: texto
        },
        success: function (data) {
            // Construção do painel de modais.
            var painel = document.getElementById("painel");
            ultimoElemento = painel.lastElementChild;
            // Removendo os documentos já existentes.
            while (ultimoElemento) {
                painel.removeChild(ultimoElemento);
                ultimoElemento = painel.lastElementChild;
            }
            // Adicionando os novos documentos.
            painel.classList.add("w3-display-container");
            for (index in data) {
                // Criando o modal.
                modal = criarModal(data[index]);
                painel.appendChild(modal);
            }
        },
        error: function () {
            alert("Não foi possível carregar ranking de palavras...");
        }
    });
}