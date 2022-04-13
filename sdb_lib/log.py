from datetime import datetime


def time_now():
    return datetime.now().strftime("[%H:%M:%S]")


class Styles:
    reset = "\033[0m"
    bold = "\033[1m"
    underline = "\033[4m"
    reverse = "\033[7m"


class Colors:
    black = "\033[0;30m"
    red = "\033[0;31m"
    green = "\033[0;32m"
    yellow = "\033[0;33m"
    blue = "\033[0;34m"
    purple = "\033[0;35m"
    cyan = "\033[0;36m"
    white = "\033[0;37m"


class Log:
    def info(text: str):
        print(f"{Colors.cyan}{time_now()} [INFO]{Colors.white} {text}")

    def warning(text: str):
        print(f"{Colors.yellow}{time_now()} [WARNING]{Colors.white} {text}")

    def error(text: str):
        print(f"{Colors.red}{time_now()} [ERROR]{Colors.white} {text}")
