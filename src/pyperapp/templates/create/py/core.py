"""
Core classes needed by PyperApp.

Copyright © 2020 Nicholas H.Tollervey

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from browser import document


_COLOURS = {
    "darkred": "#8b0000",
    "brown": "#a52a2a",
    "firebrick": "#b22222",
    "rosybrown": "#bc8f8f",
    "indianred": "#cd5c5c",
    "lightcoral": "#f08080",
    "snow": "#fffafa",
    "red": "#ff0000",
    "mistyrose": "#ffe4e1",
    "salmon": "#fa8072",
    "tomato": "#ff6347",
    "darksalmon": "#e9967a",
    "coral": "#ff7f50",
    "orangered": "#ff4500",
    "lightsalmon": "#ffa07a",
    "sienna": "#a0522d",
    "seashell": "#fff5ee",
    "saddlebrown": "#8b4513",
    "chocolate": "#d2691e",
    "sandybrown": "#f4a460",
    "peachpuff": "#ffdab9",
    "peru": "#cd853f",
    "linen": "#faf0e6",
    "bisque": "#ffe4c4",
    "darkorange": "#ff8c00",
    "burlywood": "#deb887",
    "antiquewhite": "#faebd7",
    "tan": "#d2b48c",
    "navajowhite": "#ffdead",
    "blanchedalmond": "#ffebcd",
    "papayawhip": "#ffefd5",
    "moccasin": "#ffe4b5",
    "orange": "#ffa500",
    "wheat": "#f5deb3",
    "oldlace": "#fdf5e6",
    "floralwhite": "#fffaf0",
    "darkgoldenrod": "#b8860b",
    "goldenrod": "#daa520",
    "cornsilk": "#fff8dc",
    "lightgoldenrod": "#eedd82",
    "gold": "#ffd700",
    "lemonchiffon": "#fffacd",
    "khaki": "#f0e68c",
    "palegoldenrod": "#eee8aa",
    "darkkhaki": "#bdb76b",
    "beige": "#f5f5dc",
    "lightgoldenrodyellow": "#fafad2",
    "ivory": "#fffff0",
    "lightyellow": "#ffffe0",
    "yellow": "#ffff00",
    "olivedrab": "#6b8e23",
    "yellowgreen": "#9acd32",
    "darkolivegreen": "#556b2f",
    "greenyellow": "#adff2f",
    "chartreuse": "#7fff00",
    "lawngreen": "#7cfc00",
    "darkgreen": "#006400",
    "forestgreen": "#228b22",
    "darkseagreen": "#8fbc8f",
    "limegreen": "#32cd32",
    "lightgreen": "#90ee90",
    "palegreen": "#98fb98",
    "honeydew": "#f0fff0",
    "green": "#00ff00",
    "seagreen": "#2e8b57",
    "mediumseagreen": "#3cb371",
    "springgreen": "#00ff7f",
    "mintcream": "#f5fffa",
    "mediumspringgreen": "#00fa9a",
    "mediumaquamarine": "#66cdaa",
    "aquamarine": "#7fffd4",
    "turquoise": "#40e0d0",
    "lightseagreen": "#20b2aa",
    "mediumturquoise": "#48d1cc",
    "darkslategrey": "#2f4f4f",
    "darkcyan": "#008b8b",
    "paleturquoise": "#afeeee",
    "azure": "#f0ffff",
    "lightcyan": "#e0ffff",
    "cyan": "#00ffff",
    "darkturquoise": "#00ced1",
    "cadetblue": "#5f9ea0",
    "powderblue": "#b0e0e6",
    "lightblue": "#add8e6",
    "deepskyblue": "#00bfff",
    "skyblue": "#87ceeb",
    "lightskyblue": "#87cefa",
    "steelblue": "#4682b4",
    "aliceblue": "#f0f8ff",
    "dodgerblue": "#1e90ff",
    "slategrey": "#708090",
    "lightslategrey": "#778899",
    "lightsteelblue": "#b0c4de",
    "cornflowerblue": "#6495ed",
    "royalblue": "#4169e1",
    "midnightblue": "#191970",
    "navy": "#000080",
    "darkblue": "#00008b",
    "mediumblue": "#0000cd",
    "lavender": "#e6e6fa",
    "ghostwhite": "#f8f8ff",
    "blue": "#0000ff",
    "slateblue": "#6a5acd",
    "lightslateblue": "#8470ff",
    "darkslateblue": "#483d8b",
    "mediumslateblue": "#7b68ee",
    "mediumpurple": "#9370db",
    "blueviolet": "#8a2be2",
    "purple": "#a020f0",
    "darkorchid": "#9932cc",
    "darkviolet": "#9400d3",
    "mediumorchid": "#ba55d3",
    "darkmagenta": "#8b008b",
    "thistle": "#d8bfd8",
    "plum": "#dda0dd",
    "violet": "#ee82ee",
    "magenta": "#ff00ff",
    "orchid": "#da70d6",
    "violetred": "#d02090",
    "mediumvioletred": "#c71585",
    "deeppink": "#ff1493",
    "hotpink": "#ff69b4",
    "maroon": "#b03060",
    "lavenderblush": "#fff0f5",
    "palevioletred": "#db7093",
    "pink": "#ffc0cb",
    "lightpink": "#ffb6c1",
    "black": "#000000",
    "dimgrey": "#696969",
    "darkgrey": "#a9a9a9",
    "grey": "#bebebe",
    "lightgrey": "#d3d3d3",
    "gainsboro": "#dcdcdc",
    "whitesmoke": "#f5f5f5",
    "white": "#ffffff",
} 


def palette(name):
    """
    Given a colour name (e.g. "red", "green" or "blue",), returns the corect
    HTML hex colour value (e.g. "#FF5500").

    Raises a ValueError if the name doesn't exist.
    """
    name = name.lower()
    if name in _COLOURS:
        return _COLOURS[name]
    raise ValueError("No such colour: " + name)


class Card:
    """
    Represents a card in the application.
    """

    def __init__(self, name, text=None, text_color=None, buttons=None):
        """
        Initialise and check the state of the Card. Will raise an exception if
        the passed in state is inconsistent.
        """
        self.name = name
        self.text = text
        if text_color.startswith("#"):
            self.text_color = text_color
        else:
            self.text_color = palette(text_color)
        self.buttons = buttons

    def show(self):
        """
        Ensures this card is displayed.
        """
        browser["main"].innerHTML = browser[self.name].innerHTML
