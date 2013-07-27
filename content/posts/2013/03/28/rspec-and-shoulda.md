Date: 2013-03-28
Title: Some Custom Matchers for RSpec with Shoulda
Category: Software
Tags: ruby, rspec, shoulda, factory_girl

### It should have a valid factory

I use [Factory Girl][factory girl] in my tests, and I have found it useful to
check that I have valid factories for each model in my tests/specs. Here is a
matcher you can use for that purpose.

<script src="https://gist.github.com/jimjh/5263666.js"></script>

Add this file to `spec/support`. Then in your specs, just use

    :::ruby
    describe User do
      it { should have_a_valid_factory }
    end

### It should validate the existence of X

In some of my models, I have validations that ensure existence of a given
foreign key _i.e._ the foreign key must refer to an existing record. You can
use the [validates_existence][validates_existence] gem, or write your own. Here
is a matcher for `validates_existence_of`.

<script src="https://gist.github.com/jimjh/5230194.js"></script>

In your specs, just use

    :::ruby
    describe Membership do
      it { should validate_existence_of :user }
    end


  [factory girl]: https://github.com/thoughtbot/factory_girl
  [validates_existence]: https://github.com/perfectline/validates_existence
