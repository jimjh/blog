Date: 2013-03-30
Title: Numbering the Last Line of Align* in LaTex
Category: Writing
Tags: latex

On numerous occasions, I find myself trying to number the last line (and _only_
the last line!) of a long series of derivations in an `align*` environment. I
usually switch to the `align` environment and use `\notag` to turn off the
number on each line except the last.

There is a better solution, offered by egreg on [StackOverflow][so]:

<script src="https://gist.github.com/anonymous/5276841.js"></script>

By using `equation` and `aligned`, we get an environment similar to `align*`
that only numbers the last line.

  [so]: http://tex.stackexchange.com/questions/66759/make-align-number-the-last-equation

