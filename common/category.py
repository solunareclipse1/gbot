import re

def getCategory(module):
    try:
        category = re.search(r"cogs\.(\w+)\.",module).groups()[0]
    except AttributeError:
        category = "Misc"
    return category