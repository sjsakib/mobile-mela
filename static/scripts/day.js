var api_url = "http://localhost:8080/";
jQuery.ajaxSetup({async:false});

$(document).ready(function() {
    $("#datepicker").datepicker({
        firstDay : 6,
        onSelect: function() {
            var today = new Date(this.value);
            var t2 = Math.floor(today.getTime()/1000) + 86399;
            var t1 = Math.floor(today.getTime()/1000);
            data = {
                "t1" : t1,
                "t2" : t2
            };
            $.post(api_url+"getSales",data,function(data,status) {
                $("#incomeData").html(data);
            });
            $.post(api_url+"getExpenses",data,function(data,status) {
                $("#outcomeData").html(data);
            });
            $.post(api_url+"getDues",data,function(data,status) {
                $("#dueData").html(data);
            });
            $.post(api_url+"getCash",data,function(data,status) {
                $("#cashData").html(data);
            }).fail(function() {
                $("#cashData").html("");
                alert("No record found!")
            });
        } 
    });
});