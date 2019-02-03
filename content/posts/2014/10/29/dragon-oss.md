Date: 2014-10-29
Title: dragon - an OSS File System for Hadoop
Category: Software
Tags: hadoop, oss

[OSS] is Aliyun’s offering of a distributed, highly available storage service.
[dragon] allows YARN applications (incl. MapReduce jobs) to read and write data
to OSS through the HDFS API. This allows you to swap filesystems without
modifying your YARN application, MapReduce job, Pig script, Hive script etc.

The source code is available [on GitHub](https://github.com/quixey/dragon-oss).
The dragon jar may be built using

    :::sh
    $ ./gradlew jar

dragon’s dependencies may be downloaded using

    :::sh
    $ ./gradlew copyDeps

To use dragon in your Hadoop cluster, add `dragon-*.jar` and its dependencies
to Hadoop’s classpath on your clusters. Then modify `core-site.xml` to add the
following properties:

- `fs.oss.impl`: `com.quixey.hadoop.fs.oss.OSSFileSystem`
- `fs.oss.accessKeyId`: `...`
- `fs.oss.secretAccessKey`: `...`

This tells the Hadoop clients to use the dragon implementation of HDFS for all
URIs with the `oss://` scheme.

You may verify that your setup works by running the following command:

    :::sh
    $ hdfs dfs -ls oss://your-bucket/


([dragon] is an open-source project by [Quixey].)


  [OSS]: http://www.aliyun.com/product/oss/
  [dragon]: https://github.com/quixey/dragon-oss
  [Quixey]: http://www.quixey.com/
