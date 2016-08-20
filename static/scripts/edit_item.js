var api_url = "http://localhost:8080/";
jQuery.ajaxSetup({async:false});

var today = new Date(new Date().toDateString());
var t2 = Math.floor(today.getTime()/1000) + 86399;
var t1 = Math.floor(today.getTime()/1000);
var data = {
    "t1" : t1,
    "t2" : t2
};

$(document).ready(function(){
    $.post(api_url+"getAllItems",{},function(data,status) {
        if(status = "success") {
            $("#allitems").append(data);
        }

        $(".itemform").submit(function(e) {
            console.log("triggerd");
            data = {
                "id":this.id.value,
                "brand":this.brand.value,
                "model":this.model.value,
                "type":this.type.value,
                "buyingprice":this.price.value,
                "count":this.count.value,
                "dt": Math.floor(new Date().getTime()/1000)
            }
            $.post(api_url+"updateItem",data,function(data,status) {
                if(status!= "success") {
                    e.preventDefaut();
                    alert("Some error occured. Not updated, try again");
                }
            });
        });

    });
    $.post(api_url+"getSalesForm",data,function(data,status) {
        if(status = "success") {
            $("#salesitems").append(data);
        }

        $(".salesform").submit(function(e) {
            data = {
                "id":this.id.value,
                "price":this.price.value,
            }
            $.post(api_url+"updateSales",data,function(data,status) {
                if(status!= "success") {
                    e.preventDefaut();
                    alert("Some error occured. Not updated, try again");
                }
            });
        });

    });
    $.post(api_url+"getExpForm",data,function(data,status) {
        if(status = "success") {
            $("#expitems").append(data);
        }

        $(".expform").submit(function(e) {
            var data = {
                "id":this.id.value,
                "type":this.type.value,
                "amount":this.amount.value,
                "details":this.details.value
            };
            $.post(api_url+"updateExp",data,function(data,status) {
                if(status!= "success") {
                    e.preventDefaut();
                    alert("Some error occured. Not updated, try again");
                }
            });
        });

    });
});