import os

from dotenv import load_dotenv
from pushover import Pushover

load_dotenv()

from logger_config import logger


def send(trend):
    po = Pushover(os.getenv("PUSHOVER_API_TOKEN"))
    po.user(os.getenv("PUSHOVER_USER"))

    msg = po.msg(f"{trend['summary']}\n\n* " + "\n\n* ".join(trend['sources']))

    msg.set("title", f"{trend["trend"]}\n({trend["search_volume"]})")

    logger.info(f"publish trend '{trend["trend"]}' to pushover")

    po.send(msg)


if __name__ == '__main__':
    send({
        "summary": "Das ist die Zusammenfassung",
        "trend": "Das ist der Titel"
    })
