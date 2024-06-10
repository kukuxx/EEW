import os, uuid
from ..config import Config
from ..earthquake.eew import EEW
from ..logging import Logger
from .abc import NotificationClient
from flask import Flask
from linebot import LineBotApi
from linebot.models import TextSendMessage

class LineNotification(NotificationClient):
    """
    Represents a linebot EEW notification client.
    """
    alerts: dict[str, str] = {}
    notification_channels: list[str] = []

    def __init__(self, logger: Logger, config: Config, access_token: str, channel_secret: str) -> None:
        """
        Initialize a new linebot notification client.

        :param logger: The logger instance.
        :type logger: Logger
        :param config: The configuration.
        :type config: Config
        :param access_token: The LINE Messaging API access token.
        :type access_token: str
        :param channel_secret: The LINE Messaging API channel secret.
        :type channel_secret: str
        """
        self.logger = logger
        self.config = config
        
        line_host = config['host']

        for channel_id in self.config['channels']:
            # TODO: check channel status
            self.notification_channels.append(channel_id)

        self.api = LineBotApi(access_token)
       

    async def run(self) -> None:
        """
        The entrypoint for the notification client.
        """        
        self.logger.info(
            "LINE Bot is ready.\n"
            # "-------------------------\n"
            # f"Logged in as: {self.user.name}#{self.user.discriminator} ({self.user.id})\n"  # type: ignore
            # f" API Latency: {self.latency * 1000:.2f} ms\n"
            # f"Guilds Count: {len(self.guilds)}\n"
            # "-------------------------"
        )

    async def send_eew(self, eew: EEW) -> None:
        """
        If an new EEW is detected, this method will be called.

        Note: This method should not do any blocking calls.

        :param eew: The EEW.
        :type eew: EEW
        """
        self.logger.info
        if len(self.notification_channels) == 0:
            self.logger.error(f"No LINE notification channels available")
            return
        m = TextSendMessage(text=f"地震警報: {eew.earthquake.magnitude}M")
        
        for channel_id in self.notification_channels:
            self.api.push_message(channel_id, messages=m)
            self.logger.info(f"Sent EEW alert to {channel_id}")
    

    async def update_eew(self, eew: EEW):
        """
        If an EEW is updated, this method will be called.

        Note: This method should not do any blocking calls.

        :param eew: The updated EEW.
        :type eew: EEW
        """
        ...

    async def lift_eew(self, eew: EEW):
        """
        If an EEW alert was lifted, this method will be called.

        Note: This method should not do any blocking calls.

        :param eew: The lifted EEW.
        :type eew: EEW
        """
        ...


NAMESPACE = "line-bot"


def register(config: Config, logger: Logger) -> None:
    """
    Register the linebot notification client.

    Note: DO NOT run or start the client in this function, just register it.
    If you want to run it in the event loop, do it in :method:`NotificationClient.run`.

    :param config: The configuration of linebot notification client.
    :type config: Config
    :param logger: The logger instance.
    :type logger: Logger
    """
    access_token = os.environ.get("LINEBOT_ACCESS_TOKEN")
    channel_secret = os.environ.get("LINEBOT_CHANNEL_SECRET")
    if access_token is None or channel_secret is None:
        logger.error(f"{NAMESPACE} LINEBOT_ACCESS_TOKEN or LINEBOT_CHANNEL_SECRET is not set")
        return

    return LineNotification(logger, config, access_token, channel_secret)