import re


NORMALIZATION_MAP = {
    # Food
    "snaks": "snacks",
    "snack": "snacks",
    "snakas": "snacks",
    "snkas": "snacks",
    "snakcks": "snacks",

    "bannana": "banana",
    "bannan": "banana",
    "bsnana": "banana",
    "banna": "banana",

    "cha": "tea",
    "chai": "tea",

    "nasta": "breakfast",
    "brekfast": "breakfast",
    "breakkfast": "breakfast",

    "veg": "vegetables",
    "vegetable": "vegetables",
    "vegtable": "vegetables",

    "vadapaav": "vadapav",
    "vadapava": "vadapav",
    "vadapabv": "vadapav",

    "dhabha": "dhaba",
    "desi daba": "dhaba",
    "desi dhaba": "dhaba",

    "ice-cream": "icecream",
    "kulpi": "kulfi",

    # Transport
    "bus charges": "bus charge",
    "buscharge": "bus charge",
    "bus ticket": "bus",

    # Rent
    "room rent": "rent",
    "room old rent": "rent",

    # Shopping
    "d mart": "dmart",

    # Subscriptions
    "mobile recharge": "recharge",

    # Toastmasters
    "toastmasters club": "toastmasters",
    "toastmaster": "toastmasters",
    "toasmasters": "toastmasters",
    "toastmaster renew": "toastmasters",

    # Donation
    "ganapathi patti": "donation",
    "ganesh patti": "donation",
    "ganapati patti": "donation",
}


CATEGORY_MAP = {
    "food": [
        "lunch", "splitwise", "dinner", "breakfast", "snacks", "tea", "coffee", "banana",
        "thali", "egg", "biryani", "bhel", "vadapav", "vada", "dabeli", "pani puri",
        "panipuri", "kachori", "samosa", "pattice", "misal", "dosa", "uttappa", "pohe",
        "poha", "maggie", "momos", "gobi", "chole bhature", "chole bature", "chapati",
        "fries", "juice", "fruit", "fruits", "watermelon", "mango", "lassi", "icecream",
        "kulfi", "cake", "chocolate", "sweet", "pede", "rabadi", "milk", "curd", "dahi",
        "dhai", "paneer", "oats", "dal", "sugarcane", "sugar", "oil", "vegetables",
        "grocery", "groceries", "kirani", "kirana", "green mart", "greenmart", "zepto",
        "dhaba", "food", "hungerbox", "hunger box", "athithi","uta","khana","7/12 hotel","mcdonald's"
    ],

    "transport": [
        "bus", "bus charge", "bus pass", "petrol", "fuel", "ola", "uber", "cab", "auto",
        "rickshaw", "rikshaw", "train", "sleeper", "parking", "bike", "scooty", "transport",
    ],

    "rent": ["rent", "room rent", "deposit", "room expenses", "room deposit", "room deposit & rent"],

    "utilities": [
        "light bill", "electricity", "light", "gas bill", "gas", "wifi", "tv bill", "cylinder",
    ],

    "shopping": [
        "dmart", "market", "dress", "shirt", "pant", "t shirt", "shoes", "chappal", "slipper",
        "book", "bag", "umbrella", "mobile", "watch", "charger", "earphone", "earbuds", "screen guard",
        "screenguard", "thermosteel", "brush", "shampoo", "soap", "powder", "colgate", "stationary",
        "stationery", "home items", "home expense", "home use", "mirror", "matress", "mattress", "fan",
        "pipe", "cement", "paint", "color", "trends", "flipkart", "myntra", "zudio", "buds", "amazon",
    ],

    "health": [
        "hospital", "doctor", "tablet", "medical", "medicine", "injection", "dolo", "ors",
        "calcium", "leg oil", "moov",
    ],

    "investment": ["sip", "mutual fund", "lic"],

    "home loan": [
        "home loan", "janata", "the janata", "gangadhar", "gangadhara", "ganadhar", "shivaraj",
        "loan", "home key", "khandu baad", "wallputti",
    ],

    "subscriptions": [ "hotstar subscription"],

    "toastmasters": [
        "toastmasters", "toastmaster", "toastmasters membership", "toastmaster renew", "tltp 2.0"
    ],

    "trip": [
        "trip", "travel", "hampi", "dandeli", "ajanta", "ellora", "kumarparvat", "andharban",
        "lavasa", "raighad", "raigad", "toranhalli", "torhanahalli", "tornahalli", "tamhini",
        "tikona", "akkalkoat", "chikkamagaluru", "bhimashankar", "mysore", "solapur", "rajapur", "wet & joy",
        "jyothiba trip", "jyothiba yatra", "wari", "zen spring","traveling", "go karting", "washing machine repair"
    ],

    "donation": [
        "donation", "donate", "ganapati patti", "ganapathi patti", "ganesh patti", "donations to sikh"
    ],

    "Fitness": ["gym", "marathon", "yoga", "exercise", "health club", "swimming", "run"],

    "events": [
        "festival", "sankalp marriage", "annappa marriage", "wedding", "vaibhav marriage", "vivek marriage", "gift", "gifts & events", "fair"
    ],

    "maintenance": [
       "debit card charge", "annual maintenance", "debit card fee"
    ],
}


def normalize(expense):
    exp = str(expense).lower().strip()

    if exp in NORMALIZATION_MAP:
        return NORMALIZATION_MAP[exp]

    return exp


def categorize(expense):
    exp = normalize(expense)

    # Ignore blank values
    if not exp:
        return "unrecognized"

    # Ignore total/month rows
    if exp.startswith("total"):
        return "unrecognized"

    for category, keywords in CATEGORY_MAP.items():
        for keyword in keywords:
            if keyword in exp:
                return category

    return "unrecognized"