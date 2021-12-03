//Datos del rol limitaciones
const campoNombreRol = $("[name='nombreRol']");
const campoDescripcionRol = $("[name='descripcionRol']");

campoNombreRol.attr("required", true);
campoNombreRol.attr("oninvalid", "this.setCustomValidity('Este campo es obligatorio')");
campoNombreRol.attr("oninput", "setCustomValidity('')")
campoNombreRol.attr("title", "")

//limitar valor
function cortaValor(elemento, cantidadCaracteres){
    elemento.val(elemento.val().slice(0,cantidadCaracteres))
}

//limitacion de caracteres
campoNombreRol.keydown(function(){
    cortaValor(campoNombreRol, 50)
});
campoNombreRol.keyup(function(){
    cortaValor(campoNombreRol, 50)
});

campoDescripcionRol.keydown(function(){
    cortaValor(campoDescripcionRol, 100)
});
campoDescripcionRol.keyup(function(){
    cortaValor(campoDescripcionRol, 100)
});


$("#guardarButton").click(function () {
    
    const checks = $("[name='privilegio_nombre']");
    if(!checks.is(":checked")){
        const MENSAJE = "Al menos debe seleccionar un privilegio"
        const componenteDeAlerta = `<div class='alert alert-danger' role='alert'>${MENSAJE}</div>`;
        $("#mensajeAlerta").empty();
        $("#mensajeAlerta").append(componenteDeAlerta);
        return false;
    }

});    
