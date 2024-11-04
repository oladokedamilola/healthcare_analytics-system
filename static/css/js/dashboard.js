/////// CHARTS ////////

var barChartOptions = {
    series: [{
      name: 'Products',
      data: [ 10, 8, 6,4, 2],
}],
    chart: {
    height: 350,
    type: 'bar',
    background:"transparent",
    toolbar:{
        show: false,
    }
  },
  colors: ['#00E396', 'd50000', '#2e7d32', '#ff6d00', '#538cb3'],

  plotOptions: {
    bar: {
      horizontal: false,
      distributed:true,
      borderRadius:4,
      columnwidth:"40",
    }
  },
  dataLabels: {
    enable: false,
  },
  fill:{
    opacity:1
  },
  grid:{
    borderColor:"#5559e",
    yaxis:{
        lines:{
            show: true,
        },
    },
    xaxis:{
        lines:{
            show: true,
        },
    },
  },
  legend: {
    labels:{
        colors:"#f5f7ff"
    },
    show: true,
    position:"top",
  },
  stroke:{
    colors:["transparent"],
    show: true,
    width:2,
  },
  tooltip:{
    shared:true,
    intersect:false,
    theme:"dark",
  },
  xaxis:{
    categories:["Laptop", "Phone","Monitor","Camera"],
    title:{
        style:{
            color:"#f5f7ff",
        },
    },
    axixborder:{
        style:{
            color:"#55596e",
            show: true,
        },
        axisTicks:{
            color:"#55596e",
            show:true,
        },
        labels:{
            style:{
                color:"#f5f7ff",
            },
        },
    },
  }
  };

  var chart = new ApexCharts(document.querySelector("#bar-chart"), barChartOptions);
  chart.render();






  ///***AREA CHART ******/
  var options = {
    series: [{
    name: 'TEAM A',
    type: 'area',
    data: [44, 55, 31, 47, 31, 43, 26, 41, 31, 47, 33]
  }, {
    name: 'TEAM B',
    type: 'line',
    data: [55, 69, 45, 61, 43, 54, 37, 52, 44, 61, 43]
  }],
    chart: {
    height: 350,
    type: 'line',
  },
  stroke: {
    curve: 'smooth'
  },
  fill: {
    type:'solid',
    opacity: [0.35, 1],
  },
  labels: ['Dec 01', 'Dec 02','Dec 03','Dec 04','Dec 05','Dec 06','Dec 07','Dec 08','Dec 09 ','Dec 10','Dec 11'],
  markers: {
    size: 0
  },
  yaxis: [
    {
      title: {
        text: 'Series A',
      },
    },
    {
      opposite: true,
      title: {
        text: 'Series B',
      },
    },
  ],
  tooltip: {
    shared: true,
    intersect: false,
    y: {
      formatter: function (y) {
        if(typeof y !== "undefined") {
          return  y.toFixed(0) + " points";
        }
        return y;
      }
    }
  }
  };

  var chart = new ApexCharts(document.querySelector("#area-chart"), options);
  chart.render();