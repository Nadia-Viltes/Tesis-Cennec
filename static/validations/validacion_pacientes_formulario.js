import {obtenerFechaActual} from "/static/validations/utils.js"

//carga el dropdown de provincias por pais
$("[name='pais']").change(function () {
    let idPais = $(this).val();
    $.ajax({
        url: `/pacientes/provincias_dropdown/${idPais}`, 
        method: "GET",
        success: function (response) {
            $("[name='provincia'] option").remove();
            $("[name='provincia']").append(response.htmlresponse);
        }
    });
});

//carga el dropdown de localidades por provincia
$("[name='provincia']").change(function () {
    let idProvincia = $(this).val();
    $.ajax({
        url: `/pacientes/localidades_dropdown/${idProvincia}`, 
        method: "GET",
        success: function (response) {
            $("[name='localidad'] option").remove();
            $("[name='localidad']").append(response.htmlresponse);
            $("[name='barrio'] option").remove();
            $("[name='barrio']").append("<option value='' selected disabled>Seleccionar...</option>");
        }
    });
});

//carga el dropdown de localidades por provincia
$("[name='localidad']").change(function () {
    let idLocalidad = $(this).val();
    $.ajax({
        url: `/pacientes/barrios_dropdown/${idLocalidad}`, 
        method: "GET",
        success: function (response) {
            $("[name='barrio'] option").remove();
            $("[name='barrio']").append(response.htmlresponse);
        }
    });
});

const tituloPantalla = $("[name='tituloPantalla']").text()

//Datos personales limitacion de caracteres
//tab datos personales
const campoNombrePaciente = $("[name='nombrePaciente']");
const campoApellidoPaciente = $("[name='apellidoPaciente']");
const campoDocumento = $("[name='nroDocumento']");
const campoDocumentoValorInicial = $("[name='nroDocumento']").val();
const campoFechaNacimiento = $("[name='fechaNacimiento']");
const campoCalle = $("[name='calle']");
const campoAltura = $("[name='altura']");
const campoPiso = $("[name='piso']");
const campoDpto = $("[name='dpto']");

//tab Datos Tutor
const campoNombreTutor = $("[name='nombreTutor']");
const campoApellidoTutor = $("[name='apellidoTutor']");
const campoOcupacion = $("[name='ocupacion']");
const campoNroCelular = $("[name='nroCelular']");
const campoNroFijo = $("[name='nroFijo']");

//Tab financiador
const campoFinanciador = $("[name='financiador']")
const campoNroAfiliado = $("[name='nroAfiliado']")
//esto lo hago para poder hacer las validaciones en el editar
const campoNroAfiliadoValorInicial = campoNroAfiliado.val()

//seteo al campo
$(campoFechaNacimiento).attr("min", "1960-01-01")
$(campoFechaNacimiento).attr("max", "2090-01-01")

//si valor contiene numeros los quito
function removeNumber(element){
    const REGEXP = /[0-9]/g;
    element.val(element.val().replace(REGEXP, ""))
}

//limitar valor
function cortaValor(elemento, cantidadCaracteres){
    elemento.val(elemento.val().slice(0,cantidadCaracteres))
}

//no permite valor negativo
function valorNegativo(elemento){
    if(elemento.val() < 0){
        elemento.val('')
    }
}

//limitacion de caracteres
campoNombrePaciente.keydown(function(){
    cortaValor(campoNombrePaciente, 50)
    removeNumber(campoNombrePaciente)
});

campoNombrePaciente.keyup(function(){
    cortaValor(campoNombrePaciente, 50)
    removeNumber(campoNombrePaciente)
});

campoApellidoPaciente.keydown(function(){
    cortaValor(campoApellidoPaciente, 50)
    removeNumber(campoApellidoPaciente)
});

campoApellidoPaciente.keyup(function(){
    cortaValor(campoApellidoPaciente, 50)
    removeNumber(campoApellidoPaciente)
});

campoDocumento.keydown(function(){
    cortaValor(campoDocumento, 8)
    valorNegativo(campoDocumento)
});

campoDocumento.keyup(function(){
    cortaValor(campoDocumento, 8)
    valorNegativo(campoDocumento)
});

