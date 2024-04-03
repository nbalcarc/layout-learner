import config
import classes


def main():
    """Main entry point."""
    keyboard_config = classes.KeyboardConfig(config.layout.qwerty, config.coordinate_grid.standard, config.effort_grid.standard)
    analyzer = classes.Analyzer(keyboard_config)


if __name__ == "__main__":
    main()


