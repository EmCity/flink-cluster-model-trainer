  var result;
  var a;
function handleFileSelect(fileID)
  {

    if (!window.File || !window.FileReader || !window.FileList || !window.Blob) {
      alert('The File APIs are not fully supported in this browser.');
      return;
    }

    input = document.getElementById(fileID);
    if (!input) {
      alert("Um, couldn't find the fileinput element.");
    }
    else if (!input.files) {
      alert("This browser doesn't seem to support the `files` property of file inputs.");
    }
    else if (!input.files[0]) {
      alert("Please select a file before clicking 'Load'");
    }
    else {
      file = input.files[0];
      readFile(file, function(e) {
             // use result in callback...
            $("#fileReading").val(e.target.result)
             result = e.target.result;
             console.log("output");
             a = result;
         });
    }
    console.log(result)
    return a  ;
  }

  function readFile(file, onLoadCallback){
      var reader = new FileReader();
      reader.onload = onLoadCallback;
      reader.readAsText(file);
  }
