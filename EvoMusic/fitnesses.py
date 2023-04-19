from main import *
from note_utilities import *


"""
this function checks if chords
have the same note but on different
octaves
"""
def fit_duplicate_tones(c) -> int:
    c_length = len(c) - 1
    for i in range(c_length):
        if i + 2 > c_length:
            pass
        else:
            # specific notes in chords are accessed through array indexing
            if is_same_pitch(c[i], c[i + 1]) or is_same_pitch(c[i], c[i + 2]) or\
                    is_same_pitch(c[i + 1], c[i + 2]):
                return -10
    return 2


"""
this function checks if the root note of the chord
and the 3rd note of the chord have a perfect fifth
between them
"""
def fit_perfect_fifth(c) -> int:
    notes = [0] * len(c)
    for n in range(len(c)):
        if n + 2 > len(c) - 1:
            pass
        else:
            # specific notes in chords are accessed through array indexing
            if interval_between(c[n], c[n + 2]) == database.perfect_fifth:
                return 3
    return -1


"""
this function checks if the root note and
2nd note of the chord form a minor third
"""
def fit_minor_third(c) -> int:
    length = len(c)
    degrees = [0] * length
    for n in range(length):
        degrees[n] = c[n].degree

    for i in range(length):
        if i + 1 >= length:
            break

        # bring note down an octave if more than 12 semitones apart
        if degrees[i] - degrees[i + 1] <= -12:
            degrees[i + 1] = degrees[i + 1] - 12

        if (degrees[i] - degrees[i + 1]) * -1 == database.minor_third:
            return 2
    return 0


"""
this function checks if the root note and
2nd note of the chord form a major third
"""
def fit_major_third(c) -> int:
    length = len(c)
    degrees = [0] * length
    for n in range(length):
        degrees[n] = c[n].degree

    for i in range(length):
        if i + 1 >= length:
            break

        # bring note down an octave if more than 12 semitones apart
        if degrees[i] - degrees[i + 1] <= -12:
            degrees[i + 1] = degrees[i + 1] - 12

        if (degrees[i] - degrees[i + 1]) * -1 == database.major_third:
            return 2
    return 0


"""
this function checks if the root note and
2nd note of the chord form a minor second
"""
def fit_minor_second(c) -> int:
    length = len(c)
    degrees = [0] * length
    for n in range(length):
        degrees[n] = c[n].degree

    for i in range(length):
        if i + 1 >= length:
            break

        # bring note down an octave if more than 12 semitones apart
        if degrees[i] - degrees[i + 1] <= -12:
            degrees[i + 1] = degrees[i + 1] - 12

        if (degrees[i] - degrees[i + 1]) * -1 == database.minor_second:
            return -5
    return 0


"""
this function checks if the root note and
2nd note of the chord form a major second
"""
def fit_major_second(c) -> int:
    length = len(c)
    degrees = [0] * length
    for n in range(length):
        degrees[n] = c[n].degree

    for i in range(length):
        if i + 1 >= length:
            break

        # bring note down an octave if more than 12 semitones apart
        if degrees[i] - degrees[i + 1] <= -12:
            degrees[i + 1] = degrees[i + 1] - 12

        if (degrees[i] - degrees[i + 1]) * -1 == database.major_second:
            return -5
    return 0


"""
this function checks if three chord notes
form a triad
"""
def fit_triad(c) -> int:
    no_of_notes = len(c)
    if no_of_notes < 3:
        return 0

    # chord notes are accessed through array indexing
    for n in range(no_of_notes - 1):
        if (n + 1) > no_of_notes:
            return -1
        elif ((c[n].degree - c[n + 1].degree) * -1 == database.minor_third or (
                c[n].degree - c[n + 1].degree) * -1 == database.major_third) \
                and (c[n].degree - c[n + 2].degree) * -1 == database.perfect_fifth:
            return 5
        else:
            return -1


"""
this function defines the ii-V-I-I chord progression
in the C major scale (D minor, G major, C major, C major)
"""
def fitness_ii_V_I_I(root_notes) -> True | False:
    notes_list = root_notes

    # checks for chord progression while ignoring octave
    # as chords have same function regardless of pitch
    if is_same_pitch(root_notes[0], N('D3')) and is_same_pitch(root_notes[1], N('G3')) and \
            is_same_pitch(root_notes[2], N('C3')) and is_same_pitch(root_notes[3], N('C3')):
        return True
    else:
        return False


"""
this function defines the I-vi-ii-V chord progression
in the C major scale (C major, A minor, D minor, G major)
"""
def fitness_I_vi_ii_V(root_notes) -> True | False:
    notes_list = root_notes

    # checks for chord progression while ignoring octave
    # as chords have same function regardless of pitch
    if is_same_pitch(root_notes[0], N('C3')) and is_same_pitch(root_notes[1], N('A3')) and \
            is_same_pitch(root_notes[2], N('D3')) and is_same_pitch(root_notes[3], N('G3')):
        return True
    else:
        return False


