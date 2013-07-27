Date: 2013-07-11
Title: jQuery Plugin - Box Lid Menu
Category: Software
Tags: javascript, jquery, css

Smashing Magazine wrote [a piece][smashing] about [Toybox][toybox]'s navigation menu today, describing the user experience as "peeking behind the page or the lid of a toybox". I really liked the design, took a shot at creating a [jQuery plugin][plugin] to replicate the effect. Here is a [demo][demo].

Most of the work is done in CSS3, and Javascript is only used to toggle the menu. When a user hovers her mouse over the menu bar, a script adds the `.box-lid-open` class to the root element which triggers the CSS3 transitions.

The skewing effect is achieved with `perspective`, `perspective-origin`, and a `rotateY` transformation. Credit goes to [BBY][bby].


  [smashing]: http://www.smashingmagazine.com/2013/07/11/innovative-navigation-designs/
  [plugin]: https://github.com/jimjh/box-lid/
  [toybox]: http://www.toybox.co.nz/
  [demo]: http://jimjh.com/box-lid/
  [bby]: http://bby.net.nz/
