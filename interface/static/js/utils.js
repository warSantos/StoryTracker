function criarModal(documento) {

    
    // Configurando a cor das classes.
    if (documento.classe == "mercado"){
        cor = "w3-orange";
    }else if (documento.classe == "poder"){
        cor = "w3-red";
    }else if (documento.classe == "tec"){
        cor = "w3-indigo";
    }else if (documento.classe == "ilustrada"){
        cor = "w3-light-blue";
    }else if (documento.classe == "esporte"){
        cor = "w3-light-green";
    }else { // Mundo
        cor = "w3-amber";
    }
    // Criando o card e configurando sua posição.
    card = document.createElement("div");
    card.classList.add("w3-card-4");
    card.classList.add("w-25");
    card.classList.add("rounded");
    card.classList.add("m-1");
    // Configurando o header com a classe do documento.
    h = document.createElement("header");
    classe = document.createElement("h1");
    classe.innerHTML = documento.classe;
    classe.classList.add("w3-container");
    classe.classList.add(cor);
    h.appendChild(classe);
    // Configurando o espaço com o título.
    titulo = document.createElement("p");
    titulo.innerHTML = documento.titulo;
    div_titulo = document.createElement("div");
    div_titulo.classList.add("w3-container");
    div_titulo.appendChild(titulo);
    // Configurando a barra de texto.
    rodape = document.createElement("footer");
    rodape.classList.add("w3-container");
    rodape.classList.add(cor);
    texto_rodape = document.createElement("p");
    texto_underscore = document.createElement("a");
    texto_underscore.innerHTML = "See more..."
    texto_underscore.href = '#';
    texto_rodape.appendChild(texto_underscore);

    // Adicionando o moda com o texto no documento.
    modal = document.createElement("div");
    modal.classList.add("w3-modal");
    //modal.classList.add("w-50");
    modal.id = documento.id_documento;
    //modal.style.display = 'block';
    sub_div = document.createElement("div");
    sub_div.classList.add("w3-modal-content");
    sub_div.classList.add("w3-animate-zoom");
    sub_div.classList.add("w3-card-4");
    header_modal = document.createElement("header");
    header_modal.classList.add("w3-container");
    header_modal.classList.add(cor);
    h_titulo = document.createElement("h3");
    h_titulo.innerHTML = documento.titulo;
    fechar = document.createElement("span");
    fechar.classList.add("w3-button");
    fechar.classList.add("w3-display-topright");
    fechar.innerHTML = "&times;";

    div_texto = document.createElement("div");
    div_texto.classList.add("w3-container");
    texto_modal = document.createElement("p");
    texto_modal.innerHTML = documento.texto;
    footer_link = document.createElement("footer");
    footer_link.classList.add("w3-container");
    footer_link.classList.add(cor);
    link = document.createElement("a");
    link.innerHTML = documento.link;
    link.href = documento.link;
    link.target = "_blank";

    // Adicionando os elementos na árvore.
    footer_link.appendChild(link);
    div_texto.appendChild(texto_modal);
    header_modal.appendChild(h_titulo);
    sub_div.appendChild(header_modal);
    sub_div.appendChild(div_texto);
    sub_div.appendChild(footer_link);
    modal.appendChild(sub_div);

    // Configurando link para o modal.
    texto_rodape.onclick = function () {
        document.getElementById(documento.id_documento.toString()).style.display = 'block';
    }
    rodape.appendChild(texto_rodape);
    // Configurando o botão de fechar do modal.
    fechar.onclick = function () {
        document.getElementById(documento.id_documento.toString()).style.display = 'none';
    }
    header_modal.appendChild(fechar);
    // Adicionando os elementos no card.
    card.appendChild(classe);
    card.appendChild(div_titulo);
    card.appendChild(rodape);

    return [card, modal];
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
            //painel.classList.add("w3-display-container");
            cont = 0;
            var divs = [];
            for (index in data) {
                // Criando os modais.
                divs.push(criarModal(data[index]));
                if (cont == 3) {
                    var nova_div = document.createElement("div");
                    nova_div.classList.add("d-flex");
                    nova_div.classList.add("justify-content-between");
                    while (divs.length > 0) {
                        cards = divs.shift();
                        nova_div.appendChild(cards[0]);
                        nova_div.appendChild(cards[1]);
                    }
                    painel.appendChild(nova_div);
                    cont = -1;
                }
                cont += 1;
            }
            var nova_div = document.createElement("div");
            nova_div.classList.add("d-flex");
            nova_div.classList.add("justify-content-between");
            while (divs.length > 0) {
                cards = divs.shift();
                nova_div.appendChild(cards[0]);
                nova_div.appendChild(cards[1]);
            }
            painel.appendChild(nova_div);
        },
        error: function () {
            alert("Não foi possível carregar ranking de palavras...");
        }
    });
}