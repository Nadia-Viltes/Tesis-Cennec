import {beautyRGBColorList} from "/static/validations/reports/generar_random_color.js"

export const graficoBarras = (idGrafico, titulo, categorias, datos) => {

  let dataset = []
  for(let i=0; i < datos.length; i++){
    for(let y=0; y < categorias.length; y++){
      if(`${datos[i][0]} ${datos[i][1]}` == categorias[y]){
        dataset[y] = datos[i][2]
      }
    }
  }

  const data = {
    labels: categorias,
    datasets: [
      {
        label: titulo,
        backgroundColor: "rgb(255,20,147)",
        data: dataset,
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