import {generateRandomRGBColorList} from "/static/validations/reports/generar_random_color.js"

export const graficoPolar = (idGrafico, titulo, categorias, datos) => {
  const labels = categorias;

  const data = {
    labels: labels,
    datasets: [
      {
        label: titulo,
        backgroundColor: generateRandomRGBColorList(datos),
        data: datos,
      },
    ],
  };
  const config = {
    type: "polarArea",
    data: data,
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: titulo
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