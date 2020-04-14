# Betfund Web Application

The best way to reproduce this is to do the following:

###### Clone the repository. Change into the `app` directory.

```
$ git checkout <branch>
```

###### Create a new `conda` environment from the `environment.yml` file.

```
$ conda env create environment.yml
$ conda activate betfund
```

###### Install the package.

```
$ pip install -e .
```

###### Create the database.

```
$ flask db upgrade
```

###### Run the app.

```
$ flask run
```
