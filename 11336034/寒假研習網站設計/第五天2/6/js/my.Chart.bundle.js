var ctx = document.getElementById("myChart").getContext('2d');

var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ["102年", "103年", "104年", "105年", "106年"],
        datasets: [{
            label: '新生人口(千人)',
            data: [183.7, 199.2, 201.5, 196.8, 183.4],
            fill: false,
            backgroundColor: 'rgba(212, 106, 106, 1)',
            borderColor: 'rgba(212, 106, 106, 1)'
        }, 
        {
            label: '20歲人口(千人)',
            data: [325.1, 321.4, 323.4, 321.4, 322.4],
            fill: false,
            backgroundColor: 'rgba(128, 21, 21, 1)',			
            borderColor: 'rgba(128, 21, 21, 1)'
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});
