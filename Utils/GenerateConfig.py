import os


def inicheck():
    if os.path.exists("../config.ini"):
        i = 11
        while i > 10:
            print("Config exists are you sure you want to over write it. Y/N")
            choice = input()
            if choice == "Y":
                write()
                exit()
            else:
                pass
            if choice == "y":
                write()
                exit()
            else:
                pass
            if choice == "N":
                exit()
            else:
                pass
            if choice == "n":
                exit()
            else:
                pass
            if choice == "yes":
                write()
                exit()
            else:
                pass
            if choice == "Yes":
                write()
                exit()
            else:
                pass
            if choice == "no":
                exit()
            else:
                pass
            if choice == "No":
                exit()
            else:
                pass
        else:
            print("Unknown Response")
    else:
        write()


def write():
    f = open("../config.ini", "a")  # THIS IS NOT CORRECT
    f.write("\n;This is a config file for the PikaChewniverse settings.")
    f.write("\n")
    f.write("\n[CHARACTER]")
    f.write("\nHost = 0.0.0.0")
    f.write("\nPort = 1002")
    f.write("\n")
    f.write("\n[AUTH]")
    f.write("\nHost = 0.0.0.0")
    f.write("\nPort = 1001")
    f.write("\n")
    f.write("\n[1100]")
    f.write("\nHost = 0.0.0.0")
    f.write("\nPort = 2100")
    f.write("\n")
    f.write("\n[1200]")
    f.write("\nHost = 0.0.0.0")
    f.write("\nPort = 2200")
    f.write("\n")
    f.write("\n[LOGGING]")
    f.write("\nLogOutput = True")
    f.write("\n")
    f.write("\n")
    f.close()


if __name__ == "__main__":
    inicheck()
