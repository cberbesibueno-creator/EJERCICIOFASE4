"""
Módulo Cliente de Software FJ.

Encapsula los datos personales del cliente (atributos privados + propiedades)
y aplica validaciones estrictas, lanzando DatosInvalidosError ante cualquier
dato inválido.
"""
import re

from entidad import Entidad
from excepciones import DatosInvalidosError


class Cliente(Entidad):
    """Representa un cliente registrado en Software FJ."""

    def __init__(self, nombre, identificacion, correo, telefono):
        """Inicializa un cliente con sus datos personales."""
        # Primero se valida todo: si algo falla, no se consume ningún id.
        nombre = self._validar_nombre(nombre)
        identificacion = self._validar_identificacion(identificacion)
        correo = self._validar_correo(correo)
        telefono = self._validar_telefono(telefono)

        # Solo con datos válidos se asigna el identificador único.
        super().__init__()

        # Atributos privados (encapsulación).
        self._nombre = nombre
        self._identificacion = identificacion
        self._correo = correo
        self._telefono = telefono

    # ------------------------------------------------------------------
    # Validaciones de los datos del cliente
    # ------------------------------------------------------------------

    @staticmethod
    def _validar_nombre(nombre):
        """Comprueba que el nombre tenga un formato válido."""
        if not isinstance(nombre, str):
            raise DatosInvalidosError("El nombre debe ser texto.")

        nombre = nombre.strip()  # elimina espacios al inicio y al final

        if not nombre:
            raise DatosInvalidosError("El nombre no puede estar vacío.")

        # Solo letras (con tildes y ñ), espacios, apóstrofes y guiones.
        patron = r"^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s'-]+$"
        if not re.fullmatch(patron, nombre):
            raise DatosInvalidosError("El nombre contiene caracteres no permitidos.")

        return nombre

    @staticmethod
    def _validar_identificacion(identificacion):
        """Comprueba que la identificación sea válida."""
        if not isinstance(identificacion, str):
            raise DatosInvalidosError("La identificación debe ser texto.")

        identificacion = identificacion.strip()

        if not identificacion:
            raise DatosInvalidosError("La identificación no puede estar vacía.")

        if not identificacion.isdigit():
            raise DatosInvalidosError("La identificación solo debe contener números.")

        return identificacion

    @staticmethod
    def _validar_correo(correo):
        """Comprueba que el correo tenga un formato válido."""
        if not isinstance(correo, str):
            raise DatosInvalidosError("El correo debe ser texto.")

        correo = correo.strip()

        if not correo:
            raise DatosInvalidosError("El correo no puede estar vacío.")

        # Formato general usuario@dominio.extension
        patron = r"^[\w.+-]+@[\w-]+(?:\.[\w-]+)*\.[a-zA-Z]{2,}$"
        if not re.fullmatch(patron, correo):
            raise DatosInvalidosError("El correo electrónico no tiene un formato válido.")

        return correo

    @staticmethod
    def _validar_telefono(telefono):
        """Comprueba que el teléfono tenga un formato válido."""
        if not isinstance(telefono, str):
            raise DatosInvalidosError("El teléfono debe ser texto.")

        telefono = telefono.strip()

        if not telefono:
            raise DatosInvalidosError("El teléfono no puede estar vacío.")

        if not telefono.isdigit():
            raise DatosInvalidosError("El teléfono solo debe contener números.")

        if not 7 <= len(telefono) <= 15:
            raise DatosInvalidosError("El teléfono debe tener entre 7 y 15 dígitos.")

        return telefono

    # ------------------------------------------------------------------
    # Propiedades de los atributos (getters y setters validados)
    # ------------------------------------------------------------------

    @property
    def nombre(self):
        """Permite consultar el nombre del cliente."""
        return self._nombre

    @nombre.setter
    def nombre(self, nuevo_nombre):
        """Modifica el nombre previa validación."""
        self._nombre = self._validar_nombre(nuevo_nombre)

    @property
    def identificacion(self):
        """Permite consultar la identificación (solo lectura)."""
        return self._identificacion

    @property
    def correo(self):
        """Permite consultar el correo del cliente."""
        return self._correo

    @correo.setter
    def correo(self, nuevo_correo):
        """Modifica el correo previa validación."""
        self._correo = self._validar_correo(nuevo_correo)

    @property
    def telefono(self):
        """Permite consultar el teléfono del cliente."""
        return self._telefono

    @telefono.setter
    def telefono(self, nuevo_telefono):
        """Modifica el teléfono previa validación."""
        self._telefono = self._validar_telefono(nuevo_telefono)

    # ------------------------------------------------------------------
    # Descripción de la entidad
    # ------------------------------------------------------------------

    def describir(self) -> str:
        """Devuelve una descripción de los datos del cliente."""
        return (
            f"Cliente N.° {self.id}: {self._nombre} | "
            f"ID: {self._identificacion} | "
            f"Correo: {self._correo} | "
            f"Tel: {self._telefono}"
        )
