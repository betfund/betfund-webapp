### Betfund

The best way to reproduce this is to do the following:

1. Clone the repository. Change into the `app` directory.

```
$ git checkout <branch>
$ cd app
```


2. Create a new `conda` environment from the `environment.yml` file.

```
$ conda env create environment.yml
$ conda activate betfund
```

3. Install the package (optionally, in editable mode).

```
$ pip install -e .
```

4. Export development environment variables

```
$ export FLASK_APP=application
$ export FLASK_ENV=development
```

5. Create the test database.

```
$ cd tests
$ python make_test_database.py
$ cd ..
```

6. Run the app.

```
$ flask run
```
