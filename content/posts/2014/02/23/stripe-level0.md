Date: 2014-02-23
Title: Stripe CTF 2014, Level 0
Category: Software
Tags: ruby, stripe

I participated in a week-long CTF hosted by Stripe in Jan 2014. This series of blog posts will cover some of the problems and their solutions.

### Level 0

The first level was pretty easy, and mainly served as an introduction/tutorial
for participating in the CTF. We were given the following code, and asked to
improve its running time:

<script src="https://gist.github.com/jimjh/9178255.js"></script>

This looks like a simple spellchecker. Given an input of size _m_ and a
dictionary of size _n_, the above implementation has a running time of O(_mn_).
The easiest way to get past this level is to use a hash set, instead of an
array, for the dictionary. This reduces the running time to O(_m_).

To get on the leader board, we needed to put in more work. It quickly became
clear (through profiling) that most of the time was spent reading and
initializing the dictionary. I tried generating/serializing the set beforehand
and loading it (using `Marshal#load`) at runtime, but that did not yield any
significant improvements. Next, I tried rewriting the code in Java, and tuning
the JVM to squeeze more performance out of it. I eventually settled on the
following flags, which brought the running time from ~0.3 seconds to ~0.2
seconds.

<script src="https://gist.github.com/jimjh/9178295.js"></script>

Again, I tried using Java to serialize and deserialize the hash set, but that
didn't yield any improvements. Using nio's `MappedByteBuffer` didn't help either.

I also tried using gperf to see if it could find a reasonable perfect hash
function for the dictionary, but it took too many hours to generate and
compile, and I gave up. At this point I decided to move on to the next level.
However, here are some ideas that might have worked:

- implement a hash map in C,  pre-process the dictionary, persist it to disk,
then use mmap to load the set at runtime
- implement a bloom filter in C, then use mmap to load the filter at runtime

Note that using a bloom filter is probabilistic - it could get you on the
leader board if you push enough times.

| Strategy | Time |
| ------------ | ------- |
| Ruby Array | 7.15 s |
| Ruby Hash Map | 0.386 s |
| Java with Flags | 0.253 s |

(I didn't bother to calculate the exact variance - the numbers of significant
figures indicate my "feel" of the deviation.)

I uploaded [some of my work][github] to GitHub. Take a shot.

  [github]: https://github.com/jimjh/stripe-level0
