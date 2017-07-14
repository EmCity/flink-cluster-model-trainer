
function predict() {
  var data = new Object();
  data.data = new Object();
  data.data.train_x = new Object();
  data.data.train_y = new Object();
  data.data.test_x = new Object();
  data.data.test_y = new Object();
  data.data.valid_x = new Object();
  data.data.valid_y = new Object();
  let a = handleFileSelect("trainingXFile");
    let b = handleFileSelect("trainingYFile");
    let c = handleFileSelect("testingXFile");
    let d = handleFileSelect("testingYFile");
    let e = handleFileSelect("validationXFile");
    let f = handleFileSelect("validationYFile");
    data.job_name = $("#job").val();
    var date = new Date();
    data.timestart = date.getTime();
    data.algorithms = new Object();
    $(".mdl-checkbox__input:checkbox:checked").each(function() {
        var algoID = $(this).val();
        data.algorithms[algoID] = new Object();
        $("#" + algoID + " :input").each(function() {
            id = this.id;
            data.algorithms[algoID][id] = new Object();
            if ($(this).is(':checkbox'))
                data.algorithms[algoID][id] = ($(this).prop('checked') == true);

            else {
                if (id == "gamma" && !($(this).val().length))
                    data.algorithms[algoID][id] = "auto";
                else if($(this).val().split(',').length > 1)
                {
                    var array = $(this).val().split(',')
                    console.log("Was parsable as String");
                    data.algorithms[algoID][id] = array;
                }
                else
                {
                    //data.algorithm[algoID][id] = "[".concat($(this).val(), "]");
                    var array = [$(this).val()];
                    data.algorithms[algoID][id] = array;
                }

            }
        });
    });
     if(data.algorithms['SVM'])
     {
          data.algorithms['SVM']['tolerance'] = data.algorithms['SVM']['tolerance'][0];
          data.algorithms['SVM']['cache_size'] = data.algorithms['SVM']['cache_size'][0];
          data.algorithms['SVM']['max_iter'] = data.algorithms['SVM']['max_iter'][0];

     }
     Promise.all([a, b, c, d]).then(function() {
        fetch("http://sambahost.dyndns.lrz.de:8500/api", {
            method: 'POST',
            body: JSON.stringify(data), // stringify JSON
            headers: new Headers({
                "Content-Type": "application/json", 'Access-Control-Allow-Origin':'*'
            }) // add headers
        }).then(function(response) {
            // The response is a Response instance.
            // You parse the data into a useable format using `.json()`
            return response.json();
        }).then(function(data) {
            // `data` is the parsed version of the JSON returned from the above endpoint.
            console.log(data); // { "userId": 1, "id": 1, "title": "...", "body": "..." }
        }).catch(function(error) {
            console.log('Request failed', error);
        })
    })


}

function browse_fct(){
        window.open('get_results','_blank');
}
