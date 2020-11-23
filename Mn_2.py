import matplotlib.pyplot as plt
import math as m
import numpy as np
import matplotlib.animation as animation


class Point:
    # Класс Point - содержит координаты точки
    def __init__(self, point_input):
        self.x_axis = point_input[0]
        self.y_axis = point_input[1]

    # Просто удобный вывод, на всякий случай
    def __repr__(self):
        return "X coordinate: {}; Y coordinate: {}".format(self.x_axis, self.y_axis)


class Polygon:
    # Класс Polygon - многоугольник
    def __init__(self, point_arr, velocity_input):
        # Массивы координат многоугольника по X и Y
        self.x_axis_g = [point_arr[x].x_axis for x in range(len(point_arr))]
        self.y_axis_g = [point_arr[y].y_axis for y in range(len(point_arr))]

        # Ещё добавляем туда по первой точке. Т.о. у нас как бы список, от как пройти весь многоугольник
        self.x_axis_g.append(point_arr[0].x_axis)
        self.y_axis_g.append(point_arr[0].y_axis)

        # Скорость и угол её направления для многоугольника
        # Направление - относительно направление направо, против часовой стрелки, в радианах
        self.velocity = velocity_input[0]
        self.angle = velocity_input[1]

        # Массив коэф-тов a и b прямых, составляющих многоугольник
        self.a = []
        self.b = []

        # Скорость сближения. Её приобретёт многоугольник, если второй зафиксируем
        self.new_velocity = 0

        # Вычисление коэф-тов a
        for i in range(1, len(self.x_axis_g)):
            if not self.x_axis_g[i] - self.x_axis_g[i - 1] == 0:
                # "Нормальный" случай
                self.a.append((self.y_axis_g[i] - self.y_axis_g[i - 1]) / (self.x_axis_g[i] - self.x_axis_g[i - 1]))
            else:
                # X-ы одинаковые => вертикальная прямая, => уравнением y = ax + b так просто не опишется
                self.a.append(m.inf)

        # Вычисление коэф-тов b
        for i in range(len(self.x_axis_g) - 1):
            if not self.a[i] == m.inf:
                # "Нормальный" случай
                self.b.append(self.y_axis_g[i] - (self.a[i] * self.x_axis_g[i]))
            else:
                # Вертикальная прямая =>  надо сохранить лишь положение по x. Запишем его в b
                self.b.append(self.x_axis_g[i])

    # Если захотите построить многоугольники, см. далее
    # def ploting(self):
    #     pl = plt.plot(self.x_axis_g, self.y_axis_g, '-', label = 'Hi')
    #     return(pl)

    def a_ploting(self):
        apl = ax.plot(self.x_axis_g, self.y_axis_g, '-', label='Hi')
        return apl


point_input = []
point_coord = []
i = 0
point_arr = []
pgn_arr = []
velocity_input = []

for pngs in range(2):  # 2 многоугольника
    point_arr = []
    point_input = []

    print("Write coordinates of your points, please")
    print("Consistenly enter coordinates along the X and Y axis separated by SPACE, please")

    for point_input in iter(input, ''):
        point_input = point_input.split() # Вводим точки до пустой строки, разбиваем по пробелу

        # Проверка, ввели ли только 2 координаты
        if not len(point_input) == 2:
            print("ERROR: Two coordinates should be given")
            exit(0)

        # Проверка, ввели ли числа
        try:
            point_input[0] = float(point_input[0])
            point_input[1] = float(point_input[1])

        except:
            print("ERROR: Coordinates should be set by numbers")
            exit(0)

        point_arr.append(Point(point_input))  # Добавляем в массив точек новую точку

        i += 1

    # Вводим величину и направление скорости многоугольника
    print("Write velocity and its direction separated by SPACE, please")
    velocity_input = input().split()
    velocity_input = [float(i) for i in velocity_input]
    # Т.о. получаем массив [величина_скорости угол_скорости]
    # СДЕЛАТЬ ПРОВЕРКУ ВВОДА КАК ДЛЯ КООРДИНАТ (ну это так, для разминки)

    # Создаём многоугольник из полученный массивов точек и сторости
    p = Polygon(point_arr, velocity_input)
    pgn_arr.append(p)  # В массив многоугольников добавляем этот многоугольник

# Оставлю на всякий случай - это нарисовать введённые многоугольники
# for i in range(2):
#     pgn_arr[i].ploting()
#
# plt.show()

