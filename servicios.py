"""
Módulo de Servicios de Software FJ.

Define la clase abstracta Servicio y tres servicios especializados:
ReservaSala, AlquilerEquipo y Asesoria. Demuestra:
  - Abstracción: Servicio no se puede instanciar.
  - Herencia: los tres servicios heredan de Servicio.
  - Polimorfismo: cada uno sobrescribe calcular_costo() y describir().
  - Sobrecarga (en Python, mediante parámetros opcionales): calcular_costo()
    admite variantes con impuesto, descuento y parámetros propios de cada servicio.

Convención: impuesto y descuento son FRACCIONES entre 0 y 1 (0.19 = 19 %).
"""
import math
from abc import abstractmethod

from entidad import Entidad
from excepciones import (
    DatosInvalidosError,
    ServicioNoDisponibleError,
    CalculoInconsistenteError,
)

# ----------------------------------------------------------------------
# Funciones auxiliares de validación (privadas del módulo)
# ----------------------------------------------------------------------


def _es_numero(valor):
    """True si es int o float, excluyendo booleanos (True/False)."""
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


def _validar_texto(valor, campo):
    """Valida un texto obligatorio y devuelve su versión sin espacios."""
    if not isinstance(valor, str) or not valor.strip():
        raise DatosInvalidosError(f"El campo '{campo}' es obligatorio y debe ser texto.")
    return valor.strip()


def _validar_entero_positivo(valor, campo):
    """Valida que el valor sea un entero positivo (sin booleanos)."""
    if not isinstance(valor, int) or isinstance(valor, bool) or valor <= 0:
        raise DatosInvalidosError(f"El campo '{campo}' debe ser un entero positivo.")
    return valor


def _validar_calculo(duracion, impuesto, descuento):
    """Valida los parámetros comunes de cualquier cálculo de costo."""
    if not _es_numero(duracion) or duracion <= 0:
        raise DatosInvalidosError("La duración debe ser un número mayor que cero.")
    if not _es_numero(impuesto) or not 0 <= impuesto <= 1:
        raise DatosInvalidosError("El impuesto debe estar entre 0 y 1.")
    if not _es_numero(descuento) or not 0 <= descuento <= 1:
        raise DatosInvalidosError("El descuento debe estar entre 0 y 1.")


# ----------------------------------------------------------------------
# Clase abstracta Servicio
# ----------------------------------------------------------------------


class Servicio(Entidad):
    """Clase abstracta que representa cualquier servicio de Software FJ."""

    # Unidad en la que se cobra la tarifa; cada subclase la redefine.
    UNIDAD_TARIFA = "horas"

    def __init__(self, nombre, tarifa_base, disponible=True):
        # Valida antes de crear el id: un servicio inválido no consume id.
        nombre = _validar_texto(nombre, "nombre")
        if not _es_numero(tarifa_base) or tarifa_base <= 0:
            raise DatosInvalidosError("La tarifa base debe ser un número mayor que cero.")
        if not isinstance(disponible, bool):
            raise DatosInvalidosError("La disponibilidad debe ser verdadero o falso.")

        super().__init__()  # asigna el identificador único

        # Atributos privados (encapsulación).
        self._nombre = nombre
        self._tarifa_base = float(tarifa_base)
        self._disponible = disponible

    # --- Propiedades de solo lectura -----------------------------------

    @property
    def nombre(self):
        """Nombre del servicio."""
        return self._nombre

    @property
    def tarifa_base(self):
        """Tarifa base (por hora o por día según el servicio)."""
        return self._tarifa_base

    @property
    def disponible(self):
        """Indica si el servicio está disponible."""
        return self._disponible

    @property
    def unidad_tarifa(self):
        """Unidad en que se cobra el servicio ('horas' o 'días')."""
        return self.UNIDAD_TARIFA

    # --- Comportamiento común ------------------------------------------

    def cambiar_disponibilidad(self, disponible):
        """Activa o desactiva el servicio."""
        if not isinstance(disponible, bool):
            raise DatosInvalidosError("La disponibilidad debe ser verdadero o falso.")
        self._disponible = disponible

    def validar_disponibilidad(self):
        """Lanza ServicioNoDisponibleError si el servicio no está disponible."""
        if not self._disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self.nombre}' no está disponible.")

    @staticmethod
    def _aplicar_cargos(subtotal, impuesto, descuento):
        """Aplica impuesto y descuento al subtotal y verifica la coherencia."""
        total = round(subtotal * (1 + impuesto) * (1 - descuento), 2)
        # Un total no finito o menor/igual a cero es un cálculo inconsistente.
        if not math.isfinite(total) or total <= 0:
            raise CalculoInconsistenteError(
                f"El cálculo produjo un total inconsistente: {total}."
            )
        return total

    def calcular_costo_sin_impuesto(self, duracion, **opciones):
        """Variante del cálculo: costo sin impuesto (se reutiliza calcular_costo)."""
        return self.calcular_costo(duracion, impuesto=0, **opciones)

    # --- Métodos abstractos (contrato para las subclases) --------------

    @abstractmethod
    def calcular_costo(self, duracion, *args, **kwargs):
        """Calcula el costo total del servicio. Cada subclase lo implementa."""

    @abstractmethod
    def describir(self):
        """Describe el servicio. Cada subclase lo implementa."""


