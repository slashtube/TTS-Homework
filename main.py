import argoscuolanext
import datetime
import pyttsx3
from colorama import Fore, init
import readchar
import os


# Returns the indexes of the searched days
def get_indexes(d: list, date: str):
    date = date.split(" ", 1)[1]  # Splits the string to get only the date
    indexes = []  # List of indexes

    for i in range(len(d)):
        if d[i]['datCompiti'] == date:
            indexes.append(i)

    return indexes


# Returns the desired homeworks 
def get_homeworks(dati, ind: list):
    # Initialize tts engine
    engine = pyttsx3.init()
    # Set properties
    engine.setProperty('rate', 125)
    engine.setProperty('voice', 'italian')
    print(ind)
    for i in ind:
        print(dati[i]['docente'])
        print(dati[i]['desMateria'])
        engine.say(dati[i]['desMateria'])

        print(dati[i]['desCompiti'])
        engine.say(dati[i]['desCompiti'])
        print("\n")
        engine.runAndWait()
    engine.stop()


# Gets the days of the current week
def get_curdays():
    # gets today's date as starting value
    daycheck = datetime.date.today()
    daycheck = daycheck.strftime("%A")
    curdays = []
    if daycheck != "Sunday":
        i = 1
        # prints every day of the week with the respective date, except for Sunday
        while daycheck != "Saturday" and i < 7:
            # gets tomorrow's day
            weekday = datetime.date.today() + datetime.timedelta(days=i)
            daycheck = weekday.strftime("%A")
            # If the week ends
            if daycheck == "Sunday" and i == 1:
                print("La settimana e' finita. Riposati please")
            else:
                i += 1
                weekday = weekday.strftime("%A %Y-%m-%d")
                curdays.append(weekday)
    else:
        print("UE è frnnut a settiman. Ruomm")

    return curdays


# gets the days of the next week
def get_nextdays():
    curday = datetime.date.today().strftime("%A")
    nextdays = []
    i = 0
    if curday != "Monday":
        while curday != "Monday":
            i += 1
            temp = datetime.date.today() + datetime.timedelta(days=i)
            curday = temp.strftime("%A")
    while curday != "Saturday":
        temp = datetime.date.today() + datetime.timedelta(days=i)
        curday = temp.strftime("%A")
        weekday = temp.strftime("%A %Y-%m-%d")
        nextdays.append(weekday)
        i += 1

    return nextdays


# Logs into the ER, finds and eventually says the school homeworks
def say_homeworks(data):
    # ER Access Data
    session = argoscuolanext.Session("ssxxxxx", "username", "password")
    # Get homeworks
    compiti = session.compiti()
    dati = compiti['dati']
    # Finds the indexes of tomorrow's date
    indici = get_indexes(dati, data)
    if not indici:
        print("\n\nNon ci sono compiti per {0}".format(data))
    else:
        print("\n\nCompiti per {0}".format(data))
        get_homeworks(dati, indici)


def main():
    curdays = get_curdays()  # Gets list of remaining days of the week
    dim = len(curdays)  # Dimension of curdays[]
    nextdays = get_nextdays()  # Gets list of the days of the next week
    selectiony = 0  # This variable is used to keep trace of the selected choice, it is indeed used as index
    selectionx = 0  # This variable is used to switch through the tables
    prevy = 0  #
    init(autoreset=True)  # Sets autoreset at every print
    while True:
        print("\t\t\tMENU RICHIESTA COMPITI\n")
        j = 0
        i = 0
        while j != 6:
            if dim == 0:  # First case: curdays[] has no elements -> week has ended
                if selectiony == j:
                    print(Fore.GREEN + nextdays[j])
                else:
                    print(nextdays[j])
                j += 1
            else:  # Second case: curdays[] has elements
                try:
                    if j > dim:  # Prints the days in the same row
                        # Selection system
                        if selectionx == 0 and selectiony == i:
                            print(Fore.GREEN + curdays[selectiony] + Fore.RESET + "\t\t\t" + nextdays[j])
                        elif selectionx == 1 and selectiony == j:
                            print(curdays[i] + "\t\t\t" + Fore.GREEN + nextdays[selectiony])
                        else:
                            print(curdays[i] + "\t\t\t" + nextdays[j])
                        i += 1
                    else:  # This will execute if curdays[] is out of range
                        if selectionx == 1 and selectiony == j:
                            print(" " * 19 + "\t\t\t" + Fore.GREEN + nextdays[selectiony])
                        else:
                            print(" "*19 + "\t\t\t" + nextdays[j])

                except IndexError:  # In case one of the lists go out of index
                    print(Fore.RED + "ERRORE: " + Fore.RESET + "ARRAY FUORI INDICE")
                j += 1

        # Input system
        choice = readchar.readkey()
        if choice == '\x1b[A':  # up arrow is pressed
            if selectiony != 0:
                selectiony -= 1
        elif choice == '\x1b[B':  # down arrow is pressed
            if selectionx == 0:  # If the user is in the first column
                if dim == 0 and selectiony != 5:  # If he's in the First case
                    selectiony += 1
                elif dim != 0 and selectiony != dim-1:  # else if he's in the second case
                    selectiony += 1
            elif selectionx == 1 and selectiony != 5:  # or if he's the second case but he's in the second column
                selectiony += 1
        elif choice == '\x1b[C' and dim != 0:  # right arrow is pressed and it's not the First case
            if selectionx != 1:  # if he's not already in the second column
                # It swaps to the previous selection if there was
                temp = selectiony
                selectiony = prevy
                prevy = temp
                selectionx += 1
        elif choice == '\x1b[D':  # left arrow is pressed
            if selectionx != 0:  # If he's not already in the first column
                # It swaps to the previous selection if there was
                temp = selectiony
                selectiony = prevy
                prevy = temp
                selectionx -= 1
        elif choice == '\x0D':  # ENTER is pressed
            if selectionx == 0 and dim != 0:  # If he's in the first case
                date = curdays[selectiony]
                say_homeworks(date)
            elif selectionx == 0 and dim == 0:  # If he's in the second case and in the first column
                date = nextdays[selectiony]
                say_homeworks(date)
            elif selectionx == 1:  # Otherwise if he's in second column
                date = nextdays[selectiony]
                say_homeworks(date)
            input()
        os.system("clear")


if __name__ == '__main__':
    main()
