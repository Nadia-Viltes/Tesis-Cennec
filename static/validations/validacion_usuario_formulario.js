//Datos del rol limitaciones
const campoNombreUsuario = $("[name='NombreUsuarioInput1']");
const campoPassword = $("[name='inputPasswordUsuario']");
const campoPasswordRepetir = $("[name='inputPasswordRepetir']");

//limitar valor
function cortaValor(elemento, cantidadCaracteres){
    elemento.val(elemento.val().slice(0,cantidadCaracteres))
}

//limitacion de caracteres
campoNombreUsuario.keydown(function(){
    cortaValor(campoNombreUsuario, 50)
    removeNumber(campoNombreUsuario)
});
campoNombreUsuario.keyup(function(){
    cortaValor(campoNombreUsuario, 50)
    removeNumber(campoNombreUsuario)
});

campoPassword.keydown(function(){
    cortaValor(campoPassword, 8)
    removeNumber(campoPassword)
});
campoPassword.keyup(function(){
    cortaValor(campoPassword, 8)
    removeNumber(campoPassword)
});

campoPasswordRepetir.keydown(function(){
    cortaValor(campoPasswordRepetir, 8)
    removeNumber(campoPasswordRepetir)
});
campoPasswordRepetir.keyup(function(){
    cortaValor(campoPasswordRepetir, 8)
    removeNumber(campoPasswordRepetir)
});