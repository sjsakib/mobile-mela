var api_url = "http://localhost:8080/";
jQuery.ajaxSetup({async:false});

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

        $(".delete").click(function() {
            var fr = this.parentElement.parentElement;
            id = fr.id.value
            if(confirm("Sure to delete?")) {
                $.post(api_url+"deleteItem",{"id":id});
                location.reload();
            }
        });

    });
});