# Тут была заложена идея, которая не была реализована (она оказалась неправильной)
# Но в общем и целом - просто называем один многоугольник p_min, а другой - p_max
# Потом удобно работать с ними
p_min = pgn_arr[len(pgn_arr[0].x_axis_g) >= len(pgn_arr[1].x_axis_g)]
p_max = pgn_arr[len(pgn_arr[0].x_axis_g) < len(pgn_arr[1].x_axis_g)]

# Вычисляем проекции скорости сближения на оси X и Y
new_velocity_x = p_max.velocity * m.cos(p_max.angle) - p_min.velocity * m.cos(p_min.angle)
new_velocity_y = p_max.velocity * m.sin(p_max.angle) - p_min.velocity * m.sin(p_min.angle)
s = new_velocity_y / new_velocity_x  # Тангенс угла наклона скорости сближения
new_angle = m.atan(s)  # Угол наклона скорости сближения

# Величина скорости сближения
new_velocity = m.sqrt(new_velocity_x ** 2 + new_velocity_y ** 2)

dist_1 = []
arr_n1 = []
arr_n2 = []
# Ща буит мясо
# Фиксируем на месте многоугольник p_min. Он не двигается
# Берём грань многоугольника p_min
# Из каждой точки многоугольника p_max строим прямую, сонаправленную с вектором скорости сближения
# Берём точки пересечения этих прямых со взятой прямой-гранью
# Потом поймём, лежит ли эта точка пересечения на грани
for m1 in range(1, len(p_min.x_axis_g)):  # Берём грань многоугольника p_min
    for m2 in range(len(p_max.x_axis_g) - 1):  # Берём точки p_max
        # y = sx + k
        k = p_max.y_axis_g[m2] - (s * p_max.x_axis_g[m2])  # k прямой из точки p_max
        if not (p_min.a[m1 - 1] == 0 or p_min.a[m1 - 1] == m.inf):  # "Нормальный" случай
            x_p = (p_min.b[m1 - 1] - k) / (s - p_min.a[m1 - 1])
            y_p = s * x_p + k
        elif p_min.a[m1 - 1] == 0 and not s == 0:  # Грань - горизонтальная прямая, а скорость - не горизонтальная
            y_p = p_min.b[m1 - 1]
            x_p = (y_p - k) / s
        elif p_min.a[m1 - 1] == 0 and s == 0:  # И грань, и скорость горизонтальны
            if p_min.b[m1 - 1] == k:
                # У нас и скорость горизонтальна, и грань горизонтальна
                # Прямая может либо наложиться на прямую-грань, либо быть параллельной ей
                # Вот здель - накладывается
                y_p = k
                x_p = p_min.x_axis_g[m1 - 1]
            else:
                # А здесь - параллельна. Не пересекутся
                x_p = m.inf
                y_p = m.inf
        elif p_min.a[m1 - 1] == m.inf:  # Грань вертикальна
            x_p = p_min.b[m1 - 1]
            y_p = (s * x_p) + k

        # Проверяем, лежит ли точка пересечения на грани (уже как на отрезке, а не на прямой)
        if min(p_min.x_axis_g[m1 - 1], p_min.x_axis_g[m1]) <= x_p <= max(p_min.x_axis_g[m1 - 1], p_min.x_axis_g[m1])\
                and min(p_min.y_axis_g[m1 - 1], p_min.y_axis_g[m1]) <= y_p <= max(p_min.y_axis_g[m1 - 1], p_min.y_axis_g[m1]):
            # Расстояние между точкой пересечения и точкой p_max по оси X
            dist_1.append(abs(x_p - p_max.x_axis_g[m2]))
            arr_n1.append(m2)  # Номер подошедшей точки
            arr_n2.append(m1 - 1)  # Номер подошедшей грани

dist_2 = []
arr_n3 = []
arr_n4 = []

# Ну а здесь мы просто говорим - теперь p_min - это p_max, а p_max - это p_min
# И делаем то же самое ^_^'
# ОФОРМИТЕ ЭТО КАК ФУНКЦИЮ, НАВЕРНОЕ
(p_min, p_max) = (p_max, p_min)

