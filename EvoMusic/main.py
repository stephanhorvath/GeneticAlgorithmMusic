from fitnesses import *
from mutations import *
from musicpy import database
from musicpy.musicpy import N, C, play
from musicpy.structures import chord
import random as rnd
import musicpy as mp

C2 = 'C2'
D2 = 'D2'
E2 = 'E2'
F2 = 'F2'
G2 = 'G2'
A2 = 'A2'
B2 = 'B2'
C3 = 'C3'
D3 = 'D3'
E3 = 'E3'
F3 = 'F3'
G3 = 'G3'
A3 = 'A3'
B3 = 'B3'
C4 = 'C4'
D4 = 'D4'
E4 = 'E4'
F4 = 'F4'
G4 = 'G4'
A4 = 'A4'
B4 = 'B4'
C5 = 'C5'
D5 = 'D5'
E5 = 'E5'
F5 = 'F5'
G5 = 'G5'
A5 = 'A5'
B5 = 'B5'
C6 = 'C6'
D6 = 'D6'
E6 = 'E6'
F6 = 'F6'
G6 = 'G6'
A6 = 'A6'
B6 = 'B6'

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

c_major_scale = [C3, D3, E3, F3, G3, A3, B3,
                 C4, D4, E4, F4, G4, A4, B4,
                 C5, D5, E5, F5, G5, A5, B5]

test_population = [
    [chord('D3, F3, A3'), chord('G3, B3, D4'), chord('C3, E3, G3'), chord('D3, F3, F4'), chord('A3, F4, G5'),
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

for i in range(len(test_population)):
    for j in range(len(test_population[i])):
        test_population[i][j] = test_population[i][j].set(1, 0)


def generate_harmony() -> []:
    # solution = [rnd.choices(cmajor, None, k=32)]
    solution = [0] * 8
    for i in range(len(solution)):
        # solution[i] = rnd.choices(c_major_scale, None, k=3)
        # solution[i] = chord((rnd.choices(c_major_scale, None, k=3))).inoctave().set(0.75, 0) | mp.rest(duration=1 / 4,
        #                                                                                                dotted=None)
        solution[i] = chord((rnd.sample(c_major_scale, k=3))).inoctave().set(0.75, 0) | mp.rest(duration=1/4, dotted=None)

    print(f'Initial Sol: {solution}')
    solution = solution + solution + solution + solution
    t = generate_track(solution)
    return solution


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


def generate_track(chords):
    track = 0
    for c in range(len(chords)):
        track = track | chords[c]

    return track


def create_population(population_size) -> [[]]:
    psize = population_size
    pop = []

    for i in range(psize):
        pop.append(generate_harmony())

    return pop


def genetic_algorithm(pop_size, generations, tournament_size=2, testing_pop=False):
    if not testing_pop:
        population = create_population(pop_size)
    else:
        population = test_population

    p_size = len(population)
    g = 0
    t = tournament_size
    best = [0]
    generation_log = []

    while g <= generations:
        for individual in population:
            if individual is None:
                print("why is individual none?")
            individual_fitness = fitness(individual)
            best_fitness = fitness(best)
            if individual == best or individual_fitness > best_fitness:
                best = individual
        new_population = []
        for i in range(int(p_size / 2)):
            parent_a = tournament_selection(population, t)
            parent_b = tournament_selection(population, t)
            child_a, child_b = crossover(parent_a.copy(), parent_b.copy())
            new_population.append(mutate(child_a))
            new_population.append(mutate(child_b))
        population = new_population
        generation_log.append((g, best, fitness(best)))
        g += 1
    generation_info_printer(generation_log)
    return best


def tournament_selection(population, tournament_size):
    p = population
    pop_size = len(population)
    t_size = 1
    if pop_size > 1:
        t_size = tournament_size

    best = rnd.choice(p)

    for i in range(2, t_size):
        next_individual = rnd.choice(p)
        if fitness(next_individual) > fitness(best):
            best = next_individual
    return best


def crossover(parent_a, parent_b):
    a = parent_a
    b = parent_b
    print('\n------------------------')
    print(f'Parent A: {a}')
    print(f'Parent B: {b}')
    length = len(parent_a)

    c = rnd.randint(1, length)
    if not c == 1:
        print(f'Switching from {c} to {length}')
        for i in range(c, length):
            tmp = a[i]
            a[i] = b[i]
            b[i] = tmp
    print('------')
    print(f'Child A: {a}')
    print(f'Child B: {b}')
    print('------')
    return a, b


def generation_info_printer(generations):
    g = generations.copy()

    for a in g:
        print(f'Generation: {a[0]} - Best Solution: {a[1]} - Fitness: {a[2]}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sol = genetic_algorithm(10, 10, 5, testing_pop=False)
    while sol == [0]:
        sol = genetic_algorithm(10, 10, 5, testing_pop=False)

    melody = generate_melody()
    m1 = melody[0]
    m2 = melody[1]
    m3 = melody[2]
    m4 = melody[3]
    m5 = melody[4]
    m6 = melody[5]
    m7 = melody[6]
    m8 = melody[7]

    c1 = sol[0]
    c2 = sol[1]
    c3 = sol[2]
    c4 = sol[3]
    c5 = sol[4]
    c6 = sol[5]
    c7 = sol[6]
    c8 = sol[7]
    # c9 = sol[8]
    # c10 = sol[9]
    # c11 = sol[10]
    # c12 = sol[11]
    # c13 = sol[12]
    # c14 = sol[13]
    # c15 = sol[14]
    # c16 = sol[15]
    # C = c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8 | c9 | c10 | c11 | c12 | c13 | c14 | c15 | c16 | c1
    C = c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8
    # M = chord(f'{c1}, {c2}, {c3}, {c4}, {c5}, {c6}, {c7}').set(0.25, 0.25)
    # M = (chord(notes=[m1]).set(0.25, 0.25) | chord(notes=[m2]).set(0.25, 0.25) | chord(notes=[m3]).set(0.25, 0.25) | chord(notes=[m4]).set(0.25, 0.25) | chord(notes=[m5]).set(0.25, 0.25) | chord(notes=[m6]).set(0.25, 0.25) | chord(notes=[m7]).set(0.25, 0.25) | chord(notes=[m8]).set(0.25, 0.25)) * 4
    # p = mp.P(tracks=[C, M],
    #          instruments=['Acoustic Grand Piano', 'Electric Guitar (jazz)'],
    #          bpm=100,
    #          start_times=[0, 0],
    #          track_names=['piano', 'guitar'])

    p = mp.P(tracks=[C],
             instruments=['Acoustic Grand Piano'],
             bpm=120,
             start_times=[0],
             track_names=['piano'])
    play(p, wait=True)
