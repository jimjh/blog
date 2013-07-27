Date: 2013-07-01
Title: Implementing a Singleton in iOS
Category: Software
Tags: cocoa, ios

_This is a repost from my old blog._

While I was at Apple’s Cocoa Camp over summer, one of the speakers talked
rather passionately about the proper, thread-safe way to implement a singleton
in iOS, which I thought deserves more attention than it currently does on the
[Web](https://encrypted.google.com/search?q=ios+singleton&ie=utf-8&oe=utf-8&aq=t).

## The Common Way
According to the [first result][john] on my Google search, a singleton should
be implemented as follows:

    :::objective-c
    static SingletonClass *sharedInstance = nil;

    // Get the shared instance and create it if necessary.
    + (SingletonClass*)sharedInstance {
        if (sharedInstance == nil) {
            sharedInstance = [[super allocWithZone:NULL] init];
        }

        return sharedInstance;
    }

Although this method is quick and easy, it is not thread-safe and the object constructor might be called multiple times if several threads access the method concurrently. We need a way to lock the constructor and insist that it be executed at most once. This is where [Grand Central Dispatch][gdc] comes in.

## The ~Troublesome~ Thread-safe Way

GCD provides a neat API that makes concurrency programming in Cocoa convenient.
To implement a thread-safe singleton in Cocoa, all you need to do is the
following:

    :::objective-c
    static MyObject *singleton = nil;

    +(MyObject *) sharedInstance {

        NSLog (@"sharedInstance called.");

        if (nil != singleton) return singleton;
        static dispatch_once_t pred;        // lock
        dispatch_once(&pred, ^{             // this code is at most once
            singleton = [[MyObject alloc] init];
        });

        return singleton;

    }

Let’s look at the code in detail. First, notice that the first few lines are
the same: we have a static variable for our singleton, and we check whether it
is nil whenever we access `sharedInstance`. If `singleton` is `nil`, allocate and
initialize it; otherwise, return it.

The real difference is where we use the `dispatch_*` types and functions. You may
think of `dispatch_once_t` as a type of lock that `dispatch_once()` uses to ensure
that the code is executed at most once. Here, we wrap up whatever code we wish
to be executed during the initialization of our singleton in a block. We then
pass the block as an argument to `dispatch_once`. (Here's a pretty good tutorial
on [blocks].)

This implementation ensures that singleton is never executed more than once
even when multiple threads access `sharedInstance` concurrently:

    :::objective-c
    dispatch_queue_t queue = dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0U);

    dispatch_apply(10, queue, ^(size_t i){
      [MyObject sharedInstance];
    });

The above code results in the following output:

```
2011-09-05 10:12:05.961 SingletonTest[1602:10c03] sharedInstance called.
2011-09-05 10:12:05.961 SingletonTest[1602:12603] sharedInstance called.
2011-09-05 10:12:05.961 SingletonTest[1602:ef03] sharedInstance called.
2011-09-05 10:12:05.961 SingletonTest[1602:12703] sharedInstance called.
2011-09-05 10:12:05.966 SingletonTest[1602:10c03] init called.
2011-09-05 10:12:05.966 SingletonTest[1602:ef03] sharedInstance called.
2011-09-05 10:12:05.966 SingletonTest[1602:10c03] sharedInstance called.
2011-09-05 10:12:05.966 SingletonTest[1602:12703] sharedInstance called.
2011-09-05 10:12:05.966 SingletonTest[1602:12603] sharedInstance called.
2011-09-05 10:12:05.969 SingletonTest[1602:10c03] sharedInstance called.
2011-09-05 10:12:05.969 SingletonTest[1602:ef03] sharedInstance called.
```

  [john]: http://www.johnwordsworth.com/2010/04/iphone-code-snippet-the-singleton-pattern/
  [gdc]:  http://developer.apple.com/library/ios/#documentation/Performance/Reference/GCD_libdispatch_Ref/Reference/reference.html#//apple_ref/c/func/dispatch_apply
  [blocks]: http://pragmaticstudio.com/blog/2010/7/28/ios4-blocks-1
