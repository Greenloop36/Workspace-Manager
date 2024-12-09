# Configuration
ProgramName = "WorkspaceManager"

# Imports
import colorama
from colorama import Fore, Back, Style
import os
import subprocess

# Init
colorama.init(autoreset=True)

# Variables
CurrentDirectory: str = __file__
Login: str = os.getlogin()

# Functions
def AdvanceCd(Path: str):
    CurrentDirectory += f"/{Path}"

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

class Commands_Container:
    pass