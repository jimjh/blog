Date: 2013-07-30
Title: Thoughts from Reading Code - Foreman: Part 1
Category: Software
Tags: ruby, reading

I read a lot of open source code in my free time to make myself a better engineer. Here are some of my notes from reading foreman's [cli.rb](https://github.com/ddollar/foreman/blob/master/lib/foreman/cli.rb).

### Code Style - Raising Exceptions with a Bang

You might occasionally encounter code that looks like this:

    :::ruby
    def start(process=nil)
      raise MyException, 'oops' unless some_condition
      if some_other_condition
        puts "meaningful error message"
        raise AnotherException, 'oops'
      end
      do_something_useful
      do_some_other_useful_thing
    end
    
This seems perfectly normal - `start` validates a few conditions (possibly derived from the context or environment), and decides if it is OK to continue with the operation. However, such validations get in the way of readability, and are often duplicated in other methods. To keep things SOLID and DRY, let's extract these out into private methods.

    :::ruby
    def start(process=nil)
      check_some_condition
      check_some_other_condition
      do_something_useful
      do_some_other_useful_thing
    end
    
Much better. The code is a lot easier to read, but the helper methods have masked their side effects. (In this case, exceptions are raised and output is printed when some conditions are not met.) This can be confusing as the code base grows and becomes more complicated. A new team member would take a longer time to go through the code and learn that the `check_*` methods have potential side effects. To fix this, let's add a `!` to the end of their names.

    :::ruby
    def start(process=nil)
      check_some_condition!
      check_some_other_condition!
      do_something_useful
      do_some_other_useful_thing
    end
    
With this edit, the `start` method's purpose and operations become immediately apparent.

### Technique - Loading Configuration Files

Using Thor, one can easily create a command-line interface by defining options for tasks and accessing arguments via the `options` hash. For example,

    :::ruby
    method_option :color, type: :boolean
    def start()
      # …
    end
    
adds a `start` task that accepts a `--color` option. It is often useful to allow the user to specify frequently used configuration options with a configuration file, such as `.rspec` and `.yardopts`. With Thor, the `options` getter method provides a convenient place to merge options from the configuration file and from the command-line.

    :::ruby
    def options
      original = super                                 # get original options hash
      return original unless File.exists? CONFIG_FILE
      defaults = ::YAML::load_file(CONFIG_FILE) || {}  # read from config file
      defaults.merge(original)                         # merge
    end

Note that options provided on the command-line override the options given in the configuration file.