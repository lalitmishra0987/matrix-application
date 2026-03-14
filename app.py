from flask import Flask, render_template, request

app = Flask(__name__)

# The same palette and char set definitions the terminal version uses
# Flask just passes these to the template so the browser can use them
PALETTES = ["green", "blue", "red", "gold", "purple", "white"]
CHAR_SETS = ["katakana", "binary", "hex", "latin", "mixed"]


@app.route("/")
def index():
    """Home page — show the matrix rain with default settings."""
    return render_template(
        "index.html",
        palette="green",
        chars="katakana",
        speed=1.0,
        density=0.8,
        palettes=PALETTES,
        char_sets=CHAR_SETS,
    )


@app.route("/run")
def run():
    """Run with options chosen from the form."""
    palette = request.args.get("palette", "green")
    chars   = request.args.get("chars",   "katakana")
    speed   = float(request.args.get("speed",   1.0))
    density = float(request.args.get("density", 0.8))

    return render_template(
        "index.html",
        palette=palette,
        chars=chars,
        speed=speed,
        density=density,
        palettes=PALETTES,
        char_sets=CHAR_SETS,
    )


@app.route("/healthz")
def healthz():
    """Health check — used by Docker and Kubernetes."""
    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)