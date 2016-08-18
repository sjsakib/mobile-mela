var api_url = "http://localhost:8080/";
jQuery.ajaxSetup({async:false});

function update() {
    var t2 = new Date(new Date().toDateString());
    var t1 = new Date(t2.getTime()-(86400000*30));

    var dt = {
        t1: Math.floor(t1.getTime()/1000),
        t2: Math.floor(t2.getTime()/1000)+86399
    }

    $.post(api_url+"getSalesGraph",dt,function(data) {
        data = JSON.parse(data);
        var data2 = [];
        for (d in data) {
            data2.push({ x: new Date(data[d].dt*1000), y:data[d].sales });
        }
        var chart = new CanvasJS.Chart("salesGraph",{
            animationEnabled: true,
            axisX: {
                valueFormatString: "D",
                interval: 1,
                intervalType: "day"
            },
            title:{
                text: "Sales History"
            },
            data: [
                {
                    type: "spline",
                    lineThickness: 3,
                    dataPoints: data2
                }
            ]
        });
        chart.render();
    });
}

$(document).ready(function() {
    update();
});