import random
import time
import shutil
import click
import questionary
from colorama import init

# colorama makes ANSI codes work on Windows too
init()

# ── character sets ─────────────────────────────────────────────────
CHAR_SETS = {
    "katakana": list("アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホ"),
    "binary":   list("01"),
    "hex":      list("0123456789ABCDEF"),
    "latin":    list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"),
    "mixed":    list("アイウエオカキクケコ0123456789ABCDEF!@#$%^&*"),
}

# ── colour palettes ────────────────────────────────────────────────
# Each palette is (head_rgb, bright_rgb, dim_rgb)
PALETTES = {
    "green":  ((220, 255, 220), (0, 255, 70),   (0, 80, 20)),
    "blue":   ((220, 230, 255), (50, 120, 255),  (10, 30, 80)),
    "red":    ((255, 220, 220), (255, 40, 40),   (80, 5, 5)),
    "gold":   ((255, 255, 200), (255, 200, 0),   (80, 55, 0)),
    "purple": ((240, 220, 255), (180, 0, 255),   (60, 0, 80)),
    "white":  ((255, 255, 255), (200, 200, 200), (60, 60, 60)),
}

# ── ANSI helpers ───────────────────────────────────────────────────
def color(r, g, b):
    return f"\x1b[38;2;{r};{g};{b}m"

def lerp(a, b, t):
    """Blend between two RGB colours. t=0 gives a, t=1 gives b."""
    return (
        int(a[0] + (b[0] - a[0]) * t),
        int(a[1] + (b[1] - a[1]) * t),
        int(a[2] + (b[2] - a[2]) * t),
    )

RESET = "\x1b[0m"
HIDE  = "\x1b[?25l"
SHOW  = "\x1b[?25h"
CLEAR = "\x1b[2J"
HOME  = "\x1b[H"
BOLD  = "\x1b[1m"

# ── interactive menu ───────────────────────────────────────────────
def ask_options():
    """Show an interactive menu and return chosen options."""
    print("\n\033[32m  ╔══════════════════════════════╗")
    print("  ║      M A T R I X  R A I N   ║")
    print("  ╚══════════════════════════════╝\033[0m\n")

    palette = questionary.select(
        "Choose a colour palette:",
        choices=[
            questionary.Choice("Green   — classic Matrix",  value="green"),
            questionary.Choice("Blue    — cold digital",    value="blue"),
            questionary.Choice("Red     — danger mode",     value="red"),
            questionary.Choice("Gold    — warm circuit",    value="gold"),
            questionary.Choice("Purple  — deep space",      value="purple"),
            questionary.Choice("White   — monochrome",      value="white"),
        ]
    ).ask()

    chars = questionary.select(
        "Choose a character set:",
        choices=[
            questionary.Choice("Katakana — Japanese (classic Matrix look)", value="katakana"),
            questionary.Choice("Binary   — ones and zeros",                  value="binary"),
            questionary.Choice("Hex      — 0-9 A-F",                        value="hex"),
            questionary.Choice("Latin    — A-Z letters and numbers",         value="latin"),
            questionary.Choice("Mixed    — katakana + hex + symbols",        value="mixed"),
        ]
    ).ask()

    speed = questionary.select(
        "Choose a speed:",
        choices=[
            questionary.Choice("Slow    — 0.5x", value="0.5"),
            questionary.Choice("Normal  — 1.0x", value="1.0"),
            questionary.Choice("Fast    — 1.5x", value="1.5"),
            questionary.Choice("Turbo   — 2.5x", value="2.5"),
        ]
    ).ask()

    density = questionary.select(
        "Choose stream density:",
        choices=[
            questionary.Choice("Sparse  — 30% columns", value="0.3"),
            questionary.Choice("Normal  — 70% columns", value="0.7"),
            questionary.Choice("Dense   — 90% columns", value="0.9"),
            questionary.Choice("Full    — all columns",  value="1.0"),
        ]
    ).ask()

    # Return None for any value means the user hit Ctrl+C during menu
    if any(v is None for v in [palette, chars, speed, density]):
        return None

    # Convert speed and density from strings back to floats
    return palette, chars, float(speed), float(density)


