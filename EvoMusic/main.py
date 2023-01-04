import random as rnd

import musicpy
from enum import Enum

from musicpy import database
from musicpy.musicpy import N, C, play
from musicpy.structures import chord

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

CM3 = musicpy.chord('C3, E3, G4')
Dm3 = musicpy.chord('D3, F3, A4')
Em3 = musicpy.chord('E3, G4, B4')
FM4 = musicpy.chord('F4, A4, C4')
GM4 = musicpy.chord('G4, B4, D4')
Am4 = musicpy.chord('A4, C5, E5')
Bm4 = musicpy.chord('B4, D5, F5')
CM4 = musicpy.chord('C4, E4, G5')
Dm4 = musicpy.chord('D4, F4, A5')
Em4 = musicpy.chord('E4, G5, B5')
FM5 = musicpy.chord('F5, A5, C5')
GM5 = musicpy.chord('G5, B5, D5')
Am5 = musicpy.chord('A5, C6, E6')
Bm5 = musicpy.chord('B5, D6, F6')

Chords = [CM3, Dm3, Em3, FM4, GM4, Am4, Bm4, CM4, Dm4, Em4, FM5, GM5, Am5, Bm5]

c_major_scale = [C2, D2, E2, F2, G2, A2, B2,
                 C3, D3, E3, F3, G3, A3, B3,
                 C4, D4, E4, F4, G4, A4, B4,
                 C5, D5, E5, F5, G5, A5, B5]

test_population = [
    [chord('B2, A5, A5'), chord('D2, G3, G4'), chord('A2, B2, E3'), chord('D2, F3, F4'), chord('A2, F4, G5'), chord('E3, C4, E4'), chord('B3, C4, F4'), chord('G4, E5, B5')],
    [chord('D3, F3, B3'), chord('C3, B3, F5'), chord('B2, G3, C4'), chord('A3, C5, D5'), chord('C3, E3, E3'), chord('G3, E4, E4'), chord('D2, A2, A2'), chord('D2, C3, D3')],
    [chord('F2, E3, E3'), chord('B4, D5, D5'), chord('D4, E4, B4'), chord('C5, G5, B5'), chord('E2, G2, E3'), chord('E2, G3, A3'), chord('D4, F4, C5'), chord('C4, D4, G4')],
    [chord('B3, E5, F5'), chord('E2, F2, D3'), chord('C2, E2, B3'), chord('A4, D5, F5'), chord('G2, A2, C3'), chord('E3, G3, D4'), chord('A2, E4, A4'), chord('A3, D4, A4')],
    [chord('A3, B3, A4'), chord('F2, A2, B2'), chord('F2, C3, B4'), chord('F3, G3, C4'), chord('G3, C4, E4'), chord('F2, G2, C3'), chord('D3, E3, E3'), chord('G2, B2, D4')],
    [chord('B3, E4, A4'), chord('D2, B2, D3'), chord('E3, D4, G4'), chord('E3, E5, E5'), chord('D2, E4, D5'), chord('C3, G3, A3'), chord('D3, F4, E5'), chord('B2, F3, F3')],
    [chord('C2, G2, B2'), chord('A3, B3, G4'), chord('A2, C4, E4'), chord('F3, A3, D4'), chord('A2, C3, B3'), chord('E2, F2, C3'), chord('A2, C5, B5'), chord('D2, E2, C3')],
    [chord('E2, F2, B2'), chord('E2, A2, B2'), chord('G2, B2, F3'), chord('D2, A2, D3'), chord('G2, B3, G4'), chord('B4, F5, A5'), chord('C2, G3, G4'), chord('E3, F3, D4')],
    [chord('D4, G4, A4'), chord('D5, A5, B5'), chord('D3, F3, D4'), chord('G2, G2, A5'), chord('E3, E3, A4'), chord('C2, G2, B2'), chord('E3, G3, E4'), chord('D2, G4, E5')],
    [chord('F2, F3, G4'), chord('F4, B4, E5'), chord('D2, F2, D5'), chord('E3, D4, E4'), chord('B2, D4, E4'), chord('G3, F4, F5'), chord('C2, E2, B2'), chord('D2, A5, B5')]]

def generate_solution() -> []:
    # solution = [rnd.choices(cmajor, None, k=32)]
    solution = [0] * 8
    for i in range(len(solution)):
        # solution[i] = rnd.choices(c_major_scale, None, k=3)
        solution[i] = chord((rnd.choices(c_major_scale, None, k=3))).inoctave()

    print(f'Initial Sol: {solution}')
    return solution


def create_population(population_size) -> [[]]:
    psize = population_size
    pop = []

    for i in range(psize):
        pop.append(generate_solution())

    return pop


def genetic_algorithm(pop_size, generations, tournament_size=2, testing_pop=False):
    if not testing_pop:
        population = create_population(pop_size)
    else:
        population = test_population

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
            new_population.append(mutate(child_a))
            new_population.append(mutate(child_b))
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


# This function creates a list of all
# the mutation functions and randomly selects
# one, and returns that functions return value
def mutate(solution):
    func_list = [mutate_first_inversion, mutate_move_one_tone, mutate_flip_quality]
    return rnd.choice(func_list)(solution)


