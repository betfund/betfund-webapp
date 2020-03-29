### Betfund

The best way to reproduce this is to do the following:

1. Clone the repository.

```
$ git clone https://github.com/betfund/betfund-webapp.git
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
$ flask db init
```

6. Run the app.

```
$ flask run
```
