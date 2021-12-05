// === include 'setup' then 'config' above ===
const graficoBarras = (idGrafico, titulo, categorias, datos) => {
  const labels = categorias;

  const data = {
    labels: labels,
    datasets: [
      {
        label: titulo,
        backgroundColor: "rgb(255, 99, 132)",
        borderColor: "rgb(255, 99, 132)",
        data: datos,
      },
    ],
  };
  const config = {
    type: "bar",
    data: data,
    options: {},
  };
  const myChart = new Chart(document.getElementById(idGrafico), config);
  return myChart;
}