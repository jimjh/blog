Date: 2013-07-01
Title: Using Karma with Rails and Jenkins: Part 1
Category: Software
Tags: rails, ruby, karma, jenkins

In a recent project, I experimented with [AngularJS](http://angularjs.org) on
Rails, and managed to get [Karma][karma] to work nicely with Jenkins on
[CloudBees][cb]. This post documents the steps I took. (Part 2
will cover e2e tests, if I get that sorted out.)

An example project is available on [GitHub](https://github.com/jimjh/karma-rails).

## Setup

First, install karma locally with

    $> npm install karma

Then install angular and jquery at the following locations:

- `vendor/assets/javascripts/jquery-1.10.1.min.js`
- `vendor/assets/javascripts/angular/angular.min.js`

Note that these are necessary even if you are using a CDN for these libraries.
This ensures that your unit tests pass even without network access.

Next, setup the spec directories,

    $> mkdir -p spec/javascripts/lib/angular
    $> mkdir -p spec/javascripts/unit

If you expect to use mocks in your unit tests, install `angular-mocks.js` at
`spec/javascripts/lib/angular/angular-mocks.js`.

Finally, create a karma configuration file with the following gist

<script src="https://gist.github.com/jimjh/5904291.js"></script>

I am not perfectly satisfied with this solution, since it requires the developer to
manually synchronize `karma.conf.js` with `application.js`. Please let me know
in the comments if you figure out a better way.

## Testing

Save your tests in `spec/javascripts/unit`. For example,

    :::javascript
    /* spec/javascripts/unit/setup_spec.js */
    ;(function() {
      'use strict';

      describe('setup', function() {
        it('expects setup to be OK', function() {
          expect(1+1).toBe(2);
        });
      });

    })();

Run tests using

    $> karma start config/karma.conf.js

## Continuous Integration

To use Karma with Jenkins, update `karma.conf.js` to include

    junitReporter = {
      outputFile: 'spec/reports/karma-unit.xml',
      suite: 'unit'
    };

Write a script for jenkins at `script/ci`:
<script src="https://gist.github.com/jimjh/5904659.js"></script>

Lastly, configure Jenkins to execute `script/ci` and access the XML report at
`spec/reports/karma-unit.xml`.

  [karma]: http://karma-runner.github.io/0.8/index.html
  [cb]: http://cloudbees.com
