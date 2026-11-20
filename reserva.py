"""
Módulo Reserva de Software FJ.

Integra cliente, servicio, duración y estado. Implementa confirmación,
cancelación y procesamiento con manejo avanzado de excepciones:
  - try/except/else/finally en procesar() y confirmar()
  - encadenamiento de excepciones con 'raise ... from ...'
  - registro de eventos y errores en el archivo de logs
"""
from entidad import Entidad
from cliente import Cliente
from servicios import Servicio
from excepciones import (
    SoftwareFJError,
    DatosInvalidosError,
    ServicioNoDisponibleError,
    OperacionNoPermitidaError,
    ReservaError,
)
from logger_config import obtener_logger

logger = obtener_logger()

# Estados posibles de una reserva.
PENDIENTE = "Pendiente"
CONFIRMADA = "Confirmada"
PROCESADA = "Procesada"
CANCELADA = "Cancelada"


class Reserva(Entidad):
    """Representa una reserva de un servicio en Software FJ."""

    def __init__(self, cliente, servicio, duracion, unidad_duracion, **opciones_costo):
        """Crea una reserva.

        opciones_costo: parámetros opcionales para calcular el costo
        (impuesto, descuento, cantidad, tarifa_especial...).
        """
        # Comprueba los tipos de los objetos asociados.
        if not isinstance(cliente, Cliente):
            raise DatosInvalidosError("El cliente debe ser un objeto de la clase Cliente.")
        if not isinstance(servicio, Servicio):
            raise DatosInvalidosError("El servicio debe ser un objeto de la clase Servicio.")

        # Valida duración y unidad antes de crear la reserva.
        duracion = self._validar_duracion(duracion)
        unidad_duracion = self._validar_unidad(unidad_duracion)

        # La unidad de la reserva debe coincidir con la que cobra el servicio.
        if unidad_duracion != servicio.unidad_tarifa:
            raise DatosInvalidosError(
                f"El servicio '{servicio.nombre}' se reserva en {servicio.unidad_tarifa}, "
                f"no en {unidad_duracion}."
            )

        # Hereda de Entidad el identificador único de la reserva.
        super().__init__()

        # Atributos privados (encapsulación).
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._unidad_duracion = unidad_duracion
        self._opciones_costo = dict(opciones_costo)
        self._costo = None  # se calcula al procesar
        self._estado = PENDIENTE  # toda reserva comienza pendiente

        logger.info("Reserva %s creada (cliente %s, servicio %s)",
                    self.id, cliente.id, servicio.id)

    # ------------------------------------------------------------------
    # Validaciones
    # ------------------------------------------------------------------

    @staticmethod
    def _validar_duracion(duracion):
        """Comprueba que la duración sea un número positivo."""
        # Los booleanos son int en Python: se excluyen expresamente.
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)):
            raise DatosInvalidosError("La duración debe ser un valor numérico.")
        if duracion <= 0:
            raise DatosInvalidosError("La duración debe ser mayor que cero.")
        return duracion

    @staticmethod
    def _validar_unidad(unidad):
        """Comprueba que la unidad de duración sea válida."""
        if not isinstance(unidad, str):
            raise DatosInvalidosError("La unidad de duración debe ser texto.")
        unidad = unidad.strip().lower()
        if unidad == "dias":  # acepta la forma sin tilde
            unidad = "días"
        if unidad not in ("horas", "días"):
            raise DatosInvalidosError("La unidad debe ser horas o días.")
        return unidad

    # ------------------------------------------------------------------
    # Propiedades de consulta
    # ------------------------------------------------------------------

    @property
    def cliente(self):
        """Cliente asociado a la reserva."""
        return self._cliente

    @property
    def servicio(self):
        """Servicio asociado a la reserva."""
        return self._servicio

    @property
    def duracion(self):
        """Duración de la reserva."""
        return self._duracion

    @property
    def unidad_duracion(self):
        """Unidad de tiempo de la reserva."""
        return self._unidad_duracion

    @property
    def estado(self):
        """Estado actual de la reserva."""
        return self._estado

    @property
    def costo(self):
        """Costo total (None hasta que la reserva se procesa)."""
        return self._costo

    # ------------------------------------------------------------------
    # Operaciones de la reserva
    # ------------------------------------------------------------------

    def confirmar(self):
        """Confirma una reserva pendiente, verificando la disponibilidad."""
        if self._estado != PENDIENTE:
            raise OperacionNoPermitidaError("Solo se pueden confirmar reservas pendientes.")

        try:
            # Verifica que el servicio siga disponible.
            self._servicio.validar_disponibilidad()
        except ServicioNoDisponibleError as error:
            logger.error("Reserva %s: no se pudo confirmar (%s)", self.id, error)
            # Encadenamiento: conserva el error original como causa.
            raise ReservaError(
                f"No se pudo confirmar la reserva {self.id}."
            ) from error
        else:
            # Solo se ejecuta si NO hubo excepción.
            self._estado = CONFIRMADA
            logger.info("Reserva %s confirmada", self.id)
            return "La reserva ha sido confirmada correctamente."

    def cancelar(self):
        """Cancela una reserva pendiente o confirmada."""
        if self._estado not in (PENDIENTE, CONFIRMADA):
            raise OperacionNoPermitidaError(
                "Solo se pueden cancelar reservas pendientes o confirmadas."
            )
        self._estado = CANCELADA
        logger.info("Reserva %s cancelada", self.id)
        return "La reserva ha sido cancelada correctamente."

    def procesar(self):
        """Procesa una reserva confirmada y calcula su costo total."""
        if self._estado != CONFIRMADA:
            raise OperacionNoPermitidaError("Solo se pueden procesar reservas confirmadas.")

        try:
            # El servicio calcula el costo (polimorfismo: cada tipo lo hace distinto).
            costo = self._servicio.calcular_costo(self._duracion, **self._opciones_costo)
        except (SoftwareFJError, TypeError) as error:
            logger.error("Reserva %s: fallo al procesar (%s)", self.id, error)
            # Encadenamiento: el error original queda como __cause__.
            raise ReservaError(
                f"No se pudo procesar la reserva {self.id}."
            ) from error
        else:
            # Solo si el cálculo salió bien se actualiza el estado.
            self._costo = costo
            self._estado = PROCESADA
            logger.info("Reserva %s procesada. Costo total: %s", self.id, costo)
            return f"La reserva ha sido procesada correctamente. Total: ${costo:,.2f}"
        finally:
            # Se ejecuta SIEMPRE, haya o no error.
            logger.debug("Fin del intento de procesamiento de la reserva %s", self.id)

    # ------------------------------------------------------------------
    # Descripción
    # ------------------------------------------------------------------

    def describir(self):
        """Devuelve una descripción completa de la reserva."""
        costo = f"${self._costo:,.2f}" if self._costo is not None else "sin calcular"
        return (
            f"Reserva N.° {self.id} | Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} | "
            f"Duración: {self._duracion} {self._unidad_duracion} | "
            f"Estado: {self._estado} | Costo: {costo}"
        )
