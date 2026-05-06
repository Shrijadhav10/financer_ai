# categorizer.py

NORMALIZATION_MAP = {
    "snaks": "snacks",
    "snack": "snacks",
    "bannana": "banana",
    "cha": "tea",
    "chai": "tea",
    "cutting": "salon",
    "nasta": "breakfast",
    "veg": "vegetables",
    "vegetable": "vegetables",
    "j1":"dinner",
    "ganapati patti":"donation",
    "the janata":"loan",
    "fan":"shopping",
    "lunch and dinner": "lunch",
    "dinner dosa": "dinner",

}

CATEGORY_MAP = {
    "food": [
        "lunch", "dinner", "breakfast", "snacks", "banana", "tea",
        "thali", "egg", "biryani", "bhel", "vadapav", "j1", "splitwise","vegetables",
        "ice cream", "zepto", "kirani", "kachori","uta","cake","dabeli",
        "green mart", "chapati","grocery","vada","vadapav","gobi manchuri",
        "chokobar","pede","dhaba", "dhabha","oil","grocery","dhahi"
    ],
    "transport": [
        "bus", "bus charge", "petrol", "fuel","bus pass"
    ],
    "rent": [
        "rent", "room rent", "deposit", "room deposit & rent"
    ],
    "utilities": [
        "light bill", "gas", "gas bill", "electricity", "light",
    ],
    "shopping": [
        "dmart", "market", "dress","gift", "shoes",
        "book","bag","umbrella", "mobile","watch", "shirt"
    ],
    "health": [
        "hospital", "doctor", "tablet","doctor", "medical"
    ],
    "investment": [
        "sip" ,"mutual fund"
    ],
    "loan":[
        "home loan", "annna" , "janata", 
        "gangadhar", "shivaraj","omkar","shivam","nikhil","pavan"
    ],
    "subscriptions": [
        "recharge", "mobile recharge", "wifi", 
    ],
    "toasmasters": [
        "toastmasters club", "toastmasters", 
    ],
    "trip":[
        "travel","fair","hampi trip","ajanta & ellora trip"
    ],
    "donation":[
        "ganapati patti","ganapathi patti", "ganesh patti"
    ]
}


def normalize(expense):
    exp = str(expense).lower().strip()
    return NORMALIZATION_MAP.get(exp, exp)


def categorize(expense):
    exp = normalize(expense)

    for category, keywords in CATEGORY_MAP.items():
        if exp in keywords:
            return category

    return exp  # keep original for debugging