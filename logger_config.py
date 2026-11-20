"""
Configuración del archivo de logs de Software FJ.

Todos los errores y eventos relevantes se registran en logs/software_fj.log.
Los archivos se usan ÚNICAMENTE para logs (no hay base de datos).
"""
import logging
from pathlib import Path

# Carpeta y archivo de logs, junto a este módulo.
CARPETA_LOGS = Path(__file__).resolve().parent / "logs"
ARCHIVO_LOG = CARPETA_LOGS / "software_fj.log"


def obtener_logger(nombre: str = "software_fj") -> logging.Logger:
    """Devuelve un logger configurado que escribe en el archivo de logs."""
    # Crea la carpeta de logs si todavía no existe.
    CARPETA_LOGS.mkdir(exist_ok=True)

    # Todos los módulos comparten el mismo logger raíz "software_fj".
    logger = logging.getLogger("software_fj")

    # Evita añadir handlers duplicados si la función se llama varias veces.
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        manejador = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(module)s | %(message)s"
        )
        manejador.setFormatter(formato)
        logger.addHandler(manejador)
        logger.propagate = False  # no duplicar mensajes en la consola

    return logger
