#программа, которая находит пересечение двух отрезков (a1;b1 и a2;b2), гарантируется, что a1 < b1 и a2 < b2

a1 = int(input())
b1 = int(input())
a2 = int(input())
b2 = int(input())

if a1 < b1 < a2 < b2:
    print("пустое множество")
elif a2 < b2 < a1 < b1:
    print("пустое множество")
elif a1 < a2 < b2 < b1:
    print(a2, b2)
elif a1 < a2 < b1 < b2:
    print(a2, b1)
elif a2 < a1 < b2 < b1:
    print(a1, b2)
elif a2 < a1 < b1 < b2:
    print(a1, b1)
elif a1 < b1 == a2 < b2:
    print(b1)
elif a2 < b2 == a1 < b1:
    print(b2)
elif a1 == a2 and b1 == b2:
    print(a1,b1)
elif a1 == a2 < b1 < b2:
    print(a1, b1)
elif a2 < a1 < b1 == b2:
    print(a1,b1)
elif a1 < a2 < b2 == b1:
    print(a2,b2)
elif a1 == a2 < b2 < b1:
    print(a2, b2)