/* CODIGO QUE REALIZA LA PAGINA (detalle.html) APENAS ARRANCA*/ 
window.onload = function() {
    var code = document.getElementById("codigo").innerHTML
    var foto = document.getElementById("foto");
    var foto2 = document.getElementById("foto2");
    if (parseInt(code,10) <= 67388){
        foto.src = "https://raw.githubusercontent.com/NickCracker/Global/main/assets/Div1/"+code+"/"+code+"_1.jpg";
        foto2.src = "https://raw.githubusercontent.com/NickCracker/Global/main/assets/Div1/"+code+"/"+code+"_1.jpg";
    }
    else if (parseInt(code,10) <= 256642){
        foto.src = "https://raw.githubusercontent.com/NickCracker/Global/main/assets/Div2/"+code+"/"+code+"_1.jpg";
        foto2.src = "https://raw.githubusercontent.com/NickCracker/Global/main/assets/Div2/"+code+"/"+code+"_1.jpg";
    }
    else if (parseInt(code,10) <= 257179){
        foto.src = "https://raw.githubusercontent.com/NickCracker/Global/main/assets/Div3/"+code+"/"+code+"_1.jpg";
        foto2.src = "https://raw.githubusercontent.com/NickCracker/Global/main/assets/Div3/"+code+"/"+code+"_1.jpg";
    }
    else if (parseInt(code,10) <= 1008023){
        foto.src = "https://raw.githubusercontent.com/NickCracker/Global/main/assets/Div4/"+code+"/"+code+"_1.jpg";
        foto2.src = "https://raw.githubusercontent.com/NickCracker/Global/main/assets/Div4/"+code+"/"+code+"_1.jpg";
    }
    else if (parseInt(code,10) <= 66661102){
        foto.src = "https://raw.githubusercontent.com/NickCracker/Global/main/assets/Div5/"+code+"/"+code+"_1.jpg";
        foto2.src = "https://raw.githubusercontent.com/NickCracker/Global/main/assets/Div5/"+code+"/"+code+"_1.jpg";
    }
    else{
        foto.src = "https://raw.githubusercontent.com/NickCracker/Global/main/assets/Div6/"+code+"/"+code+"_1.jpg";
        foto2.src = "https://raw.githubusercontent.com/NickCracker/Global/main/assets/Div6/"+code+"/"+code+"_1.jpg";
    }
}
