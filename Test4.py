def rooms_equal(room_size, room_list):
    count = 0

    for room in room_list:
        if room == room_size:
            count = count + 1

    print('Комнат площадью', room_size, 'кв.м:', count)

flat = [
    5.55, 22.19, 7.78, 26.86, 5.55,
    29.84, 22.19, 5.55, 16.85, 4.52
]

hut = [9.2, 3.5, 8.1, 2.3, 9.2, 4.2, 6.9]

rooms_equal(5.55, flat)
rooms_equal(9.2, hut)