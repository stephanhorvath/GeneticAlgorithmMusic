from main import *
from note_utilities import *


def split_track(t):
    chords = list(zip(*[iter(t)]*3))
    return chords


def fit_duplicate_tones(c) -> int:
    c_length = len(c) - 1
    for i in range(c_length):
        if i+2 > c_length:
            pass
        else:
            if compare_without_octave(c[i], c[i+1]) or compare_without_octave(c[i], c[i+2]) or compare_without_octave(c[i+1], c[i+2]):
                return -5
    return 1


def fit_perfect_fifth(c) -> int:
    notes = [0] * len(c)
    for n in range(len(c)):
        if n + 2 > len(c) - 1:
            pass
        else:
            if compute_degree_separation(c[n], c[n + 2]) == database.perfect_fifth:
                return 3
    return -1


def fit_minor_third(c) -> int:
    length = len(c)
    degrees = [0] * length
    for n in range(length):
        degrees[n] = c[n].degree

    for i in range(length):
        if i + 1 >= length:
            break

        if degrees[i] - degrees[i + 1] <= -12:
            degrees[i + 1] = degrees[i + 1] - 12

        if (degrees[i] - degrees[i + 1]) * -1 == database.minor_third:
            return 1
    return 0


def fit_major_third(c) -> int:
    length = len(c)
    degrees = [0] * length
    for n in range(length):
        degrees[n] = c[n].degree

    for i in range(length):
        if i + 1 >= length:
            break

        if degrees[i] - degrees[i + 1] <= -12:
            degrees[i + 1] = degrees[i + 1] - 12

        if (degrees[i] - degrees[i + 1]) * -1 == database.major_third:
            return 1
    return 0


def fit_minor_second(c) -> int:
    length = len(c)
    degrees = [0] * length
    for n in range(length):
        degrees[n] = c[n].degree

    for i in range(length):
        if i + 1 >= length:
            break

        if degrees[i] - degrees[i + 1] <= -12:
            degrees[i + 1] = degrees[i + 1] - 12

        if (degrees[i] - degrees[i + 1]) * -1 == database.minor_second:
            return -1
    return 0


def fit_major_second(c) -> int:
    length = len(c)
    degrees = [0] * length
    for n in range(length):
        degrees[n] = c[n].degree

    for i in range(length):
        if i + 1 >= length:
            break

        if degrees[i] - degrees[i + 1] <= -12:
            degrees[i + 1] = degrees[i + 1] - 12

        if (degrees[i] - degrees[i + 1]) * -1 == database.major_second:
            return -1
    return 0


def fit_triad(c) -> int:
    no_of_notes = len(c)
    if no_of_notes < 3:
        return 0

    for n in range(no_of_notes - 1):
        if (n + 1) > no_of_notes:
            return -1
        elif ((c[n].degree - c[n + 1].degree) * -1 == database.minor_third or (
                c[n].degree - c[n + 1].degree) * -1 == database.major_third) \
                and (c[n].degree - c[n + 2].degree) * -1 == database.perfect_fifth:
            return 50
        else:
            return 0


def fitness_ii_V_I(root_notes) -> True | False:
    notes_list = root_notes

    if compare_without_octave(root_notes[0], N('D3')) and compare_without_octave(root_notes[1], N('G3')) and compare_without_octave(root_notes[2], N('C3')):
        return True


def fitness_chord_progression_window(solution, window_size=3):
    s = solution.copy()
    w = window_size
    found_ii_V_i = False

    if len(s) <= w:
        return 0

    for i in range(len(s) - w + 1):
        chord_progression_bar_1 = s[i]
        root_1 = chord_progression_bar_1[0]
        chord_progression_bar_2 = s[i+1]
        root_2 = chord_progression_bar_2[0]
        chord_progression_bar_3 = s[i+w-1]
        root_3 = chord_progression_bar_3[0]
        roots = [root_1, root_2, root_3]
        if fitness_ii_V_I(roots):
            found_ii_V_i = True
    if found_ii_V_i:
        return 10000
    else:
        return 0

def jazz_fitnesses_list(single_chord, sol_fitness):
    s_c = single_chord.copy()
    s_f = sol_fitness
    f_list = [fit_triad, fit_duplicate_tones, fit_perfect_fifth, fit_major_third, fit_minor_third, fit_major_second,
              fit_minor_second]
    for fit_func in f_list:
        s_f = s_f + fit_func(s_c)

    return s_f


def fitness(solution):
    if solution is None:
        print("????")
    s = solution.copy()
    sol_fitness = 0
    sol_fitness = sol_fitness + fitness_chord_progression_window(s)
    if solution == [0]:
        return sol_fitness
    else:
        for single_chord in s:

            # check if proper c was randomly created
            if single_chord in Chords:
                sol_fitness = sol_fitness + 1

            sol_fitness = sol_fitness + jazz_fitnesses_list(single_chord, 0)
            # sol_fitness = sol_fitness + fit_duplicate_tones(single_chord)
            # sol_fitness = sol_fitness + fit_perfect_fifth(single_chord)
            # sol_fitness = sol_fitness + fit_minor_third(single_chord)
            # sol_fitness = sol_fitness + fit_major_third(single_chord)
            # sol_fitness = sol_fitness + fit_major_second(single_chord)
            # sol_fitness = sol_fitness + fit_major_second(single_chord)
            # sol_fitness = sol_fitness + fit_triad(single_chord)

        return sol_fitness
