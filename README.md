# Opcionempleo scraper

A opcionempleo.cl searches scraper

## Dependencies

- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
- [requests](https://pypi.org/project/requests/)

If you use [pipenv](https://pypi.org/project/pipenv/), you can install the libraries with `pipenv sync`. Otherwise, you can just use `pip install -r requirements.txt`.

## Usage

```
python main.py
```

This will requestd the data from opcionempleo.cl and save it to `results.csv`. By default, it will remove commas from query's names and titles to respect the csv format.

If you don't want to do comma removal, you can use the `--preserve-commas` parameter as follows:
```
python main.py --preserve-commas
```