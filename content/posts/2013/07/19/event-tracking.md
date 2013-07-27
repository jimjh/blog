Date: 2013-07-19
Title: Event Tracking with Google Analytics and LaunchRock
Category: Analytics
Tags: javascript, analytics

It's easy to create a landing page with LaunchRock, but getting meaningful analytics out of it is more difficult. For example, I still have not figured out a way to run a Google Analytics experiment on LaunchRock - using custom Javascript code in LaunchRock sometimes crashes the previewer, forcing me to reset my project.

## Event Tracking
Anyway, back to event tracking. Open up the advanced editor, and use the following gist

<script src="https://gist.github.com/jimjh/6039414.js"></script>

A few subtle points:

- The conventional way using `_gaq.push` does not work because LaunchRock has its own `_gaq` global variable that reports to their Analytics account instead of yours.
- This tracks the keypresses and button clicks, but does not actually know if the user really signed up. For example, the user could have given an invalid email address.

To test this, watch the _Realtime_ dashboard in your Analytics account while you create a few fake signups on your landing page. The events count should increase for the _Sign Up_ action of the _Users_ category.

Once event tracking is in place, it is simple to create a goal for the event and link it to your Adwords campaign.