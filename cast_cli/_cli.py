import click

from cast_cli import __version__

from pychromecast.controllers.youtube import YouTubeController
import pychromecast


@click.group()
@click.version_option(version=__version__)
def main():
    pass


@main.command()
def list():
    """
    List the Chromecasts on the current network.
    """

    for each in pychromecast.get_chromecasts():
        click.echo(each.device.friendly_name)


@main.command()
@click.argument("url", required=False)
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

    if time == "start":
        time = "0"

    mins, _, secs = time.rpartition(":")
    chromecast, = pychromecast.get_chromecasts()
    chromecast.wait()
    chromecast.media_controller.block_until_active()
    chromecast.media_controller.seek(int(mins or 0) * 60 + int(secs))
    chromecast.media_controller.block_until_active()


@main.command()
@click.argument("video_id")
def youtube(video_id):
    """
    Play a specified YouTube video.
    """

    chromecast, = pychromecast.get_chromecasts()
    chromecast.wait()
    youtube = YouTubeController()
    chromecast.register_handler(youtube)
    youtube.play_video(video_id)
