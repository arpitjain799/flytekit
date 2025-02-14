import base64
from io import BytesIO
from typing import Union

import markdown
import pandas as pd
import plotly.express as px
from PIL import Image
from ydata_profiling import ProfileReport

from flytekit.types.file import FlyteFile


class FrameProfilingRenderer:
    """
    Generate a ProfileReport based on a pandas DataFrame
    """

    def __init__(self, title: str = "Pandas Profiling Report"):
        self._title = title

    def to_html(self, df: pd.DataFrame) -> str:
        assert isinstance(df, pd.DataFrame)
        profile = ProfileReport(df, title=self._title)
        return profile.to_html()


class MarkdownRenderer:
    """Convert a markdown string to HTML and return HTML as a unicode string.

    This is a shortcut function for `Markdown` class to cover the most
    basic use case.  It initializes an instance of Markdown, loads the
    necessary extensions and runs the parser on the given text.
    """

    def to_html(self, text: str) -> str:
        return markdown.markdown(text)


class BoxRenderer:
    """
    In a box plot, rows of `data_frame` are grouped together into a
    box-and-whisker mark to visualize their distribution.

    Each box spans from quartile 1 (Q1) to quartile 3 (Q3). The second
    quartile (Q2) is marked by a line inside the box. By default, the
    whiskers correspond to the box' edges +/- 1.5 times the interquartile
    range (IQR: Q3-Q1), see "points" for other options.
    """

    # More detail, see https://plotly.com/python/box-plots/
    def __init__(self, column_name):
        self._column_name = column_name

    def to_html(self, df: pd.DataFrame) -> str:
        fig = px.box(df, y=self._column_name)
        return fig.to_html()


class ImageRenderer:
    """Converts a FlyteFile or PIL.Image.Image object to an HTML string with the image data
    represented as a base64-encoded string.
    """

    def to_html(cls, image_src: Union[FlyteFile, Image.Image]) -> str:
        img = cls._get_image_object(image_src)
        return cls._image_to_html_string(img)

    @staticmethod
    def _get_image_object(image_src: Union[FlyteFile, Image.Image]) -> Image.Image:
        if isinstance(image_src, FlyteFile):
            local_path = image_src.download()
            return Image.open(local_path)
        elif isinstance(image_src, Image.Image):
            return image_src
        else:
            raise ValueError("Unsupported image source type")

    @staticmethod
    def _image_to_html_string(img: Image.Image) -> str:
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        return f'<img src="data:image/png;base64,{img_base64}" alt="Rendered Image" />'
