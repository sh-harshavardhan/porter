"""Base logger configuration for the application."""

__all__ = ["BaseLogger", "log"]


import logging


class BaseLogger:
    """Base logger configuration class."""

    def __init__(
        self,
        name: str = __name__,
        log_level: int = logging.INFO,
        log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        disable_project_name_print: bool = True,
    ):
        """Initializes the BaseLogger with the specified configuration."""
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        formatter = logging.Formatter(log_format)
        console_handler.setFormatter(formatter)

        if not self.logger.hasHandlers():
            self.logger.addHandler(console_handler)

        if not disable_project_name_print:
            from art import text2art

            """
            https://www.ascii-art.site/FontList.html
            https://pypi.org/project/art/
            """
            print(text2art("PORTER", font="bigchief"))

    def get_logger(self) -> logging.Logger:
        """Returns the configured logger instance."""
        return self.logger


log = BaseLogger(name="porter").get_logger()
