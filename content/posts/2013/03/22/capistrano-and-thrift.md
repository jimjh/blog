Date: 2013-03-20
Title: Deploying a Thrift Server with Capistrano
Category: Software
Tags: ruby, thrift, capistrano

At the time of writing, I couldn't find an existing [Capistrano][capistrano]
recipe for deploying [thrift][thrift] servers. So [here][github] is an example
that works with ubuntu.

Before you use the recipe, don't forget to update the configuration options to
match your server setup. At the very least, you will need to update the
following:

- `:application`
- `:repository`
- `:user`
- `:super_user`
- `:app_port`
- `role :app`

Note that the recipe assumes a system-wide rvm install. `:user` does not need
to be a sudoer, but `:super_user` must be. This is arranged as such for
security purposes, since the server process will be owned by `:user`. The super
user is used to create the Upstart job.

Finally, execute

    :::bash
    $ cap deploy:setup
    $ cap deploy

to setup and deploy your thrift server.

## Upstart

During `cap deploy:setup`, the recipe creates an Upstart job using the template
at [config/thrift_app.conf][config]. This allows Upstart to launch and monitor your
thrift server. You can use other monitoring tools if you like. Just update the
`deploy:setup` task appropriately.

## Thor

To play with the Thrift server, launch it as follows:

    :::bash
    $ bundle exec bin/my-application server

Then create a new client as follows:

    :::bash
    $ bundle exec bin/my-application client
    > ping
    pong!

  [capistrano]: http://capistranorb.com/
  [thrift]: http://thrift.apache.org/
  [github]: https://github.com/jimjh/capistrano-thrift-example
  [config]: https://github.com/jimjh/capistrano-thrift-example/blob/master/config/thrift_app.conf

