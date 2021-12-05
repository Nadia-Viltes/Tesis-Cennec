// === include 'setup' then 'config' above ===
const labels = ["January", "February", "March", "April", "May", "June"];
const data = {
  labels: labels,
  datasets: [
    {
      label: "Mi primer grafico",
      backgroundColor: "rgb(255, 99, 132)",
      borderColor: "rgb(255, 99, 132)",
      data: [0, 10, 5, 2, 20, 30, 45],
    },
  ],
};
const config = {
  type: "bar",
  data: data,
  options: {},
};
const myChart = new Chart(document.getElementById("chart"), config);