def mutate_first_inversion(solution):
    length = len(solution)
    probability = 1 / length
    # probability = -1
    random_no = rnd.uniform(0, 1)
    v = solution.copy()

    for i in range(1, length):
        if probability >= random_no:
            v[i] = v[i] / 1
    return v


def mutate_move_one_tone(solution):
    length = len(solution)
    # probability = 1 / length
    probability = -1
    random_no = rnd.uniform(0, 1)
    v = solution.copy()

    for i in range(1, length):
        if probability >= random_no:
            v[i] = v[i] + 1
    return v


def mutate_flip_quality(solution):
    length = len(solution)
    # probability = 1 / length
    probability = -1
    random_no = rnd.uniform(0, 1)
    v = solution.copy()

    for i in range(1, length):
        if probability >= random_no:
            if (v[i][0].degree - v[i][1].degree) * -1 == database.minor_third:
                v[i][1] = v[i][1] + 1
                print(f'Made minor third into major third')
            elif (v[i][0].degree - v[i][1].degree) * -1 == database.major_third:
                v[i][1] = v[i][1] - 1
                print(f'Made major third into minor third')
            else:
                pass
    return v


# def mutate_dot(solution):
#     length = len(solution)
#     probability = 1 / length
#     random_no = rnd.uniform(0, 1)
#     v = solution.copy()
#
#     for i in range(1, length):
#         if probability >= random_no:
#             random_note = rnd.choice
#             random_note =  random_note.dotted()
#
#     return v

# def mutate_maj7(solution):
#     length = len(solution)
#     probability = 1 / length
#     random_no = rnd.uniform(0,1)
#     v = solution.copy()
#
#     for i in range(1, length):
#         if probability >= random_no:
#             triad = v[i]
#             maj7 = triad('#7')
#             v[i] = maj7
#             print('Major 7th a chord!')
#     return v


def fitness(solution):
    sol_fitness = 0
    if solution == [0]:
        return sol_fitness
    else:
        for b in range(len(solution)-1):

            if solution[b] in Chords:
                sol_fitness += 6

            # check for minor seconds
            for c in range(len(solution[b])):
                if c + 1 > len(solution[b]) - 1:
                    pass
                else:
                    if (solution[b][c].degree - solution[b][c+1].degree) * -1 == database.minor_second:
                        sol_fitness -= 3

            # check that second note and third note are not further than an octave apart
            if solution[b][1].degree - solution[b][2].degree < 0:
                sol_fitness += 1

            # check that root note and second note are not a minor, nor major second apart
            if ((solution[b][0].degree - solution[b][1].degree) * -1) == database.minor_second:
                sol_fitness -= 5

            if ((solution[b][0].degree - solution[b][1].degree) * -1) == database.major_second:
                sol_fitness -= 5

            # check if first two notes of each chord in each bar
            # are at the very least a minor or major third interval
            # as the basic function for every chord comes from this interval
            if ((solution[b][0].degree - solution[b][1].degree) * -1) == database.minor_third:
                print(f'Minor third detected on bar{b+1} between root note {solution[b][0]} and {solution[b][1]}')
                sol_fitness += 3
            elif ((solution[b][0].degree - solution[b][1].degree) * -1) == database.major_third:
                print(f'Major third detected on bar{b+1} between root note {solution[b][0]} and {solution[b][1]}')
                sol_fitness += 3
            else:
                pass

            # check if root and third note of triad are a perfect fifth apart
            if ((solution[b][0].degree - solution[b][2].degree) * -1) == database.perfect_fifth:
                print(f'Perfect fifth detected on bar {b+1} between root note {solution[b][0]} and {solution[b][1]}')
                sol_fitness += 5

            # check if root and third interval are an octave or two apart
            if (solution[b][0].degree - solution[b][2].degree) == database.perfect_octave or (solution[b][0].degree - solution[b][1].degree) == (database.perfect_octave * 2):
                sol_fitness -= 1

            # checks for basic inversions
            # as they can be pleasing, but more checks should be made
            # for chord functions, as inversions change the function
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

            # checks for a perfect fifth interval between a bar and the next bar
            # as a V-I progression is found in most western music
            # if b+1 > len(solution)-1:
            #     print("too far chief")
            # else:
            #     next_bar_check_fifth = solution[b+1][0]
            #     next_bar_check_fifth = next_bar_check_fifth.with_interval(database.perfect_fifth)
            #     chord_to_compare_interval_next_bar = chord_to_compare[0]
            #     if next_bar_check_fifth[1] == chord_to_compare_interval_next_bar:
            #         print(f'perfect fifth detected between root note of bar {b+1} and {b+2}')
            #         sol_fitness += 1
            #
            # if b+1 > len(solution)-1:
            #     print("too far chief")
            # else:
            #     next_bar_check_fourth = solution[b+1][0]
            #     next_bar_check_fourth = next_bar_check_fourth.with_interval(database.perfect_fourth)
            #     chord_to_compare_interval_next_bar = chord_to_compare[0]
            #     if next_bar_check_fourth[1] == chord_to_compare_interval_next_bar:
            #         print(f'perfect fourth detected between root note of bar {b+1} and {b+2}')
            #         sol_fitness += 1
        print(sol_fitness)
        return sol_fitness


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    sol = genetic_algorithm(10, 50, 2, testing_pop=True)
    while sol == [0]:
        sol = genetic_algorithm(10, 50, 2, testing_pop=True)

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
    play(C, wait=True)
