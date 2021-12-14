import { listOfColors } from "/static/validations/reports/generar_random_color.js"

export const graficoBarras = (idGrafico, titulo, categorias, datos) => {

  let asignado = []
  let atendido = []
  let reprogramado = []
  let ausente = []
  let anulado = []


  for(let i=0; i < datos.length; i++){
    for(let y=0; y < categorias.length; y++){
      if(datos[i][1] == categorias[y]){
        if(datos[i][2] == "Asignado"){
          asignado[y] = datos[i][0]
        }
        if(datos[i][2] == "Atendido"){
          atendido[y] = datos[i][0]
        }
        if(datos[i][2] == "Reprogramado"){
          reprogramado[y] = datos[i][0]
        }
        if(datos[i][2] == "Ausente"){
          ausente[y] = datos[i][0]
        }
        if(datos[i][2] == "Anulado"){
          anulado[y] = datos[i][0]
        }
      }
    }
  }

  const data = {
    labels: categorias,
    datasets: [
      {
        label: "Asignado",
        backgroundColor: listOfColors()[0],
        data: asignado,
      },
      {
        label: "Atendido",
        backgroundColor: listOfColors()[1],
        data: atendido,
      },
      {
        label: "Reprogramado",
        backgroundColor: listOfColors()[2],
        data: reprogramado,
      },
      {
        label: "Ausente",
        backgroundColor: listOfColors()[8],
        data: ausente,
      },
      {
        label: "Anulado",
        backgroundColor: listOfColors()[4],
        data: ausente,
      }
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