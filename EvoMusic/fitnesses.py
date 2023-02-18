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
            return 1
        else:
            return 0


def fitness(solution):
    if solution is None:
        print("????")
    s = solution.copy()
    sol_fitness = 0
    if solution == [0]:
        return sol_fitness
    else:
        for single_chord in s:

            # check if proper c was randomly created
            if single_chord in Chords:
                sol_fitness = sol_fitness + 1

            sol_fitness = sol_fitness + fit_duplicate_tones(single_chord)
            sol_fitness = sol_fitness + fit_perfect_fifth(single_chord)
            sol_fitness = sol_fitness + fit_minor_third(single_chord)
            sol_fitness = sol_fitness + fit_major_third(single_chord)
            sol_fitness = sol_fitness + fit_major_second(single_chord)
            sol_fitness = sol_fitness + fit_major_second(single_chord)
            sol_fitness = sol_fitness + fit_triad(single_chord)

            # check for minor seconds
            # for c in range(len(solution[single_chord])):
            #     if c + 1 > len(solution[single_chord]) - 1:
            #         pass
            #     else:
            #         if (solution[single_chord][c].degree - solution[single_chord][c+1].degree) * -1 == database.minor_second:
            #             sol_fitness -= 3
            #
            # # check that second note and third note are not further than an octave apart
            # if solution[single_chord][1].degree - solution[single_chord][2].degree < 0:
            #     sol_fitness += 1
            #
            # # check that root note and second note are not a minor, nor major second apart
            # if ((solution[single_chord][0].degree - solution[single_chord][1].degree) * -1) == database.minor_second:
            #     sol_fitness -= 5
            #
            # if ((solution[single_chord][0].degree - solution[single_chord][1].degree) * -1) == database.major_second:
            #     sol_fitness -= 5
            #
            # # check if first two notes of each c in each bar
            # # are at the very least a minor or major third interval
            # # as the basic function for every c comes from this interval
            # if ((solution[single_chord][0].degree - solution[single_chord][1].degree) * -1) == database.minor_third:
            #     print(f'Minor third detected on bar{single_chord+1} between root note {solution[single_chord][0]} and {solution[single_chord][1]}')
            #     sol_fitness += 3
            # elif ((solution[single_chord][0].degree - solution[single_chord][1].degree) * -1) == database.major_third:
            #     print(f'Major third detected on bar{single_chord+1} between root note {solution[single_chord][0]} and {solution[single_chord][1]}')
            #     sol_fitness += 3
            # else:
            #     pass
            #
            # # check if root and third note of triad are a perfect fifth apart
            # if ((solution[single_chord][0].degree - solution[single_chord][2].degree) * -1) == database.perfect_fifth:
            #     print(f'Perfect fifth detected on bar {single_chord+1} between root note {solution[single_chord][0]} and {solution[single_chord][1]}')
            #     sol_fitness += 5
            #
            # # check if root and third interval are an octave or two apart
            # if (solution[single_chord][0].degree - solution[single_chord][2].degree) == database.perfect_octave or (solution[single_chord][0].degree - solution[single_chord][1].degree) == (database.perfect_octave * 2):
            #     sol_fitness -= 1
            #
            # # checks for basic inversions
            # # as they can be pleasing, but more checks should be made
            # # for c functions, as inversions change the function
            # chord_to_compare = solution[single_chord]
            # chord_to_compare_1st_inversion = (chord_to_compare / 1)
            # chord_to_compare_2nd_inversion = (chord_to_compare / 2)
            # if chord_to_compare in Chords:
            #     print(f'c found in {single_chord+1}th element!')
            #     sol_fitness += 1
            #
            # if chord_to_compare_1st_inversion in Chords:
            #     print(f'first inversion found in {single_chord+1}th element!')
            #     sol_fitness += 1
            #
            # if chord_to_compare_2nd_inversion in Chords:
            #     print(f'second inversion found in {single_chord+1}th element!')
            #     sol_fitness += 1

            # checks for a perfect fifth interval between a bar and the next bar
            # as a V-I progression is found in most western music
            # if single_chord+1 > len(solution)-1:
            #     print("too far chief")
            # else:
            #     next_bar_check_fifth = solution[single_chord+1][0]
            #     next_bar_check_fifth = next_bar_check_fifth.with_interval(database.perfect_fifth)
            #     chord_to_compare_interval_next_bar = chord_to_compare[0]
            #     if next_bar_check_fifth[1] == chord_to_compare_interval_next_bar:
            #         print(f'perfect fifth detected between root note of bar {single_chord+1} and {single_chord+2}')
            #         sol_fitness += 1
            #
            # if single_chord+1 > len(solution)-1:
            #     print("too far chief")
            # else:
            #     next_bar_check_fourth = solution[single_chord+1][0]
            #     next_bar_check_fourth = next_bar_check_fourth.with_interval(database.perfect_fourth)
            #     chord_to_compare_interval_next_bar = chord_to_compare[0]
            #     if next_bar_check_fourth[1] == chord_to_compare_interval_next_bar:
            #         print(f'perfect fourth detected between root note of bar {single_chord+1} and {single_chord+2}')
            #         sol_fitness += 1
        # print(sol_fitness)
        return sol_fitness
