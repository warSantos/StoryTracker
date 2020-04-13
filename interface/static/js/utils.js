
function pageRanking(){

    var texto = document.getElementById("texto").value;
    var data = document.getElementById("data").value;
    $.ajax({
        url: "pageranking",
        type: "POST",
        data: {
            data: data,
            texto: texto
        },
        success: function(data){
            
        },
        error: function(){
            alert("Não foi possível carregar ranking de palavras...");
        }
    });
}