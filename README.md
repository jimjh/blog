### Installing

This is in maintenance mode. Uses Python 3.

```bash
$ git clone git@github.com:gfidente/pelican-svbhack.git
$ git clone git@github.com:getpelican/pelican-plugins.git
$ git clone git@github.com:jimjh/blog.git
$ cd blog  # setup virtualenv however you like
$ pip install -r requirements.txt
$ pelican-themes -i ../pelican-svbhack
```

### Generating

```bash
$ make html
```

### Publishing

```bash
$ make github
```
