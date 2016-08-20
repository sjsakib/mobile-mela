var api_url = "http://localhost:8080/";
jQuery.ajaxSetup({async:false});

var brands =  [];
var models = [];

var types = [
    "Smartphone",
    "Feature Phone",
    "Accessory"
];

$(document).ready(function () {
    $("#product").submit(function (e) {
        e.preventDefault();

        var brandval = $.trim($("#brand").val());
        var modelval = $.trim($("#model").val());
        var typeval  = $.trim($("#type").val());
        var buyingpriceval =  $.trim($("#buyingprice").val());
        var countval = $.trim($("#count").val());
        var fromcash;
        if($("#cashcheckbox").is(":checked")) {
            fromcash = "True";
        } else {
            fromcash = "";
        }
        var data = {
            "brand": brandval,
            "model": modelval,
            "type" : typeval,
            "buyingprice" : buyingpriceval,
            "count" : countval,
            "fromcash": fromcash,
            "dt": Math.floor(new Date().getTime()/1000)
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
                source: brands,
                minLength: 0
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
        source: types,
        minLength: 0
    });
    $("#brand").focusout(function() {
        data = { brand: $.trim(this.value) }
        $.post(api_url+"getModels",data,function(data,status,xhr) {
            if(status == "success") {
                modellist = JSON.parse(data);
                $("#model").autocomplete({
                    source: modellist,
                    minLength: 0
                });
            }
        });
    });
    $.post(api_url+"getBrands",{},function(data,status) {
        if(status == "success") {
            brands = JSON.parse(data);
            $("#brand").autocomplete({
                source: brands,
                minLength: 0
            });
        }
    });
    $("#model").autocomplete({
        source : models,
        minLength: 0
    });

});