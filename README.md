# Generic Django Online Shop

The current version of the database-driven ecommerce web application uses Django 3.1 and Python 3.7.

## Dependencies

### Development

1. Black
2. Flake8
3. Isort
4. SphixAwsome theme

## Setting Up Development Environment

### Isort

pyproject.toml is the configuration file of choice and has been included in the current repository.

For more information, see [documentation](https://pycqa.github.io/isort/).

### Sphinx

Follow, step by step, the installation and configuration process in the [documentation](https://www.sphinx-doc.org/en/master/tutorial/index.html).

## Quick Reference

### Running Isort On Modules

```
# To run on specific files:
isort mypythonfile.py mypythonfile2.py

# To apply recursively:
isort .

# To view proposed changes without applying them:
isort mypythonfile.py --diff
```

### Sphinx Usage

After running the command for creation of the documentation layout, you get the following files:

- **build/:** The directory that will hold the rendered documentation.
- **make.bat and Makefile:** Convenience scripts to simplify some common Sphinx operations, such as rendering the content.
- **source/conf.py:** A Python script holding the configuration of the Sphinx project. It contains the project name and release you specified to sphinx-quickstart, as well as some extra configuration keys.
- **source/index.rst:** The root document of the project, which serves as welcome page and contains the root of the “table of contents tree” (or toctree).

To build, from the root folder (i.e. folder containing docs/), run the following:

```
sphinx-build -b html docs/source/ docs/build/html
```

or leverage the convinience script as follows:

```
cd docs
make html
```

- Customise the index.rst root file.
- [Change themes](https://www.sphinx-doc.org/en/master/tutorial/more-sphinx-customization.html).

## Apps

The following are the currently functional features (apps) of the overall web application:

### shop:

- This is the main app of the project used for customer interaction with the products as well as management of the products.
-

# Configuring Project

## Add the path to the settings file as an environment variable by adding the following lines to the bottom of the virtual environment:

** Linux: venv/bin/activate **
export PYTHONPATH="/home/tom/Documents/django-basic-shop/src/shop:$PYTHONPATH"
export DJANGO_SETTINGS_MODULE=shop.settings

**Powershell: Scripts\activate.ps1**
$env:PYTHONPATH = "C:\Users\Thomas\Documents\django-basic-shop\src\shop" + $env:PYTHONPATH
$env:DJANGO_SETTINGS_MODULE = "shop.settings"

# Tools

Not using flakehell.
