class DomainException(Exception):
    """Excepción base para todas las reglas de negocio del dominio."""
    pass


class DatosInvalidosError(DomainException):
    """Se lanza cuando un dato no cumple las reglas de negocio del dominio."""
    pass
