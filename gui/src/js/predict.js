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
