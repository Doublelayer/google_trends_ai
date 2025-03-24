import logging
import os


def setup_logger():
    """
    Erstellt und konfiguriert eine Logger-Instanz,
    die in allen anderen Dateien genutzt werden kann.
    """
    logger = logging.getLogger("app_logger")

    # Logging Level abhängig von ENV-Variable
    running_profile = os.getenv("RUNNING_PROFILE", "dev")
    log_level = logging.DEBUG if running_profile == "dev" else logging.INFO
    logger.setLevel(log_level)

    # Formatter für konsistente Log-Nachrichten
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # StreamHandler für Konsolenausgabe
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)

    # Datei-Handler für das Speichern in einer Datei
    file_handler = logging.FileHandler("app.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Handler zum Logger hinzufügen
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger


logger = setup_logger()
