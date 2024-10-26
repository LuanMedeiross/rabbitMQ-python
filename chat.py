from os import system, name

def banner():
    """
    Exibe um banner ASCII no terminal.
    """

    p_yellow('    ____        __    __    _ __  __  _______  ________  _____  ______')
    p_blue('   / __ \\____ _/ /_  / /_  (_) /_/  |/  / __ \\/ ____/ / / /   |/_  __/')
    p_green('  / /_/ / __ `/ __ \\/ __ \\/ / __/ /|_/ / / / / /   / /_/ / /| | / /   ')
    p_red(' / _, _/ /_/ / /_/ / /_/ / / /_/ /  / / /_/ / /___/ __  / ___ |/ /    ')
    p_yellow('/_/ |_|\\__,_/_.___/_.___/_/\\__/_/  /_/\\___\\_\\____/_/ /_/_/  |_/_/\n\n')

def clear():
    _ = system('cls') if name == 'nt' else system('clear')

def p_red(text, end='\n'):
    print(f"\033[3;31m{text}\033[0m", end=end)

def p_green(text, end='\n'):
    print(f"\033[3;32m{text}\033[0m", end=end)

def p_yellow(text, end='\n'):
    print(f"\033[3;33m{text}\033[0m", end=end)

def p_blue(text, end='\n'):
    print(f"\033[3;34m{text}\033[0m", end=end)

