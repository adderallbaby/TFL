import StateEliminator 
if __name__ == "__main__":
    alpha = input('Введите алфавит без точек и запятых (например, abcde): ')
    regex = input('Введите регулярное выражение: ')
    StateEliminator.main(alpha, regex)
