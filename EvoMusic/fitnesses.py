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


def fit_perfect_fifth(chord) -> int:
    split_track(chord)
    notes = [0] * len(chord)
    for n in range(len(chord)):
        if n + 2 > len(chord) - 1:
            pass
        else:
            if compute_degree_separation(chord[n], chord[n+2]) == database.perfect_fifth:
                return 3
    return -1


def fit_minor_third(chord) -> int:
    length = len(chord)
    degrees = [0] * length
    for n in range(length):
        degrees[n] = chord[n].degree

    for i in range(length):
        if i + 1 >= length:
            break

        if degrees[i] - degrees[i + 1] <= -12:
            degrees[i + 1] = degrees[i + 1] - 12

        if (degrees[i] - degrees[i + 1]) * -1 == database.minor_third:
            return 1
    return 0


def fit_major_third(chord) -> int:
    length = len(chord)
    degrees = [0] * length
    for n in range(length):
        degrees[n] = chord[n].degree

    for i in range(length):
        if i + 1 >= length:
            break

        if degrees[i] - degrees[i + 1] <= -12:
            degrees[i + 1] = degrees[i + 1] - 12

        if (degrees[i] - degrees[i + 1]) * -1 == database.major_third:
            return 1
    return 0


def fit_minor_second(chord) -> int:
    length = len(chord)
    degrees = [0] * length
    for n in range(length):
        degrees[n] = chord[n].degree

    for i in range(length):
        if i + 1 >= length:
            break

        if degrees[i] - degrees[i + 1] <= -12:
            degrees[i + 1] = degrees[i + 1] - 12

        if (degrees[i] - degrees[i + 1]) * -1 == database.minor_second:
            return -1
    return 0


def fit_major_second(chord) -> int:
    length = len(chord)
    degrees = [0] * length
    for n in range(length):
        degrees[n] = chord[n].degree

    for i in range(length):
        if i + 1 >= length:
            break

        if degrees[i] - degrees[i + 1] <= -12:
            degrees[i + 1] = degrees[i + 1] - 12

        if (degrees[i] - degrees[i + 1]) * -1 == database.major_second:
            return -1
    return 0


def fit_triad(chord) -> int:
    no_of_notes = len(chord)
    if no_of_notes < 3:
        return 0

    for n in range(no_of_notes - 1):
        if (n + 1) > no_of_notes:
            return -1
        elif ((chord[n].degree - chord[n + 1].degree) * -1 == database.minor_third or (
                chord[n].degree - chord[n + 1].degree) * -1 == database.major_third) \
                and (chord[n].degree - chord[n + 2].degree) * -1 == database.perfect_fifth:
            return 1
        else:
            return 0


def fitness(solution):
    sol_fitness = 0
    if solution == [0]:
        return sol_fitness
    else:
        for b in solution:
            notes = [0] * len(b)

            # check if proper chord was randomly created
            if b in Chords:
                sol_fitness = sol_fitness + 1

            sol_fitness = sol_fitness + fit_duplicate_tones(b)
            sol_fitness = sol_fitness + fit_perfect_fifth(b)
            sol_fitness = sol_fitness + fit_minor_third(b)
            sol_fitness = sol_fitness + fit_major_third(b)
            sol_fitness = sol_fitness + fit_major_second(b)
            sol_fitness = sol_fitness + fit_major_second(b)
            sol_fitness = sol_fitness + fit_triad(b)

            # check for minor seconds
            # for c in range(len(solution[b])):
            #     if c + 1 > len(solution[b]) - 1:
            #         pass
            #     else:
            #         if (solution[b][c].degree - solution[b][c+1].degree) * -1 == database.minor_second:
            #             sol_fitness -= 3
            #
            # # check that second note and third note are not further than an octave apart
            # if solution[b][1].degree - solution[b][2].degree < 0:
            #     sol_fitness += 1
            #
            # # check that root note and second note are not a minor, nor major second apart
            # if ((solution[b][0].degree - solution[b][1].degree) * -1) == database.minor_second:
            #     sol_fitness -= 5
            #
            # if ((solution[b][0].degree - solution[b][1].degree) * -1) == database.major_second:
            #     sol_fitness -= 5
            #
            # # check if first two notes of each chord in each bar
            # # are at the very least a minor or major third interval
            # # as the basic function for every chord comes from this interval
            # if ((solution[b][0].degree - solution[b][1].degree) * -1) == database.minor_third:
            #     print(f'Minor third detected on bar{b+1} between root note {solution[b][0]} and {solution[b][1]}')
            #     sol_fitness += 3
            # elif ((solution[b][0].degree - solution[b][1].degree) * -1) == database.major_third:
            #     print(f'Major third detected on bar{b+1} between root note {solution[b][0]} and {solution[b][1]}')
            #     sol_fitness += 3
            # else:
            #     pass
            #
            # # check if root and third note of triad are a perfect fifth apart
            # if ((solution[b][0].degree - solution[b][2].degree) * -1) == database.perfect_fifth:
            #     print(f'Perfect fifth detected on bar {b+1} between root note {solution[b][0]} and {solution[b][1]}')
            #     sol_fitness += 5
            #
            # # check if root and third interval are an octave or two apart
            # if (solution[b][0].degree - solution[b][2].degree) == database.perfect_octave or (solution[b][0].degree - solution[b][1].degree) == (database.perfect_octave * 2):
            #     sol_fitness -= 1
            #
            # # checks for basic inversions
            # # as they can be pleasing, but more checks should be made
            # # for chord functions, as inversions change the function
            # chord_to_compare = solution[b]
            # chord_to_compare_1st_inversion = (chord_to_compare / 1)
            # chord_to_compare_2nd_inversion = (chord_to_compare / 2)
            # if chord_to_compare in Chords:
            #     print(f'chord found in {b+1}th element!')
            #     sol_fitness += 1
            #
            # if chord_to_compare_1st_inversion in Chords:
            #     print(f'first inversion found in {b+1}th element!')
            #     sol_fitness += 1
            #
            # if chord_to_compare_2nd_inversion in Chords:
            #     print(f'second inversion found in {b+1}th element!')
            #     sol_fitness += 1

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
        # print(sol_fitness)
        return sol_fitness
