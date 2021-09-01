def fib(num):
    if num == 0:
        return 0
    elif num == 1:
        return 1
    return fib(num - 1) + fib(num - 2)




def fib2(posicion):
    if posicion < 0:
        return "No se puede con una posicion menor a 0"
    if posicion == 0:
        return 0
    if posicion == 1:
        return 1
    valor = 1
    resultado = 0
    for elemento in range(posicion):
        aux = resultado
        resultado = resultado + valor
        valor = aux
    return resultado

valor = 3
print(fib(valor))
print(fib2(valor))
