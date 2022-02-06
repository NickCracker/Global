

function ver_foto(){
    var codigo = document.getElementById("codigo")
    var code = codigo.innerHTML ;
    var foto = document.getElementById("foto");
    foto.src = "https://raw.githubusercontent.com/NickCracker/Global/main/assets/Productos/"+code+"/"+code+"_1.jpg";
    console.log(foto.src)
}
