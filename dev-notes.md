# Developer Notes

A catch-all for notes related to developing this project.

## Packaging

Remove test venv
rm -rf /delete-later

Rebuild
python3 -m pip install --upgrade build twine
python3 -m build

Upload to TestPyPi
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*


Re-download for test

python3 -m pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple rolodex==0.4.2

## FAQ

### When should I run the editable install?

Run it once per virtual environment after you:

- Create or switch to a new virtual env (venv)
- Clone the repo on a new machine
- Change packaging config

You ***should*** rerun it if you:

- add a new top-level package or move code across 
packages
- rename a package
- delete/recreate the venv or clear site-packages

You ***do not need*** to re-run it for regular 
code edits.

## Reference

### How to run it locally?

This activates the virtual environment, and runs the help 
command.

- `source ./rolo/bin/activate`
- `python main.py --help`

#### Create virtual environment & run help

- `python3 venv -m rolo`
- `source ./rolo/bin/activate`
- `python main.py --help`

### Editable Install

- `python3 -m pip install -e .`

### Run Tests

Run editable install (from virtual env)

`python3 -m pip install -e .`

Run tests

> `pytest`

Run tests, verbose

> `pytest -v`