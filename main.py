"""
Software FJ - Simulación de operaciones.

Ejecuta 18 operaciones (válidas e inválidas) sobre clientes, servicios y
reservas. Cada error se captura, se muestra, se registra en logs/software_fj.log
y el programa continúa: la aplicación nunca se detiene por un error.
"""
import sys

from gestor import GestorFJ
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from excepciones import SoftwareFJError
from logger_config import obtener_logger, ARCHIVO_LOG

logger = obtener_logger()

# Contadores para el resumen final.
resumen = {"exitosas": 0, "errores_controlados": 0, "errores_inesperados": 0}


def ejecutar(numero, titulo, operacion):
    """Ejecuta una operación protegiéndola con try/except/else/finally.

    Devuelve el resultado, o None si la operación falló.
    """
    print(f"\n[{numero:02d}] {titulo}")
    logger.info("--- Operación %02d: %s", numero, titulo)
    try:
        resultado = operacion()
    except SoftwareFJError as error:
        # Error propio del sistema: se muestra y se registra.
        resumen["errores_controlados"] += 1
        print(f"     ERROR CONTROLADO ({type(error).__name__}): {error}")
        logger.error("Operación %02d falló [%s]: %s", numero, type(error).__name__, error)
        # Si el error fue encadenado, se muestra y registra la causa original.
        if error.__cause__ is not None:
            causa = error.__cause__
            print(f"     Causa original ({type(causa).__name__}): {causa}")
            logger.error("   Causa original [%s]: %s", type(causa).__name__, causa)
        return None
    except Exception as error:  # cualquier otro error inesperado
        resumen["errores_inesperados"] += 1
        print(f"     ERROR INESPERADO ({type(error).__name__}): {error}")
        logger.exception("Operación %02d: error inesperado", numero)
        return None
    else:
        # Solo si no hubo excepción.
        resumen["exitosas"] += 1
        print(f"     OK -> {resultado}")
        logger.info("Operación %02d completada correctamente", numero)
        return resultado
    finally:
        # Siempre se ejecuta, con o sin error.
        logger.debug("Fin de la operación %02d", numero)


