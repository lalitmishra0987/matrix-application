# Matrix Rain

A Matrix-style rain animation in two modes — run it in your terminal or in a browser.

---

## Modes

| Mode     | File                    | How it runs                      |
| -------- | ----------------------- | -------------------------------- |
| Terminal | `matrix.py`             | Python CLI with interactive menu |
| Web      | `app.py` + `templates/` | Flask web app, open in browser   |

---

## Project Structure

```
matrix-application/
├── matrix.py           # Terminal mode — Python CLI
├── app.py              # Web mode — Flask app
├── templates/
│   └── index.html      # Browser canvas animation
├── requirements.txt    # All dependencies
├── Dockerfile          # Alpine-based multi-stage build
└── README.md
```

---

## Prerequisites

- Python 3.12+
- Docker (for container mode)

---

## Terminal Mode

### Setup

```bash
# Create and activate virtual environment
python -m venv venv

source venv/bin/activate        # Mac / Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt
```

### Run — Interactive Menu

```bash
python matrix.py
```

Arrow keys to navigate, Enter to select. You will be asked:

- **Palette** — green, blue, red, gold, purple, white
- **Character set** — katakana, binary, hex, latin, mixed
- **Speed** — slow (0.5x) to turbo (2.5x)
- **Density** — sparse (30%) to full (100%)

Press `Ctrl+C` to stop. You will be prompted to go back to the menu or quit.

### Run — Skip the Menu

Pass options directly as flags:

```bash
python matrix.py --palette blue --chars binary
python matrix.py --palette red  --speed 1.5
python matrix.py --palette gold --chars mixed --density 0.5 --fps 60
```

### All Options

```
--palette    green | blue | red | gold | purple | white   (default: green)
--chars      katakana | binary | hex | latin | mixed       (default: katakana)
--speed      float, 0.5=slow  2.5=turbo                   (default: 1.0)
--density    float, 0.1=sparse  1.0=full                   (default: 0.8)
--fps        integer                                        (default: 30)
```

### Exit Cleanly

```
Ctrl+C          # stop the animation → returns to menu or exits
deactivate      # exit the virtual environment
```

If the terminal gets stuck (cursor gone):

```bash
reset
```

---

## Web Mode

### Run Locally

```bash
# Activate venv and install dependencies (same as above)
source venv/bin/activate
pip install -r requirements.txt

python app.py
```

Open your browser at `http://localhost:8080`

Use the settings panel (top right) to change palette, character set, speed and density. Click **APPLY** — no page reload needed.

### Endpoints

| Endpoint   | Description                               |
| ---------- | ----------------------------------------- |
| `/`        | Matrix rain with default settings         |
| `/run`     | Matrix rain with query parameters         |
| `/healthz` | Health check — returns `{"status": "ok"}` |

### Query Parameters on `/run`

```
http://localhost:8080/run?palette=blue&chars=binary&speed=1.5&density=0.9
```

---

## Docker

### Build

```bash
docker build -t matrix-rain .
```

To build from a specific branch:

```bash
docker build --build-arg BRANCH=develop -t matrix-rain .
```

### Run — Web Mode (default)

```bash
docker run -p 8080:8080 matrix-rain
```

Open `http://localhost:8080`

### Run — Terminal Mode

```bash
docker run -it matrix-rain python3 matrix.py
```

The `-it` flags are required for the terminal version:

- `-i` keeps stdin open so arrow keys work in the menu
- `-t` allocates a TTY so the terminal has a size and colours render correctly

Without `-it` the terminal animation will not work.

---

## Dependencies

| Package     | Version | Used by                                   |
| ----------- | ------- | ----------------------------------------- |
| colorama    | 0.4.6   | Terminal — ANSI colour support on Windows |
| click       | 8.3.1   | Terminal — CLI flag parsing               |
| questionary | 2.1.1   | Terminal — interactive arrow-key menu     |
| Flask       | 3.1.3   | Web — HTTP server and templating          |
| gunicorn    | 25.1.0  | Web — production WSGI server              |
| Werkzeug    | 3.1.6   | Web — Flask dependency                    |

---

## Palettes

| Name   | Look                          |
| ------ | ----------------------------- |
| green  | Classic Matrix — the original |
| blue   | Cold digital                  |
| red    | Danger mode                   |
| gold   | Warm circuit                  |
| purple | Deep space                    |
| white  | Monochrome                    |

## Character Sets

| Name     | Characters                              |
| -------- | --------------------------------------- |
| katakana | Japanese katakana — closest to the film |
| binary   | 0 and 1 only                            |
| hex      | 0–9 and A–F                             |
| latin    | A–Z, a–z, 0–9                           |
| mixed    | Katakana + hex + symbols                |
