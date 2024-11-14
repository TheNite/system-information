import sys
import os
import logging
from logging.handlers import RotatingFileHandler
import webview
from system_info import fetch_system_info
import multiprocessing

multiprocessing.freeze_support()

log_directory = os.path.join(".", "system_info_logs")

if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_file_path = os.path.join(log_directory, "system_info.log")

# Set up a rotating log file handler
log_handler = RotatingFileHandler(log_file_path, maxBytes=1_000_000, backupCount=3)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[log_handler]
)

logger = logging.getLogger(__name__)
logger.info("Logging setup complete. Logs will be stored in '%s'.", log_file_path)


class Api:
    def get_system_info(self):
        logger.debug("API call: get_system_info()")
        try:
            logger.info("Fetching system information...")
            system_info = fetch_system_info()
            logger.info("System information fetched successfully.")
            logger.debug(f"System Information: {system_info}")
            return system_info
        except Exception as e:
            logger.error(f"Error in fetching system info: {e}", exc_info=True)
            return "An error occurred while fetching system information."


def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def start_gui():
    logger.info("Initializing GUI...")

    if os.environ.get("PYWEBVIEW_STARTED") == "1":
        logger.warning("Application already started. Exiting to prevent recursion.")
        return
    os.environ["PYWEBVIEW_STARTED"] = "1"  # Flag to prevent re-initialization

    try:
        api = Api()
        html_path = get_resource_path("gui/index.html")
        logger.debug(f"HTML path: {html_path}")

        # Creating the webview window
        window = webview.create_window(
            "System Information",
            html_path,
            js_api=api,
            width=800,
            height=600,
            resizable=True
        )
        logger.info("Starting the webview...")

        webview.start(gui='default')
        logger.info("Webview started successfully.")
    except Exception as e:
        logger.error(f"Error starting the GUI: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    if getattr(sys, 'frozen', False) and len(sys.argv) > 1 and sys.argv[1] == '--multiprocessing-fork':
        sys.exit()
    logger.info("Application started.")
    start_gui()
