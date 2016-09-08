var api_url = "http://localhost:8080/";
jQuery.ajaxSetup({async:false});


$(document).ready(function () {
    var d = new Date();
    $("#date").html(d.toDateString());
    setInterval(function() {
        d = new Date();
        $("#time").html(d.toLocaleTimeString(navigator.language,{hour: "2-digit",minute:"2-digit"}));
    });

    $("#addDue").submit(function (e) {
        e.preventDefault();
        var de = $.trim($("#details").val());
        var am = $("#amount").val();

        data = {
            "details" : de,
            "amount" : am,
            "dt" : Math.floor(d.getTime()/1000)
        }

        $.post(api_url+"addDue",data)
            .done(function(){alert("Rocorded!");})
            .fail(function(){alert("Failed. Please try again");});
        this.reset();
    });

    $.post(api_url+"getDueForm",{},function(data,status) {
        if(status = "success") {
            $("#allitems").append(data);
        }

        $(".dueform").submit(function(e) {
            data = {
                id:this.id.slice(2),
                amount:this.amount.value
            }
            $.post(api_url+"updateDue",data,function(data,status) {
                if(status!= "success") {
                    e.preventDefaut();
                    alert("Some error occured. Not updated, try again");
                }
            });
        });

        $(".delete").click(function() {
            var fr = this.parentElement.parentElement;
            var id = fr.id.slice(2);
            if(confirm("Sure To Remove?")) {
                $.post(api_url+"removeDue",{
                    "id":id,
                    "amount":fr.amount.value,
                    "date": Math.floor(new Date().getTime()/1000)
                });
                //location.reload();
            }
        });

    });
 
});