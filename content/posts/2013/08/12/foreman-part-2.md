Date: 2013-08-12
Title: Thoughts from Reading Code - Foreman and Pipes
Category: Software
Tags: ruby, reading

### Using Pipes for Cheap IPC

A [UNIX pipe][wiki] is a unidirectional interprocess communication channel with
a read end and a write end. You have probably used pipes in the command line.
For example,

    :::bash
    $ git ls-files | xargs grep foo

This executes both commands concurrently and creates a pipe for interprocess
communication. The output from `git ls-files` is redirected to the write end of
the pipe, and the input to `xargs grep foo` is redirected from the read end.

Within foreman, pipes are used to aggregate output from the child process it
manages. A simplified structure of the code is as follows:

    :::ruby
    # single process example
    process = create_process
    reader, writer = create_pipe

    # invokes POSIX::Spawn, with STDOUT duped to the pipe
    process.run output: writer
    watch_for_output reader

### Reading from Multiple Pipes

Of course, Foreman is more useful when it's used to manage multiple processes.
Most of the above is still valid, but `watch_for_output` must be able to read
from multiple pipes concurrently. Two techniques come to mind: use separate
threads for each pipe, or use an event-based approach such as `select`. Foreman
uses the latter, because it's harder to coordinate multiple threads with signal
handlers. The former also costs more memory, since it uses a whole stack for
each thread. (For a more detailed comparison of these strategies, please refer
to [The C10K problem][1].)

Inside [Foreman::Engine][engine], `select` is used in the following way:

    :::ruby
    loop do
      io = IO.select(@readers.values, nil, nil, 30) # block until a fd is ready
      io.first.each do |reader|
        if reader.eof?
          @readers.delete_if { |key, value| value == reader }
        else
          # read from read end of pipe, send to STDOUT/log file
          output reader.gets
        end
      end
    end

### Deferring Signals

Foreman also listens for the `TERM`, `INT`, and `HUP` signals, and terminates
all child processes when one of them is received. However, it's difficult to
write reentrant signal handlers in Ruby, since developers do not have complete
control over which C functions are called. Thus, it's usually recommended to
[defer signal handling][defer] by pushing signals onto a queue and handling
them sequentially. For example,

    :::ruby
    # push signals onto a queue
    trap('INT') { some_queue << :INT }

    Thread.new do
      process_queue
    end

This presents new problems. In the `select` example above, the thread is
blocked while waiting for one or more of the file descriptors to become ready.
We need a way to interrupt the thread so that it may exit gracefully when a
signal is received. Moreover, `process_queue` needs to know when a signal has
been received, so that it does not have to poll the queue for changes. To solve
these, Foreman uses the self-pipe trick.

#### The Self-Pipe Trick

A self-pipe is a pipe that is not shared outside the process that created the
pipe. In the scenario described above, Foreman creates a self-pipe and adds it
to the list of inputs that `select` waits on.

    :::ruby
    io = IO.select([self_pipe_read] + @readers.values, nil, nil, 30)

Then, whenever `select` needs to be interrupted, a dummy value is written on
the write end of the self-pipe, causing `select` to return. The code following
`select` will have to determine if `select` has found valid input from one of
the readers, or if it was interrupted for another reason. For Foreman, it needs
to check if there are pending signals in the queue that needs to be handled.

This kills two birds with one stone.

    :::ruby
    Thread.new do
      loop do
        io = IO.select([self_pipe_read] + @readers.values, nil, nil, 30)
        process_queue
        io.first.each do |reader|
        if reader.eof?
          @readers.delete_if { |key, value| value == reader }
        else
          # read from read end of pipe, send to STDOUT/log file
          output reader.gets
        end
      end
    end


  [1]: http://www.kegel.com/c10k.html#strategies
  [wiki]: https://en.wikipedia.org/wiki/Pipeline_(Unix)
  [engine]: https://github.com/ddollar/foreman/blob/master/lib/foreman/engine.rb
  [defer]: http://blog.rubybestpractices.com/posts/ewong/016-Implementing-Signal-Handlers.html
