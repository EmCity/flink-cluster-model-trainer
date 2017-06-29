package org.lmu;

import org.apache.flink.api.java.ExecutionEnvironment;
import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.api.java.DataSet;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.core.fs.FileSystem;
import org.apache.flink.util.Collector;
import org.apache.http.HttpResponse;
import org.apache.http.client.HttpClient;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.log4j.varia.NullAppender;

import org.lmu.JSON.JSONArray;
import org.lmu.JSON.JSONObject;
import org.lmu.JSON.parser.JSONParser;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

public class FlinkJobDistribution {

    public static void main(String[] args) throws Exception {

        String jobName = "";
        if (args.length > 0 && args[0] != null) {
            jobName = args[0];
            System.out.println("Got JobName: " + jobName);
        } else {
            throw new Exception("check args parameters: " + args);
        }

		/*
        //connect to DB
		MongoClient mongoClient = new MongoClient("sambahost.dyndns.lrz.de", 27017);
		DBCollection coll = mongoClient.getDB("samba").getCollection("jobs");


		BasicDBObject query = new BasicDBObject("job_name", jobName);
		DBCursor cursor = coll.find(query);

		if(cursor== null){
			System.out.println("Problem with Database");
			return ;
		}

		BasicDBObject jobs = null;
		try{
			while(cursor.hasNext()){
				jobs = (BasicDBObject) cursor.curr();
				System.out.println(jobs);

			}
		} finally{
				cursor.close();
		}

		if(jobs != null){
			System.out.println("jobs: " + jobs.toString());
		} else {
			System.out.println("Query: " + query + " found nothing");
		}
		*/

        String testjsonFile = "./BigDataScience/sose17-small-data/flink/flink-python-job/src/main/java/org/lmu/JobDef.json";
        JSONObject jobsjson;
        jobsjson = (JSONObject) new JSONParser().parse(new FileReader(testjsonFile));

        //JSONObject jobsjson = (JSONObject) new JSONParser().parse(obj.toString());

        System.out.println("jobsjson: " + jobsjson.toString());

        List<Tuple2<String, String>> resCollect = distribute(jobsjson);

        System.out.println("resCollect: " + resCollect);

        //String response = sendResultPostToBackend((JSONObject) new JSONParser().parse(tasks.get(0)));
        //System.out.println("-----------" + response + "----------");

    }

    public static List<Tuple2<String, String>> distribute(JSONObject json) throws Exception {
        // set up the batch execution environment
        final ExecutionEnvironment env = ExecutionEnvironment.getExecutionEnvironment();
        env.getConfig().disableSysoutLogging();
        org.apache.log4j.BasicConfigurator.configure(new NullAppender());
        JSONObject algorithms = (JSONObject) json.get("algorithms");
        JSONObject data = (JSONObject) json.get("data");
        JSONObject svm = (JSONObject) algorithms.get("SVM");
        JSONObject lr = (JSONObject) algorithms.get("LR");
        JSONObject nn = (JSONObject) algorithms.get("NN");
        JSONArray svmArray = svm != null ? createSVMJobs(svm) : new JSONArray();
        JSONArray lrArray = lr != null ? createLRJobs(svm) : new JSONArray();
        JSONArray nnArray = nn != null ? createNNJobs(svm) : new JSONArray();

        // get input data
        ArrayList<String> tasks = new ArrayList<>();
        fillList(data, svmArray, tasks);
        fillList(data, lrArray, tasks);
        fillList(data, nnArray, tasks);

        DataSet<String> elementsDataSet = env.fromCollection(tasks);

        //distribute on workers
        DataSet<String> dataset = elementsDataSet.flatMap(new OnWorkers());

        //saves the result as text
        dataset.writeAsText("result.txt", FileSystem.WriteMode.OVERWRITE);

        // workers are executing
        List<Tuple2<String, String>> res = new ArrayList<>();

        // execute program
        env.execute("Flink Batch RunCMD Job");
        dataset.print();

        //String response = sendResultPostToBackend((JSONObject) new JSONParser().parse(tasks.get(0)));
        //System.out.println("-----------" + response + "----------");
        return res;
    }

    private static void fillList(JSONObject data, JSONArray array, ArrayList<String> tasks) {
        for (Object obj : array) {
            obj = new JSONObject((JSONObject) obj);
            ((JSONObject) obj).put("data", data);
            tasks.add(((JSONObject) obj).toJSONString());
        }
    }

