Date: 2014-10-29
Title: dragon - an OSS File System for Hadoop
Category: Software
Tags: hadoop, oss

OSS is Aliyun’s offering of a distributed, highly available storage service.
dragon allows YARN applications (incl. MapReduce jobs) to read and write data
to OSS through the HDFS API. This allows you to swap filesystems without
modifying your YARN application, MapReduce job, Pig script, Hive script etc.

The source code is available [on GitHub](https://github.com/quixey/dragon-oss).
The dragon jar may be built using

    ./gradlew jar

dragon’s dependencies may be downloaded using

    ./gradlew copyDeps

To use dragon in your Hadoop cluster, add dragon and its dependencies to
Hadoop’s classpath on our clusters. Then modify core-site.xml to add the
following properties

    <property>
        <name>fs.oss.impl</name>
        <value>com.quixey.hadoop.fs.oss.OSSFileSystem</value>
    </property>
    <property>
        <name>fs.oss.accessKeyId</name>
        <value>...</value>
    </property>
    <property>
        <name>fs.oss.secretAccessKey</name>
        <value>...</value>
  </property>

This tells the Hadoop clients to use the dragon implementation of HDFS for all
URIs with the `oss://` scheme.

You may verify that your setup works by running the following command

    hdfs dfs -ls oss://your-bucket/
