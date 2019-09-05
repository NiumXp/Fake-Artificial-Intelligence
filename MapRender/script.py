from os import listdir, system, name
from os.path import isfile, basename, split, abspath
from getpass import getuser
from sys import argv, exit as _exit
from re import match

NoReturn = None
user_name = getuser().title()

def _pause() -> NoReturn:
    'Pause the console'
    system('pause > nul' if name == 'nt' else 'read dummy')

def _clear() -> NoReturn:
    'Clear the console'
    system('cls' if name == 'nt' else 'clear')

def _pause_with_clear() -> NoReturn:
    _pause(); _clear()

def _pause_with_exit() -> NoReturn:
    _pause(); _exit()

def red(string: str):
    return "\033[1;91m" + string + "\033[0m"

def green(string: str):
    return "\033[1;32m" + string + "\033[0m"

def exit_print(message: str) -> NoReturn:
    if type(message) is not str:
        raise TypeError('expected str')
    else:
        print(green(message), "-> Press any key to exit.", sep='\n')
        _pause_with_exit()

def _spaces_and_arrow(amount_of_spaces: int, *, margin: int=8, arrow: str="^"):
    if type(amount_of_spaces) is not int:
        raise TypeError('expected int')
    elif type(arrow) is not str:
        raise TypeError('expected str')
    else:
        return (amount_of_spaces + margin) * " " + red(arrow)

def _valid_string(string: str) -> str:
    if type(string) is not str:
        raise TypeError('expected str')
    else:
        return string.isalpha()

def _line(*, lenght: int, middle_char: str=' '):
    if type(lenght) is not int:
        raise TypeError('expected int')
    elif type(middle_char) is not str:
        raise TypeError('expected str')
    else:
        return f".{middle_char * (lenght - 2)}."

def _create_map(dimension: tuple, name: str, path: str):
    with open(path + name + '.map', 'w') as file:
        lines = [
            _line(lenght=int(dimension[1]), middle_char='.') + '\n',
            *(_line(lenght=int(dimension[1])) + '\n' for _ in range(int(dimension[0]) - 2)),
            _line(lenght=int(dimension[1]), middle_char='.'),
            ]
        file.writelines(lines)

def _map_exists(name: str):
    if type(name) is not str:
        raise TypeError('expected int')
    else:
        return name + '.map' in listdir('./Maps')

if len(argv) > 1:
    if not argv[1].startswith('-'):
        print(_spaces_and_arrow(len(abspath(".")) + 1 + len(argv[0])))
        exit_print('\'-\' expected in the first argument.')
    else:
        _function = argv[1]
        if _function not in "-new-run":
            print(_spaces_and_arrow(len(abspath(".")) + 2 + len(argv[0])))
            exit_print(f'\'{_function}\' function not exists. (Try use "-new" or "-run")')
        else:
            if len(argv) > 2:
                _file_name = argv[2]
                if _valid_string(_file_name):
                    if _function in "-new":
                        if len(argv) > 3:
                            _dimension = argv[3]
                            _dimension_splited = _dimension.split('x')
                            if match(r"\b[1-9]\d+x[1-9]\d+\b", _dimension) and len(_dimension_splited) == 2:
                                try:
                                    _create_map(_dimension_splited, _file_name, './Maps/')
                                except Exception as error:
                                    exit_print(f'Could not create map. ({error.__class__.__name__}, {error})')
                                else:
                                    exit_print(f'{_file_name} created in \'./Maps/\'!')
                            else:
                                print(_spaces_and_arrow(len(abspath(".")) + len(_function) + len(argv[0]) + 4))
                                exit_print('Invalid dimension informed. (Example: 24x67)')
                        else:
                            print(_spaces_and_arrow(len(abspath(".")) + len(_function) + len(argv[0]) + 4))
                            exit_print('Dimension not informed.')
                    else:
                        if _map_exists(_file_name):
                            pass
                            # ------------------------------------------
                            # Map transform
                            # ------------------------------------------
                        else:
                            print(_spaces_and_arrow(len(abspath(".")) + len(_function) + len(argv[0]) + 2))
                            exit_print('Map not found. (Make sure the map is in the "Maps" folder)')
                else:
                    print(_spaces_and_arrow(len(abspath(".")) + len(_function) + len(argv[0]) + 2))
                    exit_print('Invalid name informed. (Use only letters. Example: NiumMap)')
            else:
                print(_spaces_and_arrow(len(abspath(".")) + len(_function) + len(argv[0]) + 2))
                exit_print('Name not informed. (Read "Functions" in GitHub README for help)')
else:
    print(_spaces_and_arrow(len(abspath(".")) + 1 + len(argv[0])))
    exit_print('Function not informed. (Functions: "-new" and "-run")')
