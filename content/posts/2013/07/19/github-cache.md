Date: 2013-07-19
Title: Making Conditional Requests with Peter Murach's gem
Category: Software
Tags: ruby, github api

GitHub imposes a rate limit on API requests, and encourages developers to use [conditional requests][conditional]. Here is how to do that using Peter's popular [github api gem][github].

## Method A - Faraday HTTP Cache w. ActiveSupport::Cache

This uses the [faraday-http-cache gem][faraday-http-cache], which takes care of expiration, etags, and response statuses.

<script src="https://gist.github.com/jimjh/5961836.js"></script>

## Method B - Faraday HTTP Cache w. Moneta

<script src="https://gist.github.com/jimjh/5985170.js"></script>

More details are available in this [issue][issue].

  [conditional]: http://developer.github.com/v3/#conditional-requests
  [github]: https://github.com/peter-murach/github
  [faraday-http-cache]: https://github.com/plataformatec/faraday-http-cache
  [issue]: https://github.com/peter-murach/github/issues/112#issuecomment-20882465