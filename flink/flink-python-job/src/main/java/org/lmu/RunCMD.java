package org.lmu;

import org.apache.flink.api.java.ExecutionEnvironment;
import org.apache.flink.api.java.ExecutionEnvironment;

import java.io.BufferedReader;
import java.io.InputStreamReader;

public class RunCMD {
	
	/** private constructor. */
    private RunCMD() { }

	public static void main(String[] args) throws Exception {
		// set up the batch execution environment
		final ExecutionEnvironment env = ExecutionEnvironment.getExecutionEnvironment();
		
		// DataSet<String> text = env.readTextFile("path/to/file");
		// text.writeAsCsv(outputPath, "\n", " ");

		Runtime rt = Runtime.getRuntime();
		String[] commands = {"system.exe","-get t"};
		String cmd1 = "pwd";

		// path depends on the folder where the command of flink run was called
		String cmd2 = "python ./BigDataScience/sose17-small-data/python/traffic-prediction/src/flink/mysklearntest.py";

		

		Process proc = rt.exec(cmd2);

		BufferedReader stdInput = new BufferedReader(new
                InputStreamReader(proc.getInputStream()));

		BufferedReader stdError = new BufferedReader(new
				InputStreamReader(proc.getErrorStream()));

		// read the output from the command
		System.out.println("----Here is the standard output of the command:\n");
		String s = null;
		while ((s = stdInput.readLine()) != null) {
			System.out.println(s);
		}

		// read any errors from the attempted command
		System.out.println("----Here is the standard error of the command (if any):\n");
		while ((s = stdError.readLine()) != null) {
			System.out.println(s);
		}



		// execute program
		env.execute("Flink Batch RunCMD Job");
	}
	
	
	
}