campoDocumento.change(function(){
    if(campoDocumento.val() <= 0) {
        campoDocumento.val('');
    }    
});   

campoCalle.keydown(function(){
    cortaValor(campoCalle, 50)
});

campoCalle.keyup(function(){
    cortaValor(campoCalle, 50)
});

campoAltura.keydown(function(){
    cortaValor(campoAltura, 10)
    valorNegativo(campoAltura)
});

campoAltura.keyup(function(){
    cortaValor(campoAltura, 10)
    valorNegativo(campoAltura)
});

campoAltura.change(function(){
    if(campoAltura.val() <= 0) {
        campoAltura.val('');
    }    
});    

campoPiso.keydown(function(){
    cortaValor(campoPiso, 5)
    valorNegativo(campoPiso)
});

campoPiso.keyup(function(){
    cortaValor(campoPiso, 5)
    valorNegativo(campoPiso)
});

campoPiso.change(function(){
    if(campoPiso.val() <= 0) {
        campoPiso.val('');
    }    
});

campoDpto.keydown(function(){
    cortaValor(campoDpto, 5)
    valorNegativo(campoDpto)
});

campoDpto.keyup(function(){
    cortaValor(campoDpto, 5)
    valorNegativo(campoDpto)
});

campoDpto.change(function(){
    if(campoDpto.val() <= 0) {
        campoDpto.val('');
    }    
}) 

//limitacion en tab tutor
campoNombreTutor.keydown(function(){
    cortaValor(campoNombreTutor, 50)
    removeNumber(campoNombreTutor)
});

campoNombreTutor.keyup(function(){
    cortaValor(campoNombreTutor, 50)
    removeNumber(campoNombreTutor)
});

campoApellidoTutor.keydown(function(){
    cortaValor(campoApellidoTutor, 50)
    removeNumber(campoNombreTutor)
});

campoApellidoTutor.keyup(function(){
    cortaValor(campoApellidoTutor, 50)
    removeNumber(campoNombreTutor)
});

campoOcupacion.keydown(function(){
    cortaValor(campoOcupacion, 50)
});

campoOcupacion.keyup(function(){
    cortaValor(campoOcupacion, 50)
});

campoNroCelular.keydown(function(){
    cortaValor(campoNroCelular, 15)
    valorNegativo(campoNroCelular)
});

campoNroCelular.keyup(function(){
    cortaValor(campoNroCelular, 15)
    valorNegativo(campoNroCelular)
});

campoNroFijo.keydown(function(){
    cortaValor(campoNroFijo, 15)
    valorNegativo(campoNroFijo)
});

campoNroFijo.keyup(function(){
    cortaValor(campoNroFijo, 15)
    valorNegativo(campoNroFijo)
});

//limitacion en financiador tab
campoNroAfiliado.keydown(function(){
    cortaValor(campoNroAfiliado, 20)
});

campoNroAfiliado.keyup(function(){
    cortaValor(campoNroAfiliado, 20)
});

