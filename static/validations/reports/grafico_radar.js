import {beautyRGBColorList} from "/static/validations/reports/generar_random_color.js"

export const graficoRadar = (idGrafico, titulo, categorias, datos) => {


  /*
  function alternatePointStyles(ctx) {
    const index = ctx.dataIndex;
    return index % 2 === 0 ? 'circle' : 'rect';
  }
  */
  
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
    type: "radar",
    data: data,
    options: {
      responsive: true
    },
  };
  const myChart = new Chart(document.getElementById(idGrafico), config);
  return myChart;
}