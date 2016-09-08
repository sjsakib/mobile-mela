var api_url = "http://localhost:8080/";
jQuery.ajaxSetup({async:false});



$(document).ready(function () {
    var d = new Date();
    $("#date").html(d.toDateString());
    setInterval(function() {
        d = new Date();
        $("#time").html(d.toLocaleTimeString(navigator.language,{hour: "2-digit",minute:"2-digit"}));
    });

    $("#expense-record").submit(function (e) {
        e.preventDefault();
        var de = $.trim($("#details").val());
        var ty = $.trim($("input[type='radio']:checked").val());
        var am = $("#amount").val();

        data = {
            "details" : de,
            "type" : ty,
            "amount" : am,
            "dt" : Math.floor(d.getTime()/1000)
        }

        $.post(api_url+"recordExpense",data)
            .done(function(){alert("Rocorded!");})
            .fail(function(){alert("Failed. Please try again");});
    });

    
});