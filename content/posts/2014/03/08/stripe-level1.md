Date: 2014-03-08
Title: Stripe CTF 2014, Level 1
Category: Software
Tags: ruby, stripe

This is the second installment of a series on Stripe's CTF 2014. You may wish
to start from [level 0]({filename}../../02/23/stripe-level0.md).

### Level 1

Level 1 proposed a crypto-currency named Gitcoin that used Git's SHA1 hashes. The player was provided with a git repository and asked to create a commit with a SHA1 that is lexicographically less than a given value _i.e._ difficulty. Moreover, the commit must include an update to the ledger that awards a single Gitcoin to the player. It's a lot like Bitcoin mining, and the player's miner raced against Stripe's bot to push the commit to the remote repository.

The general solution was to try many different git commits by altering a token/nonce in the commit message until the desired SHA1 was found.

Since the repository came with an naïve miner, my first - admittedly bad - intuition was to use [GNU parallel] and have each miner iterate through a slice of integers. That probably brought some improvements, but not much - the given miner was slow because it used a new process to compute the SHA1 of each commit. I rewrote parts of the miner in Ruby to compute multiple hashes within the same process, which attained a 30x improvement in the hash rate and passed the level handily. The tricky part was figuring out the data format of a git commit.

For future reference, a git commit looks like the following:

```
commit <size>\0tree <tree>
parent <parent>
author <author details>
committer <committer details>

<commit message>
```

A GPU miner would certainly be much faster. The implementation is left as an exercise for the reader.

I uploaded some of my work on [Github]. Give it a shot.

  [gnu parallel]: http://www.gnu.org/software/parallel/
  [Github]: https://github.com/jimjh/stripe-level1
