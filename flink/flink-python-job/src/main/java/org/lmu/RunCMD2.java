package org.lmu;

import org.apache.avro.data.Json;
import org.apache.flink.api.java.ExecutionEnvironment;

import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.api.java.DataSet;
import org.apache.flink.util.Collector;
import org.lmu.JSON.JSONArray;
import org.lmu.JSON.JSONObject;
import org.lmu.JSON.parser.JSONParser;
import org.mortbay.util.ajax.JSON;


import java.io.FileReader;
import java.util.Locale;
import java.util.*;


import java.io.BufferedReader;
import java.io.InputStreamReader;

public class RunCMD2 {
	
	/** private constructor. */
    private RunCMD2() { }

	public static void main(String[] args) throws Exception {
		// set up the batch execution environment
		final ExecutionEnvironment env = ExecutionEnvironment.getExecutionEnvironment();
		String jsonPath = args[0];
		JSONObject json;
		if(jsonPath!=null){
			 json = (JSONObject) new JSONParser().parse(new FileReader(jsonPath));
		}
		else{
			throw new Exception("NO JSON PATH AS INPUT");
		}

		JSONObject algorithms = (JSONObject) json.get("algorithms");
		JSONObject data = (JSONObject) json.get("data");

		JSONObject svm = (JSONObject) algorithms.get("SVM");
		JSONObject lr = (JSONObject) algorithms.get("LR");
		JSONObject nn = (JSONObject) algorithms.get("NN");

		System.out.println(lr);

		JSONArray svmArray = svm!= null ? createSVMJobs(svm) : new JSONArray();
		JSONArray lrArray = lr != null ? createLRJobs(svm) : new JSONArray();
		JSONArray nnArray = nn != null ? createNNJobs(svm) : new JSONArray();

		if(args.length > 0){
			System.out.println("----args:" + args[0]);
		}else{
			System.out.println("----args: none");
		}

		// DataSet<String> text = env.readTextFile("path/to/file");
		// get input data
		ArrayList<String> tasks = new ArrayList<>();
		fillList(data, svmArray, tasks);
		fillList(data, lrArray, tasks);
		fillList(data, nnArray, tasks);

		DataSet<String> elementsDataSet = env.fromCollection(tasks);
		DataSet<String> res = elementsDataSet.flatMap(new OnWorkers());
		// text.writeAsCsv(outputPath, "\n", " ");


		// execute program
		//env.execute("Flink Batch RunCMD Job");
		
		// execute and print result
        res.print();
	}

	private static void fillList(JSONObject data, JSONArray array, ArrayList<String> tasks) {
		for(Object obj : array){
			obj = new JSONObject((JSONObject)obj);
			((JSONObject) obj).put("data", data);
			tasks.add(obj.toString());
			System.out.println(obj);
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
		//for(int i = 0; i < cParams.size(); i++){
		//	for(int j = 0; j< eParams.size(); j++){
		//		Long c = (Long)cParams.get(i);
		//		Double e = (Double)eParams.get(j);
				JSONObject obj = new JSONObject();
		obj.put("algorithm", "LR");
		obj.put("normalize", normalize);
		//obj.put("E", e);
		result.add(obj);
		System.out.println(result);
		//	}
		//}
		return result;
	}

	private static JSONArray createNNJobs(JSONObject nn) {
    	return new JSONArray();
	}

	public static final class OnWorkers
            implements FlatMapFunction<String, String>{


        /** serial uid. */
        public static final long serialVersionUID = 1L;

        @Override
        public void flatMap(final String value, final Collector<String> out) {
			
			try{									
			Runtime rt = Runtime.getRuntime();
			String[] commands = {"system.exe","-get t"};
			String cmd1 = "pwd";

			// path depends on the folder where the command of flink run was called
			String cmd2 = "python3 ../BigDataScience/sose17-small-data/python/traffic-prediction/src/flink/mysklearntest.py";

			
			Process proc = rt.exec(cmd2);

			BufferedReader stdInput = new BufferedReader(new
					InputStreamReader(proc.getInputStream()));

			BufferedReader stdError = new BufferedReader(new
					InputStreamReader(proc.getErrorStream()));


			
			String res = "";
			
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
			} catch(Exception e){
				
			}
			
			/*
            // normalize and split the line
            String[] tokens = value.toLowerCase(Locale.US).split("\\W+");

            // emit the pairs
            for (String token : tokens) {
                if (token.length() > 0) {
                    out.collect(new Tuple2<String, Integer>(token, 1));
                }
            }
            */
            
        }
    }
	
	
	
}
