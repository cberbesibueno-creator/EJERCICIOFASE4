# EJERCICOFASE4
# CRISTI ROSALIN BERBESI BUENO 
# BREYNER YESID GELVEZ BAUTISTA
# KAREN DANIELA OVIEDO GODOY
"""
Clase abstracta base del sistema.

Representa a cualquier "entidad general" de Software FJ (Cliente, Servicio,
Reserva). Centraliza lo que todas comparten: un identificador único y el
contrato de que toda entidad debe poder describirse a sí misma.
"""
from abc import ABC, abstractmethod


class Entidad(ABC):
    """Clase abstracta: no se puede instanciar directamente."""

    # Atributo de clase: contador compartido por todas las entidades
    _contador = 0

    def __init__(self):
        Entidad._contador += 1
        self._id = Entidad._contador  # encapsulado: solo lectura vía property

    @property
    def id(self) -> int:
        """Identificador único e inmutable de la entidad."""
        return self._id

    @abstractmethod
    def describir(self) -> str:
        """Devuelve una descripción legible. Cada subclase debe implementarla."""

    def __str__(self) -> str:
        return self.describir()

    def __repr__(self) -> str:
        return f"<{type(self).__name__} id={self._id}>"
