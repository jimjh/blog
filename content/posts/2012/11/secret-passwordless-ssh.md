Date: 2012-11-08
Title: Passwordless Kerberized SSH for CMU's UNIX machines
Category: Software
Tags: ssh, kerberos, unix, cmu

If you use SSH frequently to access `unix.andrew.cmu.edu`, you must have tried at some point to set up [passwordless login][ssh] using public/private keys. That didn't work for me, and when I did `ssh -vv unix.andrew.cmu.edu`, it always failed at

	debug2: we did not send a packet, disable method

and then asked me for a password. After _much_ trial and error (including locking myself out of my account), I finally uncovered the secret.

**Note: this tutorial is for Mac OS X only, although you might be able to
configure a similar setup on Linux.**

## Setup A Few Things
First, let's get a basic things out of the way. These are optional, but I will assume that you have these for the rest of the tutorial.

1. Download and install Mac OS X Kerberos Extras from [MIT][mit].
2. Setup a default SSH user for the `unix.andrew.cmu.edu` domain, by ensuring that there is a file at `~/.ssh/config` that contains the following:

`~/.ssh/config`

    :::aconf
    Host unix.andrew.cmu.edu
    	User your_andrew_ID

## Configure Kerberos
Instead of using public/private keys for passwordless login, we will use kerberos tickets.

First, copy the configuration file from the UNIX machines to your local machine.

	:::bash
	$> scp unix.andrew.cmu.edu:/etc/krb5.conf krb5.conf
	$> sudo mv krb5.conf /etc/krb5.conf

Next, try to obtain a kerberos ticket for your andrew account, then try to login.

	:::bash
	$> kinit my_andrew_id@ANDREW.CMU.EDU
	# enter your password when prompted ...
	$> ssh unix.andrew.cmu.edu

The last step should succeed without asking you for your password.

## Renew Daily
Once you have completed the above configuration, at the start of each day, issue the following command:

	:::bash
	$> kinit my_andrew_id@ANDREW.CMU.EDU
	# enter your password when prompted ...

And you should be able to ssh into `unix.andrew.cmu.edu` for the rest of the day without a password. The tickets expire after 11 hours.

## Store Password in Keychain Access
If you like, you can keep your password in keychain access by using the following command:

	:::bash
	$> security add-generic-password -a "my_andrew_id" \
		-s "ANDREW.CMU.EDU" \
		-w "mypasswd" \
		-c "aapl" \
		-T "/usr/bin/kinit"

Entering passwords in plain text on the command line may scare some people. You can leave that out and enter it manually in the KeyChain Access app.

Once that is done, `kinit` will get your password from KeyChain Access automatically.

## Done!
Now you can `git pull` and `git push` like a pro without that pesky password prompt.

## Advanced: Auto-Renewal
There might be a way for you to [automatically renew][forum] kerberos tickets when they expire. It's not too annoying for me to enter my password once a day, so I will leave that to you.

  [ssh]: http://osxdaily.com/2012/05/25/how-to-set-up-a-password-less-ssh-login/
  [mit]: http://web.mit.edu/macdev/www/osx-kerberos-extras.html
  [forum]: http://www.linuxquestions.org/questions/linux-software-2/automatic-renewal-of-kerberos-tickets-792305/

