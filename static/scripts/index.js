var api_url = "http://localhost:8080/";

jQuery.ajaxSetup({async:false});

$(document).ready(function() {
    setInterval(function() {
        var d = new Date();
        $("#clock").html(d.toDateString()+" "+d.toLocaleTimeString());
    },100);

    
    /*initiate date*/
    var today = new Date(new Date().toDateString());
    var t1 = Math.floor(today.getTime()/1000);
    $.post(api_url+"startDay",{day:t1})
        .fail(function() {
            alert("Something went wrong. Please reload the page");
        });

    t2 = t1 + 86399;

    data = {
        "t1" : t1,
        "t2" : t2
    };
    console.log(data);
    $.post(api_url+"getSales",data,function(data,status) {
        $("#incomebox").append(data);
    });
    $.post(api_url+"getExpenses",data,function(data,status) {
        $("#outcomebox").append(data);
    });
    $.post(api_url+"getDues",data,function(data,status) {
        $("#duebox").append(data);
    });
    $.post(api_url+"getCash",data,function(data,status) {
        $("#cashbox").append(data);
    });
});