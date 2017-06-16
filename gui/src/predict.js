function predict() {
	//alert("Predict");
	$.post( "http://teamsamba.pythonanywhere.com/predict", function( data ) {
	  console.log( "Data Loaded: " + data );
	});
}