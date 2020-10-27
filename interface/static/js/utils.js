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
    
    // Criando div para conter o header.
    var div_h_card = document.createElement("div");
    div_h_card.classList.add("d-flex");
    div_h_card.classList.add("flex-row");
    div_h_card.classList.add("justify-content-around");
    
    // Configurando o header com a classe do documento.
    //h = document.createElement("header");
    classe = document.createElement("h1");
    classe.innerHTML = documento.classe;
    classe.classList.add("w3-container");
    classe.classList.add(cor);
    //h.appendChild(classe);
    
    // Adicionando input de selecionado.
    var selecao = document.createElement("INPUT");
    selecao.setAttribute("type", "checkbox");
    selecao.id = "checkbox_"+documento.id_documento.toString();
    label = document.createElement("label");
    label.htmlFor = "checkbox_"+documento.id_documento.toString();
    label.appendChild(document.createTextNode('Select'));
    
    //selecao.classList.add("custom-control-input");
    selecao.classList.add("custom-select-lg");
    div_h_card.append(classe);
    div_h_card.append(label);
    div_h_card.append(selecao);
    
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

    // Adicionando o modal com o texto no documento.
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
    //card.appendChild(selecao);
    //card.appendChild(classe);
    card.appendChild(div_h_card);
    card.appendChild(div_titulo);
    card.appendChild(rodape);

    return [card, modal];
}

function pageRanking() {

    var texto = document.getElementById("texto").value;
    var data = document.getElementById("data").value;
    var meses = document.getElementById("meses").value;
    var n_docs = document.getElementById("n_arquivos_ranking").value;
    $.ajax({
        url: "pageranking/",
        type: "POST",
        data: {
            data: data,
            texto: texto,
            meses: meses,
            n_docs: n_docs
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

            // Ativando o botão de envio dos documentos.
            var btn = document.getElementById("botao_timeline");
            btn.style.display = 'block';
        },
        error: function () {
            alert("Não foi possível carregar ranking de palavras...");
        }
    });
}

function gerarTimeline(){

    var id_doc = -1;
    // Selecionando DIV com os cards onde estão os documentos para seleção.
    var checkboxes = document.getElementById('painel').querySelectorAll('input');
    for (var check = 0; check < checkboxes.length; check++){
        // Se os elementos estiverem selecionados.
        if (checkboxes[check].checked){
            id_doc = checkboxes[check].id;
            break;
        }
    }

    if (id_doc == -1){
        alert("You have to select one document at least.");
        return;
    }

    // Criando e configurando o formulário para realizar o submit.
    const form = document.createElement('form');
    form.method = "POST";
    form.action = 'timeline/';
    // Configurando o input para levar as informações de filtro.
    const input_falso = document.createElement('input');
    input_falso.type = 'hidden';
    input_falso.name = 'info';
    // Configurando os valores.
    var info = {};
    info["id_doc"] = id_doc
    info["query"] = document.getElementById("texto").value;
    info["query_doc"] = document.getElementById("query_doc").value;
    info["meses"] = document.getElementById("advanced_meses").value;
    info["tam_intervalo"] = document.getElementById("advanced_intervalo").value;
    input_falso.value = JSON.stringify(info);
    form.appendChild(input_falso);
    document.body.appendChild(form);
    form.submit();
}