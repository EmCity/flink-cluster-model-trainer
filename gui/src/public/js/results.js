function decodeHtml(html) {
    var txt = document.createElement("textarea");
    txt.innerHTML = html;
    return txt.value;
}

var x = decodeHtml(data);
var res = JSON.parse(x);


function createTable(){
var str = "";
var str_detail = "";
var str_head = "";
       for (var i = 0; i < res.length; i++) {
           str += "<tr>";
           str += "<td><input type=\"button\" value=\"Details\"/ class=\"mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--colored mdl-color-text--white\"></td>";
           str += "<td>"+ res[i].job_name +"</td>";
           str += "<td>"+ res[i].mape +"</td>";
           str += "</tr>";

            if(res[i].parameter_set.algorithm == "LR"){
                str_detail += format_LR(res[i]);
//               str_head = "<tr>";
//               str_head += "<th class=\"text-center\">Algorithm</th>";
//               str_head += "<th class=\"text-center\">Fit_intercept</th>";
//               str_head += "<th class=\"text-center\">Normalize</th>";
//               str_head += "</tr>";
//
//               str_detail = "<tr>";
//               str_detail +=   "<td>"+ res[i].parameter_set.algorithm +"</td>";
//               str_detail +=   "<td>"+ res[i].parameter_set.fit_intercept +"</td>";
//               str_detail +=   "<td>"+ res[i].parameter_set.normalize +"</td>";
//               str_detail += "</tr>";
//

            }
            else if(res[i].parameter_set.algorithm == "SVM"){
            str_detail += format_SVM(res[i]);
//               str_head += "<tr>";
//               str_head += "<th class=\"text-center\">Algorithm</th>";
//               str_head += "<th class=\"text-center\">C</th>";
//               str_head += "<th class=\"text-center\">Epsilon</th>";
//               str_head += "<th class=\"text-center\">Kernel</th>";
//               str_head += "<th class=\"text-center\">Gamma</th>";
//               str_head += "<th class=\"text-center\">Shrinking</th>";
//               str_head += "<th class=\"text-center\">Tolerance</th>";
//               str_head += "<th class=\"text-center\">Cache_size</th>";
//               str_head += "<th class=\"text-center\">Max_iter</th>";
//               str_head += "</tr>";
//
//               str_detail += "<tr>";
//               str_detail +=   "<td>"+ res[i].parameter_set.algorithm +"</td>";
//               str_detail +=   "<td>"+ res[i].parameter_set.C +"</td>";
//               str_detail +=   "<td>"+ res[i].parameter_set.epsilon +"</td>";
//               str_detail +=   "<td>"+ res[i].parameter_set.kernel +"</td>";
//               str_detail +=   "<td>"+ res[i].parameter_set.gamma +"</td>";
//               str_detail +=   "<td>"+ res[i].parameter_set.shrinking +"</td>";
//               str_detail +=   "<td>"+ res[i].parameter_set.tolerance +"</td>";
//               str_detail +=   "<td>"+ res[i].parameter_set.cache_size +"</td>";
//               str_detail +=   "<td>"+ res[i].parameter_set.max_iter +"</td>";
//               str_detail += "</tr>";
            }
            else {
            str_detail += format_NN(res[i]);
//               str_head += "<tr>";
//               str_head += "<th class=\"text-center\">Algorithm</th>";
//               str_head += "<th class=\"text-center\">Normalization</th>";
//               str_head += "<th class=\"text-center\">Learning_rate</th>";
//               str_head += "<th class=\"text-center\">Epochs</th>";
//               str_head += "<th class=\"text-center\">Display_step</th>";
//               str_head += "<th class=\"text-center\">Cost_function</th>";
//               str_head += "</tr>";
//
//               str_detail += "<tr>";
//               str_detail +=   "<td>"+ res[i].parameter_set.algorithm +"</td>";
//               str_detail +=   "<td>"+ res[i].parameter_set.normalization +"</td>";
//               str_detail +=   "<td>"+ res[i].parameter_set.learning_rate +"</td>";
//               str_detail +=   "<td>"+ res[i].parameter_set.epochs +"</td>";
//               str_detail +=   "<td>"+ res[i].parameter_set.display_step +"</td>";
//               str_detail +=   "<td>"+ res[i].parameter_set.cost_function +"</td>";
//               str_detail += "</tr>";
            }


      };

        document.querySelector('#tbody').innerHTML = str;
//        document.querySelector('#thead').innerHTML = str_head;
        document.querySelector('#tbody_detail').innerHTML = str_detail;

      console.log(typeof str_detail);
      console.log(str_detail);
};

function reload_fct(){
        window.location.reload();
};

$(document).delegate('input[type="button"]','click',function(){
	$('[colspan="5"]').parent('tr').remove();
	$(this).parents('tr').after('<tr/>').next().append('<td colspan="5"/>').children('td').append('<div/>').children().css({'display': 'none', 'padding': '10px'}).html($('#content').html()).slideDown();

	$("#hide_details").on("click",function(){
		$("#content").hide();
		$("#tbody").show();
	});

});

function format_LR (d) {
    return '<b>Algorithm: </b>'+d.parameter_set.algorithm+'<br>'+
        '<b>Fit_intercept: </b>'+d.parameter_set.fit_intercept+'<br>'+
        '<b>Normalize: </b>'+d.parameter_set.normalize+'<br><br>';
};

function format_SVM (d) {
    return '<b>Algorithm: </b>'+d.parameter_set.algorithm+'<br>'+
        '<b>C: </b>'+d.parameter_set.C+'<br>'+
        '<b>Epsilon: </b>'+d.parameter_set.epsilon+'<br>'+
        '<b>Kernel: </b>'+d.parameter_set.kernel+'<br>'+
        '<b>Gamma: </b>'+d.parameter_set.gamma+'<br>'+
        '<b>Shrinking: </b>'+d.parameter_set.shrinking+'<br>'+
        '<b>Tolerance: </b>'+d.parameter_set.tolerance+'<br>'+
        '<b>Cache_size: </b>'+d.parameter_set.cache_size+'<br>'+
        '<b>Max_iter: </b>'+d.parameter_set.max_iter+'<br><br>';
};

function format_NN (d) {
    return '<b>Algorithm: </b>'+ d.parameter_set.algorithm+'<br>'+
        '<b>Normalize: </b>'+d.parameter_set.normalization+'<br>'+
        '<b>Learning_rate: </b>'+d.parameter_set.learning_rate+'<br>'+
        '<b>Epochs: </b>'+d.parameter_set.epochs+'<br>'+
        '<b>Display_step: </b>'+d.parameter_set.display_step+'<br>'+
        '<b>Cost_function: </b>'+d.parameter_set.cost_function+'<br><br>';
};

