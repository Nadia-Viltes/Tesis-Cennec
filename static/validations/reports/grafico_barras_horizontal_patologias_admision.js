import { generateRandomRGBColor } from "/static/validations/reports/generar_random_color.js"

export const graficoBarrasHorizontal = (idGrafico, titulo, categorias, datos) => {

  let dataset = []

  for (let i = 0; i < datos.length; i++) {
    let patologia = datos[i][4];
    let cantidad = []
    let color = generateRandomRGBColor()
    for (let y = 0; y < categorias.length; y++) {
      if (categorias[y] == datos[i][2]) {
        cantidad.push(datos[i][0]);
      } else {
        cantidad.push(0);
      }
    }
    dataset.push({
      label: patologia,
      backgroundColor: color,
      data: cantidad
    })
  }

  const data = {
    labels: categorias,
    datasets: dataset
  };
  const config = {
    type: "bar",
    data: data,
    options: {
      indexAxis: 'y',
      scales: {
        x: {
          ticks: {
            stepSize: 1
          }
        }
      },
      responsive: true,
      plugins: {
        legend: {
          position: 'right',
        },
        title: {
          display: true,
          text: titulo
        }
      }
    },
  };
  const myChart = new Chart(document.getElementById(idGrafico), config);
  return myChart;
}