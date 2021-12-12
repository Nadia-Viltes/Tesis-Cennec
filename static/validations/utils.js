//Validacion
export const obtenerFechaActual = function () {
    let fecha_actual = new Date()
    let dia = fecha_actual.getDate()
    let mes = fecha_actual.getMonth() + 1
    let anio = fecha_actual.getFullYear()
    return `${anio}-${mes}-${dia}`
}