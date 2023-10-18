import random
import string

"""Helper functions for phonebook""" ""
VORWAHL = "0190-"


def get_phonebook():
    """Get phonebook"""
    fake_phonebook = {
        "John Doe": f"{VORWAHL}1234",
        "Jane Smith": f"{VORWAHL}5678",
        "Michael Johnson": f"{VORWAHL}9876",
        "Emily Davis": f"{VORWAHL}4321",
        "David Brown": f"{VORWAHL}8765",
        "Sarah Wilson": f"{VORWAHL}2345",
        "Matthew Lee": f"{VORWAHL}6789",
        "Jessica Clark": f"{VORWAHL}3456",
        "Daniel Hall": f"{VORWAHL}7890",
        "Linda Lewis": f"{VORWAHL}6543",
    }

    return fake_phonebook


def generate_random_phonebook_entries(n):
    entries = {}
    for _ in range(n):
        # Generate a random fake name
        fake_name = (
            "".join(random.choices(string.ascii_uppercase, k=5))
            + " "
            + "".join(random.choices(string.ascii_uppercase, k=5))
        )
        # Generate a random fake phone number
        fake_phone_number = VORWAHL + "".join(random.choices(string.digits, k=4))
        entries[fake_name] = fake_phone_number
    return entries
