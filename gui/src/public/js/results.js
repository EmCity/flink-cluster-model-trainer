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
    var data = $.parseJSON('[{"_id":"59665c5be4b0dcdabd7828e6","timeend":1499880539895,"job_name":"JobLR001","mape":0.7079879882057265,"parameter_set":{"fit_intercept":false,"job_name":"JobLR001","normalize":false,"algorithm":"LR"},"status":"Finished"},{"_id":"59665d24e4b06b224fbbb39d","timeend":1499880740055,"job_name":"JobLR002","mape":0.7079879882057265,"parameter_set":{"fit_intercept":false,"job_name":"JobLR002","normalize":true,"algorithm":"LR"},"status":"Finished"},{"_id":"59666dd5e4b0cdd4ac468c35","timeend":1499885012882,"job_name":"JobSVM003","mape":0.9616451912556343,"parameter_set":{"epsilon":0.1,"shrinking":true,"C":1,"job_name":"JobSVM003","cache_size":0.001,"kernel":"rbf","max_iter":-1,"gamma":0.1,"tolerance":0.001,"algorithm":"SVM"},"status":"Finished"},{"_id":"59667325e4b0902d868b266b","timeend":1499886373753,"job_name":"JobSVM004","mape":0.9616451912556343,"parameter_set":{"epsilon":0.1,"shrinking":true,"C":1,"job_name":"JobSVM004","cache_size":0.001,"kernel":"rbf","max_iter":-1,"gamma":0.1,"tolerance":0.001,"algorithm":"SVM"},"status":"Finished"},{"_id":"5966749be4b029a19cbaad22","timeend":1499886747503,"job_name":"JobSVM005","mape":0.9616451912556343,"parameter_set":{"epsilon":0.1,"shrinking":true,"C":1,"job_name":"JobSVM005","cache_size":0.001,"kernel":"rbf","max_iter":-1,"gamma":0.1,"tolerance":0.001,"algorithm":"SVM"},"status":"Finished"},{"_id":"596745e1e4b047838b738465","timeend":1499940321169,"job_name":"NewDayJob","mape":0.7504897891813936,"parameter_set":{"fit_intercept":true,"job_name":"NewDayJob","normalize":false,"algorithm":"LR"},"status":"Finished"},{"_id":"5967c096e4b0ce5df0110223","timeend":1499971734025,"job_name":"trainNN","mape":216.4586559719538,"parameter_set":{"cost_function":"mean_squared_error","job_name":"trainNN","normalization":true,"learning_rate":0.01,"epochs":3,"algorithm":"NN"},"status":"Finished"},{"_id":"5967c22ce4b0a1bc79e913f2","timeend":1499972140876,"job_name":"trainNN001","mape":182.79861934442522,"parameter_set":{"cost_function":"mean_squared_error","job_name":"trainNN001","normalization":true,"learning_rate":0.03,"epochs":5,"algorithm":"NN"},"status":"Finished"}]');
    console.log(data);

    function createTable(data){

        $.each( data, function( key, val ) {
            tr = $("<tr/>");

            $("<td/>",{
                "class": "mdl-data-table__cell--non-numeric",
                html: val.job_name
            }).appendTo(tr);

            $("<td/>",{
                html: val.parameter_set.timestart
            }).appendTo(tr);

            $("<td/>",{
                html: new Date(val.timeend).toLocaleString('de')
            }).appendTo(tr);

            $("<td/>",{
                html: val.timeend
            }).appendTo(tr);

            $("<td/>",{
                html: val.mape.toFixed(4)
            }).appendTo(tr);

            tr.appendTo( "#result_table_body" );
        });
    }

    $( "#reload_btn" ).click(function() {
        console.log('do reload');
        $( "#result_table_body" ).empty();

        createTable(data);

        /* TODO
        $.ajax({
            //url: "http://sambahost.dyndns.lrz.de:8500/get_results_api",
            url: "http://sambahost.dyndns.lrz.de:8500/get_results_api",
            type: 'GET',
            crossDomain: true,
            dataType: 'jsonp'
        }).done(function(data) {
            console.log(data);
            //$('#result_list').html( data );
        });
        */



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



});