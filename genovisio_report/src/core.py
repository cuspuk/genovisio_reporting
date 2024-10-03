import os

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
TEMPLATE_FILENAME = "index.html"
CSS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "styles/main.css")

FLOAT_FORMAT_STRING = "%.2f"


def float_format(value: float) -> str:
    return FLOAT_FORMAT_STRING % value
