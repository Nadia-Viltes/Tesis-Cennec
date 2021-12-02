$("[name='checkRol']").change(function () {
    const idRol = $(this).val();
    $.ajax({
        url: "/configuracion/usuarios/setear_privilegios_rol_seleccionado",
        method: "POST",
        data: {
            "idRol": idRol
        },
        success: function (response) {
            const privilegios = response.privilegios
            $(`[type='checkbox']`).prop('checked', false)
            for (const privilegio of privilegios) {
                $(`[type='checkbox'][value='${privilegio}']`).prop('checked', true)
            }
        }
    });
});

//Datos del rol limitaciones
const campoNombreUsuario = $("[name='NombreUsuarioInput']");
const campoNombreUsuarioInicial = $("[name='NombreUsuarioInput']").val();
const campoPassword = $("[name='inputPasswordUsuario']");
const campoPasswordRepetir = $("[name='inputPasswordRepetir']");

//campos obligatorio
let camposValidacion = $("[validation-field='true']")
for(let i=0; i < camposValidacion.length; i++){
        $(camposValidacion[i]).attr("required", true);
        $(camposValidacion[i]).attr("oninvalid", "this.setCustomValidity('Este campo es obligatorio')");
        $(camposValidacion[i]).attr("oninput", "setCustomValidity('')")
        $(camposValidacion[i]).attr("title", "")
}

//limitar valor
function cortaValor(elemento, cantidadCaracteres){
    elemento.val(elemento.val().slice(0,cantidadCaracteres))
}

//limitacion de caracteres
campoNombreUsuario.keydown(function(){
    cortaValor(campoNombreUsuario, 50)
});
campoNombreUsuario.keyup(function(){
    cortaValor(campoNombreUsuario, 50)
});

campoPassword.keydown(function(){
    cortaValor(campoPassword, 8)
});
campoPassword.keyup(function(){
    cortaValor(campoPassword, 8)
});

campoPasswordRepetir.keydown(function(){
    cortaValor(campoPasswordRepetir, 8)
});
campoPasswordRepetir.keyup(function(){
    cortaValor(campoPasswordRepetir, 8)
});

$("#buttonGuardarUsuario").click(function () {
    //chequear existencia de nombre de usuario
    if(campoNombreUsuarioInicial != campoNombreUsuario.val()){
        let usuarioPermitido = true
        $.ajax({
            url: "/configuracion/usuarios/chequear_usuario_existente",
            async: false,
            method: "POST",
            data: {
                "nombre_usuario": campoNombreUsuario.val()
            },
            success: function (response) {
                if(response.chequea){
                    campoNombreUsuario.addClass("is-invalid");
                    usuarioPermitido = false;
                }
            }
        });
        if(!usuarioPermitido){
            return usuarioPermitido;
        }
    }

    if(campoPassword.val() != campoPasswordRepetir.val()){
        campoPassword.addClass("is-invalid");
        campoPasswordRepetir.addClass("is-invalid");
        return false;
    }
});    