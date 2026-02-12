from flask import Flask, request, jsonify, render_template
import random
import os

midterm = Flask(__name__)

GRAMMARS = {
    "character": {
        "harsh": {
            "chunks": ["drak", "skor", "grim", "thar", "zhi", "dro"],
            "prefixes": ["Ash", "Than", "Iro", ""],
            "suffixes": ["rak", "zor", "th", ""],
            "range": (1, 2),
        },
        "elegant": {
            "chunks": ["va", "ser", "al", "ri", "na", "au", "san", "phin"],
            "prefixes": ["El", "Va", "Al", "Ser", ""],
            "suffixes": ["a", "ia", "eth", "ine", ""],
            "range": (2, 2),
        },
        "whimsical": {
            "chunks": ["di", "sa", "vi", "lu", "me", "na", "wa", "bo"],
            "prefixes": ["Vio", "Lu", "Rosa", "Bir", ""],
            "suffixes": ["bel", "lyn", "la", "die", ""],
            "range": (1, 2),
        }
    },
    "place": {
        "harsh": {
            "chunks": ["krag", "mor", "drun", "zak", "kre", "zon"],
            "prefixes": ["Black", "Iron", "Silv", ""],
            "suffixes": ["hold", "keep", "gaith", "hollow", ""],
            "range": (1, 2),
        },
        "elegant": {
            "chunks": ["el", "ara", "li", "the", "sa", "ri", "san", "va"],
            "prefixes": ["Ael", "Ser", "Aur", "Cel", "El", ""],
            "suffixes": ["vale", "spire", "gard", ""],
            "range": (2, 3),
        },
        "whimsical": {
            "chunks": ["bun", "no", "pi", "la", "mo", "lu", "bo"],
            "prefixes": ["Sun", "Old", "Sweet", ""],
            "suffixes": ["town", "field", "hill", "pond", ""],
            "range": (1, 2),
        }
    }
}

BACKGROUNDS = {
    "character": {
        "harsh": {
            "roles": ["mercenary", "thief", "warlock", "scientist", "assassin"],
            "traits": ["scarred", "ruthless", "vengeful", "cruel", "rigid", "selfish"],
            "goals": ["seeks revenge", "hunts ancient beasts", "guards hideouts", "overthrows the crown", "punishes betrayers"],
        },
        "elegant": {
            "roles": ["scholar", "mage", "healer", "noble", "oracle", "diplomat", "jeweler"],
            "traits": ["graceful", "soft-spoken", "dignified", "confident", "genuine", "generous"],
            "goals": ["studies lost magic", "protects ancient knowledge", "guides royal courts", "restores hidden secrets"],
        },
        "whimsical": {
            "roles": ["archer", "farmer", "tinker", "dreamer", "fortune teller"],
            "traits": ["cheerful", "playful", "curious", "eccentric", "imaginative", "mischievous"],
            "goals": ["collects strange stories", "searches for shiny things", "runs around in circles", "digs for mushrooms"],
        }
    },
    "place": {
        "harsh": {
            "description": ["fortified", "abandoned", "torn", "gloomy", "sunken", "rotting", "corrupted"],
            "features": ["jagged cliffs", "rustic gates", "ghostly ruins", "deep mines"],
        },
        "elegant": {
            "description": ["luxurious", "ancient", "enchanted", "starlit", "shimmering", "ethereal"],
            "features": ["towering flags", "gold fountains", "fairy gardens", "ornate halls", "shimmering statues"],
        },
        "whimsical": {
            "description": ["colorful", "sleepy", "miniature", "iridescent", "whispering", "translucent"],
            "features": ["floating forests", "singing wells", "flower fields", "friendly markets", "rolling hills"],
        }
    }
}


LENGTH_RANGE = {
    "short": (1, 2),
    "medium": (4, 6),
    "long": (8, 12),
}

def generate_name(category, tone, length=None):
    grammar = GRAMMARS[category][tone]
    prefix = random.choice(grammar["prefixes"])
    suffix = random.choice(grammar["suffixes"])

    min_len, max_len = LENGTH_RANGE.get(length, (2, 12))
    core = ""
    while len(core) < min_len:
        core += random.choice(grammar["chunks"])
    core = core[:max_len]

    name = prefix + core + suffix
    return name.capitalize()

def generate_background(category, tone, name):
    bg = BACKGROUNDS[category][tone]

    if category == "character":
        role = random.choice(bg["roles"])
        trait = random.choice(bg["traits"])
        goal = random.choice(bg["goals"])
        return f"{name} is a {trait} {role} who {goal}."

    elif category == "place":
        descriptor = random.choice(bg["description"])
        feature = random.choice(bg["features"])
        return f"{name} is a {description} place known for its {feature}."

@midterm.route("/")
def index():
    return render_template("index.html")

@midterm.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    category = data.get("category")
    tone = data.get("tone")
    length = data.get("length")
    count = data.get("count")

    if category not in GRAMMARS or tone not in GRAMMARS[category] or length not in LENGTH_RANGE:
        return jsonify({"Error": "Invalid input"}), 400

    try:
        count = int(count)
        if count <= 0:
            raise ValueError
    except:
        return jsonify({"Error": "Number must be positive"}), 400

    results = []

for _ in range(count):
    name = generate_name(category, tone, length)
    description = generate_background(category, tone, name)
    results.append(description)

return jsonify({"results": results})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    midterm.run(host="0.0.0.0", port=port, debug=True)