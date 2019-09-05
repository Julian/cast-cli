import click

from cast_cli import __version__

import pychromecast


@click.group()
@click.version_option(version=__version__)
def main():
    pass


@main.command()
@click.option("--url", default=None)
@click.option("--content-type", default="video/mp4")
def play(url, content_type):
    """
    Play the given URL.
    """

    chromecast, = pychromecast.get_chromecasts()
    chromecast.wait()

    if url is not None:
        chromecast.media_controller.play_media(url, content_type=content_type)
    else:
        chromecast.media_controller.block_until_active()
        chromecast.media_controller.play()

    chromecast.media_controller.block_until_active()


@main.command()
@click.argument("time")
def seek(time):
    """
    Seek to the specified time.
    """

    mins, _, secs = time.rpartition(":")
    chromecast, = pychromecast.get_chromecasts()
    chromecast.wait()
    chromecast.media_controller.block_until_active()
    chromecast.media_controller.seek(int(mins or 0) * 60 + int(secs))
    chromecast.media_controller.block_until_active()