    private static JSONArray createSVMJobs(JSONObject svm) {
        JSONArray c_array = (JSONArray) svm.get("C");
        JSONArray e_array = (JSONArray) svm.get("epsilon");
        JSONArray kernel_array = (JSONArray) svm.get("kernels");
        JSONArray degree_array = (JSONArray) svm.get("degree");
        JSONArray gamma_array = (JSONArray) svm.get("gamma");
        JSONArray coef_array = (JSONArray) svm.get("coef0");
        Boolean shrinking = Boolean.parseBoolean((String) svm.get("shrinking"));
        Double tol = (Double) svm.get("tol");
        Long cache_size = (Long) svm.get("cache_size");
        Integer max_iter = (Integer) svm.get("max_iter");

        JSONArray result = new JSONArray();
        for (Object c : c_array) {
            for (Object e : e_array) {
                for (Object kernel : kernel_array) {
                    for (Object degree : degree_array) {
                        for (Object gamma : gamma_array) {
                            for (Object coef0 : coef_array) {
                                JSONObject obj = new JSONObject();
                                obj.put("algorithm", "SVM");
                                obj.put("C", c);
                                obj.put("epsilon", e);
                                obj.put("kernel", kernel);
                                obj.put("degree", degree);
                                obj.put("gamma", gamma);
                                obj.put("coef0", coef0);
                                obj.put("shrinking", shrinking);
                                obj.put("tol", tol);
                                obj.put("cache_size", cache_size);
                                obj.put("max_iter", max_iter);
                                result.add(obj);
                            }
                        }
                    }
                }
            }
        }
        return result;
    }

    private static JSONArray createLRJobs(JSONObject lr) {
        Boolean normalize = Boolean.parseBoolean((String) lr.get("normalize"));
        Boolean fit_intercept = Boolean.parseBoolean((String) lr.get("normalize"));
        JSONArray result = new JSONArray();
        JSONObject obj = new JSONObject();
        obj.put("algorithm", "LR");
        obj.put("normalize", normalize);
        obj.put("fit_intercept", fit_intercept);
        result.add(obj);
        return result;
    }

    private static JSONArray createNNJobs(JSONObject nn) {
        return new JSONArray();
    }

    public static final class OnWorkers implements FlatMapFunction<String, String> {
        /**
         * serial uid.
         */
        public static final long serialVersionUID = 1L;

        @Override
        public void flatMap(String value, final Collector<String> out) {

            String res = "Worker res: ";
            try {
                Runtime rt = Runtime.getRuntime();
                String cmd = "python";
                // TODO: check path
                String pythonPath = "../../../sose17-small-data/python/traffic-prediction/src/flink/trainModel.py";
                value = value.replaceAll("\"", "?");

                //TODO: activate correct environment
                //rt.exec("activate dataScience");
                Process proc = rt.exec(new String[]{cmd, pythonPath, value});

                BufferedReader stdInput = new BufferedReader(new InputStreamReader(proc.getInputStream()));
                BufferedReader stdError = new BufferedReader(new InputStreamReader(proc.getErrorStream()));

                // read the output from the command
                //System.out.println("----Here is the standard output of the command:\n");
                String s = null;
                while ((s = stdInput.readLine()) != null) {
                    System.out.println(s);
                    res += "\nvalue: " + value + " " + s;
                }

                // read any errors from the attempted command
                //System.out.println("----Here is the standard error of the command (if any):\n");
                while ((s = stdError.readLine()) != null) {
                    System.out.println(s);
                    res += "\n" + s;
                }

            } catch (Exception e) {
                System.out.println(e);
            }
            out.collect(res);
        }
    }

    public static String sendResultPostToBackend(JSONObject resultJSON) {
        HttpClient httpClient = HttpClientBuilder.create().build(); //Use this instead
        String jsonString = resultJSON.toJSONString();
        String serverResponse = "error";

        try {

            HttpPost request = new HttpPost("http://sambahost.dyndns.lrz.de:8500/save_result");
            StringEntity se = new StringEntity("details={\"name\":\"myname\",\"age\":\"20\"} ");
            //StringEntity se = new StringEntity(jsonString);
            request.addHeader("content-type", "application/json");
            request.setEntity(se);
            HttpResponse response = httpClient.execute(request);
            serverResponse = response.toString();
            //handle response here...

        } catch (Exception ex) {

            //handle exception here
            serverResponse = ex.toString();
        } finally {
            //Deprecated
            //httpClient.getConnectionManager().shutdown();
        }
        return serverResponse;
    }
}
