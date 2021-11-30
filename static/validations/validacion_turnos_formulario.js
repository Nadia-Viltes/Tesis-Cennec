
//seteo fecha de turno por defecto
let tipoTurnoSelect = $("[name='tipoTurno']")
let especialidadSelect = $("[name='nameEspecialidadDropdown']")
let profesionalSelect = $("[name='nameProfesionalDropdown']")
let fechaTurnoCampo = $("[name='fechaTurno']")
let horaInicioCampo = $("[name='nameHoraInicio']")
let horaFinCampo = $("#idhoraFin")
let horaFinOculta = $("[name='nameHoraFin']")
let campoRequeridos = $("[validation='true']")

const obtenerFechaActual = function () {
    let fecha_actual = new Date()
    let dia = fecha_actual.getDate()
    let mes = fecha_actual.getMonth() + 1
    let anio = fecha_actual.getFullYear()
    return `${anio}-${mes}-${dia}`
}

for (let i= 0; i < campoRequeridos.length; i++) {
    $(campoRequeridos[i]).attr("required", true);
    $(campoRequeridos[i]).attr("oninvalid", "this.setCustomValidity('Este campo es obligatorio')");
    $(campoRequeridos[i]).attr("oninput", "setCustomValidity('')")
    $(campoRequeridos[i]).attr("title", "")
}

//carga el dropdown de profesional por especialidad
$("#idEspecialidadDropdown").change(function () {
    let idEspecialidad = $(this).val();
    $.ajax({
        url: `/turnos/profesionales_dropdown/${idEspecialidad}`,
        method: "GET",
        success: function (response) {
            $("#idProfesionalDropdown option").remove();
            $("#idProfesionalDropdown").append(response.htmlresponse);
        }
    });
});

//Inteligencia en minutos
horaInicioCampo.change(function () {
    let horaInicio = horaInicioCampo.val()
    if (horaInicio != null) {
        horaInicio = horaInicio.split(":")
        let hora = horaInicio[0]
        let minutos = horaInicio[1]
        let date = new Date()
        date.setHours(hora)
        date.setMinutes(minutos)
        date.setMinutes(date.getMinutes() + 30)
        let horaFinal = date.getHours() < 10 ? `0${date.getHours()}` : date.getHours();
        let minutoFinal = date.getMinutes() < 10 ? `0${date.getMinutes()}` : date.getMinutes();
        horaFinOculta.val(`${horaFinal}:${minutoFinal}`)
        horaFinCampo.val(`${horaFinal}:${minutoFinal}`)
    } else {
        horaFinOculta.val('')
        horaFinCampo.val('')
    }
});

$("#formularioDeTurno").on("submit", function(event) {
    let flag = false
    //fechaTurno
    let valorDeFecha = fechaTurnoCampo.val()
    let fechaCampo = new Date(valorDeFecha.replace('-', '/'))
    let fechaActual = new Date(obtenerFechaActual().replace('-', '/'))
    if (fechaCampo < fechaActual) {
        fechaTurnoCampo.addClass("is-invalid")
        return flag;
    }
    if (fechaCampo.getTime() == fechaActual.getTime()) {
        //hora que viene del campo inicio
        //validacion horaInicio
        if (horaInicioCampo.val() == null) {
            horaInicioCampo.addClass("is-invalid")
            return flag;
        }
        let tiempoCompleto = horaInicioCampo.val().split(":");
        let hora = tiempoCompleto[0]
        let minutos = tiempoCompleto[1]
        let fechaActual = new Date()
        let horaActual = fechaActual.getHours()
        let minutosActuales = fechaActual.getMinutes()
        if (hora > horaActual) {
            flag = true
        }
        if (hora == horaActual && minutos > minutosActuales) {
            flag = true
        }
        if (!flag) {
            horaInicioCampo.addClass("is-invalid")
            return flag;
        }
    }

    //validación turno existente
    $.ajax({
        url: "/turnos/chequear_disponibilidad", 
        method: "POST",
        async: false,
        data: {
            "profesionalId": profesionalSelect.val(),
            "fechaTurno": fechaTurnoCampo.val(),
            "horaInicio": horaInicioCampo.val()
        },
        success: function(response) {
            if(response.chequea){
                const componenteDeAlerta = "<div class='alert alert-danger' role='alert'>La fecha y hora del turno ya se encuentran ocupados.</div>";
                $("#mensajeAlerta").append(componenteDeAlerta);
                flag = false;
            }else{
                flag = true;
            }
        }
    });
    if(!flag){
        return flag;
    }
})

