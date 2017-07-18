package org.lmu;

import com.mongodb.BasicDBObject;
import com.mongodb.MongoCredential;
import com.mongodb.DBCollection;
import com.mongodb.DBCursor;
import com.mongodb.DBObject;
import com.mongodb.MongoClient;
import com.mongodb.ServerAddress;
import org.apache.flink.api.java.ExecutionEnvironment;
import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.api.java.DataSet;
import org.apache.flink.util.Collector;
import org.lmu.JSON.parser.JSONParser;
import org.lmu.JSON.JSONArray;
import org.lmu.JSON.JSONObject;
import org.lmu.JSON.parser.ParseException;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.Collections;

/***
 * Distribution of the job onto the workers.
 */
final class FlinkJobDistribution {
    /**
     * DB name.
     */
    private static final  String DBNAME = "samba";
    /**
     * DB credentials.
     */
    private static final  MongoCredential CREDENTIALS = MongoCredential.createMongoCRCredential(
            "sambauser", DBNAME, "teamsamba".toCharArray());
    /**
     * host name.
     */
    private static final  String URL = "sambahost.dyndns.lrz.de";
    /**
     * port of the DB.
     */
    private static final  int PORT = 27017;

    /**
     *
     * @param json json job
     * @return json array with results
     * @throws Exception if parse error happens
     */
     JSONArray distribute(final JSONObject json) throws Exception {
        final ExecutionEnvironment env = ExecutionEnvironment.getExecutionEnvironment();

        JSONObject algorithms = (JSONObject) json.get("algorithms");
        JSONObject svm = (JSONObject) algorithms.get("SVM");
        JSONObject lr = (JSONObject) algorithms.get("LR");
        JSONObject nn = (JSONObject) algorithms.get("NN");

        String jobName = json.get("job_name").toString();
        System.out.println("FlinkJobDistribution: Job: " + jobName);

        JSONArray svmArray = svm != null ? createSVMJobs(svm) : new JSONArray();
        JSONArray lrArray = lr != null ? createLRJobs(lr) : new JSONArray();
        JSONArray nnArray = nn != null ? createNNJobs(nn) : new JSONArray();

        // get input data
        ArrayList<String> tasks = new ArrayList<>();
        fillList(json, svmArray, tasks);
        fillList(json, lrArray, tasks);
        fillList(json, nnArray, tasks);

        System.out.println("FlinkJobDistripbution: Distribute: " + tasks.size() + " jobs on the workers:");
        //DataSet<String> dataset = env.fromCollection(tasks).flatMap(new OnWorkers());
        DataSet<String> dataset = env.fromCollection(tasks).setParallelism(tasks.size()).flatMap(new OnWorkers());
        JSONArray resJsonArray = new JSONArray();
        JSONParser parser = new JSONParser();
        for (String s : dataset.collect()) {
            System.out.print(s);
            resJsonArray.add((JSONObject) parser.parse(s));
        }
        return resJsonArray;
    }

    /**
     * Fills the ArrayList with the tasks.
     * @param json jsonObject
     * @param array jsonarray
     * @param tasks arrayList with the tasks
     */
    private static void fillList(final JSONObject json, final JSONArray array, final ArrayList<String> tasks) {
        for (Object obj : array) {
            obj = new JSONObject((JSONObject) obj);
            ((JSONObject) obj).put("job_name", json.get("job_name"));
            tasks.add(((JSONObject) obj).toJSONString());
        }
    }

    /**
     * Creates the SVM tasks.
     * @param svm svm json object.
     * @return json array with the svm tasks.
     */
    private static JSONArray createSVMJobs(final JSONObject svm) {
        JSONArray cArray = (JSONArray) svm.get("C");
        JSONArray eArray = (JSONArray) svm.get("epsilon");
        JSONArray kernelArray = (JSONArray) svm.get("kernel");
        JSONArray gammaArray = (JSONArray) svm.get("gamma");

        JSONArray result = new JSONArray();
        if (cArray != null & eArray != null & kernelArray != null & gammaArray != null) {
            for (Object c : cArray) {
                for (Object e : eArray) {
                    for (Object kernel : kernelArray) {
                        for (Object gamma : gammaArray) {
                            JSONObject obj = new JSONObject();
                            obj.put("algorithm", "SVM");
                            obj.put("C", Double.parseDouble(c.toString().replaceAll("\\s+", "")));
                            obj.put("epsilon", Double.parseDouble(e.toString().replaceAll("\\s+", "")));
                            obj.put("kernel", kernel);
                            obj.put("gamma", Double.parseDouble(gamma.toString().replaceAll("\\s+", "")));
                            obj.put("shrinking", svm.get("shrinking"));
                            obj.put("tolerance", Double.parseDouble(svm.get("tolerance").toString().replaceAll("\\s+", "")));
                            obj.put("cache_size", Double.parseDouble(svm.get("cache_size").toString().replaceAll("\\s+", "")));
                            obj.put("max_iter", Integer.parseInt(svm.get("max_iter").toString().replaceAll("\\s+", "")));
                            result.add(obj);
                        }
                    }
                }
            }
        } else {
            System.out.println("SVM-ARRAYS NULL");
        }
        return result;
    }

