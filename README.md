# GPUI (General Purpose User Interface)

GPUI is a flexible, composable UI framework for Python that lets you build sophisticated user interfaces using simple, reusable components. It's designed to work with different rendering backends, with built-in support for Pygame.

## Features

- **XML-Based Layouts**: Define UIs declaratively using intuitive XML syntax
- **Component System**: Build complex UIs from simple primitives (box, line, text)
- **Event System**: Lightweight event handling for user interactions
- **Style System**: Separate appearance from structure with reusable styles
- **Flexible Positioning**: Constraint-based layout system for responsive designs
- **Backend Agnostic**: Support for different rendering engines (currently Pygame)

## Installation

```bash
# Clone the repository
git clone https://github.com/SvenSZim/GPUI.git
cd GPUI

# Install dependencies
# note: GPUI does not need any dependencies.
# pygame and numpy are just needed for the example-usecase.
pip install pygame numpy
```

## Documentation

For detailed documentation of all UI components, the event system, and styling capabilities, see the [manual](docs/manual.pdf).

Key concepts:
- **Elements**: Basic building blocks (Box, Line, Text)
- **Composites**: Complex elements (Button, Toggle, Dropdown)
- **Events**: System for handling user interactions
- **Styles**: Reusable visual themes
- **Layout**: Constraint-based positioning system

## Examples

Check out these examples to learn more:
- `layoutexample.xml`: Comprehensive UI layout demonstration
- `styleexample.xml`: Style system showcase
- `main.py`: Complete application example with physics simulation

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## License

This project is open source and available under the MIT License.

## Acknowledgments

Special thanks to:
- Copilot for the documentation