for m1 in range(1, len(p_min.x_axis_g)):
    for m2 in range(len(p_max.x_axis_g) - 1):
        k = p_max.y_axis_g[m2] - (s * p_max.x_axis_g[m2])
        if not (p_min.a[m1 - 1] == 0 or p_min.a[m1 - 1] == m.inf):
            x_p = (p_min.b[m1 - 1] - k) / (s - p_min.a[m1 - 1])
            y_p = s * x_p + k
        elif p_min.a[m1 - 1] == 0 and not s == 0:
            y_p = p_min.b[m1 - 1]
            x_p = (y_p - k) / s
        elif p_min.a[m1 - 1] == 0 and s == 0:
            if p_min.b[m1 - 1] == k:
                y_p = k
                x_p = p_min.x_axis_g[m1 - 1]
            else:
                x_p = m.inf
                y_p = m.inf
        elif p_min.a[m1 - 1] == m.inf:
            x_p = p_min.b[m1 - 1]
            y_p = (s * x_p) + k

        if min(p_min.x_axis_g[m1 - 1], p_min.x_axis_g[m1]) <= x_p <= max(p_min.x_axis_g[m1 - 1], p_min.x_axis_g[m1])\
                and min(p_min.y_axis_g[m1 - 1], p_min.y_axis_g[m1]) <= y_p <= max(p_min.y_axis_g[m1 - 1], p_min.y_axis_g[m1]):
            dist_2.append(abs(x_p - p_max.x_axis_g[m2]))
            arr_n3.append(m2)
            arr_n4.append(m1 - 1)

# Если так получилось, что прямые одного многоугольника не пересекли ни одной грани другого
# Представьте себе магнитик на холодильнике. Ни одна горизонтальная прямая холодильника
# не пересекает грань магнитика
# Не пора ли нам подкрепиться?
if dist_1 == []:
    dist_1 = [m.inf]
if dist_2 == []:
    dist_2 = [m.inf]

min_1 = min(min(dist_1), min(dist_2))  # Самое минимальное расстояние между двумя точками

# Время, через которое многоугольники столкнутся
t = min_1 / new_velocity_x

if t < 0 or t == m.inf:
    print("Polygons won't collide")
    exit(0)
    # Но есть потенциально возможность сказать, что какое-то время назад были столкнувшимися
elif t == 0:
    print("Polygons are already collided")
    exit(0)

# Анимация :D
fig, ax = plt.subplots()

# Будем делать снимок каждые 0,25с. Поэтому там frame/4 будет
def animate(frame):
    ax.clear()  # Объяснение - ниже

    # Координаты вершин многоугольников по X и по Y в момент времени frame/4
    p_1_x = [p_max.x_axis_g[i] + (p_max.velocity * m.cos(p_max.angle) * frame/4) for i in range(len(p_max.x_axis_g))]
    p_1_y = [p_max.y_axis_g[i] + (p_max.velocity * m.sin(p_max.angle) * frame/4) for i in range(len(p_max.y_axis_g))]
    p_2_x = [p_min.x_axis_g[i] + (p_min.velocity * m.cos(p_min.angle) * frame/4) for i in range(len(p_min.x_axis_g))]
    p_2_y = [p_min.y_axis_g[i] + (p_min.velocity * m.sin(p_min.angle) * frame/4) for i in range(len(p_min.y_axis_g))]

    # Массивы точек многоугольников в момент времени frame/4
    point_arr_1 = [Point([p_1_x[i], p_1_y[i]]) for i in range(len(p_1_x))]
    point_arr_2 = [Point([p_2_x[i], p_2_y[i]]) for i in range(len(p_2_x))]

    # Многоугольники в момент времени frame/4
    P_1 = Polygon(point_arr_1, [0, 0])
    P_2 = Polygon(point_arr_2, [0, 0])

    # Рисуем эти самые многоугольники в момент времени frame/4
    # Тут в первом случае нет "curve =", т.к. когда мы делаем a_ploting, у нас изменяется ax
    # При следующем a_ploting эти изменения на стираются, а дополняются
    # Поэтому мы сначала в ax вписываем P_1, потом P_2 и присваеваем curve то, что в ax
    # Поэтому и ax.clear() в начале
    P_1.a_ploting()
    curve = P_2.a_ploting()
    ax.axis([0, 8, 0, 8]) # Просто какие-то рамки
    # НАДО НАПИСАТЬ, КАК ЭТИ РАМКИ ВЫЧИСЛЯТЬ
    plt.title('Time: {}'.format(round(frame/4, 2)), loc="center", fontsize=19)
    ax.grid(True)
    return curve


fr = [i for i in np.arange(0, 4*t, 0.1)]
if not fr[-1] == 4*t: # Надо нарисовать момент времени, когда столкнутся!
    fr.append(4*t)

curve_animation = animation.FuncAnimation(fig, animate, frames=[i for i in np.arange(0, 4*t, 0.25)], interval=3000, repeat=True, repeat_delay=2000)
curve_animation.save('p_animation.gif', writer='imagemagick', fps=10)
