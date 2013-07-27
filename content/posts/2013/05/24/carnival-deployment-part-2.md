Date: 2013-05-24
Title: Deployment is Scary - Part 2
Category: Software
Tags: ruby, rails

The is the second installation of a series of posts about my deployment experiences with Enteract. Part 1 is available [here][part 1].

In this post, I will focus on our use of [Faraday][faraday] and [Upstart][upstart] for some simple monitoring.

## Faraday
We wanted a tool to monitor the web application and notify a member of the team should the web application be unreachable or defaced. The first requirement was relatively simple, and can be easily satisfied by using Amazon's Elastic Load Balancer with the [health check][health check] gem for Rails.

The second requirement was slightly trickier, and I wrote a ruby script using Faraday that periodically

- visits the sign in page,
- signs in,
- visits the home page,
- ensures that the names of all 24 entries exist on the page, and
- notifies the team, via text messages, should any of the assertions fail.

(On hindsight, it would have been much easier to use Capybara or JMeter for this purpose; I was using this as an excuse to learn how to use Faraday and Amazon's [Simple Notification Service][sns].)

I uploaded a [gist][ipads] of the relevant script with the sensitive information redacted. The only tricky part was retrieving the CSRF token and preserving cookie information between requests.

## Upstart
Next, I wanted to some reasonably reliable way to ensure that the monitoring process is alive - it wouldn't be a very useful monitoring tool if the process terminates prematurely. For this we used Upstart, an event-based init daemon that supervises the process and restarts it if it terminates.

The configuration file that worked for me is as follows:

<script src="https://gist.github.com/jimjh/5646473.js"></script>

There is probably an easier to set this up that uses a shorter command.


  [part 1]: http://blog.jimjh.com/deployment-is-scary-part-1.html
  [faraday]: https://github.com/lostisland/faraday
  [upstart]: http://upstart.ubuntu.com/
  [health check]: https://github.com/ianheggie/health_check
  [sns]: http://aws.amazon.com/sns/
  [ipads]: https://gist.github.com/jimjh/5646333