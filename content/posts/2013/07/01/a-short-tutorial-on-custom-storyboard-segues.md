Date: 2013-07-01
Title: A Short Tutorial on Custom Storyboard Segues
Category: Software
Tags: ios, storyboards, segues

_This is a repost from my old blog._

We will use the [last tutorial][cmu] as a base to learn how to use custom segues.

Suppose you don't want to _push_ between view controllers. In particular,
suppose you want first view controller to _flip_ to the second view controller.
To achieve this, you need a [custom segue][custom].

Create a new Objective-C class in the StoryboardDemo2 project with the name
`JHCustomSegue.m` and let it be a subclass of `UIStoryboardSegue`. Open up
`JHCustomSegue.m` and add the following code:

    :::objective-c
    - (void) perform {
        UIViewController *src = (UIViewController *) self.sourceViewController;
        UIViewController *dst = (UIViewController *) self.destinationViewController;
        [UIView transitionWithView:src.navigationController.view duration:0.2
                           options:UIViewAnimationOptionTransitionFlipFromLeft
                        animations:^{
                            [src.navigationController pushViewController:dst animated:NO];
                             }
                        completion:NULL];
    }

Next, open up the storyboard in XCode and click on the _segue_. In other words,
click on the arrow pointing from the first view controller to the second view
controller.

![Segue](|static|/images/2013/07/01/braces.png)

Hit `Alt+Cmd+0` to open up the Utilities pane. Navigate to the Attributes
Inspector, choose `Custom` for _Style_ and input `JHCustomSegue` for _Segue Class_.

![Inspector](|static|/images/2013/07/01/inspector.png)

Now, run your app in the simulator. You should be able to flip from the first
view controller to the second by tapping on the button at the top right-hand
corner.

  [cmu]: http://www.cmumobileapps.com/2011/10/25/a-really-short-tutorial-on-storyboards/
  [custom]: https://developer.apple.com/library/ios/#documentation/UIKit/Reference/UIStoryboardSegue_Class/Reference/Reference.html#//apple_ref/doc/uid/TP40010911
