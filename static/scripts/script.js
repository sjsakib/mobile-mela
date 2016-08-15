var api_url = "http://localhost:8080/";

var brands =  [];

var types = [
    "Smartphone",
    "Freature Phone",
    "Accessory",
    "Sim",
];

$(document).ready(function () {
    $("#brand").focusout(function() {
        data = { brand: $.trim(this.value) }
        $.post(api_url+"getModels",data,function(data,status,xhr) {
            if(status == "success") {
                modellist = JSON.parse(data);
                $("#model").autocomplete({
                    source: modellist
                });
            }
        });
    });

    $("#product").submit(function (e) {
        e.preventDefault();

        var brandval = $.trim($("#brand").val());
        var modelval = $.trim($("#model").val());
        var typeval  = $.trim($("#type").val());
        var buyingpriceval =  $.trim($("#buyingprice").val());
        var countval = $.trim($("#count").val());

        var data = {
            "brand": brandval,
            "model": modelval,
            "type" : typeval,
            "buyingprice" : buyingpriceval,
            "count" : countval
        };
        $.post("http://localhost:8080/addItem",data,function(resp,status,xhr) {
            if(status != "success" || resp != "OK") {
                $("#formbox").after("<p class='error'>Not added try Again</p>");
            } else {
                $("#formbox").after("<p class='success'>"+data.count+" "+data.brand+" "+data.model+" added</p>");
            }
        });
        if(brands.indexOf(brandval)<0) {
            brands.push(brandval);
            $("#brand").autocomplete({
                source: brands
            });
        }
        if($("#checkbox").is(":checked")) {
            this.reset();
        } else {
            this.count.value = 0;
        }
    });

    $("#reset").click(function() {
        $("#product").trigger('reset');
    });

    $("#type").autocomplete({
        source: types
    });
    $.post(api_url+"getBrands",{},function(data,status) {
        if(status == "success") {
            brands = JSON.parse(data);
            $("#brand").autocomplete({
                source: brands
            });
        }
    });

});