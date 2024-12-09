# Configuration
ProgramName = "WorkspaceManager"

# Imports
import colorama
from colorama import Fore, Back, Style
import os
import subprocess
import sys

# Init
colorama.init(autoreset=True)

# Variables
CurrentDirectory: str = __file__
Login: str = os.getlogin()

# Functions
def AdvanceCd(Path: str):
    return CurrentDirectory + f"/{Path}"

def RewindCd():
    CurrentDirectory = os.path.dirname(CurrentDirectory)

def GetInputPrefix():
    return f"{Fore.GREEN}{Login}@{ProgramName} {Fore.YELLOW}{CurrentDirectory}{Fore.MAGENTA}\n$ {Fore.RESET}"

def GetCommandArgs(Args: list, Separator: str | None, SeparatorEnd: int | None):
    if Separator == None:
        return Args[1:]
    else:
        CommandArgs: str = Args[1]
        Parsed: list[str] = CommandArgs.split(Separator, maxsplit=SeparatorEnd)

def FileInCd(Name: str):
    return CurrentDirectory + "/" + Name

def Error(Message: str):
    print(f"{Fore.RED}error{Fore.RESET}: {Message}")

def Warning(Message: str):
    print(f"{Fore.LIGHTYELLOW_EX}warning{Fore.RESET}: {Message}")

def Notice(Message: str):
    print(f"{Fore.LIGHTMAGENTA_EX}notice{Fore.RESET}: {Message}")

def Success(Message: str):
    print(f"{Fore.GREEN}success{Fore.RESET}: {Message}")

def CustomException(Message: str):
    print(f"{Fore.LIGHTRED_EX}{Message}{Fore.RESET}")

def Quit(Message: str, ErrorCode: int = 0):
    CustomException(Message)
    sys.exit(ErrorCode)

class Commands_Container:
    def cd(*args):
        path = GetCommandArgs(args)

        if os.path.exists(path):
            CurrentDirectory = path
        elif os.path.exists(AdvanceCd(path)):
            CurrentDirectory = AdvanceCd(path)
        elif path == "":
            RewindCd()
        else:
            Error(f"Unknown directory \"{Fore.BLUE}{path}{Fore.RESET}\"!")
    

    def lst(*args):
        for i in os.listdir(CurrentDirectory):
            if os.path.isfile(i):
                print(f"{i}")
            else:
                print(f"{Fore.YELLOW}{i}/{Fore.RESET}")
    
    def launch(*args):
        os.startfile(FileInCd())


if __name__ == "__main__":
    while True:
        try:
            Query: str = input(GetInputPrefix())
        except KeyboardInterrupt:
            Quit("KeyboardInterrupt")
        except EOFError:
            continue
        
        
