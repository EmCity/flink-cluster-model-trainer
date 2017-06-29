package org.lmu;
import org.apache.flink.api.java.ExecutionEnvironment;
import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.api.java.DataSet;
import org.apache.flink.core.fs.FileSystem;
import org.apache.flink.util.Collector;
import org.apache.http.HttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.lmu.JSON.JSONArray;
import org.lmu.JSON.JSONObject;
import org.lmu.JSON.parser.JSONParser;
import java.io.FileReader;
import java.util.*;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import org.apache.http.client.*;
import org.apache.http.impl.client.*;

public class RunCMD2 {
	
	/** private constructor. */
    private RunCMD2() { }

	public static void main(String[] args) throws Exception {
		// set up the batch execution environment
		final ExecutionEnvironment env = ExecutionEnvironment.getExecutionEnvironment();
		JSONObject json;
		if(args.length > 0 && args[0]!=null){
			 json = (JSONObject) new JSONParser().parse(new FileReader(args[0]));
		}
		else{
			throw new Exception("NO JSON PATH AS INPUT");
		}

		JSONObject algorithms = (JSONObject) json.get("algorithms");
		JSONObject data = (JSONObject) json.get("data");
		JSONObject svm = (JSONObject) algorithms.get("SVM");
		JSONObject lr = (JSONObject) algorithms.get("LR");
		JSONObject nn = (JSONObject) algorithms.get("NN");
		JSONArray svmArray = svm!= null ? createSVMJobs(svm) : new JSONArray();
		JSONArray lrArray = lr != null ? createLRJobs(svm) : new JSONArray();
		JSONArray nnArray = nn != null ? createNNJobs(svm) : new JSONArray();

		// get input data
		ArrayList<String> tasks = new ArrayList<>();
		fillList(data, svmArray, tasks);
		fillList(data, lrArray, tasks);
		fillList(data, nnArray, tasks);

		// print tasks
		for (int i = 0; i < tasks.size(); i++) {
			System.out.println(tasks.get(i).toString());
		}

		DataSet<String> elementsDataSet = env.fromCollection(tasks);

		//distribute on workers
		DataSet<String> res = elementsDataSet.flatMap(new OnWorkers());


		//saves the result as text
		res.writeAsText("result.txt", FileSystem.WriteMode.OVERWRITE);


		// execute program
		env.execute("Flink Batch RunCMD Job");
		res.print();

		// workers are executing

		List<String> resCollect = res.collect();

		System.out.println(resCollect);


		String response = sendResultPostToBackend((JSONObject) new JSONParser().parse(tasks.get(0)));
		System.out.println("-----------" + response + "----------");

	}

	private static void fillList(JSONObject data, JSONArray array, ArrayList<String> tasks) {
		for(Object obj : array){
			obj = new JSONObject((JSONObject)obj);
			((JSONObject) obj).put("data", data);
			tasks.add(obj.toString());
		}
	}

	private static JSONArray createSVMJobs(JSONObject svm) {
		JSONArray cParams = (JSONArray) svm.get("C");
		JSONArray eParams = (JSONArray) svm.get("E");
		JSONArray result = new JSONArray();
		for(int i = 0; i < cParams.size(); i++){
			for(int j = 0; j< eParams.size(); j++){
				Long c = (Long)cParams.get(i);
				Double e = (Double)eParams.get(j);
				JSONObject obj = new JSONObject();
				obj.put("algorithm", "SVM");
				obj.put("C", c);
				obj.put("E", e);
				result.add(obj);
			}
		}
		return result;
	}

	private static JSONArray createLRJobs(JSONObject lr) {
		Boolean normalize = Boolean.parseBoolean((String)lr.get("normalize"));
		JSONArray result = new JSONArray();
		JSONObject obj = new JSONObject();
		obj.put("algorithm", "LR");
		obj.put("normalize", normalize);
		result.add(obj);
		return result;
	}

	private static JSONArray createNNJobs(JSONObject nn) {
    	return new JSONArray();
	}

	public static String sendResultPostToBackend(JSONObject resultJSON){
		HttpClient httpClient = HttpClientBuilder.create().build(); //Use this instead
		String jsonString = resultJSON.toJSONString();
		String serverResponse = "error";

		try {

			HttpPost request = new HttpPost("http://sambahost.dyndns.lrz.de:8500/save_result");
			StringEntity se =new StringEntity("details={\"name\":\"myname\",\"age\":\"20\"} ");
			//StringEntity se = new StringEntity(jsonString);
			request.addHeader("content-type", "application/json");
			request.setEntity(se);
			HttpResponse response = httpClient.execute(request);
			serverResponse = response.toString();
			//handle response here...

		}catch (Exception ex) {

			//handle exception here
			serverResponse = ex.toString();
		} finally {
			//Deprecated
			//httpClient.getConnectionManager().shutdown();
		}
		return serverResponse;
	}

	public static final class OnWorkers
            implements FlatMapFunction<String, String>{


        /** serial uid. */
        public static final long serialVersionUID = 1L;

        @Override
        public void flatMap(final String value, final Collector<String> out) {
			try{
			Runtime rt = Runtime.getRuntime();
			String cmd = "python";
			String pythonPath = "../../../sose17-small-data/python/traffic-prediction/src/flink/trainModel.py";

			// path depends on the folder where the command of flink run was called
			String cmd2 = cmd + " " + pythonPath + " " + value;
			rt.exec("source activate dataScience");
			Process proc = rt.exec(cmd2);

			BufferedReader stdInput = new BufferedReader(new InputStreamReader(proc.getInputStream()));
			BufferedReader stdError = new BufferedReader(new InputStreamReader(proc.getErrorStream()));

			String res = "blabla";
			System.out.println(res);

				// read the output from the command
			//System.out.println("----Here is the standard output of the command:\n");
			String s = null;
			while ((s = stdInput.readLine()) != null) {
				System.out.println(s);
				res += "\nvalue: "+ value + " " + s;
			}
			

			// read any errors from the attempted command
			//System.out.println("----Here is the standard error of the command (if any):\n");
			while ((s = stdError.readLine()) != null) {
				System.out.println(s);
				res += "\n"+s;
			}
			out.collect(res);

			out.close();
			} catch(Exception e){
			}
        }
    }
}
