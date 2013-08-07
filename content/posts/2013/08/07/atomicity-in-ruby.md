Date: 2013-08-07
Title: Atomicity in Ruby
Category: Software
Tags: ruby, concurrency

While reading foreman's source code, I noticed that it was using deferred
signal handling, as follows:

    :::ruby
    trap(sig) { Thread.main[:signal_queue] << sig ; notice_signal }

It's important to note that the append operation `<<` is not atomic. In other
words, while `sig` is being appended to `:signal_queue`, another signal could
come in, interrupting the operation. In this particular case, the order of
signals would be affected, but that doesn't hurt the grand scheme of things.

This piqued my curiosity about atomicity in Ruby. Using a simple Mutex would
not work, since signals can interrupt synchronized code. The [atomic
gem][atomic] seems like a good start, but I wonder if there are any operations
in Ruby that are guaranteed to be atomic. I posted a [question on
StackOverflow][so], and will update this post as answers come in.

  [so]: http://stackoverflow.com/questions/18113522/are-there-any-operations-methods-in-ruby-that-are-guaranteed-documented-to-be-at
  [atomic]: https://github.com/headius/ruby-atomic
