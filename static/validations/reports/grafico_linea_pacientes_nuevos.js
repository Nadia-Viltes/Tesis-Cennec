export const graficoLineaPacientesNuevos = (idGrafico, titulo, categorias, datos) => {

  let masculino = []
  let femenino = []
  let total = []

  for(let i=0; i < datos.length; i++){
    if(datos[i][1] == "Masculino"){
       masculino[datos[i][2] - 1] = datos[i][0]
    }else{
       femenino[datos[i][2] - 1] = datos[i][0]
    }
    total[datos[i][2] - 1] = (total[datos[i][2] - 1] || 0) + datos[i][0]
  }

  const data = {
    labels: categorias,
    datasets: [
      {
        label: "Masculino",
        borderColor: "rgb(0, 0, 255)",
        backgroundColor: "rgb(0, 0, 255)", //azul
        data: masculino,
      },
      {
        label: "Femenino",
        borderColor: "rgb(247, 191, 190)",
        backgroundColor: "rgb(247, 191, 190)", //rosa
        data: femenino,
      },
      {
        label: "Total",
        borderColor: "rgb(0,0,0)",
        backgroundColor: "rgb(0,0,0)", 
        data: total,
      },
    ],
  };
  const config = {
    type: "line",
    data: data,
    options: {
      responsive: true,
      scales: {
        y: {
          ticks: {
            stepSize: 10
          }
        }
      },
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