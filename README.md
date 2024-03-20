# Step


## Virtual Environment
```bash
python -m venv myenv
```

## Activate
```sh
.\myenv\Scripts\Activate.ps1
```

## Git 

### Initialized the project
```sh
git init
```

### Git Ignore

Add `.gitignore`

## Create Repo in Github

1. Stage files `git add`
2. Commit `git commit -m "message"`
3. Push to Github

## Installing Flask

It is a micro framework that allows us to create rest APIs, Flexibility to have and use any package that we want

Make sure your env is activated - [ref](https://flask.palletsprojects.com/en/3.0.x/installation/)

```sh
pip install flask
```

# Run flask?

```sh
flask --app hello run
```
> Only if the file name is `app.py`
Then you can just do flask run

For development 

```sh
flask run --debug
```

