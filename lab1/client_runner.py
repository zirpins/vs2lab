from lab1.phonebook_helper import get_phonebook
from lab1.clientserver import Client

"""Simple Client example."""

names = list(get_phonebook().keys())
names.append("Klaus Existiertnicht")
with Client() as cl:
    for name in names:
        print(f"{name}: {cl.get(name)}")
    print()
    print(cl.get_all())
