export MR_OUTPUT=s3a://<output-bucket>/output-data
hadoop fs -rm -r $MR_OUTPUT

hadoop jar "$HADOOP_MAPRED_HOME"/hadoop-streaming.jar \
-Dmapred.job.name='Taxi map-reduce job' \
-Dmapred.reduce.tasks=1 \
-Dmapreduce.map.memory.mb=1024 \
-file /tmp/mapreduce/mapper.py -mapper /tmp/mapreduce/mapper.py \
-file /tmp/mapreduce/reducer.py -reducer /tmp/mapreduce/reducer.py \
-input s3a://<input-bucket>/2020 -output $MR_OUTPUT

hadoop fs -cat s3a://<output-bucket>/output-data/part-0000* | sort -t, -k2,2 -k1,1 > result.csv