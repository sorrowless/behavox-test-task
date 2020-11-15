# sbog.behavox-test-task

There is a repo for Behavox test task.

## Prerequisites

You have to have Python 3.6+ (tested on py3.8) and installed requirements. To
get them, run

```bash
pip install -r requirements.txt
```

## How to use

Just read the code, haha. Or run the tests:

```bash
pytest
```

## How to actually use it

Simply run

```bash
./finder.py
```

to get proper help. Overall idea is to support `start` and `stop` arguments
and allow to pass file to parse. So, example is

```bash
./finder.py start -f fixtures/bh-example.yml
```

or

```bash
./finder.py stop -f fixtures/bh-example.yml
```

## How does it work

Overall codebase is located in file [ordering.py](depsfinder/ordering.py). It
is getting given file and iterates over it by trying to find deps for each
service. Code is good commented, so feel free to read it.

## License

Apache 2.0

## Author Information

This code was created by [Stan Bogatkin](https://sbog.ru).
