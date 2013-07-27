Date: 2012-11-02
Title: Backbone, Faye, and Reaction
Category: Software
Tags: ruby, rails, javascript, mvc

I was jealous of what MeteorJS did for NodeJS developers, and decided to steal
some of their ideas for Rails. The result is the [reaction gem][reaction], and
a demo app can be downloaded from [here][todos].

## Transparent Synchronization
Using Reaction, you write your app like a usual Backbone app. However, instead
of using `Backbone.Collection`, use `Reaction.Collection` to create a
synchronized collection.

    :::javascript
    var collection = new Reaction.Collection({
      controller_name: 'todos',
      model_name: 'todo'
    });

The collection provides a custom `sync` function that routes changes to the
conventional CRUD endpoints of the Rails application. For example, when you
invoke `collection.create({...}, {wait:true})`, it makes a POST request to the
Rails app.

When updates are _pushed_ from the Rails server to the client, the collection is
updated and `add`, `remove`, or `change` events are fired. For example, a view
may react to an `add` event as follows:

    :::javascript
    collection.bind('add', this.addOne, this);
    // ...
    addOne: function(obj) {
      $('x').append(new XView(obj).render().el);
    }

## Local HTML5 Storage
Objects in the collection are cached in the local HTML5 storage.  If the client
is online, this helps to reduce the initial time required to load the
interface; if the client is offline, this allows the collection to be
re-created from the cache, showing the user a decent (but outdated) interface.

## Separate App Server and Push Server
For scaling purposes, the app server can be separated from the push server.
This also allows multiple app servers to share the same push server. When these
servers are started, a shared secret must be provided. This secret will be used
to sign messages sent from the app servers to the push server.

If you wish to learn more, head to the [quickstart][quickstart].

  [reaction]: https://github.com/jimjh/reaction
  [todos]: https://github.com/jimjh/reaction-todos
  [quickstart]: https://github.com/jimjh/reaction/blob/master/QUICKSTART.md
