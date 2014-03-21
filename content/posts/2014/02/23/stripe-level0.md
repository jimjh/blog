Date: 2014-02-23
Title: Stripe CTF 2014, Level 0
Category: Software
Tags: ruby, stripe

I participated in a week-long CTF hosted by Stripe in Jan 2014. This series of blog posts will cover some of the problems and their solutions.

### Level 0

The first level was a breeze, and mainly served as an introduction/tutorial
for participating in the CTF. We were given the following code, and asked to
improve its running time:

<script src="https://gist.github.com/jimjh/9178255.js"></script>

This looks like a simple spellchecker. Given an input of size _m_ and a
dictionary of size _n_, the above implementation has a running time of O(_mn_).
The easiest way to get past this level is to use a hash set, instead of an
array, to hold the dictionary. This reduces the running time to O(_m_).

Next, I tried rewriting the code in Java, and tuning the JVM to squeeze more
performance out of it. I eventually settled on the following flags, which
brought the running time from ~0.3 seconds to ~0.2 seconds.

<script src="https://gist.github.com/jimjh/9178295.js"></script>

Most of the gains came from setting the initial heap size with `Xms` (to avoid
increasing the heap size at runtime) and setting the initial capacity for the
hashmap to some reasonably large number (to avoid expanding and copying the
set's contents at runtime.) The latter worked because the same dictionary was
used every time, and we knew the exact number of elements that would be added to
the set.

To get on the leader board, we needed to put in more work. It quickly became
clear (through profiling) that most of the time was spent reading and
initializing the dictionary. This can be dramatically reduced by pre-processing
the hash set and then using mmap to load it into memory. (You could also get
fancier and use `objcopy` to create a compiled object that could be linked into
the executable.) For this, I implemented [my own hashset][github] that uses
contiguous memory and can be loaded using mmap.

| Strategy | Time |
| ------------ | ------- |
| Ruby Array | 7.15 s |
| Ruby Hash Map | 0.386 s |
| Java with Flags | 0.253 s |
| C with mmap | 0.008 s |

Other things I tried but didn't work:

- serializing the set beforehand and deserializing it (using `Marshal#load`, or
Java's equivalent) at runtime
- using nio's `MappedByteBuffer` to load the hash set (didn't expect this to
make a huge difference anyway)

I also tried using gperf to try finding a reasonable perfect hash function for
the dictionary, but it took too many hours to generate and compile, and I gave
up. At this point I decided to move on to the next level.  However, here are
some ideas that might have worked:

- implementing a bloom filter in C, then using mmap to load the filter at runtime

Note that using a bloom filter is probabilistic - it could get you on the
leader board if you pushed enough times.

I uploaded [some of my work][github] to GitHub. Take a shot.

  [github]: https://github.com/jimjh/stripe-level0
