Date: 2014-03-30
Title: Stripe CTF 2014, Level 2 - Defending against a DDOS attack
Category: Software
Tags: nodejs, stripe


If your service comes under a major DDOS attack, what would you do?

In the third level of Stripe’s CTF, participants were tasked to build a proxy
to defend a couple of backend servers against a DDOS attack. The proxy needed
to do the following:

- distribute requests across a number of backend servers
- reject requests from attackers

Here is an [easy solution](https://github.com/jimjh/stripe-level2) - track the
number of requests coming from each IP address, and, with each request, update
the mean and standard deviation. Then, assuming a normal distribution,
calculate the z-score for each IP address. If the z-score is larger than some
tolerance figure, block the IP address.  (Determining the tolerance figure
requires some trial-and-error.)

Here is a [cooler solution](https://github.com/jimjh/stripe-level2/tree/nginx)
- download and build nginx, and use it to forward requests to the backend
servers. Finally, adjust the parameters in the nginx configuration, using the
`limit_req` module to handle bursts and block elephants.
