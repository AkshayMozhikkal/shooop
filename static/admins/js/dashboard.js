/* globals Chart:false, feather:false */

(() => {
  'use strict'

  feather.replace({ 'aria-hidden': 'true' })

 var sales_by_day = document.getElementById('sales_by_day').value;
 sales_by_day = JSON.parse(sales_by_day);




  // Extract 'day' values for labels
  var sale_labels = sales_by_day.map(item => item.day);
//   var sale_labels = []
//   var sale_labels = sales_by_day.map(function(dateTimeString) {
//     var datePart = dateTimeString.split(' ')[0];
//     return datePart;
//   });
  

  // Extract 'total_sales' values for data
  var sale_data = sales_by_day.map(item => item.total_sales);


  // Graphs
  const ctx = document.getElementById('myChart')
  // eslint-disable-next-line no-unused-vars
  const myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: sale_labels,
      datasets: [{
        data: sale_data,
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
      }]
    },
    options: {
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          boxPadding: 3
        }
      }
    }
  })
})()
