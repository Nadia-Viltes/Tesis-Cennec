//Datos del rol limitaciones
const campoNombreRol = $("[name='nombreRol']");
const campoDescripcionRol = $("[name='descripcionRol']");

//limitar valor
function cortaValor(elemento, cantidadCaracteres){
    elemento.val(elemento.val().slice(0,cantidadCaracteres))
}

//limitacion de caracteres
campoNombreRol.keydown(function(){
    cortaValor(campoNombreRol, 50)
    removeNumber(campoNombreRol)
});
campoNombreRol.keyup(function(){
    cortaValor(campoNombreRol, 50)
    removeNumber(campoNombreRol)
});

campoDescripcionRol.keydown(function(){
    cortaValor(campoDescripcionRol, 100)
    removeNumber(campoDescripcionRol)
});
campoDescripcionRol.keyup(function(){
    cortaValor(campoDescripcionRol, 100)
    removeNumber(campoDescripcionRol)
});