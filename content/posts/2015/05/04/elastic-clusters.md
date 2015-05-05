Date: 2015-05-04
Title: Building Elastic Clusters
Category: Software
Tags: distributed, devops

(Authors: Jim Lim, [Adam Gray])

One of the main advantages of using a cloud provider, such as Amazon Web
Services (AWS), is the ability to launch new instances on demand. However, it
also means giving up control over physical machines and their retirement
schedules; the cloud provider may terminate or retire a VM at any time for many
reasons. As a business grows, the probability that one of our many VMs
terminates on any given day increases, and it can rapidly become uneconomical
to manually administer these instances.

The answer to this problem is automation - distributed systems should recover
from failures and grow automatically.

At Quixey, we depend on distributed systems such as Zookeeper, Kafka, and
Cassandra in various critical parts of our infrastructure e.g. service
discovery, instrumentation, and storage for app-tier services. To ensure that
these foundational services can respond to traffic spikes and VM retirement
events, we have put in much effort into [cluster elasticity].

## Making Kafka Elastic

Kafka is a distributed message system. Our Kafka clusters are configured with
default [replication factor] of 3 and a fixed number of [partitions] for each
topic. In most cases, the clusters can tolerate up to 2 failures: at least one
of the 3 replicas has to remain available.

On AWS, Quixey uses [Auto Scaling Groups] (ASG) to manage our Kafka clusters.
Each ASG is configured with a lower bound on the the number of instances, and a
scaling policy to increase the size of the cluster when necessary. When
instances are terminated, or when certain CloudWatch metrics (e.g. network I/O,
disk use) exceed their configured thresholds, new EC2 instances are launched.

When a new instance is launched, it requests for a new broker ID using a tool
called Bumper. Bumper increments an atomic integer on Zookeeper and copies it
to a file on disk for use as the broker ID. Our provisioning tool then installs
Kafka, starts the service, and runs a tool called Balancer. Balancer iterates
through a list of strategies to determine the partitions to reassign to the new
broker, such as under-replicated partitions. A different set of strategies can
be written for each cloud; on AWS, for example, we are concerned about
availability zone (AZ) outages, and want to ensure that each partition is
replicated over multiple AZs.

The above solution has been tested in production, and works reasonably well. We
are working on Balancer strategies to automatically increase the number of
partitions for heavy topics, so that their messages can be spread over more
instances.

## Making Zookeeper Elastic

Zookeeper is a coordination service. It uses [ZAB] for replication, which
requires a quorum of servers to be up to remain available. For example, if we
have 3 nodes in the ensemble, we can afford to lose up to one of them.

Managing Zookeeper is slightly trickier than managing Kafka:  each Zookeeper
server needs to have the entire list of server IDs and address/port combos. Any
change to the set of members requires the administrator to update the
configuration files across the ensemble and perform a [rolling restart]. We tried
various solutions, and ended up using Netflix’s [Exhibitor]. Exhibitor is not as
mature as Zookeeper and has some rough edges, but we got it to do what we
wanted with a few slight modifications.

It works as follows: Exhibitor maintains a shared configuration on S3 or [OSS],
and each instance in the cluster runs a pair of Exhibitor and Zookeeper
processes. Each Exhibitor process polls the shared configuration for changes,
and triggers a rolling restart when the list of members in the shared
configuration is updated.

In the event of an instance failure/termination, the relevant ASG launches a
replacement instance, which obtains a new identifier and adds itself to the
shared configuration. The Exhibitor processes will detect the change and
trigger a rolling restart across the ensemble to keep the configurations in
sync. Note that Exhibitor’s polling frequency is configurable.

Currently, the Zookeeper ASGs are configured to maintain the ensemble at a
fixed size; we intend to create policies that will increase the number of
[observers] as the number of clients grows to improve read performance.

## Enforcing Discipline

Modern Internet operations practices shrug off constraints on the uptime of any
specific single server by making all servers “trashable.” Working in the cloud
with on-demand instances allows us to terminate instances at the first sign of
trouble, such as [noisy neighbors] or hardware degradation. We can even do this
automatically when a server fails a health check for the service it is
providing (e.g. we cannot produce and consume a message in Kafka using that
server).

In an ideal deployment, humans should be paged only in extraordinary and
unexpected situations. Instance termination and traffic spikes are expected,
and should be handled by automation tools. This helps us focus more on
throughput and overall uptime and less on diagnosing individual problems. To
prevent future reoccurrences of issues, logs can be copied to S3/OSS for
post-mortem analysis of the system as a whole, rather than a case-by-case
examination of the nitty-gritty details.

As organizations mature and grow, they can no longer afford to handcraft and
tend to each [pet instance]. The realities of cloud services, such as VM
terminations and noisy neighbors, prod us to invest time into configuration
automation and make sure that every instance is [reproducible]. Such discipline
can be enforced by terminating instances regularly and exercising the
automation scripts to prevent configuration drift, but that’s a topic for
another post.

  [Adam Gray]: http://addumb.com/
  [cluster elasticity]: http://en.wikipedia.org/wiki/Elasticity_(data_store)#Clustering_elasticity
  [replication factor]: http://kafka.apache.org/documentation.html#replication
  [partitions]: http://kafka.apache.org/documentation.html#introduction
  [Auto Scaling Groups]: http://aws.amazon.com/autoscaling/
  [ZAB]: http://web.stanford.edu/class/cs347/reading/zab.pdf
  [rolling restart]: https://issues.apache.org/jira/browse/ZOOKEEPER-107
  [Exhibitor]: https://github.com/Netflix/exhibitor
  [OSS]: http://www.aliyun.com/product/oss/
  [observers]: http://zookeeper.apache.org/doc/r3.4.5/zookeeperObservers.html
  [noisy neighbors]: http://en.wikipedia.org/wiki/Cloud_computing_issues#Performance_interference_and_noisy_neighbors
  [pet instance]: https://blog.engineyard.com/2014/pets-vs-cattle
  [reproducible]: http://martinfowler.com/bliki/PhoenixServer.html
