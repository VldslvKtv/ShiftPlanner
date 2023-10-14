# -*- coding:utf-8 -*-
import random


class Employee:
    def __init__(self, name, working_days=0):
        self.name = name
        self.working_days = working_days

    def __str__(self):
        return f'{self.name}'


# Константы
DAYS_IN_MONTH = [28, 30, 31]
SHIFT_DURATION = 12
AVERAGE_LOAD = [3, 4]
START_TIMES = ['08:00', '10:00']
END_TIMES = ['20:00', '22:00']
WEEKDAYS = {
    '1': 'Понедельник',
    '2': 'Вторник',
    '3': 'Среда',
    '4': 'Четверг',
    '5': 'Пятница',
    '6': 'Суббота',
    '7': 'Воскресенье'
}
# Работники
WORKERS = [Employee('worker' + str(i)) for i in range(1, 11)]


# Вывод загруженности работника
def print_workers():
    for worker in WORKERS:
        print(f'{worker.name}, Количество рабочих дней: {worker.working_days}')


# Вывод расписания на конкретный день
def print_shifts(shifts_day):
    for s in shifts_day:
        for k, v in s.items():
            print("{} - {}".format(k, v))
    print('\n')


# Проверка номера дня недели
def check_of_the_day(day):
    if day >= 7:
        return 1
    return day + 1


# Проверка занятости сотрудника. Так как максимум 144 часа, то есть 12 дней по 12 часов,
#  значит больше 12 дней быть не может
def check_worker(worker: Employee, workers: list):
    if worker.working_days < SHIFT_DURATION and worker not in workers:
        worker.working_days += 1
        return True
    return False


# Распределение количества сотрудников исходя из средней нагрузки. Если дней 28, то средняя нагрузка будет
# 4 дня, а если дней 30 или 31 - 3 дня. Если брать среднюю нагрузку больше, то нельзя будет равномерно
# распределить сотрудников по дням с учетом +1/-1 сотрудник по понедельникам/воскресеньям.
def workers_by_day(month_days, weekday):
    if month_days == DAYS_IN_MONTH[0]:
        workers = [AVERAGE_LOAD[1] for _ in range(month_days)]
    else:
        workers = [AVERAGE_LOAD[0] for _ in range(month_days)]
    for i in range(len(workers)):
        if weekday == 1:
            workers[i] += 1
        elif weekday == 7:
            workers[i] -= 1
        weekday = check_of_the_day(weekday)
    return workers


# Генерация расписания на конкретный день
def shifts(workers_needed):
    mas_worker = []
    schedule_day = []
    hours_assigned = 0
    count = -1
    daily_load = SHIFT_DURATION * workers_needed
    while hours_assigned < daily_load:
        worker = random.choice(WORKERS)
        if check_worker(worker, mas_worker):
            count += 1
            hours_assigned += 12
            if count == 0:
                start_time = START_TIMES[0]
            else:
                start_time = random.choice(START_TIMES)
            end_time = END_TIMES[START_TIMES.index(start_time)]
            mas_worker.append(worker)
            schedule_day.append({f'Сотрудник {str(worker)}': f'Рабочий день: {start_time}-{end_time}'})
    return schedule_day


# Генерации расписания смен на месяц
def generate_schedule(month_days, weekday):
    schdl = []

    workers_per_day = workers_by_day(month_days, weekday)

    for i in range(len(workers_per_day)):
        workers_needed = workers_per_day[i]
        schdl.append({f'{WEEKDAYS[str(weekday)]}, День {i + 1}': shifts(workers_needed)})
        weekday = check_of_the_day(weekday)

    return schdl


# Проверка ввода целого числа
def validate_int():
    """Проверка ввода данных типа int."""
    while True:
        try:
            int_obj = int(input())
        except ValueError:
            print('Введите целое неотрицательное число.')
        else:
            return int_obj


# Проверка на корректность дней в месяце и номера дня недели
def validate_date(days_in_month, weekday):
    if days_in_month in DAYS_IN_MONTH and 1 <= weekday <= 7:
        return True
    return False


# Ввод количества дней в месяце и номера дня недели
def input_date():
    print('Какое количество дней в месяце? (ввести один из трех вариантов: 28, 30, 31)')
    days_in_month = validate_int()
    print('С какого дня недели начать? (ввести число от 1 до 7)')
    weekday = validate_int()
    return days_in_month, weekday


# Основная программа
amount_of_days, wday = input_date()
while True:
    if validate_date(amount_of_days, wday):
        schedule = generate_schedule(amount_of_days, wday)
        for shift in schedule:
            for key, value in shift.items():
                print("{}: ".format(key))
                print_shifts(value)
        print(f'Общая загруженность работников:')
        print_workers()
        exit(0)
    else:
        print('Были введены некорректные данные. Повторите попытку.')
        amount_of_days, wday = input_date()
