#программа, которая считывает названия двух основных цветов для смешивания
a = str(input())
b = str(input())
red = 'красный'
yel = 'желтый'
blue = 'синий'
if (a == blue or a == red) and (b == red or b == blue) and (a != b):
    print('фиолетовый')
elif a == b == red:
    print(red)
elif b == a == blue:
    print(blue)
elif (a == yel or a == red) and (b == red or b == yel) and (a != b):
    print('оранжевый')
elif a == b == yel:
    print(yel)
elif b == a == red:
    print(red)
elif (a == yel or a == blue) and (b == blue or b == yel) and (a != b):
    print('зеленый')
elif a == b == blue:
    print(blue)
elif b == a == yel:
    print(yel)
elif (a != yel or a != blue or a != red ) and (b != blue or b != yel or b != red):
    print('ошибка цвета')