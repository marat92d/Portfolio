
#В массиве,найти наиболее самое близкое число к 0, и если их 2,и с разными знаками то вывести положительное:

def foo(lst):
    a=lst[0] #в переменную а записываем первое число из массива
    s=[a] #и сразу добавляем его в список
    for i in lst[1:]: #запускаем цикл во всем остальном массиве
        if abs(i)<abs(a): #сравниваем абсолютные значения
            s=[] #и меньшее число записываем в обнуленный список
            s+=[i]
            a=i
        elif abs(i)==a: #если число равно по модулю просто добавляем его в список
            s+=[i]
    return max(s) #в списке равных по абс. значению чисел выбираем максимальное, т.е. положительное
#lst2=[3,9,-5,-2,56,2,6,5]
#print(foo(lst2))
#Out:2
