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
        $.post(api_url+"getStatsTable",dt,function(data) {
            $("#stattable").html(data);
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