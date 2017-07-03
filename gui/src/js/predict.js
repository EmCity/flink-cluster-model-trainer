
function predict() {
    data = new Object();
    handleFileSelect("trainingXFile", data);
    handleFileSelect("trainingYFile", data);
    handleFileSelect("testingXFile", data);
    handleFileSelect("testingYFile", data);
    handleFileSelect("validationXFile", data);
    handleFileSelect("validationYFile", data);
    data.job_name = $("#job").val();
    data.timestart = Date.now();
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

    console.log(data);


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
