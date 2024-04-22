import config
import hands
from analyzer import analyze


def main():
    """Main entry point."""
    keyboard_config = config.KeyboardConfig(config.layout.qwerty, config.coordinate_grid.standard, config.hand_placement.home_row_us)
    analyzer = analyze(keyboard_config, [""])


if __name__ == "__main__":
    main()


