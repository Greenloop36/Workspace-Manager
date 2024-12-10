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
global CurrentDirectory
CurrentDirectory: str = __file__
Login: str = os.getlogin()
CatchCommandExceptions = True
AutoList = False

# Functions
def YesNo(prompt: str = None) -> bool:
    print(prompt,"(Y/n)")

    while True:
        selection: str = input("> ")
        selection = selection.lower()

        if selection == "y":
            return True
        elif selection == "n":
            return False

def ClearWindow():
    os.system("cls")

def IsInt(Value: any) -> bool:
    try:
        int(Value)
    except ValueError:
        return False
    else:
        return True

def Pause():
    os.system("pause")

def AdvanceCd(Path: str):
    return CurrentDirectory + f"\\{Path}"

def RewindCd():
    global CurrentDirectory
    CurrentDirectory = os.path.dirname(CurrentDirectory)

def GetInputPrefix():
    Prefix = ""

    if not CatchCommandExceptions:
        Prefix += f"[{Fore.LIGHTRED_EX}unsafe{Fore.RESET}]"

    Prefix += Prefix != "" and " " or ""
    return f"{Prefix}{Fore.GREEN}{Login}@{ProgramName} {Fore.YELLOW}{CurrentDirectory}{Fore.MAGENTA}\n$ {Fore.RESET}"

def GetCommandArgs(Args: list, Separator: str | None = None, SeparatorEnd: int | None = None):
    if Separator == None:
        return Args[1]
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

def PrintSuccess(Message: str):
    print(f"{Fore.GREEN}success{Fore.RESET}: {Message}")

def CustomException(Message: str):
    print(f"{Fore.LIGHTRED_EX}{Message}{Fore.RESET}")

def Quit(Message: str, ErrorCode: int = 0):
    CustomException(Message)
    sys.exit(ErrorCode)

def ParseCommand(Query: str):
    if Query == "" or Query.startswith(" "):
        return
    
    Command: str = Query.split(" ")[0]
    Arguments: str = Query[len(Command) + 1:]
    
    Method: function = getattr(Commands, Command, None)

    if callable(Method):
        if CatchCommandExceptions:
            try:
                Method(Arguments)
            except Exception as e:
                print()
                if e == None or e == "":
                    e = "Unknown exception"
                CustomException(f"An exception occurred whilst running the command {Fore.LIGHTBLUE_EX}{Command}{Fore.LIGHTRED_EX}!\n{Fore.RESET}{Style.DIM}{e}{Style.RESET_ALL}")
        else:
            Method(Arguments)
    
    else:
        CustomException(f"\"{Command}\" is not recognised as an internal command.")

def NumberToPath(Index: int, MustBeDir: bool = False) -> tuple[bool, str]:
    Files = os.listdir(CurrentDirectory)

    if (0 <= Index) and (Index < len(Files)):
        if (not os.path.isfile(f"{CurrentDirectory}\\{Files[Index]}") and MustBeDir) or MustBeDir == False:
            return True, f"{CurrentDirectory}\\{Files[Index]}"
        else:
            return False, "Path does not exist"
    else:
        return False, "Index out of range"

class Commands_Container:
    def cd(*args):
        global CurrentDirectory
        path: str = GetCommandArgs(args)

        path = path.replace("/", "\\")

        if path == "__file__":
            CurrentDirectory = __file__
            RewindCd()
        elif os.path.exists(path):
            CurrentDirectory = path
        elif path == "":
            RewindCd()
        elif os.path.exists(AdvanceCd(path)) or IsInt(path):
            if not IsInt(path):
                NewPath = AdvanceCd(path)
                
                if os.path.isfile(NewPath):
                    Error("Path does not exist")
                else:
                    CurrentDirectory = NewPath
            else:
                Index = int(path)
                ValidPath, Result = NumberToPath(Index, True)

                if ValidPath:
                    CurrentDirectory = Result
                else:
                    Error(Result)

        else:
            Error(f"Unknown directory \"{Fore.BLUE}{path}{Fore.RESET}\"!")

    def lst(*args):
        Count: int = 0

        for i in os.listdir(CurrentDirectory):
            if os.path.isfile(f"{CurrentDirectory}\\{i}"):
                print(f"{Fore.CYAN}{Count}{Fore.RESET}: {i}")
            else:
                print(f"{Fore.CYAN}{Count}{Fore.RESET}: {Fore.YELLOW}{i}/{Fore.RESET}")
            
            Count += 1
    
    def launch(*args):
        path: str = GetCommandArgs(args)

        if IsInt(path):
            ValidPath, Result = NumberToPath(int(path), False)

            if ValidPath:
                path = Result
            else:
                Error(Result)
        else:
            path = FileInCd(path)

        try:
            os.startfile(path)
        except Exception as e:
            CustomException(f"This file cannot be started!\n{Fore.BLUE}{e}{Fore.RESET}")
    
    def catchexceptions(*args):
        global CatchCommandExceptions
        CatchCommandExceptions = not CatchCommandExceptions

        if not CatchCommandExceptions:
            Warning("Exceptions will no longer be caught!")
        else:
            print("Exceptions will now be caught.")

    def autolist(*args):
        global AutoList
        AutoList = not AutoList

        if not AutoList:
            Notice("Autolist is disabled.")
        else:
            Notice("Autolist is enabled.")
            Pause()
    
    def cls(*args):
        ClearWindow()
    
    def rem(*args):
        path: str = GetCommandArgs(args)

        if path == "":
            Error("Provide a file or directory to remove")
            return

        if IsInt(path):
            ValidPath, Result = NumberToPath(int(path), False)

            if ValidPath:
                path = Result
            else:
                Error(Result)
        else:
            path = FileInCd(path)

        if not YesNo(f"Will remove \"{Fore.YELLOW}{path}{Fore.RESET}\"!"):
            return

        try:
            if os.path.isfile(path):
                os.rmdir(path)
            else:
                os.remove(path)
        except Exception as e:
            if os.path.isfile(path):
                Error(f"Failed to remove \"{Fore.YELLOW}{path}{Fore.RESET}\"!\n{Fore.BLUE}{e}")
            else:
                Error(f"Failed to remove \"{Fore.YELLOW}{path}{Fore.RESET}\"! Is the directory empty?\n{Fore.BLUE}{e}")


Commands = Commands_Container()

if __name__ == "__main__":
    RewindCd()
    while True:
        
        try:
            os.listdir(CurrentDirectory)
        except PermissionError:
            Error(f"Access is denied to directory \"{Fore.YELLOW}{CurrentDirectory}{Fore.RESET}\"\n")
            RewindCd()
            continue
        except FileNotFoundError:
            Error(f"Unknown directory \"{Fore.YELLOW}{CurrentDirectory}{Fore.RESET}\"\n")
            RewindCd()
            continue

        if AutoList:
            ClearWindow()
            Commands.lst()
            print()

        try:
            Query: str = input(GetInputPrefix())
        except KeyboardInterrupt:
            Quit("KeyboardInterrupt")
        except EOFError:
            continue
        
        ParseCommand(Query)
        print()
        
        
