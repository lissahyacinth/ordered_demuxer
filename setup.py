import pathlib
from setuptools import setup

LOCAL = pathlib.Path(__file__).parent
README = (LOCAL / "README.md").read_text()

setup(
    name = "ordered_demuxer",
    description="Break iterators into ordered chunks",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/lissahyacinth/ordered_demuxer",
    license="MIT",
    version = "0.1.0",
    packages=["ordered_demuxer"],
    package_data={'ordered_demuxer': ['py.typed']},
    extras_require={'dev': ['pytest']}
)