# ----------------------------------------------------------------------
# Servicios especializados
# ----------------------------------------------------------------------


class ReservaSala(Servicio):
    """Reserva de salas: se cobra por HORA."""

    UNIDAD_TARIFA = "horas"

    def __init__(self, nombre, tarifa_hora, capacidad, disponible=True):
        # Valida el atributo propio antes de construir la parte común.
        capacidad = _validar_entero_positivo(capacidad, "capacidad")
        super().__init__(nombre, tarifa_hora, disponible)
        self._capacidad = capacidad

    @property
    def capacidad(self):
        """Cantidad máxima de personas de la sala."""
        return self._capacidad

    def calcular_costo(self, duracion, impuesto=0.19, descuento=0):
        """Costo = tarifa * horas, con impuesto y descuento opcionales."""
        self.validar_disponibilidad()
        _validar_calculo(duracion, impuesto, descuento)
        subtotal = self._tarifa_base * duracion
        return self._aplicar_cargos(subtotal, impuesto, descuento)

    def describir(self):
        return (
            f"Sala '{self.nombre}' (ID {self.id}) | Capacidad: {self._capacidad} personas "
            f"| ${self._tarifa_base:,.0f} por hora"
        )


class AlquilerEquipo(Servicio):
    """Alquiler de equipos: se cobra por DÍA y por unidad."""

    UNIDAD_TARIFA = "días"

    def __init__(self, nombre, tarifa_dia, unidades, disponible=True):
        unidades = _validar_entero_positivo(unidades, "unidades")
        super().__init__(nombre, tarifa_dia, disponible)
        self._unidades = unidades

    @property
    def unidades(self):
        """Unidades disponibles del equipo."""
        return self._unidades

    def calcular_costo(self, duracion, impuesto=0.19, descuento=0, cantidad=1):
        """Costo = tarifa * días * cantidad, con impuesto y descuento opcionales."""
        self.validar_disponibilidad()
        _validar_calculo(duracion, impuesto, descuento)
        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad < 1:
            raise DatosInvalidosError("La cantidad debe ser un entero positivo.")
        if cantidad > self._unidades:
            raise DatosInvalidosError(
                f"La cantidad solicitada ({cantidad}) supera las unidades disponibles ({self._unidades})."
            )
        subtotal = self._tarifa_base * duracion * cantidad
        return self._aplicar_cargos(subtotal, impuesto, descuento)

    def describir(self):
        return (
            f"Equipo '{self.nombre}' (ID {self.id}) | Unidades: {self._unidades} "
            f"| ${self._tarifa_base:,.0f} por día"
        )


class Asesoria(Servicio):
    """Asesoría especializada: se cobra por HORA, con tarifa especial opcional."""

    UNIDAD_TARIFA = "horas"

    def __init__(self, nombre, tarifa_hora, especialidad, disponible=True):
        especialidad = _validar_texto(especialidad, "especialidad")
        super().__init__(nombre, tarifa_hora, disponible)
        self._especialidad = especialidad

    @property
    def especialidad(self):
        """Especialidad de la asesoría."""
        return self._especialidad

    def calcular_costo(self, duracion, impuesto=0.19, descuento=0, tarifa_especial=0):
        """Costo = tarifa * horas. Si hay tarifa_especial (>0), reemplaza la base."""
        self.validar_disponibilidad()
        _validar_calculo(duracion, impuesto, descuento)
        if not _es_numero(tarifa_especial) or tarifa_especial < 0:
            raise DatosInvalidosError("La tarifa especial debe ser un número no negativo.")
        tarifa = tarifa_especial if tarifa_especial > 0 else self._tarifa_base
        subtotal = tarifa * duracion
        return self._aplicar_cargos(subtotal, impuesto, descuento)

    def describir(self):
        return (
            f"Asesoría '{self.nombre}' (ID {self.id}) | Especialidad: {self._especialidad} "
            f"| ${self._tarifa_base:,.0f} por hora"
        )