"""
this function defines the I-IV-V-I chord progression
in the C major scale (C major, F major, G major, C major)
"""
def fitness_I_IV_V_I(root_notes) -> True | False:

    # checks for chord progression while ignoring octave
    # as chords have same function regardless of pitch
    if is_same_pitch(root_notes[0], N('C3')) and is_same_pitch(root_notes[1], N('F3')) and \
            is_same_pitch(root_notes[2], N('G3')) and is_same_pitch(root_notes[3], N('C3')):
        return True
    else:
        return False


"""
this function defines the I-V-vi-IV chord progression
in the C major scale (C major, G major, A minor, F major)
"""
def fitness_I_V_vi_IV(root_notes) -> True | False:

    # checks for chord progression while ignoring octave
    # as chords have same function regardless of pitch
    if is_same_pitch(root_notes[0], N('C3')) and is_same_pitch(root_notes[1], N('G3')) and \
            is_same_pitch(root_notes[2], N('A3')) and is_same_pitch(root_notes[3], N('F3')):
        return True
    else:
        return False


"""
this sliding window function checks the solutions
to see if the chord progressions are anywhere within them
"""
def fitness_chord_progression_window(solution, window_size=4):
    s = solution.copy()
    w = window_size
    jazz_progression = False
    rock_progression = False

    if len(s) <= w:
        return 0

    # sliding window that checks an index and the following 3
    # as one unit

    # the loop always stops at length-4
    for i in range(len(s) - w + 1):
        chord_progression_bar_1 = s[i]
        root_1 = chord_progression_bar_1[0]
        chord_progression_bar_2 = s[i + 1]
        root_2 = chord_progression_bar_2[0]
        chord_progression_bar_3 = s[i + w - 1]
        root_3 = chord_progression_bar_3[0]
        chord_progression_bar_4 = s[i + w - 1]
        root_4 = chord_progression_bar_4[0]
        roots = [root_1, root_2, root_3, root_4]

        if fitness_ii_V_I_I(roots) or fitness_I_vi_ii_V(roots):
            jazz_progression = True

        if fitness_I_IV_V_I(roots) or fitness_I_V_vi_IV(roots):
            rock_progression = True

        if jazz_progression or rock_progression:
            return 8
    else:
        return 0


"""
this function runs every chord through every fitness measure
"""
def fitnesses_list(single_chord, sol_fitness):
    s_c = single_chord.copy()
    s_f = sol_fitness
    # list of fitness measures
    f_list = [fit_triad, fit_duplicate_tones, fit_perfect_fifth, fit_major_third, fit_minor_third, fit_major_second,
              fit_minor_second]
    # iterate through all fitness measures and add fitness values
    for fit_func in f_list:
        s_f = s_f + fit_func(s_c)

    return s_f


"""
this function calculates the fitness for each solution
"""
def fitness(solution, genre):
    if solution is None:
        print("????")
    s = solution.copy()
    sol_fitness = 0
    # sol_fitness = sol_fitness + fitness_chord_progression_window(s)
    sol_fitness = sol_fitness + fitness_chord_progression_window(s, 4)
    if solution == [0]:
        return sol_fitness
    else:
        for single_chord in s:

            # check if proper c was randomly created
            if single_chord in Chords:
                sol_fitness = sol_fitness + 1

            # the idea was to have more genre specific measures
            if genre == "jazz":
                print("jazz")
                sol_fitness = sol_fitness + fitnesses_list(single_chord, 0)
            elif genre == "rock":
                sol_fitness = sol_fitness + fitnesses_list(single_chord, 0)
                print("rock")

        return sol_fitness


"""
this function compares the first note of each bar
in the bass solution and harmony solution
"""
def bass_fitness_compare_roots(h, b):
    fit = 0
    b_first_beat = []
    if not len(b) < 32:
        for i in range(len(b)):
            if i % 4 == 0:
                b_first_beat.append(b[i])

        # increment fitness by 1 every time
        # the bass note and chord root match
        for j in range(len(h)):
            if h[j] == b[j]:
                fit = fit + 1

    return fit


"""
this function calculates the bass solution fitness
"""
def bass_fitness(harmony_solution, bass_solution):
    harmony_root_notes = []

    for c in harmony_solution:
        harmony_root_notes.append(c[0])

    bassline_fitness = 0
    bassline_fitness = bassline_fitness + bass_fitness_compare_roots(harmony_root_notes, bass_solution)

    return bassline_fitness