def main():
    """Función principal: orquesta las 18 operaciones de la simulación."""
    # Evita problemas de tildes en consolas de Windows.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass

    gestor = GestorFJ()
    logger.info("=== INICIO DE LA SIMULACIÓN DE SOFTWARE FJ ===")
    print("=== SOFTWARE FJ: SIMULACIÓN DE OPERACIONES ===")

    # ------------------------- CLIENTES --------------------------------
    maria = ejecutar(1, "Registrar cliente válido (María José)",
                     lambda: gestor.registrar_cliente(
                         "María José", "1098765432", "maria@gmail.com", "3001234567"))

    carlos = ejecutar(2, "Registrar cliente válido (Carlos Pérez)",
                      lambda: gestor.registrar_cliente(
                          "Carlos Pérez", "1010101010", "carlos@correo.co", "3109876543"))

    ejecutar(3, "Cliente INVÁLIDO: correo sin formato correcto",
             lambda: gestor.registrar_cliente(
                 "Ana Ruiz", "1234567890", "ana-sin-arroba.com", "3001112233"))

    ejecutar(4, "Cliente INVÁLIDO: identificación con letras y teléfono corto",
             lambda: gestor.registrar_cliente("Luis Gómez", "12AB34", "luis@mail.com", "123"))

    ejecutar(5, "Cliente INVÁLIDO: identificación duplicada",
             lambda: gestor.registrar_cliente(
                 "María Clon", "1098765432", "clon@mail.com", "3005556677"))

    # ------------------------- SERVICIOS -------------------------------
    sala = ejecutar(6, "Crear servicio válido: Sala de reuniones",
                    lambda: gestor.registrar_servicio(
                        ReservaSala, "Sala Ejecutiva", 50000, 12))

    equipo = ejecutar(7, "Crear servicio válido: Alquiler de portátiles",
                      lambda: gestor.registrar_servicio(
                          AlquilerEquipo, "Portátil Pro", 30000, 5))

    asesoria = ejecutar(8, "Crear servicio válido: Asesoría en Python",
                        lambda: gestor.registrar_servicio(
                            Asesoria, "Asesoría Python", 80000, "Desarrollo de software"))

    ejecutar(9, "Servicio INVÁLIDO: tarifa negativa",
             lambda: gestor.registrar_servicio(ReservaSala, "Sala Rota", -100, 8))

    # ------------------------- RESERVAS --------------------------------
    # Reserva exitosa completa: crear -> confirmar -> procesar.
    def reserva_exitosa_sala():
        reserva = gestor.crear_reserva(maria, sala, 3, "horas")
        reserva.confirmar()
        return reserva.procesar()

    ejecutar(10, "Reserva EXITOSA: sala 3 horas (con IVA 19 %)", reserva_exitosa_sala)

    # Reserva exitosa con parámetros opcionales (descuento y cantidad).
    def reserva_exitosa_equipo():
        reserva = gestor.crear_reserva(carlos, equipo, 2, "días", descuento=0.10, cantidad=2)
        reserva.confirmar()
        return reserva.procesar()

    ejecutar(11, "Reserva EXITOSA: 2 portátiles por 2 días con 10 % de descuento",
             reserva_exitosa_equipo)

    # Reserva exitosa con tarifa especial.
    def reserva_exitosa_asesoria():
        reserva = gestor.crear_reserva(maria, asesoria, 2, "horas", tarifa_especial=60000)
        reserva.confirmar()
        return reserva.procesar()

    ejecutar(12, "Reserva EXITOSA: asesoría 2 horas con tarifa especial",
             reserva_exitosa_asesoria)

    ejecutar(13, "Reserva FALLIDA: el cliente no es un objeto Cliente",
             lambda: gestor.crear_reserva("María", sala, 2, "horas"))

    ejecutar(14, "Reserva FALLIDA: duración negativa",
             lambda: gestor.crear_reserva(maria, sala, -5, "horas"))

    ejecutar(15, "Reserva FALLIDA: equipo reservado en horas (se cobra por día)",
             lambda: gestor.crear_reserva(carlos, equipo, 3, "horas"))

    # Servicio que deja de estar disponible antes de confirmar.
    def reserva_servicio_no_disponible():
        reserva = gestor.crear_reserva(carlos, sala, 1, "horas")
        sala.cambiar_disponibilidad(False)  # el servicio se desactiva
        try:
            return reserva.confirmar()
        finally:
            sala.cambiar_disponibilidad(True)  # se restablece para seguir operando

    ejecutar(16, "Reserva FALLIDA: servicio no disponible al confirmar (error encadenado)",
             reserva_servicio_no_disponible)

    # Operación no permitida: procesar sin confirmar.
    def procesar_sin_confirmar():
        reserva = gestor.crear_reserva(maria, sala, 1, "horas")
        return reserva.procesar()

    ejecutar(17, "Operación NO PERMITIDA: procesar una reserva sin confirmar",
             procesar_sin_confirmar)

    # Cálculo inconsistente: descuento del 100 % deja el total en cero.
    def calculo_inconsistente():
        reserva = gestor.crear_reserva(maria, sala, 2, "horas", descuento=1)
        reserva.confirmar()
        return reserva.procesar()

    ejecutar(18, "Cálculo INCONSISTENTE: descuento del 100 % (error encadenado)",
             calculo_inconsistente)

    # Cancelación válida y luego intento inválido de confirmar.
    def cancelar_y_reconfirmar():
        reserva = gestor.crear_reserva(carlos, asesoria, 1, "horas")
        print("     " + reserva.cancelar())
        return reserva.confirmar()  # debe fallar: ya está cancelada

    ejecutar(19, "Cancelar una reserva y luego intentar confirmarla",
             cancelar_y_reconfirmar)

    # Error inesperado (no es de Software FJ): el sistema también lo contiene.
    ejecutar(20, "Error INESPERADO: división por cero fuera del dominio",
             lambda: 1 / 0)

    # ------------------------- RESULTADOS ------------------------------
    print("\n=== POLIMORFISMO: descripción de todos los servicios ===")
    for servicio in gestor.servicios:
        print("  -", servicio.describir())

    print("\n=== RESERVAS REGISTRADAS ===")
    for reserva in gestor.reservas:
        print("  -", reserva.describir())

    print("\n=== RESUMEN ===")
    print(f"  Operaciones exitosas:      {resumen['exitosas']}")
    print(f"  Errores controlados:       {resumen['errores_controlados']}")
    print(f"  Errores inesperados:       {resumen['errores_inesperados']}")
    print(f"  Total de operaciones:      {sum(resumen.values())}")
    print(f"  Archivo de logs:           {ARCHIVO_LOG}")
    print("El programa terminó SIN interrumpirse.")

    logger.info("=== FIN DE LA SIMULACIÓN === %s", resumen)


if __name__ == "__main__":
    main()
