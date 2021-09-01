def fib(num):
    if num == 0:
        return 0
    elif num == 1:
        return 1
    return fib(num - 1) + fib(num - 2)


print(fib(8))

def fib2(posicion):
    if posicion == 0:
        return 0
    if posicion == 1:
        return 1
    valor = 1
    resultado = 1
    for elemento in range(posicion-1):
        resultado = resultado + valor
    return resultado
print(fib(8))
