"""
The template for a custom notification client.

See also: https://github.com/watermelon1024/EEW/blob/main/docs/zh-TW/dev/notification.md#開發客戶端功能
"""

from ...config import Config
from ...earthquake.eew import EEW
from ...logging import Logger
from ..base import NotificationClient


class CustomNotificationClient(NotificationClient):
    """
    Represents a [custom] EEW notification client.
    """

    def __init__(self, logger: Logger, config: Config) -> None:
        """
        Initialize a new [custom] notification client.

        :param logger: The logger instance.
        :type logger: Logger
        :param config: The configuration.
        :type config: Config
        """
        self.logger = logger
        self.config = config
        ...

    async def run(self) -> None:
        """
        The entrypoint for the notification client.
        If this client doesn't need to run in the event loop, just type `pass` because this method is required.

        Note: DO NOT do any blocking calls to run the otification client.
        Example:
        ```py
        # Bad
        time.sleep(10)
        requests.post(...)

        # Good
        await asyncio.sleep(10)
        await aiohttp.request("POST", ...)
        ```
        """
        self.logger.info("Starting [Custom Notification Client]...")
        ...

    async def send_eew(self, eew: EEW):
        """
        If an new EEW is detected, this method will be called.

        Note: This method should not do any blocking calls.

        :param eew: The EEW.
        :type eew: EEW
        """
        ...

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
