function predict() {
	var content;
	content = handleFileSelect("trainingXFile")
	console.log(content)

	x_train = $("#fileReading")[0].value;
	console.log(x_train)

	/*
	y_train = handleFileSelect("trainingYFile")
	x_test = handleFileSelect("testingXFile")
	y_test = handleFileSelect("testingYFile")
	x_validation = handleFileSelect("validationXFile")
	y_validation = handleFileSelect("validationYFile")
*/
	var data = {
		job_name : $("#job").val(),
		algorithm : $("input.mdl-radio__button:checked").val(),
		data : {
			training : {
				x : x_train
				//y : y_train
			},
			testing : {
				////x : x_test,
				//y : y_test
			},
			validation : {
				//x : x_validation,
				//y : y_validation
			}
		}

	}
	console.log(data)
	$.post( "http://teamsamba.pythonanywhere.com/predict", function( data ) {
	  console.log( "Data Loaded: " + data );
		window.open("results.html");
	});
}
