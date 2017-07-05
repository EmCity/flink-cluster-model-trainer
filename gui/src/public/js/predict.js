function predict() {
    data = new Object();
    data.data = new Object();
    data.data.train_x = new Object();
    data.data.train_y = new Object();
    data.data.test_x = new Object();
    data.data.test_y = new Object();
    data.data.valid_x = new Object();
    data.data.valid_y = new Object();
    let a = handleFileSelect("trainingXFile")
    let b = handleFileSelect("trainingYFile");
    let c = handleFileSelect("testingXFile");
    let d = handleFileSelect("testingYFile");
    let e = handleFileSelect("validationXFile");
    let f = handleFileSelect("validationYFile");


    data.job_name = $("#job").val();
    data.timestart = Date.now();
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
                else
                    data.algorithms[algoID][id] = "[".concat($(this).val(), "]");
            }
        });
    });

    Promise.all([a, b, c, d, e, f]).then(function() {
        console.log(data);

        fetch("http://sambahost.dyndns.lrz.de:8500/api", {
            method: 'POST',
            body: JSON.stringify(data), // stringify JSON
            headers: new Headers({
                "Content-Type": "application/json"
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

    //},15000)

};
