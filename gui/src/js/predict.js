function predict() {
    var content;
     handleFileSelect("trainingXFile");
     handleFileSelect("trainingYFile");
    handleFileSelect("testingXFile");
    handleFileSelect("testingYFile");
		 handleFileSelect("validationXFile");
   handleFileSelect("validationYFile");
    data.job_name = $("#job").val();
    data.algorithm = $("input.mdl-radio__button:checked").val();

    console.log(data)
		console.log(data.job_name.length)
    // $.post("http://teamsamba.pythonanywhere.com/predict", function(data) {
    //     console.log("Data Loaded: " + data);
    //     window.open("results.html");
    // });
		var d=data.data;
		if (d.training.x &&d.training.y
		&&d.testing.x && d.testing.y
	&&d.validation.x&&d.validation.y && data.job_name.length!==0){
			$.ajax({
	  type: "POST",
	  url: "http://teamsamba.pythonanywhere.com/predict",
	  data: data,
	  success: function(data) {
				console.log("Data Loaded: " + data);
				window.open("results.html");
		}
	});
		}
		else {
			alert("complete form please");
		}

}
