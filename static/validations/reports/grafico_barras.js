import {beautyRGBColorList} from "/static/validations/reports/generar_random_color.js"

export const graficoBarras = (idGrafico, titulo, categorias, datos) => {
  const labels = categorias;

  const data = {
    labels: labels,
    datasets: [
      {
        label: titulo,
        backgroundColor: "rgb(255,20,147)",
        data: datos,
      },
    ],
  };
  const config = {
    type: "bar",
    data: data,
    options: {
      responsive: true
    },
  };
  const myChart = new Chart(document.getElementById(idGrafico), config);
  return myChart;
}