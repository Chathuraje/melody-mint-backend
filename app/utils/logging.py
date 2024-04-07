import logging
from colorlog import ColoredFormatter

log_setup_done = False  # Flag to track whether logging setup is already done

# class ExcludeHttpRequestFilter(logging.Filter):
#     def filter(self, record):
#         # Exclude log messages related to the HTTP request
#         http_request_message = "HTTP Request: POST https://api.openai.com/v1/chat/completions"

#         # Constant substring in the YouTube API-related log message
#         youtube_api_constant_substring = 'HTTP/1.1'
#         google_drive_string = 'oauth2client<4.0.0'

#         return http_request_message not in record.getMessage() and record.getMessage() != youtube_api_constant_substring and google_drive_string not in record.getMessage()


def setupLogger():
    global log_setup_done

    if not log_setup_done:
        FORMAT_LOG = "%(reset)s %(log_color)s%(levelname)-8s%(reset)s %(green)s%(asctime)s - %(white)s%(message)s"
        FORMAT_SAVE = f"%(levelname)-8s %(asctime)s - %(message)s"

        formatter = ColoredFormatter(
            FORMAT_LOG,
            datefmt="%Y-%m-%d %H:%M:%S",
            reset=True,
            log_colors={
                "DEBUG": "bold_cyan",
                "INFO": "bold_green",
                "WARNING": "bold_yellow",
                "ERROR": "bold_red",
                "CRITICAL": "bold_red,bg_white",
            },
        )

        logging.basicConfig(
            filename="system.log", level=logging.INFO, format=FORMAT_SAVE
        )

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        # console_handler.addFilter(ExcludeHttpRequestFilter())
        logging.getLogger().addHandler(console_handler)

        log_setup_done = True


def getLogger():
    return logging.getLogger()
