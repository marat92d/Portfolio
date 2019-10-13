step=int(input())
stringr=input().strip()
alphavite=' abcdefghijklmnopqrstuvwxyz'
destring=''
for symb in stringr:
    index=alphavite.find(symb)
    destring+=alphavite[(index+step)%len(alphavite)]
print("Result: " + '"'+destring+'"')


Код,шифрующий текст шифром Цезаря.Шифр Цезаря заключается в замене каждого символа входной строки
на символ, находящийся на несколько позий левее или правее его алфавите. Для всех символов сдвиг 
один и тот же. Сдвиг циклический, т.е. если последнему символу применить единичный сдвиг, то он
заменится на первый символ и наооборот.