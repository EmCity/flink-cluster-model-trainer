/*
var training = document.querySelectorAll(".mdl-textfield mdl-js-textfield textfield-demo")
var trainingFile = document.querySelectorAll(".none")
var trainingFileText = document.querySelectorAll(".trainingXFileText mdl-textfield__input")
*/
/*TRAINING X*/

var trainingX = document.getElementById('trainingX');
var trainingXFile = document.getElementById('trainingXFile');
var trainingXFileText = document.getElementById('trainingXFileText');

trainingXFile.addEventListener('change', changeInputTextTRAININGX);
trainingXFile.addEventListener('change', changeStateTRAININGX);

function changeInputTextTRAININGX() {
  var str = trainingXFile.value;
  var i;
  if (str.lastIndexOf('\\')) {
    i = str.lastIndexOf('\\') + 1;
  } else if (str.lastIndexOf('/')) {
    i = str.lastIndexOf('/') + 1;
  }
  trainingXFileText.value = str.slice(i, str.length);
}

function changeStateTRAININGX() {
  if (trainingXFileText.value.length != 0) {
    if (!trainingX.classList.contains("is-focused")) {
      trainingX.classList.add('is-focused');
    }
  } else {
    if (trainingX.classList.contains("is-focused")) {
      trainingX.classList.remove('is-focused');
    }
  }
}

/*TRAINING Y*/

var trainingY = document.getElementById('trainingY');
var trainingYFile = document.getElementById('trainingYFile');
var trainingYFileText = document.getElementById('trainingYFileText');

trainingYFile.addEventListener('change', changeInputTextTRAININGY);
trainingYFile.addEventListener('change', changeStateTRAININGY);

function changeInputTextTRAININGY() {
  var str = trainingYFile.value;
  var i;
  if (str.lastIndexOf('\\')) {
    i = str.lastIndexOf('\\') + 1;
  } else if (str.lastIndexOf('/')) {
    i = str.lastIndexOf('/') + 1;
  }
  trainingYFileText.value = str.slice(i, str.length);
}

function changeStateTRAININGY() {
  if (trainingYFileText.value.length != 0) {
    if (!trainingY.classList.contains("is-focused")) {
      trainingY.classList.add('is-focused');
    }
  } else {
    if (trainingY.classList.contains("is-focused")) {
      trainingY.classList.remove('is-focused');
    }
  }
}


/*TESTING X*/

var testing = document.getElementById('testingX');
var testingXFile = document.getElementById('testingXFile');
var testingXFileText = document.getElementById('testingXFileText');

testingXFile.addEventListener('change', changeInputTextTESTINGX);
testingXFile.addEventListener('change', changeStateTESTINGX);

function changeInputTextTESTINGX() {
  var str = testingXFile.value;
  var i;
  if (str.lastIndexOf('\\')) {
    i = str.lastIndexOf('\\') + 1;
  } else if (str.lastIndexOf('/')) {
    i = str.lastIndexOf('/') + 1;
  }
  testingXFileText.value = str.slice(i, str.length);
}

function changeStateTESTINGX() {
  if (testingXFileText.value.length != 0) {
    if (!testingX.classList.contains("is-focused")) {
      testingX.classList.add('is-focused');
    }
  } else {
    if (testingX.classList.contains("is-focused")) {
      testingX.classList.remove('is-focused');
    }
  }
}

/*TESTING Y*/

var testingY = document.getElementById('testingY');
var testingYFile = document.getElementById('testingYFile');
var testingYFileText = document.getElementById('testingYFileText');

testingYFile.addEventListener('change', changeInputTextTESTINGY);
testingYFile.addEventListener('change', changeStateTESTINGY);

function changeInputTextTESTINGY() {
  var str = testingYFile.value;
  var i;
  if (str.lastIndexOf('\\')) {
    i = str.lastIndexOf('\\') + 1;
  } else if (str.lastIndexOf('/')) {
    i = str.lastIndexOf('/') + 1;
  }
  testingYFileText.value = str.slice(i, str.length);
}

function changeStateTESTINGY() {
  if (testingYFileText.value.length != 0) {
    if (!testingY.classList.contains("is-focused")) {
      testingY.classList.add('is-focused');
    }
  } else {
    if (testingY.classList.contains("is-focused")) {
      testingY.classList.remove('is-focused');
    }
  }
}

/*VALIDATION X*/

var validationX = document.getElementById('validationX');
var validationXFile = document.getElementById('validationXFile');
var validationXFileText = document.getElementById('validationXFileText');

validationXFile.addEventListener('change', changeInputTextVALIDATIONX);
validationXFile.addEventListener('change', changeStateVALIDATIONX);

function changeInputTextVALIDATIONX() {
  var str = validationXFile.value;
  var i;
  if (str.lastIndexOf('\\')) {
    i = str.lastIndexOf('\\') + 1;
  } else if (str.lastIndexOf('/')) {
    i = str.lastIndexOf('/') + 1;
  }
  validationXFileText.value = str.slice(i, str.length);
}

function changeStateVALIDATIONX() {
  if (validationXFileText.value.length != 0) {
    if (!validationX.classList.contains("is-focused")) {
      validationX.classList.add('is-focused');
    }
  } else {
    if (validationX.classList.contains("is-focused")) {
      validationX.classList.remove('is-focused');
    }
  }
}

/*VALIDATION Y*/

var validationY = document.getElementById('validationY');
var validationYFile = document.getElementById('validationYFile');
var validationYFileText = document.getElementById('validationYFileText');

validationYFile.addEventListener('change', changeInputTextVALIDATIONY);
validationYFile.addEventListener('change', changeStateVALIDATIONY);

function changeInputTextVALIDATIONY() {
  var str = validationYFile.value;
  var i;
  if (str.lastIndexOf('\\')) {
    i = str.lastIndexOf('\\') + 1;
  } else if (str.lastIndexOf('/')) {
    i = str.lastIndexOf('/') + 1;
  }
  validationYFileText.value = str.slice(i, str.length);
}

function changeStateVALIDATIONY() {
  if (validationYFileText.value.length != 0) {
    if (!validationY.classList.contains("is-focused")) {
      validationY.classList.add('is-focused');
    }
  } else {
    if (validationY.classList.contains("is-focused")) {
      validationY.classList.remove('is-focused');
    }
  }
}
