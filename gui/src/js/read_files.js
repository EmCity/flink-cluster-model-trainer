var data = new Object();
data.data = new Object();
data.data.training = new Object();
data.data.testing = new Object();
data.data.validation = new Object();


function handleFileSelect(fileID) {

    if (!window.File || !window.FileReader || !window.FileList || !window.Blob) {
        alert('The File APIs are not fully supported in this browser.');
        return;
    }

    input = document.getElementById(fileID);
    if (!input) {
        alert("Um, couldn't find the fileinput element.");
    } else if (!input.files) {
        alert("This browser doesn't seem to support the `files` property of file inputs.");
    }
     else if (!input.files[0]) {
         //console.log("Please select a file before clicking 'Load'");
    }
     else {
        file = input.files[0];
        var reader = new FileReader();

        reader.onload = function(e) {
            var text = reader.result;
            switch (fileID) {
                case "trainingXFile":
                    data.data.training.x = text;
                    break;
                case "trainingYFile":
                    data.data.training.y = text;
                    break;
                case "testingXFile":
                    data.data.testing.x = text;
                    break;
                case "testingYFile":
                    data.data.testing.y = text;
                    break;
                case "validationXFile":
                    data.data.validation.x = text;
                    break;
                case "validationYFile":
                    data.data.validation.y = text;
                    break;
            }
        }
        reader.readAsText(file);
    }
}
