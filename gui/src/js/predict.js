<<<<<<< HEAD
function predict() {
    handleFileSelect("trainingXFile");
    handleFileSelect("trainingYFile");
    handleFileSelect("testingXFile");
    handleFileSelect("testingYFile");
    handleFileSelect("validationXFile");
    handleFileSelect("validationYFile");
    data.job_name = $("#job").val();
    data.start_time = Date.now();
    data.algorithm = new Object();
    $(".mdl-checkbox__input:checkbox:checked").each(function() {
        var algoID = $(this).val();
        data.algorithm[algoID] = new Object();
        $("#" + algoID + " :input").each(function() {
            id = this.id;
            data.algorithm[algoID][id] = new Object();
            if ($(this).is(':checkbox'))
                data.algorithm[algoID][id] = ($(this).prop('checked') == true);

            else {
                if (id == "gamma" && !($(this).val().length))
                    data.algorithm[algoID][id] = "auto";
                else
                    data.algorithm[algoID][id] = $(this).val();
            }
        });
    });


    fetch("http://sambahost.dyndns.lrz.de:8500/api", {
  method: 'POST',
  body: JSON.stringify(data), // stringify JSON
  headers: new Headers({ "Content-Type": "application/json" }) // add headers
}).then(function(response) {
    // The response is a Response instance.
    // You parse the data into a useable format using `.json()`
    return response.json();
  }).then(function(data) {
    // `data` is the parsed version of the JSON returned from the above endpoint.
    console.log(data);  // { "userId": 1, "id": 1, "title": "...", "body": "..." }
  }).catch(function(error) {
    console.log('Request failed', error);
  });
}
=======
function predict() {
    handleFileSelect("trainingXFile");
    handleFileSelect("trainingYFile");
    handleFileSelect("testingXFile");
    handleFileSelect("testingYFile");
    handleFileSelect("validationXFile");
    handleFileSelect("validationYFile");
    data.job_name = $("#job").val();
    data.algorithm = new Object();
    $(".mdl-checkbox__input:checkbox:checked").each(function() {
        var algoID = $(this).val();
        data.algorithm[algoID] = new Object();
        $("#" + algoID + " :input").each(function() {
            id = this.id;
            data.algorithm[algoID][id] = new Object();
            if ($(this).is(':checkbox'))
                data.algorithm[algoID][id] = ($(this).prop('checked') == true);

            else {
                if (id == "gamma" && !($(this).val().length))
                    data.algorithm[algoID][id] = "auto";
                else
                    data.algorithm[algoID][id] = $(this).val();
            }
        });
    });


    console.log(data)
    console.log(typeof(data))
    $.ajax({
   url: 'http://sambahost.dyndns.lrz.de:8000/api',
   type: 'POST',
   data: data,
   contentType: 'application/json; charset=utf-8',
   dataType: 'json',
   success: function(msg) {
       alert(msg);
   }
});
    var d = data.data;
    // if (d.training.x && d.training.y &&
    //     d.testing.x && d.testing.y &&
    //     d.validation.x && d.validation.y && data.job_name.length !== 0) {
    //     $.ajax({
    //         type: "POST",
    //         url: "http://sambahost.dyndns.lrz.de:8000/predict",
    //         data: data,
    //         dataType : jsonp,
    //         success: function(data) {
    //             console.log("Data Loaded: " + data);
    //             window.open("results.html");
    //         }
    //     });
    // } else {
    //     alert("complete form please");
    // }

}
>>>>>>> 84f81f04de4075c3d97a7b96f418db518797a25b
