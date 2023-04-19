from fitnesses import *
from mutations import *
from musicpy import database
from musicpy.musicpy import N, C, play
from musicpy.structures import chord
import random as rnd
import musicpy as mp
import c_major_notes as c



CM3 = chord('C3, E3, G4')
Dm3 = chord('D3, F3, A4')
Em3 = chord('E3, G4, B4')
FM4 = chord('F4, A4, C4')
GM4 = chord('G4, B4, D4')
Am4 = chord('A4, C5, E5')
Bm4 = chord('B4, D5, F5')
CM4 = chord('C4, E4, G5')
Dm4 = chord('D4, F4, A5')
Em4 = chord('E4, G5, B5')
FM5 = chord('F5, A5, C5')
GM5 = chord('G5, B5, D5')
Am5 = chord('A5, C6, E6')
Bm5 = chord('B5, D6, F6')

Chords = [CM3, Dm3, Em3, FM4, GM4, Am4, Bm4, CM4, Dm4, Em4, FM5, GM5, Am5, Bm5]

c_major_scale = [c.C3, c.D3, c.E3, c.F3, c.G3, c.A3, c.B3,
                 c.C4, c.D4, c.E4, c.F4, c.G4, c.A4, c.B4,
                 c.C5, c.D5, c.E5, c.F5, c.G5, c.A5, c.B5]

bass_notes = [c.E1, c.F1, c.G1, c.A1, c.B1, c.C2, c.D2,
              c.E2, c.F2, c.G2, c.A2, c.B2, c.C3, c.D3,
              c.E3, c.F3, c.G3, c.A3, c.B3, c.C4, c.D4, c.E4]

test_population = [
    [chord('C3, E3, G4'), chord('F3, A3, C4'), chord('G3, B3, D3'), chord('C3, E3, G4'), chord('A3, F4, G5'),
     chord('E3, C4, E4'), chord('B3, C4, F4'), chord('G4, E5, B5')],
    [chord('D3, F3, B3'), chord('C3, B3, F5'), chord('B3, G3, C4'), chord('A3, C5, D5'), chord('C3, E3, E3'),
     chord('G3, E4, E4'), chord('D3, A3, A3'), chord('D3, C3, D3')],
    [chord('F3, E3, E3'), chord('B4, D5, D5'), chord('D4, E4, B4'), chord('C5, G5, B5'), chord('E3, G3, E3'),
     chord('E3, G3, A3'), chord('D4, F4, C5'), chord('C4, D4, G4')],
    [chord('B3, E5, F5'), chord('E3, F3, D3'), chord('C3, E3, B3'), chord('A4, D5, F5'), chord('G3, A3, C3'),
     chord('E3, G3, D4'), chord('A3, E4, A4'), chord('A3, D4, A4')],
    [chord('A3, B3, A4'), chord('F3, A3, B3'), chord('F3, C3, B4'), chord('F3, G3, C4'), chord('G3, C4, E4'),
     chord('F3, G3, C3'), chord('D3, E3, E3'), chord('G3, B3, D4')],
    [chord('B3, E4, A4'), chord('D3, B3, D3'), chord('E3, D4, G4'), chord('E3, E5, E5'), chord('D3, E4, D5'),
     chord('C3, G3, A3'), chord('D3, F4, E5'), chord('B3, F3, F3')],
    [chord('C3, G3, B3'), chord('A3, B3, G4'), chord('A3, C4, E4'), chord('F3, A3, D4'), chord('A3, C3, B3'),
     chord('E3, F3, C3'), chord('A3, C5, B5'), chord('D3, E3, C3')],
    [chord('E2, F2, B2'), chord('E2, A2, B2'), chord('G2, B2, F3'), chord('D2, A2, D3'), chord('G2, B3, G4'),
     chord('B4, F5, A5'), chord('C2, G3, G4'), chord('E3, F3, D4')],
    [chord('D4, G4, A4'), chord('D5, A5, B5'), chord('D3, F3, D4'), chord('G2, G2, A5'), chord('E3, E3, A4'),
     chord('C2, G2, B2'), chord('E3, G3, E4'), chord('D2, G4, E5')],
    [chord('F2, F3, G4'), chord('F4, B4, E5'), chord('D2, F2, D5'), chord('E3, D4, E4'), chord('B2, D4, E4'),
     chord('G3, F4, F5'), chord('C2, E2, B2'), chord('D2, A5, B5')]]

global_genre = "jazz"

for i in range(len(test_population)):
    for j in range(len(test_population[i])):
        test_population[i][j] = test_population[i][j].set(1, 0)


def generate_harmony() -> []:
    chords = []
    for _ in range(8):
        chord_notes = chord((rnd.sample(c_major_scale, k=3))).inoctave().set(0.75, 0)
        chord_rest = mp.rest(duration=1/4, dotted=None)
        chords.append(chord_notes | chord_rest)

    print(f'Initial Sol: {chords}')
    return chords


