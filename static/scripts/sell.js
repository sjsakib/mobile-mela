var api_url = "http://localhost:8080/";
jQuery.ajaxSetup({async:false});

var brands =  [];
var models = [];

$(document).ready(function () {
    var d = new Date();
    $("#date").html(d.toDateString());
    setInterval(function() {
        d = new Date();
        $("#time").html(d.toLocaleTimeString(navigator.language,{hour: "2-digit",minute:"2-digit"}));
    });

    $("#sell-item").submit(function (e) {
        e.preventDefault();
        var br = $.trim($("#brand").val());
        var mo = $.trim($("#model").val());
        var pro =  $.trim($("#profit").val());

        data = {
            "brand" : br,
            "model" : mo,
            "profit" : pro,
            "seller" : $("#seller").val(),
            "dt" : Math.floor(d.getTime()/1000)
        }

        $.post(api_url+"recordSell",data)
            .done(function(){alert("Rocorded!");})
            .fail(function(){alert("Failed. Please try again");});

        this.reset();
    });

    $("#brand").focusout(function() {
        data = { brand: $.trim(this.value) }
        $.post(api_url+"getModels",data,function(data,status,xhr) {
            if(status == "success") {
                modellist = JSON.parse(data);
                $("#model").autocomplete({
                    source: modellist,
                    minLength: 0,
                    select: function(e,ui) {
                        if($("#brand").val()) {
                            var data = {
                                "brand":$("#brand").val(),
                                "model": ui.item.value
                            };
                            $.post(api_url+"getPrice",data,function(price,status) {
                                $("#buyingprice").val(price);
                                price = parseInt(price);
                                if(price) {
                                    $("#sellingprice").val((price+(price*.1)).toFixed(0));
                                    $("#profit").val((price*.1).toFixed(0));
                                    $("#percent").val(10);
                                }
                            });
                        }
                        return true;
                    }
                });
            }
        });
    });
    $.post(api_url+"getBrands",{},function(data,status) {
        if(status == "success") {
            brands = JSON.parse(data);
            $("#brand").autocomplete({
                source: brands,
                minLength: 0,
                select: function(e,ui) {
                    if($("#model").val()) {
                        var item = {
                            "brand" : ui.item.value,
                            "model" : $("#model").val()
                        };
                        $.post(api_url+"getPrice",item,function(price,status) {
                            $("#buyingprice").val(price);
                            price = parseInt(price);
                            if(price) {
                                $("#sellingprice").val((price+(price*.1)).toFixed(0));
                                $("#profit").val((price*.1).toFixed(0));
                                $("#percent").val(10);
                            }
                        });
                    }
                    return true;
                }
            });
        }
    });


    $("#profit").on("change paste keyup",function() {
        pri = parseInt($("#buyingprice").val());
        pro = parseInt($("#profit").val());
        if(pri && pro) {
            per = (pro/pri*100).toFixed(1);
            spri = pri+pro;
            console.log(per,spri);
            $("#percent").val(per);
            $("#sellingprice").val(spri);
        } else if (pro == 0) {
            $("#percent").val(0);
            $("#sellingprice").val(pri);
        }

    });
    $("#percent").on("change paste keyup",function() {
        pri = parseInt($("#buyingprice").val());
        per = parseInt($("#percent").val());
        if(pri && per) {
            pro = pri*per/100;
            spri = pri+pro;
            $("#profit").val(pro.toFixed(0));
            $("#sellingprice").val(spri.toFixed(0));
        } else if (per == 0) {
             $("#profit").val(0);
            $("#sellingprice").val(pri);
        }

    });

    $("#sellingprice").on("change paste keyup",function() {
        pri = parseInt($("#buyingprice").val());
        spri = parseInt($("#sellingprice").val());
        if(pri && spri) {
            pro = spri - pri;
            per = pro/pri*100;
            $("#profit").val(pro.toFixed(0));
            $("#percent").val(per.toFixed(1));
        } else if(spri == 0) {
            $("#profit").val(0);
            $("#percent").val(0);
        }

    });

});