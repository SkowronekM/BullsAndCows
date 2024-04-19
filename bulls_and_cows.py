import random

def menu():
    menu = {
        1: 'Nowa gra',
        2: 'Zasady gry',
        3: 'Koniec'
    }

    for i in menu.keys():
        print(i, ': ', menu[i])

def zasady():
    print('\nTekstowa gra w której komputer (Host) losuje słowo które jest izogramem\n'
          '(izogram jest to wyraz w którym nie powtarzają się żadne litery) i informuje\n'
          'użytkownika (Guesser) o ilości liter w słowie. Użytkownik (Guesser) stara się zgadnąć\n'
          'co to za słowo. Komputer (Host) po każdej próbie zwraca liczbe  Cows & Bulls. Liczba\n'
          'przy słowie Cows oznacza literę występującą w słowie lecz na złej pozycji,\n'
          'liczba przy słowie Bulls oznacza poprawną literę na poprawnej pozycji. Gra kończy się,\n'
          'kiedy liczba przy Bulls będzie taka sama jak długość słowa wylosowanego przez komputer.\n')

def liczenie_stat(stats, generated_word, user_word):
    stats.zeruj()
    for i, letter in enumerate(user_word):
        index = generated_word.find(letter)
        if index != -1:
            if generated_word[i] == letter:
                stats.add_bulls()
            else:
                stats.add_cows()

class Engine:
    proby = 10

    def start_game(self):
        game = True

        while game:
            menu()
            opcja = int(input('Podaj opcje: ') or '0')

            if opcja == 1:
                self._start_game_process(self.proby)
            elif opcja == 2:
                zasady()
            elif opcja == 3:
                game = False
            else:
                print("Wybrałeś niewłaściwą opcję!")
    
    def _start_game_process(self, proby):
        czy_wygral = False
        aktualna_proba = 0
        pozostale = 11
        stats = Stats()
        dictionary = Dictionary()
        validator = Validator()

        host_word = dictionary.losowe_slowo()
        host_word_len = len(host_word)

        while not czy_wygral:
            aktualna_proba += 1
            pozostale -= 1
            if aktualna_proba > proby:
                print(f'Przegrałeś :( \nPoprawne słowo to: {host_word}\n')
                break

            print(f'Długość wylosowanego słowa to: {host_word_len}\n')
            print(f'Pozostało prób: {pozostale}')
            user_word = input('Wprowadź słowo: ')


            while not (validator.check_isogram(user_word) and len(user_word) <= host_word_len):
                user_word = input('Podaj izogram (litery nie mogą się powtarzać) ')

            liczenie_stat(stats, host_word, user_word)

            if host_word_len == int(stats.get_bulls()):
                print(f'Brawo, wygrałeś! Poprawne słowo to: {host_word}, Wygrałeś w {aktualna_proba} próbie')
                czy_wygral = True
                break

            print(f'{stats.get_cows()} Cows, {stats.get_bulls()} Bulls')


#losowanie słowa z pliku

class Dictionary:
    with open('dictionary.txt') as plik:
        wszystko = plik.read()
        slowa = list(map(str, wszystko.split()))

        def losowe_slowo(self):
            slowo = random.choice(self.slowa)

            return slowo

#sprawdzanie czy slowo wpisane przez uzytkownika jest izogramem

class Validator:

    def check_isogram(self, user_word):
        izogram = len(user_word) == len(set(user_word.lower()))
        if izogram == False:
            return False
        else:
            return True

class Stats:
    bulls = 0
    cows = 0

    def zeruj(self):
        self.cows = 0
        self.bulls = 0
        
    def get_bulls(self):
        return self.bulls

    def add_bulls(self):
        self.bulls += 1

    def get_cows(self):
        return self.cows

    def add_cows(self):
        self.cows += 1


engine = Engine()

engine.start_game()