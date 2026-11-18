
from abc import ABC, abstractmethod
import re


class Entidad(ABC):
    """
    Clase abstracta que representa una entidad general
    dentro del sistema Software FJ.
    """

    def __init__(self, identificador):
        if not identificador or not str(identificador).strip():
            raise ValueError("El identificador no puede estar vacío.")

        self._identificador = str(identificador).strip()

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def validar(self):
        """Método que cada entidad debe implementar."""
        pass


class Cliente(Entidad):
    """
    Clase que representa a los clientes de Software FJ.
    Hereda de Entidad y protege sus datos personales.
    """

    def __init__(self, identificador, nombre, documento,
                 correo, telefono):

        super().__init__(identificador)

        self.__nombre = nombre
        self.__documento = documento
        self.__correo = correo
        self.__telefono = telefono

        self.validar()

    @property
    def nombre(self):
        return self.__nombre

    @property
    def documento(self):
        return self.__documento

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def validar(self):
        """Valida los datos personales del cliente."""

        if not isinstance(self.__nombre, str):
            raise TypeError("El nombre debe ser texto.")

        if len(self.__nombre.strip()) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres.")

        if not isinstance(self.__documento, str):
            raise TypeError("El documento debe ser texto.")

        if not re.fullmatch(r"\d{5,15}", self.__documento.strip()):
            raise ValueError(
                "El documento debe contener entre 5 y 15 dígitos."
            )

        if not isinstance(self.__correo, str):
            raise TypeError("El correo debe ser texto.")

        patron_correo = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"

        if not re.fullmatch(patron_correo, self.__correo.strip()):
            raise ValueError("El correo electrónico no es válido.")

        if not isinstance(self.__telefono, str):
            raise TypeError("El teléfono debe ser texto.")

        if not re.fullmatch(r"\+?\d{7,15}", self.__telefono.strip()):
            raise ValueError(
                "El teléfono debe contener entre 7 y 15 dígitos."
            )

        return True

    def __str__(self):
        return (
            f"Cliente: {self.__nombre} | "
            f"Documento: {self.__documento} | "
            f"Correo: {self.__correo} | "
            f"Teléfono: {self.__telefono}"
        )
