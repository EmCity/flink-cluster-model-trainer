function createTable() {
    var str = "";
    var str_detail = "";
    var str_head = "";
    for (var i = 0; i < res.length; i++) {
        str += "<tr>";
        str += "<td><input type=\"button\" value=\"Details\"/ class=\"mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--colored mdl-color-text--white\"></td>";
        str += "<td>" + res[i].job_name + "</td>";
        str += "<td>" + res[i].mape + "</td>";
        str += "</tr>";

        if (res[i].parameter_set.algorithm == "LR") {
            str_detail += format_LR(res[i]);

        } else if (res[i].parameter_set.algorithm == "SVM") {
            str_detail += format_SVM(res[i]);

        } else {
            str_detail += format_NN(res[i]);

        }


    };

    document.querySelector('#tbody').innerHTML = str;
    //        document.querySelector('#thead').innerHTML = str_head;
    document.querySelector('#tbody_detail').innerHTML = str_detail;

    console.log(typeof str_detail);
    console.log(str_detail);
};

function format_LR(d) {
    return '<b>Algorithm: </b>' + d.parameter_set.algorithm + '<br>' +
        '<b>Fit_intercept: </b>' + d.parameter_set.fit_intercept + '<br>' +
        '<b>Normalize: </b>' + d.parameter_set.normalize + '<br><br>';
};

function format_SVM(d) {
    return '<b>Algorithm: </b>' + d.parameter_set.algorithm + '<br>' +
        '<b>C: </b>' + d.parameter_set.C + '<br>' +
        '<b>Epsilon: </b>' + d.parameter_set.epsilon + '<br>' +
        '<b>Kernel: </b>' + d.parameter_set.kernel + '<br>' +
        '<b>Gamma: </b>' + d.parameter_set.gamma + '<br>' +
        '<b>Shrinking: </b>' + d.parameter_set.shrinking + '<br>' +
        '<b>Tolerance: </b>' + d.parameter_set.tolerance + '<br>' +
        '<b>Cache_size: </b>' + d.parameter_set.cache_size + '<br>' +
        '<b>Max_iter: </b>' + d.parameter_set.max_iter + '<br><br>';
};

function format_NN(d) {
    return '<b>Algorithm: </b>' + d.parameter_set.algorithm + '<br>' +
        '<b>Normalize: </b>' + d.parameter_set.normalization + '<br>' +
        '<b>Learning_rate: </b>' + d.parameter_set.learning_rate + '<br>' +
        '<b>Epochs: </b>' + d.parameter_set.epochs + '<br>' +
        '<b>Display_step: </b>' + d.parameter_set.display_step + '<br>' +
        '<b>Cost_function: </b>' + d.parameter_set.cost_function + '<br><br>';
};



