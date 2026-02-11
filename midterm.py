from flask import Flask, request, jsonify, render_template
import random

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
        return jsonify({"error": "Invalid input"}), 400

    try:
        count = int(count)
        if count <= 0:
            raise ValueError
    except:
        return jsonify({"error": "Count must be a positive integer"}), 400

    names = [generate_name(category, tone, length) for _ in range(count)]
    return jsonify({"names": names})

if __name__ == "__main__":
    midterm.run(debug=True)