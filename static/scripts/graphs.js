var api_url = "http://localhost:8080/";
jQuery.ajaxSetup({async:false});

function update() {
    var  f = $("#from").val();
    var t = $("#to").val();
    if(f && t) {
        dt = {
            t1: Math.floor(new Date(f)/1000),
            t2: Math.floor(new Date(t)/1000)+86399
        };
        $.post(api_url+"getStats",dt,function(data) {
            data = JSON.parse(data);
            var data2 = [];
            for (d in data.proTime) {
                data2.push({ x: new Date(data.proTime[d].dt*1000), y:data.proTime[d].profit });
            }

            var chart = new CanvasJS.Chart("statsTime",{
                zoomEnabled: true,
                animationEnabled: true,
                title:{
                    text: "Profit By day"
                },
                data: [
                    {
                        type: "line",
                        dataPoints: data2
                    }
                ]
            });
            chart.render();
            var chart = new CanvasJS.Chart("byBrand",{
                animationEnabled: true,
                theme: "theme2",
                title:{
                    text: "Profit By Brand"
                },
                data: [
                    {
                        type: "pie",
                        toolTipContent: "{y} - #percent %",
                        yValueFormatString: "Tk #",
                        dataPoints: data.byBrand
                    }
                ]
            });
            chart.render();
            var chart = new CanvasJS.Chart("byType",{
                animationEnabled: true,
                theme: "theme2",
                title:{
                    text: "Profit By Type"
                },
                data: [
                    {
                        type: "pie",
                        toolTipContent: "{y} - #percent %",
                        yValueFormatString: "Tk #",
                        dataPoints: data.byType
                    }
                ]
            });
            chart.render();
        });
    }
}

$(document).ready(function() {
    $("#from").datepicker({
        firstDay : 6,
        onSelect: update
    });
    $("#to").datepicker({
        firstDay : 6,
        onSelect: update
    });
});