    /**
     * @param lr linear Regression json object
     * @return json array splitted with the tasks
     */
    private static JSONArray createLRJobs(final JSONObject lr) {
        Boolean normalize = (Boolean) lr.get("normalize");
        Boolean fitIntercept = (Boolean) lr.get("fit_intercept");
        JSONArray result = new JSONArray();
        JSONObject obj = new JSONObject();
        obj.put("algorithm", "LR");
        obj.put("normalize", normalize);
        obj.put("fit_intercept", fitIntercept);
        result.add(obj);
        return result;
    }

    /**
     *
     * @param nn nn json object
     * @return json array splitted with the tasks
     */
    private static JSONArray createNNJobs(final JSONObject nn) {
        JSONArray learningRates = (JSONArray) nn.get("learning_rate");
        JSONArray epochs = (JSONArray) nn.get("epochs");
        JSONArray costFunctions = (JSONArray) nn.get("cost_function");
        JSONArray result = new JSONArray();
        if (learningRates != null & epochs != null & costFunctions != null) {
            for (Object learningRate : learningRates) {
                for (Object epoch : epochs) {
                    for (Object costFunction : costFunctions) {
                        JSONObject obj = new JSONObject();
                        obj.put("algorithm", "NN");
                        obj.put("normalization", nn.get("normalization"));
                        obj.put("learning_rate", Double.parseDouble(learningRate.toString().replaceAll("\\s+", "")));
                        obj.put("epochs", Integer.parseInt(epoch.toString().replaceAll(" ", "").replaceAll("\\s+", "")));
                        obj.put("cost_function", costFunction);
                        result.add(obj);
                    }
                }
            }
        } else {
            System.out.println("NN-ARRAYS NULL");
        }
        return result;
    }

    /**
     *
     * @param jobName name of the job
     * @return the jsonObject from DB
     * @throws UnknownHostException if DB is unknown
     * @throws ParseException if json isnt able to parase the job
     */
    JSONObject getJobJSONObject(final String jobName) throws UnknownHostException, ParseException {
        MongoClient mongoClient = new MongoClient(new ServerAddress(
                URL, PORT), Collections.singletonList(CREDENTIALS));
        DBCollection coll = mongoClient.getDB(DBNAME).getCollection("jobs");
        BasicDBObject query = new BasicDBObject("job_name", jobName);

        DBCursor cursor = coll.find(query);
        if (cursor == null) {
            return null;
        }
        BasicDBObject job = null;
        try {
            while (cursor.hasNext()) {
                job = (BasicDBObject) cursor.next();
            }
        } finally {
            cursor.close();
        }
        mongoClient.close();
        return job == null ? (JSONObject) new JSONParser().parse(
                "Query: " + query + " found nothing") : (
                        JSONObject) new JSONParser().parse(job.toString());
    }

    /**
     * @param jsonObject result jsonObject
     * @throws UnknownHostException if DB is unknown
     */
    void saveResultJSONObjectToMongoDB(final JSONObject jsonObject) throws UnknownHostException {
        MongoClient mongoClient = new MongoClient(new ServerAddress(
                URL, PORT), Collections.singletonList(CREDENTIALS));
        DBCollection coll = mongoClient.getDB(DBNAME).getCollection("results");
        DBObject b = (DBObject) com.mongodb.util.JSON.parse(jsonObject.toString());

        System.out.println("Object: " + b);
        coll.insert(b);
        mongoClient.close();
    }

    /**
     * @param resultsJSONArray jsonArray with results
     * @return best JSONObject
     */
    JSONObject getBestMapeJsonObject(final JSONArray resultsJSONArray) {
        double bestmape = 420;
        //double bestValidMape = 420;
        JSONObject bestJsonObject = new JSONObject();
       // JSONObject bestJsonValidObject = new JSONObject();
        for (Object o : resultsJSONArray) {
            JSONObject jsonObject = (JSONObject) o;
            double mape = (double) jsonObject.get("mape");
            //double mape_valid = (double) jsonObject.get("mape_valid");
            if (bestmape > mape) {
                bestmape = mape;
                bestJsonObject = jsonObject;
            }
           // if (bestValidMape > mape) {
            //    bestValidMape = mape;
              //  bestJsonObjectValid = jsonObject;
                //
         //}
        }
       // if (bestJsonObject!=bestJsonValidObject)
       //     bestJsonObject=bestJsonValidObject;
        return bestJsonObject;
    }

    /**
     * Distributes the tasks on the workers.
     */
    public static final class OnWorkers implements FlatMapFunction<String, String> {
        @Override
        public void flatMap(final String value, final Collector<String> out) {
            StringBuilder sB = new StringBuilder();
            try {
                String pythonPath = "/root/anaconda/envs/dataScience/bin/python3";
                String trainModelPath = "/root/code/sose17-small-data/python"
                        + "/traffic-prediction/src/flink/trainModel.py";
                Process proc = Runtime.getRuntime().exec(
                        pythonPath + " " + trainModelPath + " " + value);
                BufferedReader stdInput = new BufferedReader(
                        new InputStreamReader(proc.getInputStream()));
                BufferedReader stdError = new BufferedReader(
                        new InputStreamReader(proc.getErrorStream()));
                String s;
                while ((s = stdInput.readLine()) != null) {
                    sB.append("\n");
                    sB.append(s);
                }
                while ((s = stdError.readLine()) != null) {
                    sB.append("\n");
                    sB.append(s);
                }
                stdInput.close();
                stdError.close();
            } catch (Exception e) {
                sB.append(e.toString());
            }
            out.collect(sB.toString());
        }
    }
}
