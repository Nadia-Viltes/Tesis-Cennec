import { beautyRGBColorList } from "/static/validations/reports/generar_random_color.js"

export const graficoBarrasStacked = (idGrafico, titulo, categorias, datos) => {

  let masculinos = []
  let femeninos = []

  for (let i = 0; i < datos.length; i++) {
    for (let y = 0; y < categorias.length; y++) {
      if (datos[i][2] == "Masculino") {
        if (categorias[y] == datos[i][1]) {
          masculinos[y] = datos[i][0]
        }
      } else {
        if (categorias[y] == datos[i][1]) {
          femeninos[y] = datos[i][0]
        }
      }
    }
  }

  const data = {
    labels: categorias,
    datasets: [
      {
        label: 'Varones',
        data: masculinos,
        backgroundColor: "rgb(0,0,255)"
      },
      {
        label: 'Mujeres',
        data: femeninos,
        backgroundColor: "rgb(255,0,128)"
      },
    ]
  };
  const config = {
    type: "bar",
    data: data,
    options: {
      plugins: {
        title: {
          display: true,
          text: titulo
        },
      },
      responsive: true,
      scales: {
        x: {
          stacked: true,
        },
        y: {
          stacked: true
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