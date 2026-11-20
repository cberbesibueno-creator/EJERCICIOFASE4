"""
Gestor central de Software FJ.

Administra las listas internas de clientes, servicios y reservas
(sin base de datos) y registra los eventos en el archivo de logs.
"""
from cliente import Cliente
from servicios import Servicio
from reserva import Reserva
from excepciones import DatosInvalidosError
from logger_config import obtener_logger

logger = obtener_logger()


class GestorFJ:
    """Maneja las colecciones en memoria del sistema."""

    def __init__(self):
        # Listas internas: reemplazan a la base de datos.
        self._clientes = []
        self._servicios = []
        self._reservas = []

    # --- Registro --------------------------------------------------------

    def registrar_cliente(self, nombre, identificacion, correo, telefono):
        """Crea y registra un cliente; rechaza identificaciones duplicadas."""
        cliente = Cliente(nombre, identificacion, correo, telefono)
        if any(c.identificacion == cliente.identificacion for c in self._clientes):
            raise DatosInvalidosError(
                f"Ya existe un cliente con la identificación {cliente.identificacion}."
            )
        self._clientes.append(cliente)
        logger.info("Cliente registrado: %s", cliente.describir())
        return cliente

    def registrar_servicio(self, clase_servicio, *args, **kwargs):
        """Crea y registra un servicio de cualquier subclase de Servicio."""
        if not (isinstance(clase_servicio, type) and issubclass(clase_servicio, Servicio)):
            raise DatosInvalidosError("La clase indicada no es un tipo de Servicio.")
        servicio = clase_servicio(*args, **kwargs)
        self._servicios.append(servicio)
        logger.info("Servicio registrado: %s", servicio.describir())
        return servicio

    def crear_reserva(self, cliente, servicio, duracion, unidad_duracion, **opciones_costo):
        """Crea y registra una reserva."""
        reserva = Reserva(cliente, servicio, duracion, unidad_duracion, **opciones_costo)
        self._reservas.append(reserva)
        return reserva

    # --- Consulta (copias, para no exponer las listas internas) ----------

    @property
    def clientes(self):
        return list(self._clientes)

    @property
    def servicios(self):
        return list(self._servicios)

    @property
    def reservas(self):
        return list(self._reservas)
