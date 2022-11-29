import random as rnd

import musicpy
from enum import Enum

from musicpy import database
from musicpy.musicpy import N, C, play
from musicpy.structures import chord

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

CM3 = musicpy.chord('C3, E3, G4').set(1)
Dm3 = musicpy.chord('D3, F3, A4').set(1)
Em3 = musicpy.chord('E3, G4, B4').set(1)
FM4 = musicpy.chord('F4, A4, C4').set(1)
GM4 = musicpy.chord('G4, B4, D4').set(1)
Am4 = musicpy.chord('A4, C5, E5').set(1)
Bm4 = musicpy.chord('B4, D5, F5').set(1)
CM4 = musicpy.chord('C4, E4, G5').set(1)
Dm4 = musicpy.chord('D4, F4, A5').set(1)
Em4 = musicpy.chord('E4, G5, B5').set(1)
FM5 = musicpy.chord('F5, A5, C5').set(1)
GM5 = musicpy.chord('G5, B5, D5').set(1)
Am5 = musicpy.chord('A5, C6, E6').set(1)
Bm5 = musicpy.chord('B5, D6, F6').set(1)

Chords = [CM3, Dm3, Em3, FM4, GM4, Am4, Bm4, CM4, Dm4, Em4, FM5, GM5, Am5, Bm5]

c_major_scale = [C3, D3, E3, F3, G3, A3, B3,
                 C4, D4, E4, F4, G4, A4, B4,
                 C5, D5, E5, F5, G5, A5, B5]


def generate_solution() -> []:
    # solution = [rnd.choices(cmajor, None, k=32)]
    solution = [0] * 8
    for i in range(len(solution)):
        # solution[i] = rnd.choices(c_major_scale, None, k=3)
        solution[i] = chord((rnd.choices(c_major_scale, None, k=3)))

    print(f'Initial Sol: {solution}')
    return solution


def create_population(population_size) -> [[]]:
    psize = population_size
    pop = []

    for i in range(psize):
        pop.append(generate_solution())

    return pop


def genetic_algorithm(pop_size, generations, tournament_size=2):
    population = create_population(pop_size)
    p_size = len(population)
    g = generations
    t = tournament_size
    best = [0]

    while g >= 0:
        for individual in population:
            individual_fitness = fitness(individual)
            best_fitness = fitness(best)
            if individual == best or individual_fitness > best_fitness:
                best = individual
        new_population = []
        for i in range(int(p_size/2)):
            parent_a = tournament_selection(population, t)
            parent_b = tournament_selection(population, t)
            child_a, child_b = crossover(parent_a.copy(), parent_b.copy())
            new_population.append(mutate_first_inversion(child_a))
            new_population.append(mutate_maj7(child_b))
        population = new_population
        g -= 1
    print(best)
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
    length = len(parent_a)

    c = rnd.randint(1, length)
    if not c == 1:
        for i in range(c,length):
            tmp = a[i]
            a[i] = b[i]
            b[i] = tmp
    return a, b


def mutate_first_inversion(solution):
    length = len(solution)
    probability = 1 / length
    random_no = rnd.uniform(0,1)
    v = solution.copy()

    for i in range(1, length):
        if probability >= random_no:
            v[i] = v[i] / 1
    return v


def mutate_maj7(solution):
    length = len(solution)
    probability = 1 / length
    random_no = rnd.uniform(0,1)
    v = solution.copy()

    for i in range(1, length):
        if probability >= random_no:
            triad = v[i]
            maj7 = triad('#7')
            v[i] = maj7
            print('Major 7th a chord!')
    return v


def short_composition(solution):
    chords = []
    for i in range(len(solution)):
        chords.append(musicpy.chord(solution[i]).set(1))
    fitness(solution)
    c1 = chords[0]
    c2 = chords[1]
    c3 = chords[2]
    c4 = chords[3]
    c5 = chords[4]
    c6 = chords[5]
    c7 = chords[6]
    c8 = chords[7]

    composition = c1 | c2 | c3 | c4 | c5 | c6 | c7 | c8
    play(composition, wait=True)


def fitness(solution):
    sol_fitness = 0
    if solution == [0]:
        return sol_fitness
    else:
        for b in range(len(solution)-1):
            chord_to_compare = solution[b]
            chord_to_compare_1st_inversion = (chord_to_compare / 1)
            chord_to_compare_2nd_inversion = (chord_to_compare / 2)
            if chord_to_compare in Chords:
                print(f'chord found in {b+1}th element!')
                sol_fitness += 1

            if chord_to_compare_1st_inversion in Chords:
                print(f'first inversion found in {b+1}th element!')
                sol_fitness += 1

            if chord_to_compare_2nd_inversion in Chords:
                print(f'second inversion found in {b+1}th element!')
                sol_fitness += 1

            if b+1 > len(solution)-1:
                print("too far chief")
            else:
                note_to_compare_interval = chord_to_compare[0]
                note_to_compare_interval = note_to_compare_interval.with_interval(database.perfect_fifth)
                chord_to_compare_interval_next_bar = solution[b+1][0]
                if note_to_compare_interval[1] == chord_to_compare_interval_next_bar:
                    print(f'perfect fifth detected between root note of bar {b+1} and {b+2}')
                    sol_fitness += 1

        print(sol_fitness)
        return sol_fitness


def check_chords():
    b = C('C5, E5, G6')
    b2 = C('C5, E5, G6')
    print("same") if b == b2 else print("different")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sol = genetic_algorithm(10, 100)
    while sol == [0]:
        sol = genetic_algorithm(10, 100)

    c1 = sol[0]
    c2 = sol[1]
    c3 = sol[2]
    c4 = sol[3]
    c5 = sol[4]
    c6 = sol[5]
    c7 = sol[6]
    c8 = sol[7]
    C = c1 | c2 | c3 | c4 | c5 | c6 | c7 | c1
    play(C, wait=True)
