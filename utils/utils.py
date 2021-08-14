import os


def getch():
    if os.name == "posix":
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    elif os.name == "nt":
        import msvcrt
        return msvcrt.getch().decode("utf-8") 


def clear():
    if os.name == "nt":
        os.system('cls')
    else:
        os.system('clear')
