// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Função para atualizar o gráfico de barras com requisitos não marcados
function updateBarChart() {
  // Fazer uma solicitação AJAX para obter os dados do banco de dados
  fetch('/dados-do-banco')
    .then(response => response.json())
    .then(data => {
      // Extrair os rótulos e dados do objeto JSON retornado
      var labels = data.labels;
      var dados = data.dados;

      // Atualize o gráfico com os novos dados
      myLineChart.data.labels = labels;
      myLineChart.data.datasets[0].data = dados;
      myLineChart.update();
    })
    .catch(error => {
      console.error('Erro ao buscar dados do banco de dados:', error);

      // Adicione uma mensagem de erro ou trate erros, se necessário
    });
}

// Bar Chart Example
var ctx = document.getElementById("myBarChart");
var myLineChart;

// Certifique-se de que o gráfico seja inicializado dentro da função de atualização
function initializeChart() {
  myLineChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: [], // Inicialmente vazio
      datasets: [{
        label: "Débitos Técnicos",
        backgroundColor: "rgba(2,117,216,1)",
        borderColor: "rgba(2,117,216,1)",
        data: [], // Inicialmente vazio, os dados serão preenchidos após a solicitação AJAX
      }],
    },
    options: {
      scales: {
        xAxes: [{
          gridLines: {
            display: false
          },
        }],
        yAxes: [{
          ticks: {
            min: 0,
            max: 50,
            maxTicksLimit: 5
          },
          gridLines: {
            display: false
          }
        }],
      },
      legend: {
        display: false
      }
    }
  });
}

// Chame a função de inicialização do gráfico assim que a página for carregada
document.addEventListener('DOMContentLoaded', function() {
  initializeChart();
  updateBarChart(); // Atualize o gráfico uma vez quando a página for carregada
});
