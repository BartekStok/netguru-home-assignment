import json
import os


def get_cars_list():
    """
    Returns list of objects just like from external API
    https://vpic.nhtsa.dot.gov/api/
    """
    cwd = os.path.dirname(__file__)
    with open(cwd + "/data/honda.json", "r") as f:
        data = json.load(f)
        return data["Results"][:10]
