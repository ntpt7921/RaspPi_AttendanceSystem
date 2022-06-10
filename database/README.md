# Simple database for mapping card UID to model name

This library is not very interesting, the only thing it do is making the managing a list of mapping from UID (represented as integer) to model name.

It can load these mapping from a JSON file into a dictionary in Python. In case file don't exist, create one.

Vice versa, it can save current mapping to the JSON file that it was loaded with.

The mapping list can be queried, added to, removed from and cleared altogether.

All of the functionality is implemented in class Database (`Database.py`)