def generate_melody() -> []:
    pattern_1 = [0] * 8
    for i in range(len(pattern_1)):
        pattern_1[i] = N(rnd.choice(c_major_scale))

    pattern_1 = pattern_1 * 2

    pattern_2 = [0] * 8
    for j in range(len(pattern_2)):
        pattern_2[j] = N(rnd.choice(c_major_scale))

    pattern_2 = pattern_2 * 2

    solution = pattern_1 + pattern_2
    return solution


def generate_bassline():
    bass_line = [N(rnd.choice(bass_notes)).set(duration=0.25) for _ in range(32)]
    print(f'Initial Sol: {bass_line}')
    return bass_line


def create_population(part, population_size) -> [[]]:
    if part == "harmony":
        part_func = generate_harmony
    elif part == "bass":
        part_func = generate_bassline
    elif part == "melody":
        part_func = generate_melody

    return [part_func() for _ in range(population_size)]


def genetic_algorithm(part, pop_size, generations, tournament_size=2, genre="jazz", harmony=[0], testing_pop=False):
    population = test_population if testing_pop else create_population(part, pop_size)

    first_sol = rnd.choice(population)
    p_size = len(population)
    g = 0
    t = tournament_size
    best = [0]
    generation_log = []

    while g <= generations:
        if harmony != [0]:
            for bass_individual in population:
                if bass_individual is None:
                    print("Check mutations for functions without return")
                bass_individual_fitness = bass_fitness(harmony, bass_individual)
                best_bass_fitness = bass_fitness(harmony, best)
                if bass_individual == best or bass_individual_fitness > best_bass_fitness:
                    best = bass_individual
            new_bass_population = []
            for i in range(int(p_size / 2)):
                bass_parent_a = bass_tournament_selection(population, t, global_genre)
                bass_parent_b = bass_tournament_selection(population, t, global_genre)
                bass_child_a, bass_child_b = uniform_crossover(bass_parent_a.copy(), bass_parent_b.copy())
                new_bass_population.append(bass_mutate(bass_child_a))
                new_bass_population.append(bass_mutate(bass_child_b))
            population = new_bass_population
            # generation_log.append((g, best, fitness(best, global_genre)))
            g += 1
        else:
            for individual in population:
                if individual is None:
                    print("Check mutations for functions without return")
                individual_fitness = fitness(individual, global_genre)
                best_fitness = fitness(best, global_genre)
                if individual == best or individual_fitness > best_fitness:
                    best = individual
            new_population = []
            for i in range(int(p_size / 2)):
                parent_a = tournament_selection(population, t, global_genre)
                parent_b = tournament_selection(population, t, global_genre)
                child_a, child_b = uniform_crossover(parent_a.copy(), parent_b.copy())
                new_population.append(mutate(child_a))
                new_population.append(mutate(child_b))
            population = new_population
            generation_log.append((g, best, fitness(best, global_genre)))
            g += 1
    generation_info_printer(generation_log)
    return best, first_sol


def tournament_selection(population, tournament_size, global_genre):
    p = population
    pop_size = len(population)
    t_size = 1
    if pop_size > 1:
        t_size = tournament_size

    best = rnd.choice(p)

    for i in range(2, t_size):
        next_individual = rnd.choice(p)
        if fitness(next_individual, global_genre) > fitness(best, global_genre):
            best = next_individual
    return best


def bass_tournament_selection(population, tournament_size, harmony):
    p = population
    pop_size = len(population)
    t_size = 1
    if pop_size > 1:
        t_size = tournament_size

    best = rnd.choice(p)

    for i in range(2, t_size):
        next_individual = rnd.choice(p)
        if bass_fitness(harmony, next_individual) > bass_fitness(harmony, best):
            best = next_individual
    return best


def crossover(parent_a, parent_b):
    a = parent_a
    b = parent_b
    print('\n------------------------')
    print(f'Parent A: fitness: {fitness(a, "jazz")} {a}')
    print(f'Parent B: fitness: {fitness(b, "jazz")} {b}')
    length = len(parent_a)

    c = rnd.randint(1, length)
    d = rnd.randint(1, length)
    if c > d:
        temp = c
        c = d
        d = temp

    print(f'Swapping from index {c} to {d}')
    if c != d:
        for i in range(c, d - 1):
            tmp = a[i]
            a[i] = b[i]
            b[i] = tmp
    print('------')
    print(f'Child A: fitness: {fitness(a, "jazz")} {a}')
    print(f'Child B: fitness: {fitness(b, "jazz")} {b}')
    print('------')
    return a, b


def uniform_crossover(parent_a, parent_b):
    a = parent_a
    b = parent_b
    length = len(a)
    p = 1 / length

    for i in range(length):
        if rnd.uniform(0, 1) <= p:
            a[i], b[i] = b[i], a[i]
    return a, b


def generation_info_printer(generations):
    g = generations.copy()

    for a in g:
        print(f'Generation: {a[0]} - Best Solution: {a[1]} - Fitness: {a[2]}')


