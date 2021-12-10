import {beautyRGBColorList} from "/static/validations/reports/generar_random_color.js"

export const graficoTorta = (idGrafico, titulo, categorias, datos) => {
  const labels = categorias;

  const data = {
    labels: labels,
    datasets: [
      {
        label: titulo,
        backgroundColor: beautyRGBColorList(datos),
        data: datos,
      },
    ],
  };
  const config = {
    type: "pie",
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
      }
    },
  };
  const myChart = new Chart(document.getElementById(idGrafico), config);
  return myChart;
}