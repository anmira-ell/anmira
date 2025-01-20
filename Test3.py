for current_hour in range(0, 24):
    print("На часах " + str(current_hour) + ":00.")
    if current_hour < 6:
        print('Доброй ночи!') 
    elif current_hour < 12:
        print('Доброе утро!')
    elif current_hour < 18:
        print('Добрый день!')
    elif current_hour < 23:
        print('Добрый вечер!')
    else:
        print('Доброй ночи!')