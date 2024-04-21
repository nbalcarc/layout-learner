import config
import hands
from analyzer import analyze_without_comfort


def main():
    """Main entry point."""
    keyboard_config = config.KeyboardConfig(config.layout.qwerty, config.coordinate_grid.standard, config.effort_grid.standard, config.hand_placement.home_row_us)
    analyzer = analyze_without_comfort(keyboard_config, [""])


if __name__ == "__main__":
    main()


