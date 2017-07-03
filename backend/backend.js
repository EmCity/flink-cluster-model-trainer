var express = require('express');
var bodyParser = require('body-parser');
var child = require('child_process');
var app = express();
app.use(bodyParser.json()); // add a middleware (so that express can parse request.body's json)
const hostname = 'sambahost.dyndns.lrz.de';
const port = 8500;
var MongoClient = require('mongodb').MongoClient;
var Grid = require('mongodb').Grid;
var GridStore = require('mongodb').GridStore;
var url = "mongodb://"+hostname+":27017/samba";
var path = require('path');
var pathguisrc = '/root/code/sose17-small-data/gui/src'

console.log("__dirname :" + __dirname);

app.use('/', express.static( pathguisrc+'/'));
app.use(express.static(pathguisrc+'/js'));
app.use(express.static(pathguisrc+'/img'));
app.use(express.static(pathguisrc+'/css'));

app.get('/', function(req, res) {
  res.sendFile(path.join('index.html'));
});

app.get('/results/', function(req, res) {
  res.sendFile(path.join('results.html'));
});

// save AlgoParaImputs
app.post('/api/', (req, res) => {
  console.log(typeof(req))
  console.log(req.body)
  data = req.body;

  MongoClient.connect(url, function(err, db) {
    if (err) throw err;

    
    //saveCsvToMongo(db, data.data.training.x);

    db.collection("jobs").insertOne(data);
    db.collection("jobs").find().sort({timestart:-1},function(err,cursor){});
    db.close();
    console.log(data.job_name)
    callFlink(data.job_name)
  });
    res.send(req.body);
});

function saveCsvToMongo(db, csv){
    var grid = new Grid(db,'fs');
    var buffer = new Buffer(csv);
    grid.put(buffer, {metadata:{category:'text'}, content_type: 'text'}, function(err, fileInfo){
        grid.get(fileInfo._id, function(err, data){
            if (err) throw err;
            console.log("Retrieved data: " + data.toString());
        });
    });
}

// save AlgoParaImputs
app.get('/start_job/:job_name', (req, res) => {
    console.log(req.params.job_name);
    callFlink(req.params.job_name);

});

function callFlink (jobname) {
    child.exec('~/flink-1.3.0/bin/flink run -c org.lmu.JobNameBatchDB ' +
        '~/code/sose17-small-data/flink/flink-python-job/target/flink-python-job-0.1.jar' + ' ' + jobname, (error, stdout, stderr) =>{
  if (error) {
    console.error(`exec error: ${error}`);
    return;
  }
  console.log(`stdout: ${stdout}`);
  console.log(`stderr: ${stderr}`);
});
}

// get results
app.get('/get_results/', (req, res) => {
    var x = "";
    MongoClient.connect(url, function(err, db) {
      if (err) throw err;
        var coll = db.collection('results');
        x += "error: " + err + "<br>";
        coll.find({},function(err,cursor){
          if (err) throw err;
          cursor.toArray(function(err, result){
             x=result;
              res.send(x);
            db.close();
        });
    });
  });
});

app.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});