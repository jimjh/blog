Date: 2014-04-06
Title: Stripe CTF 2014, Level 3 - Instant Code Search
Category: Software
Tags: scala, stripe

The task was to write, in Scala:

- an indexer that scans a bunch of input files, and
- a searcher that takes a query string and returns a list of lines containing it

It can be solved using the following:

In the indexer, tokenize each document, and create an inverted index of
tokens to a sets of (file name, line number) tuples. In the searcher,
break up the query string into tokens, and lookup the tokens in the
index.

To enable substring search, use 3-character substrings of the tokens as
keys in the index, instead of the entire token. Similarly, break up the
query string into 3-character substrings, and return the intersection of
all sets found in the inverted index for each substring.

Alternatively, one could use a suffix tree to enable substring search.
