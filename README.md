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

## Results

The results are saved to `results.csv` with a format like this:

```
queryA,titleA1
queryA,titleA2
...
queryB,titleB1
queryB,titleB2
```

## Screenshots

- Execution:
![Execution logs](https://user-images.githubusercontent.com/26127246/180317409-9ce4b921-5cb5-45ff-8fba-c249220c1aed.png)