def algorithm_parameter_input() -> ():
    pop_size = input("Enter desired population size (max 30): ")
    while not pop_size.isnumeric() or not int(pop_size) % 2 == 0 or not 5 <= int(pop_size) <= 100:
        print("Invalid input. Population size must be an even number between 10 and 100.")
        pop_size = input("Enter desired population size: ")

    gen_size = input("Enter desired number of generations (max 50): ")
    while not gen_size.isnumeric() or not 5 <= int(gen_size) <= 100:
        print("Invalid input. Generation size must be between 5 and 100.")
        gen_size = input("Enter desired population size: ")

    tournament_size = input("Enter selection tournament size (cannot be bigger than population size): ")
    while not tournament_size.isnumeric() or not 2 <= int(tournament_size) <= int(pop_size):
        print(f'Invalid input. Tournament size is related to population size, and '
              f'must be a number in range from 2 to {int(pop_size)}')
        tournament_size = input("Enter selection tournament size: ")

    global_genre = input("Enter 'j' for jazz, or 'r' for rock: ")

    while global_genre not in {'j', 'J', 'r', 'R'}:
        global_genre = input("Invalid input. Enter 'j' for jazz, or 'r' for rock: ")

    if global_genre in {'j', 'J'}:
        global_genre = "jazz"
    elif global_genre in {'r', 'R'}:
        global_genre = "rock"

    return pop_size, gen_size, tournament_size, global_genre


def bass_track_builder(sol):
    C = 0
    for c in sol:
        if C == 0:
            C = chord(notes=[c]).set(0.25, 0.25)
        else:
            C = C | chord(notes=[c]).set(0.25, 0.25)

    return C


def track_builder(sol):
    C = 0
    for c in sol:
        if C == 0:
            C = c
        else:
            C = C | c

    return C


def piece_composer(*args):
    if len(args) == 1:
        bpms = [80, 100, 120, 150]
        jazz_piano = args[0]

        p = mp.P(tracks=[jazz_piano],
                 instruments=['Acoustic Grand Piano'],
                 bpm=rnd.choice(bpms),
                 start_times=[0],
                 track_names=['jazz piano'])

        return p
    if global_genre == "jazz":
        bpms = [80, 100, 120, 150]
        jazz_piano = args[0]
        jazz_bass = args[1]

        p = mp.P(tracks=[jazz_piano, jazz_bass],
                 instruments=['Acoustic Grand Piano', 'Electric Bass (finger)'],
                 bpm=rnd.choice(bpms),
                 start_times=[0, 0],
                 track_names=['jazz piano', 'jazz bass'])
    elif global_genre == "rock":
        bpms = [120, 130, 150, 180]
        rock_guitar = args[0]
        rock_bass = args[1]

        p = mp.P(tracks=[rock_guitar, rock_bass],
                 instruments=['Distortion Guitar', 'Electric Bass (pick)'],
                 bpm=rnd.choice(bpms),
                 start_times=[0, 0],
                 track_names=['overdriven guitar', 'rock bass'])

        # jazz_piano = args[0]
        #
        # p = mp.P(tracks=[jazz_piano],
        #          instruments=['Acoustic Grand Piano'],
        #          bpm=80,
        #          start_times=[0],
        #          track_names=['jazz piano'])

    return p


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # b = generate_bassline()
    # t = harmony_track_builder(b)
    # p = mp.P(tracks=[t], instruments=['Electric Bass (finger)'],bpm=80, start_times=[0], track_names=['bass'])

    pop_size, gen_size, tournament_size, global_genre = algorithm_parameter_input()

    harmony, first_sol = genetic_algorithm("harmony", int(pop_size), int(gen_size), int(tournament_size), global_genre, testing_pop=False)
    while harmony == [0]:
        harmony, first_sol = genetic_algorithm("harmony", int(pop_size), int(gen_size), int(tournament_size), global_genre, testing_pop=False)

    bass = genetic_algorithm("bass", int(pop_size), int(gen_size), int(tournament_size), global_genre, harmony)[0]

    first_sol = piece_composer(track_builder(first_sol))
    p = piece_composer(track_builder(harmony), bass_track_builder(bass))

    listen = int(input("Enter 1 to listen a random solution of the 1st generation. Enter 2 to listen to the final solution. Enter 3 to quit: "))
    while listen not in [1, 2, 3]:
        listen = int(input("Invalid input. Enter 1 to listen a random solution of the 1st generation. Enter 2 to listen to the final solution. Enter 3 to quit: "))

    repeat = True
    while repeat:
        while listen not in [1, 2, 3]:
            listen = int(input("Invalid input. Enter 1 to listen a random solution of the 1st generation. Enter 2 to listen to the final solution. Enter 3 to quit: "))
        if listen == 1:
            play(first_sol, wait=True)
            listen = int(input("Enter 1 to listen a random solution of the 1st generation. Enter 2 to listen to the final solution. Enter 3 to quit: "))
        elif listen == 2:
            play(p, wait=True)
            listen = int(input("Enter 1 to listen a random solution of the 1st generation. Enter 2 to listen to the final solution. Enter 3 to quit: "))
        elif listen == 3:
            repeat = False
        else:
            print("Something went wrong (:")