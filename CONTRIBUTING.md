So you want to contribute with thumbor-aws? Awesome! Welcome aboard!

## Steps

There are a few things you'll need in order to properly start hacking on it.

1. [Fork it](http://help.github.com/fork-a-repo/)
2. Install dependencies and initialize environment (`make setup` is your friend!)
3. Hack, in no particular order:
  - Write enough code
  - Write tests for that code
  - Check that other tests pass (`make test`)
  - Repeat until you're satisfied
4. Submit a pull request

## Install Dependencies

We seriously advise you to use
[virtualenv](http://pypi.python.org/pypi/virtualenv) since it will keep
your environment clean of thumbor aws's dependencies and you can choose when
to "turn them on".

## Initializing the Environment

You can install thumbor aws's dev dependencies with:

```
$ make setup
```

## Running the Tests

Before running the tests you need to have dependencies up:

```
$ make services
```

Then you can run the tests with:

```
$ make test
```

Or you can run both in the same command with:

```
$ make ci
```

You should see the results of running your tests after an instant.

If you are experiencing "Too many open files" errors while running the
tests, try increasing the number of open files per process, by running
this command:

```
$ ulimit -S -n 2048
```

Read
<http://superuser.com/questions/433746/is-there-a-fix-for-the-too-many-open-files-in-system-error-on-os-x-10-7-1>
for more info on this.

## Linting your code

Please ensure that your editor is configured to use
[black](https://github.com/psf/black),
[flake8](https://flake8.pycqa.org/en/latest/) and
[pylint](https://www.pylint.org/).

Even if that's the case, don't forget to run `make flake pylint` before
commiting and fixing any issues you find. That way you won't get a
request for doing so in your PR.

## Pull Requests

After hacking and testing your contribution, it is time to make a pull
request. Make sure that your code is already integrated with the `master`
branch of thumbor-aws before asking for a pull request.

To add thumbor-aws as a valid remote for your repository:

```
$ git remote add thumbor-aws git://github.com/thumbor/thumbor-aws.git
```

To merge thumbor's master with your fork:

```
$ git pull thumbor master
```

If there was anything to merge, just run your tests again. If they pass,
[send a pull request](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).
