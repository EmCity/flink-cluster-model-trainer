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

app.set('views', path.join(__dirname, '/../gui/src/views'));
app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');
app.use('/',express.static(path.join(__dirname, '/../gui/src/public/')));


app.get('/', function(req, res) {
  res.render("index")
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
  MongoClient.connect(url, function(err, db) {
    if (err) throw err;
      var coll = db.collection('results');
      cursor = coll.find({});
        cursor.toArray(function(err, result){
               res.render("results",{ data: JSON.stringify(result) });
      });
      db.close();
    });
  })

app.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});

// var Grid = require('mongodb').Grid;
// var GridStore = require('mongodb').GridStore;
// function saveCsvToMongo(db, csv){
//     var grid = new Grid(db,'fs');                                                        
//     var buffer = new Buffer(csv);
//         grid.get(fileInfo._id, function(err, data){ontent_type: 'text'}, functio$
//   console.log(`stderr: ${stderr}`);
//             if (err) throw err;
//             console.log("Retrieved data: " + data.toString());
//         });
//     });
// }
