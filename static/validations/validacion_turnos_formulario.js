import {obtenerFechaActual} from "/static/validations/utils.js"

//seteo fecha de turno por defecto
let tipoTurnoSelect = $("[name='tipoTurno']")
let especialidadSelect = $("[name='nameEspecialidadDropdown']")
let profesionalSelect = $("[name='nameProfesionalDropdown']")
let pacienteId = $("[name='inputPacienteId']").val()
let fechaTurnoCampo = $("[name='fechaTurno']")
let horaInicioCampo = $("[name='nameHoraInicio']")
let horaFinCampo = $("#idhoraFin")
let horaFinOculta = $("[name='nameHoraFin']")
let campoRequeridos = $("[validation='true']")

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

    //validaci??n turno existente
    $.ajax({
        url: "/turnos/chequear_disponibilidad", 
        method: "POST",
        async: false,
        data: {
            "pacienteId": pacienteId,
            "profesionalId": profesionalSelect.val(),
            "fechaTurno": fechaTurnoCampo.val(),
            "horaInicio": horaInicioCampo.val()
        },
        success: function(response) {
            if(response.values.horario_profesional_ocupado){
                const componenteDeAlerta = "<div class='alert alert-danger' role='alert'>La fecha y hora del turno estan ocupados por el profesional</div>";
                $("#mensajeAlerta").empty();
                $("#mensajeAlerta").append(componenteDeAlerta);
                flag = false;
            }else if(response.values.horario_paciente_ocupado){
                const componenteDeAlerta = "<div class='alert alert-danger' role='alert'>El paciente tiene otro turno en el mismo horario</div>";
                $("#mensajeAlerta").empty();
                $("#mensajeAlerta").append(componenteDeAlerta);
                flag= false;
            }else{
                flag = true;
            }
        }
    });
    if(!flag){
        return flag;
    }
})

