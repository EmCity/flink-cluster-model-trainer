var express = require('express');
var bodyParser = require('body-parser');
var child = require('child_process');
var app = express();
app.use(bodyParser.json()); // add a middleware (so that express can parse request.body's json)
const hostname = 'sambahost.dyndns.lrz.de';
const port = 8500;
var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://"+hostname+":27017/samba";
var path = require('path');
var pathguisrc = '../gui/src'

console.log("__dirname :" + __dirname);

app.use(pathguisrc, express.static( '/'));
app.use(pathguisrc, express.static('/js'));
app.use(pathguisrc, express.static('/img'));
app.use(pathguisrc, express.static('/css'));

app.get('/', function(req, res) {
  res.sendFile(path.join(__dirname + '/index.html'));
});

app.get('/results', function(req, res) {
  res.sendFile(path.join(__dirname + '/results.html'));
});

// save AlgoParaImputs
app.post('/api/', (req, res) => {
  console.log(typeof(req))
  console.log(req.body)
  data = req.body;

  MongoClient.connect(url, function(err, db) {
    if (err) throw err;
    db.collection("jobs").insertOne(data);
    db.collection("jobs").find().sort({timestart:-1},function(err,cursor){});
    db.close();
    console.log(data.job_name)
    callFlink(data.job_name)
  });
    res.send(req.body);
});

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