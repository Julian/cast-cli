import click

from cast_cli import __version__

import pychromecast


@click.group()
@click.version_option(version=__version__)
def main():
    pass


@main.command()
@click.argument("url")
@click.option("--content-type", default="video/mp4")
def play(url, content_type):
    """
    Play the given URL.
    """

    chromecast, = pychromecast.get_chromecasts()
    chromecast.wait()
    chromecast.media_controller.play_media(url, content_type=content_type)
    chromecast.media_controller.block_until_active()