//Cambia tab on submit
$("#buttonGuardarFormulario").click(function () {
    //tabs
    const datosPersonalesTab = $("[name='datosPersonalesTab']")
    const tutorTab = $("[name='tutorTab']")
    const financiadorTab = $("[name='financiadorTab']")

    //campos de tabs
    const fieldsTabPaciente = $("[validation-tab-paciente='true']");
    const fieldsTabTutor = $("[validation-tab-tutor='true']");
    const fieldsTabFinanciador = $("[validation-tab-financiador='true']");

    let validationDatosPersonales = true;
    let validationTutor = true;
    let validationFinanciador = true;

    //detectar campos vacios
    //tab pacientes
    for(let i=0; i < fieldsTabPaciente.length; i++){
        if(fieldsTabPaciente[i].value == ""){
            validationDatosPersonales = false;
        }
    }

    //detectar campos vacios
    //tab tutor
    for(let i=0; i < fieldsTabTutor.length; i++){
        if(fieldsTabTutor[i].value == ""){
            validationTutor = false;
        }
    }

    //detectar campos vacios
    //tab financiador
    for(let i=0; i < fieldsTabFinanciador.length; i++){
        if(fieldsTabFinanciador[i].value == ""){
            validationFinanciador = false;
        }
    }

    //Validacion solo campos vacios en tab datos personales
    if(!validationDatosPersonales){
        $(datosPersonalesTab).click();
        for(let i=0; i < fieldsTabPaciente.length; i++){
            if(fieldsTabPaciente[i].value == ""){
                $(fieldsTabPaciente[i]).attr("required", true);
                $(fieldsTabPaciente[i]).attr("oninvalid", "this.setCustomValidity('Este campo es obligatorio')");
                $(fieldsTabPaciente[i]).attr("oninput", "setCustomValidity('')")
                $(fieldsTabPaciente[i]).attr("title", "")
            }
        }
        return;
    }

    let valorDeFecha = campoFechaNacimiento.val()
    let fechaCampo = new Date(valorDeFecha.replace('-', '/'))
    let fechaActual = new Date(obtenerFechaActual().replace('-', '/'))
    if (fechaCampo > fechaActual) {
        $(datosPersonalesTab).click()
        campoFechaNacimiento.addClass("is-invalid")
        return false;
    }

    //Validacion solo campos vacios en tab datos tutor
    if(!validationTutor){
        $(tutorTab).click();
        for(let i=0; i < fieldsTabTutor.length; i++){
            if(fieldsTabTutor[i].value == ""){
                $(fieldsTabTutor[i]).attr("required", true);
                $(fieldsTabTutor[i]).attr("oninvalid", "this.setCustomValidity('Este campo es obligatorio')");
                $(fieldsTabTutor[i]).attr("oninput", "setCustomValidity('')")
                $(fieldsTabTutor[i]).attr("title", "")
            }
        }
        return;
    }

    //Validacion campos vacios en datos financiador
    if(!validationFinanciador){
        $(financiadorTab).click();
        for(let i=0; i < fieldsTabFinanciador.length; i++){
            if(fieldsTabFinanciador[i].value == ""){
                $(fieldsTabFinanciador[i]).attr("required", true);
                $(fieldsTabFinanciador[i]).attr("oninvalid", "this.setCustomValidity('Este campo es obligatorio')");
                $(fieldsTabFinanciador[i]).attr("oninput", "setCustomValidity('')")
                $(fieldsTabFinanciador[i]).attr("title", "")
            }
        }
        return;
    }

    //chequear numero afiliado para el agregar y el editar, ver logica, esto es inmantenible
    let financiadorDiferente = true;
    if(campoNroAfiliadoValorInicial != campoNroAfiliado.val()){
        $.ajax({
            url: "/pacientes/chequear_financiador", 
            method: "POST",
            async: false,
            data: {
                "financiador_id": campoFinanciador.val(),
                "numero_afiliado": campoNroAfiliado.val()
            },
            success: function(response) {
                if(response.chequea){
                    const MENSAJE = "El numero de financiador ya existe"
                    const componenteDeAlerta = `<div class='alert alert-danger' role='alert'>${MENSAJE}</div>`;
                    $("#mensajeAlerta").empty();
                    $("#mensajeAlerta").append(componenteDeAlerta);
                    financiadorDiferente = false;
                }
            }
        });
    }
    if(!financiadorDiferente){
        return financiadorDiferente
    }

    //para validar DNI
    let documentoDiferente = true;
    if(campoDocumentoValorInicial != campoDocumento.val()){
        $.ajax({
            url: "/pacientes/chequear_documento", 
            method: "POST",
            async: false,
            data: {
                "documento": campoDocumento.val(),
            },
            success: function(response) {
                if(response.chequea){
                    const MENSAJE = "El n??mero de documento ya existe para otra persona"
                    const componenteDeAlerta = `<div class='alert alert-danger' role='alert'>${MENSAJE}</div>`;
                    $("#mensajeAlerta").empty();
                    $("#mensajeAlerta").append(componenteDeAlerta);
                    documentoDiferente = false;
                }
            }
        });
    }
    if(!documentoDiferente){
        return documentoDiferente
    }
});
