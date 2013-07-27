Date: 2013-07-27
Title: Introducing Verbal, a Ruby Gem
Category: Software
Tags: ruby

I recently released [Verbal][github], a ruby gem that provides a fluent
DSL for creating regular expressions. It's a fork of jehna's popular
[VerbalExpressions][jehna] javascript library. Detailed documentation and code
examples are available at [rubydoc.info][rubydoc].

To create a regular expression that matches `http`, `https`, `ftp`, and `sftp`,
one can use Verbal as follows:

    :::ruby
    verbal = Verbal.new do
      find 'http'
      maybe 's'
      find '://'
      otherwise
      maybe 's'
      find 'ftp://'
    end

Note that `verbal` just a regular expression.

    :::ruby
    verbal =~ 'http://' # => 0

Capturing groups may be specified using `capture`. For example,

    :::ruby
    verbal = Verbal.new do
      capture { anything }
      find /\sby\s/
      capture { anything }
    end
    data = verbal.match('this is it by michael jackson')
    data[1] # => "this is it"

More examples can be found in the [RSpec specs][specs].

  [github]: https://rubygems.org/gems/verbal
  [jehna]: https://github.com/jehna/VerbalExpressions
  [rubydoc]: http://rubydoc.info/gems/verbal/Verbal
  [specs]: https://github.com/jimjh/verbal/tree/master/spec