def run_rain(palette, chars, speed, density, fps):
    """Run the matrix rain. Returns when Ctrl+C is pressed."""
    char_list = CHAR_SETS[chars]
    head_col, bright_col, dim_col = PALETTES[palette]

    term_cols, rows = shutil.get_terminal_size()
    rows -= 1

    WIDE_CHAR_SETS = {"katakana", "mixed"}
    wide  = chars in WIDE_CHAR_SETS
    cols  = term_cols // 2 if wide else term_cols
    empty = "  " if wide else " "

    heads      = [random.uniform(-20, 0) for _ in range(cols)]
    speeds     = [random.uniform(0.3, 1.2) * speed for _ in range(cols)]
    trail_lens = [random.randint(6, 20) for _ in range(cols)]
    active     = [random.random() < density for _ in range(cols)]
    grid       = [[random.choice(char_list) for _ in range(cols)] for _ in range(rows)]

    print(HIDE + CLEAR, end="")

    try:
        while True:
            buf = [HOME]

            for row in range(rows):
                for col in range(cols):
                    if not active[col]:
                        buf.append(empty)
                        continue

                    head_row = int(heads[col])
                    dist     = head_row - row

                    if dist == 0:
                        buf.append(BOLD + color(*head_col) + grid[row][col])
                    elif 0 < dist <= trail_lens[col]:
                        t = dist / trail_lens[col]
                        r, g, b = lerp(bright_col, dim_col, t)
                        buf.append(color(r, g, b) + grid[row][col])
                    else:
                        buf.append(empty)

                buf.append(RESET + "\n")

            buf.append(
                f"\x1b[48;2;0;20;0m{color(0, 200, 60)}"
                f"  palette: {palette:<8}"
                f"  chars: {chars:<10}"
                f"  speed: {speed:<5}"
                f"  density: {density:<4}"
                f"  {cols}x{rows}  |  Ctrl+C to go back to menu"
                .ljust(term_cols) + RESET
            )

            print("".join(buf), end="", flush=True)

            for col in range(cols):
                if not active[col]:
                    continue
                heads[col] += speeds[col]
                if random.random() < 0.1:
                    r = random.randint(0, rows - 1)
                    grid[r][col] = random.choice(char_list)
                if heads[col] - trail_lens[col] > rows:
                    heads[col]      = random.uniform(-trail_lens[col], 0)
                    speeds[col]     = random.uniform(0.3, 1.2) * speed
                    trail_lens[col] = random.randint(6, 20)

            time.sleep(1 / fps)

    except KeyboardInterrupt:
        print(SHOW + RESET, end="")


@click.command()
@click.option("--palette", default=None, type=click.Choice(list(PALETTES.keys())), help="Skip menu and set palette directly")
@click.option("--chars",   default=None, type=click.Choice(list(CHAR_SETS.keys())), help="Skip menu and set character set directly")
@click.option("--speed",   default=None, type=float, help="Skip menu and set speed directly")
@click.option("--density", default=None, type=float, help="Skip menu and set density directly")
@click.option("--fps",     default=30,   show_default=True, help="Frames per second")
def main(palette, chars, speed, density, fps):
    """Matrix rain - choose your style interactively, or pass flags directly.

    \b
    Examples:
      python matrix.py                             (interactive menu)
      python matrix.py --palette blue --chars binary
      python matrix.py --palette red  --speed 1.5
    """
    # If all flags passed, run once and exit with no menu loop
    if all(v is not None for v in [palette, chars, speed, density]):
        run_rain(palette, chars, speed, density, fps)
        return

    # Interactive loop - keeps returning to the menu until user quits
    while True:
        result = ask_options()
        if result is None:
            break

        palette, chars, speed, density = result
        run_rain(palette, chars, speed, density, fps)

        # Rain stopped (Ctrl+C) - ask what to do next
        print(CLEAR, end="")
        again = questionary.select(
            "What would you like to do?",
            choices=[
                questionary.Choice("Back to menu  - change options", value="menu"),
                questionary.Choice("Quit",                            value="quit"),
            ]
        ).ask()

        if again == "quit" or again is None:
            break

    print("\nBye.")


if __name__ == "__main__":
    main()