# Software FJ – Sistema Integral de Gestión de Clientes, Servicios y Reservas

Proyecto del curso **Programación (213023)** – UNAD, Fase 4: estabilidad, robustez y manejo de errores.
Grupo de Programación 237.

Sistema orientado a objetos en Python 3, **sin base de datos**: los datos viven en objetos y listas; los archivos se usan únicamente para el registro de eventos y errores.

## Ejecución

```bash
python main.py
```

Requiere Python 3.8 o superior. No necesita instalar librerías externas. El log se genera en `logs/software_fj.log`.

## Estructura

| Archivo | Contenido |
|---|---|
| `excepciones.py` | Jerarquía de excepciones personalizadas (`SoftwareFJError` y derivadas). |
| `logger_config.py` | Configuración del archivo de logs. |
| `entidad.py` | Clase abstracta `Entidad` (id único + `describir()`). |
| `cliente.py` | `Cliente`: encapsulación y validaciones estrictas. |
| `servicios.py` | `Servicio` (abstracta) + `ReservaSala`, `AlquilerEquipo`, `Asesoria`. |
| `reserva.py` | `Reserva`: confirmar, cancelar y procesar con manejo de excepciones. |
| `gestor.py` | `GestorFJ`: listas internas de clientes, servicios y reservas. |
| `main.py` | Simulación de 20 operaciones válidas e inválidas. |

## Conceptos de POO aplicados

- **Abstracción:** `Entidad` y `Servicio` son clases abstractas (`ABC`, `@abstractmethod`).
- **Herencia:** `Cliente`, `Servicio` y `Reserva` heredan de `Entidad`; los tres servicios heredan de `Servicio`.
- **Polimorfismo:** `calcular_costo()` y `describir()` se sobrescriben en cada servicio.
- **Encapsulación:** atributos privados con `@property` y setters validados.
- **Sobrecarga (en Python):** `calcular_costo()` admite variantes con parámetros opcionales (`impuesto`, `descuento`, `cantidad`, `tarifa_especial`) y `calcular_costo_sin_impuesto()`.

## Manejo de excepciones

- Excepciones personalizadas: `DatosInvalidosError`, `ServicioNoDisponibleError`, `OperacionNoPermitidaError`, `CalculoInconsistenteError`, `ReservaError`.
- Bloques `try/except`, `try/except/else` y `try/except/else/finally` (`Reserva.procesar()`, `Reserva.confirmar()`, `main.ejecutar()`).
- Encadenamiento con `raise ReservaError(...) from error`.
- Todos los errores se registran en `logs/software_fj.log` y la aplicación continúa ejecutándose.

## Integrantes

- Cristi Rosalin Berbesi Bueno
- Breyner Yesid Gelvez Bautista
- Karen Daniela Oviedo Godoy
- (completar integrante 4)
- (completar integrante 5)
