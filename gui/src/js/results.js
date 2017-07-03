const hostname = 'localhost';
const port = 3000;

setInterval(function(){ $.get( hostname+":"+port+"/get_results/", function( data ) {
  console.log("d")
  $( ".result" ).html( data );
}) }, 3000);

// $.ajax({
//     url: '',
//     type: '',
//     data: {},
//     timeout: 3000,
//     success: function(data){
//         // do stuff
//     }
// });
