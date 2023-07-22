google.charts.load('current', { packages: ['corechart'], 'language': 'ua'});

var currentChartId = null;

var generalOptions = {
    backgroundColor: {
        fill: 'transparent',
    },
    animation: {
        duration: 1000,
        startup: true,
        easing: 'out',
    },
};

function showProductsChart(data) {
    var chartData = data;
    var chartContainer = document.getElementById('chart_container');
    var dataTable = google.visualization.arrayToDataTable(chartData);
    var chart = new google.visualization.ComboChart(chartContainer);
    var options = Object.assign({
        title : 'ТОП ТОВАР',
        colors: ['#3ba46c', '#6e6b3c'],
        seriesType: 'bars',
        series: {0: {targetAxisIndex: 0}, 1: {targetAxisIndex: 1}},
        vAxes: {
            0: {title: 'ДОХІД'},
            1: {title: 'КІЛЬКІСТЬ'},
        },
        hAxis: {
            title: 'ПРОДУКТ',
            textStyle: {bold: true}
        },
        focusTarget: 'category',
    }, generalOptions);
    toggleChartCollapse('chart_column');
    chart.draw(dataTable, options);

}
function showSellersChart(data) {
    var chartData = data;
    for (var i = 1; i < chartData.length; i++) {
        var sellerName = chartData[i][0];
        var income = chartData[i][1]
        var amount = chartData[i][2];
        var margin = chartData[i][3];
        chartData[i][0] = sellerName + '\n$:' + income + ',   М:' + margin + ',   ~:' + amount;
    }
    var chartContainer = document.getElementById('chart_container');
    var chart = new google.visualization.PieChart(chartContainer);
    var dataTable = google.visualization.arrayToDataTable(chartData);
    var options = Object.assign({
         title : 'ТОП ПРОДАВЕЦЬ',
         is3D : true,
         slices: {0: {color: '#588d61'}, 1: {color: '#797753'}, 2: {color: '#cb7f41'}, 3: {color: '#39a487'}, 4: {color: '#9bc0ee'},
                5: {color: '#bf8cd0'}, 6: {color: '#c78c8c'}, 7: {color: '#9b9999'}, 8: {color: '#282f2f'}, 9: {color: '#d5d5d5'},
        },
    }, generalOptions);
    toggleChartCollapse('chart_pie');
    chart.draw(dataTable, options);
}

function showClientsChart(data) {
    var chartData = data;
    for (var i = 1; i < chartData.length; i++) {
        var sellerName = chartData[i][0];
        var income = chartData[i][1]
        var amount = chartData[i][2];
        chartData[i][0] = sellerName + '\n$:' + income + ',   ~:' + amount;
    }
    var chartContainer = document.getElementById('chart_container');
    var chart = new google.visualization.PieChart(chartContainer);
    var dataTable = google.visualization.arrayToDataTable(chartData);
    var options = Object.assign({
        title : 'ТОП КЛІЄНТ',
        pieHole: 0.4,
        is3D : true,
        slices: {0: {color: '#588d61'}, 1: {color: '#797753'}, 2: {color: '#cb7f41'}, 3: {color: '#39a487'}, 4: {color: '#9bc0ee'},
                5: {color: '#bf8cd0'}, 6: {color: '#c78c8c'}, 7: {color: '#9b9999'}, 8: {color: '#282f2f'}, 9: {color: '#d5d5d5'},
        },
    }, generalOptions);
    toggleChartCollapse('chart_donut');
    chart.draw(dataTable, options);
}

function showCityChart(data) {
    var chartData = data;
    var chartContainer = document.getElementById('chart_container');
    var chart = new google.visualization.BubbleChart(chartContainer);
    var dataTable = google.visualization.arrayToDataTable(chartData);
    var options = Object.assign({
        title: 'ТОП МІСТО',
        hAxis: {title: 'ДОХІД',
                viewWindow: {
                    min: 0,
                }},
        vAxis: {title: 'КІЛЬКІСТЬ'},
        sizeAxis: {minSize: 5, maxSize: 30},
        bubble: {textStyle: {fontSize: 15}},
        explorer: {
            actions: ['dragToPan', 'rightClickToReset'],
        }
    }, generalOptions);

    toggleChartCollapse('chart_geo');
    chart.draw(dataTable, options);

}

function toggleChartCollapse(chartId) {
    var chartCollapse = document.getElementById('chartCollapse');
    if (currentChartId === chartId && chartCollapse.classList.contains('show')) {
        chartCollapse.classList.remove('show');
        currentChartId = null;
    } else {
        chartCollapse.classList.add('show');
        currentChartId = chartId;
    }
}