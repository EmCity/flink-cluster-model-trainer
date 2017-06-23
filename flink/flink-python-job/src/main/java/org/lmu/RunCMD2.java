package org.lmu;

import org.apache.flink.api.java.ExecutionEnvironment;
import org.apache.flink.api.java.ExecutionEnvironment;

import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.api.java.DataSet;
import org.apache.flink.api.java.ExecutionEnvironment;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.util.Collector;
import org.apache.flink.api.common.functions.util.ListCollector;



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
		
		if(args.length > 0){
			System.out.println("----args:" + args[0]);
		}else{
			System.out.println("----args: none");
		}
		
		
		// DataSet<String> text = env.readTextFile("path/to/file");
		// get input data
        DataSet<String> elementsDataSet = env.fromElements(
                "42", "43"
        );
		
		DataSet<String> res = elementsDataSet.flatMap(new OnWorkers());
		// text.writeAsCsv(outputPath, "\n", " ");


		// execute program
		//env.execute("Flink Batch RunCMD Job");
		
		// execute and print result
        res.print();
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
			String cmd2 = "python ../BigDataScience/sose17-small-data/python/traffic-prediction/src/flink/mysklearntest.py";

			
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
