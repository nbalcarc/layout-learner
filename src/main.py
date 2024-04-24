import config
import hands
from interface import analyze, KeyboardConfig


def test_stock_layouts():
    layouts = [
        (config.layout.qwerty, "qwerty"),
        (config.layout.dvorak, "dvorak"),
        (config.colemak, "colemak"),
        (config.colemak_dh, "colemak-dh"),
        (config.workman, "workman"),
        (config.norman, "norman"),
        (config.semimak_jq, "semimak_jq"),
        (config.mtgap, "mtgap"),
        (config.alphabetical, "alphabetical"),
    ]

    with open("../data/processed/.compiled.txt") as file:
        lines = file.read().splitlines()

    results = dict()

    for layout, name in layouts:
        print(f"Running {name}")
        keyboard_config = KeyboardConfig(layout, config.coordinate_grid.standard, config.hand_placement.home_row_us)
        analyzed = analyze(keyboard_config, lines)
        results[name] = analyzed

    for layout, (events, distance, time_gaps, use_deviation, score, ) in results.items():
        print(f"\n>>> RESULTS FOR {layout}")
        print(f"EVENTS: {events}")
        print(f"DISTANCE: {distance}")
        print(f"TIME_GAPS: {time_gaps}")
        print(f"USE_DEVIATION: {use_deviation}")
        print(f"SCORE: {score}")

    #for layout, analyzed in results:
    #    print(f"RESULTS FOR {layout}")
    #    print(f"EVENTS: {analyzed[0]}")
    #    print(f"TIME_GAPS: {analyzed[1]}")
    #    print(f"DISTANCE: {analyzed[2]}")
    #    print(f"SCORE: {analyzed[3]}")


def main():
    """Main entry point."""
    #keyboard_config = KeyboardConfig(config.layout.qwerty, config.coordinate_grid.standard, config.hand_placement.home_row_us)
    #with open("../data/processed/.compiled.txt") as file:
    #    lines = file.read().splitlines()
    ##analyzed = analyze(keyboard_config, lines[:1])
    #analyzed = analyze(keyboard_config, lines)
    #print(analyzed)
    test_stock_layouts()


if __name__ == "__main__":
    main()


