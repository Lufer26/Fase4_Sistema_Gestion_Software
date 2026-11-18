
from entidades import Cliente

print("====================================")
print(" PRUEBAS DEL SISTEMA SOFTWARE FJ")
print("====================================")


# PRUEBA 1: Crear un cliente con datos correctos
print("\nPRUEBA 1: Registro de cliente válido")

try:
    cliente1 = Cliente(
        "C001",
        "Maria Perez",
        "12345678",
        "maria@gmail.com",
        "3001234567"
    )

    print("Cliente registrado correctamente.")
    print(cliente1)

except (ValueError, TypeError) as error:
    print("Error al registrar el cliente:", error)


# PRUEBA 2: Crear un cliente con correo incorrecto
print("\nPRUEBA 2: Correo electrónico inválido")

try:
    cliente2 = Cliente(
        "C002",
        "Carlos Gomez",
        "87654321",
        "correo_incorrecto",
        "3101234567"
    )

    print(cliente2)

except (ValueError, TypeError) as error:
    print("Error controlado:", error)


# PRUEBA 3: Crear un cliente con documento incorrecto
print("\nPRUEBA 3: Documento inválido")

try:
    cliente3 = Cliente(
        "C003",
        "Laura Torres",
        "ABC123",
        "laura@gmail.com",
        "3201234567"
    )

    print(cliente3)

except (ValueError, TypeError) as error:
    print("Error controlado:", error)


# PRUEBA 4: Crear un cliente con teléfono incorrecto
print("\nPRUEBA 4: Teléfono inválido")

try:
    cliente4 = Cliente(
        "C004",
        "Pedro Ruiz",
        "98765432",
        "pedro@gmail.com",
        "123"
    )

    print(cliente4)

except (ValueError, TypeError) as error:
    print("Error controlado:", error)


# PRUEBA 5: Crear un cliente con nombre muy corto
print("\nPRUEBA 5: Nombre inválido")

try:
    cliente5 = Cliente(
        "C005",
        "Lu",
        "11223344",
        "lu@gmail.com",
        "3151234567"
    )

    print(cliente5)

except (ValueError, TypeError) as error:
    print("Error controlado:", error)


# PRUEBA 6: Consultar los datos de un cliente válido
print("\nPRUEBA 6: Consultar datos del cliente")

try:
    print("Nombre:", cliente1.nombre)
    print("Documento:", cliente1.documento)
    print("Correo:", cliente1.correo)
    print("Teléfono:", cliente1.telefono)
    print("Identificador:", cliente1.identificador)

except NameError:
    print("No fue posible consultar los datos del cliente.")


print("\n====================================")
print(" FINALIZACIÓN DE LAS PRUEBAS")
print("====================================")
