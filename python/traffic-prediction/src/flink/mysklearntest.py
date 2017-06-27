import sys
from sklearn import svm

print('Number of args: ', len(sys.argv))
print('args: ',str(sys.argv))


X = [[0, 0],[1, 1]]
y = [0,1]

clf = svm.SVC()
clf.fit(X,y)

res = clf.predict([[2., 2.]])

print(res)

#old
######flink-1.3.0/bin/flink run -c org.myorg.quickstart.RunCMD BigDataScience/sose17-small-data/flink/flink-python-job/target/flink-python-job-0.1.jar


#flink-1.3.0/bin/flink run -c org.lmu.RunCMD2 BigDataScience/sose17-small-data/flink/flink-python-job/target/flink-python-job-0.1.jar -port 6123

#--jobmanager localhost:6123
#--parallelism 1

#in sose.../flink
#mvn clean install -Pbuild-jar
#or
#mvn clean package