$(function() {
    //var x = decodeHtml(data);
    //var res = JSON.parse(x);
    var data = $.parseJSON('[]');
    console.log(data);

    function createTable(data){
        $( "#result_table_body" ).empty();

        var i = 1;
        $.each( data, function( key, val ) {
            tr = $("<tr/>");

            $("<td/>",{
                html: i
            }).appendTo(tr);

            $("<td/>",{
                "class": "mdl-data-table__cell--non-numeric",
                html: val.job_name
            }).appendTo(tr);

            if(val.timestart && val.timeend){
                $("<td/>",{
                    html: new Date(val.timestart).toLocaleString('de') + '<br>' + new Date(val.timeend - 2*60*60*1000).toLocaleString('de')
                }).appendTo(tr);

                var delta = new Date(val.timeend - 3*60*60*1000 - val.timestart);

                $("<td/>",{
                    html: delta.toLocaleTimeString('de')
                }).appendTo(tr);
            }

            $("<td/>",{
                html: val.mape.toFixed(4)
            }).appendTo(tr);

            i +=1;
            tr.appendTo( "#result_table_body" );
        });
    }

    function createDetails(data){
        $("#parameterList").empty();

        console.log(data);

        ul = $("<ul/>",{
            class: "mdl-list"
        });


        li = $("<li/>",{
            class: "mdl-list__item"
        });

        $("<span/>",{
            class: "mdl-list__item-primary-content",
            html: "<b>" + data.job_name + "</b>"
        }).appendTo(li);

        li.appendTo( ul );

        $.each(data.parameter_set, function(key, val){
            li2 = $("<li/>",{
                class: "mdl-list__item"
            });

            $("<span/>",{
                class: "mdl-list__item-secondary-content",
                html: key + ": " + val
            }).appendTo(li2);

            li2.appendTo( ul );
        });

        ul.appendTo( $("#parameterList") );

        $("#parameterList").slideDown();
    }

    $( ".mdl-data-table tbody").delegate('tr', 'click', function(obj) {
        //console.log(obj);
        var tr = obj.currentTarget;
        var listNr =  obj.currentTarget.rowIndex;
        //console.log(listNr);

        if($(tr).hasClass('selected')){
            $(tr).removeClass('selected');
            $("#parameterList").slideUp("fast");

        }else{
            $(".mdl-data-table tbody tr").removeClass('selected');
            $(tr).addClass('selected');
            $("#parameterList").slideUp("fast", function() {
                createDetails(data[listNr-1]);
                $("#parameterList").slideDown("fast");
            });

        }

    });

    $(document).delegate('input[type="button"]', 'click', function() {
        $('[colspan="5"]').parent('tr').remove();
        $(this).parents('tr').after('<tr/>').next().append('<td colspan="5"/>').children('td').append('<div/>').children().css({
            'display': 'none',
            'padding': '10px'
        }).html($('#content').html()).slideDown();

        $("#hide_details").on("click", function() {
            $("#content").hide();
            $("#tbody").show();
        });

    });

    function ajaxReloadTable(fnAlways) {
        $.ajax({
            //url: "http://sambahost.dyndns.lrz.de:8500/get_results_api",
            url: "http://sambahost.dyndns.lrz.de:8500/get_results_api",
            type: 'GET',
            crossDomain: true,
            dataType: 'json'
        }).done(function(newdata) {
            console.log("done");


            data2 = newdata;
            //data2 = $.parseJSON('[{"_id":"596908e3e4b03f3870c30de9","timeend":1500055779228,"job_name":"TimestartJob","mape":0.7079879882056198,"parameter_set":{"fit_intercept":false,"job_name":"TimestartJob","normalize":false,"algorithm":"LR"},"timestart":1500048568179,"status":"Finished"},{"_id":"59690ccfe4b0241953ae964e","timeend":1500056783387,"job_name":"TimestartJob2","mape":0.7079879882057265,"parameter_set":{"fit_intercept":false,"job_name":"TimestartJob2","normalize":false,"algorithm":"LR"},"timestart":2147483647,"status":"Finished"},{"_id":"59690e71e4b050f86a82de4f","timeend":1500057201333,"job_name":"TimestartJob2","mape":0.7079879882056198,"parameter_set":{"fit_intercept":false,"job_name":"TimestartJob2","normalize":false,"algorithm":"LR"},"timestart":1500049986796,"status":"Finished"},{"_id":"59690e76e4b0f56a4df2e96d","timeend":1500057206706,"job_name":"TimestartJob223","mape":0.7079879882057265,"parameter_set":{"fit_intercept":false,"job_name":"TimestartJob223","normalize":false,"algorithm":"LR"},"timestart":1500049990838,"status":"Finished"},{"_id":"59691a55e4b0f34900c132e8","timeend":1500060245186,"job_name":"test58","mape":0.7079879882057265,"parameter_set":{"fit_intercept":false,"job_name":"test58","normalize":false,"algorithm":"LR"},"timestart":1500053032263,"status":"Finished"},{"_id":"59691b5de4b084b2ce79e665","timeend":1500060509076,"job_name":"test589","mape":0.7079879882056198,"parameter_set":{"fit_intercept":false,"job_name":"test589","normalize":false,"algorithm":"LR"},"timestart":1500053297662,"status":"Finished"},{"_id":"59691c0be4b02e9708cd1f5f","timeend":1500060683075,"job_name":"tes57","mape":0.7079879882057265,"parameter_set":{"fit_intercept":false,"job_name":"tes57","normalize":false,"algorithm":"LR"},"timestart":1500053471683,"status":"Finished"},{"_id":"59691cf1e4b03ed9605e8a16","timeend":1500060912972,"job_name":"ets","mape":0.7079879882057265,"parameter_set":{"fit_intercept":false,"job_name":"ets","normalize":false,"algorithm":"LR"},"timestart":1500053699908,"status":"Finished"},{"_id":"59691d47e4b01fed53cb04bc","timeend":1500060999156,"job_name":"ets","mape":0.7079879882056198,"parameter_set":{"fit_intercept":false,"job_name":"ets","normalize":false,"algorithm":"LR"},"timestart":1500053787546,"status":"Finished"},{"_id":"59691dade4b0ed84feacf013","timeend":1500061101895,"job_name":"azerty","mape":0.7079879882057265,"parameter_set":{"fit_intercept":false,"job_name":"azerty","normalize":false,"algorithm":"LR"},"timestart":1500053890897,"status":"Finished"},{"_id":"59691ee7e4b0faaab2505f68","timeend":1500061415864,"job_name":"ozjdzodk","mape":0.7079879882057265,"parameter_set":{"fit_intercept":false,"job_name":"ozjdzodk","normalize":false,"algorithm":"LR"},"timestart":1500054202098,"status":"Finished"},{"_id":"5969e02ae4b0d20c5c6a7cfd","timeend":1500110890864,"job_name":"NN","mape":14.581178294608508,"parameter_set":{"cost_function":"mean_squared_error","job_name":"NN","normalization":true,"learning_rate":0.01,"epochs":3,"algorithm":"NN"},"timestart":1500103671826,"status":"Finished"},{"_id":"5969e031e4b0f8fd3c2ae409","timeend":1500110897799,"job_name":"NN","mape":16.08057083674179,"parameter_set":{"cost_function":"mean_squared_error","job_name":"NN","normalization":true,"learning_rate":0.01,"epochs":3,"algorithm":"NN"},"timestart":1500103679718,"status":"Finished"},{"_id":"5969f542e4b083dbaad6f8d0","timeend":1500116290391,"job_name":"NN_lowDim","mape":9.182215883579259,"parameter_set":{"cost_function":"mean_squared_error","job_name":"NN_lowDim","normalization":true,"learning_rate":0.01,"epochs":20,"algorithm":"NN"},"timestart":1500108912178,"status":"Finished"}]');

            if(data2.length > data.length){
                data = data2;
                $( "#result_table_body" ).fadeOut();
                $( "#result_table_body" ).empty();
                console.log(data);

                // dont show it first load
                if(data.length > 0){
                    var snackbarContainer = document.querySelector('#toast');
                    var toastdata = {
                        message: 'New job result is available.'
                        };
                    snackbarContainer.MaterialSnackbar.showSnackbar(toastdata);
                }


                createTable(data);
                $( "#result_table_body" ).fadeIn();
            }
        }).always(function(info){

            //console.log("always");
            //console.log(info);
            fnAlways();

        });
    };

    // ajax reloader
    function reloader() {
        $("#loaderProcess").addClass('mdl-progress__indeterminate');
        ajaxReloadTable(function (){
            setTimeout(function(){
                $("#loaderProcess").removeClass('mdl-progress__indeterminate');
                setTimeout(reloader, 5000);
            }, 500);

        });
    };

    // load data and start reloader
    ajaxReloadTable(function(){
        setTimeout(reloader, 5000);
    });

});