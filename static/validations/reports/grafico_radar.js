export const graficoRadar = (idGrafico, titulo, categorias, datos) => {

    let point_styles = []
    let array_datos = []

    for (let i = 0; i < datos.length; i++) {
        datos[i][0] % 2 === 0 ? point_styles.push('circle') : point_styles.push('rect');
        
        for (let y = 0; y < categorias.length; y++) {
            if (datos[i][1] == categorias[y]) {
                array_datos[y] = datos[i][0]
            }
        }
    }

    console.log(point_styles)
    const data = {
        labels: categorias,
        datasets: [
            {
                label: titulo,
                backgroundColor: "rgb(255,20,147)",
                data: array_datos,
            },
        ],
    };
    const config = {
        type: "radar",
        data: data,
        options: {
            responsive: true,
            elements: {
                point: {
                    pointStyle: point_styles
                }
            },
            scale: {
                stepSize: 1
            },
        },
    };
    const myChart = new Chart(document.getElementById(idGrafico), config);
    return myChart;
}