//validacion en nro de documento
$("[name='nroDocumento']").change(function(){
    const inputDocumento = $("[name='nroDocumento']");
    if(inputDocumento.val() <= 0) {
        inputDocumento.val(1);
    }

    if(inputDocumento.val().length > 8) {
        inputDocumento.val(inputDocumento.val().slice(0,8));
    }
});

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
});
