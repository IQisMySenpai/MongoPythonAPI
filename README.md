# MongoPythonAPI
## Table of Contents

1. [About The Project](#about-the-project)
   - [Built With](#built-with)
2. [Example Uses](#example-uses)
   - [Initialization of the API](#initialization-of-the-api)
   - [Find](#find)
   - [Insert One](#insert-one)
4. [Acknowledgements](#acknowledgements)

## About The Project

The first version of this code was written in our [Discord Bot](https://github.com/IQisMySenpai/RedditTopOfBot). As I am starting to make changes to the API I wanted to track them seperately.

### Built With

* [Python 3.9](www.python.org)

## Example Uses

The API supports following actions:
- Find one entry: `find_one`
- Find multiple entries: `find`
- Insert one entry: `insert_one`
- Insert multiple entries: `insert`
- Update one entry: `update_one`
- Update multiple entrie: `update`
- Delete one entry: `delete_one`
- Delete multiple entries: `delete`
- Count multiple entries: `count`

Here are some examples how you can use the api. Further documentation can be found in the docstrings.

### Initialization of the API
```python
from mongo_api import MongoAPI

mongo = MongoAPI('db_address', 'db_name', 'db_username', 'db_password')
```

### Find
Find can be used to query the database.
```python
mongo.find('movies', {'name': 'Interstellar'})
```

### Insert One
Insert One can be used to insert single entries into the database. If you want to insert multiple use `insert` with a array of entries.
```python
new_movie = {'name': 'First Man', 'length': 141}
mongo.insert_one('movies', new_movie)
```

## Acknowledgements
* [Alisot2000](https://github.com/AliSot2000)
