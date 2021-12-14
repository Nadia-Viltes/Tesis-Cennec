import { generateRandomRGBColor } from "/static/validations/reports/generar_random_color.js"
export const graficoBarras = (idGrafico, titulo, categorias, datos) => {

  let dataset = []
  let motivos = []
  //motivos dinamicos
  for(let i=0; i < datos.length; i++){
    //el valor no existe
    if(motivos.indexOf(datos[i][2]) == -1 ){
      motivos.push(datos[i][2])
    }
  }

  //creacion del dataset
  for(let i=0; i < motivos.length; i++){
    dataset.push({
      label: motivos[i],
      backgroundColor: generateRandomRGBColor(),
      data: []
    })
  }

  //meto los valores en los datasets creados dinamicamente
  for(let i=0; i < datos.length; i++){
    for(let y=0; y < categorias.length; y++){
      if(datos[i][1] == categorias[y]){
        for(let h=0; h < dataset.length; h++){
          if(dataset[h]["label"] == datos[i][2]){
            dataset[h]["data"][y] = datos[i][0]
          }
        }
      } 
    }
  }

  const data = {
    labels: categorias,
    datasets: dataset,
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