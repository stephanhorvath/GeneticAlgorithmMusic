import random as rnd
import musicpy as mp
from musicpy import database
from musicpy.structures import chord
from musicpy.musicpy import degree_to_note, C
import note_utilities as noteut


# This function creates a list of all
# the mutation functions and randomly selects
# one, and returns that functions return value
def mutate(solution):
    func_list = [mutate_fix_second, mutate_sus2, mutate_sus4, mutate_first_inversion, mutate_move_one_tone,
                 mutate_flip_quality, mutate_rhythm, mutate_add_7]
    return rnd.choice(func_list)(solution)


"""
this function takes a solution and
calculates the intervals between the 
first and second note of each chord
if it is a major/minor second, it converts
it into a major third
"""
def mutate_fix_second(solution):
    length = len(solution)
    probability = 1 / length
    # probability = 10
    v = solution.copy()

    for i in range(0, length):
        if probability >= rnd.uniform(0, 1):
            if noteut.interval_between(v[i][0], v[i][1]) == database.minor_second:
                v[i][1] = v[i][1]+3
            elif noteut.interval_between(v[i][0], v[i][1]) == database.major_second:
                v[i][1] = v[i][1]+2
            else:
                pass

    return v


"""
this function changes the default rhythm
to a more interesting one that is almost
syncopated
"""
def mutate_rhythm(solution):
    length = len(solution)
    probability = 1 / length
    random_index = rnd.choice(range(length))
    v = solution.copy()

    for i in range(0, random_index):
        if probability >= rnd.uniform(0, 1):
            if len(v[i]) <= 3:
                c = v[i]
                v[i] = c.set(0.375, 0) | c.set(0.0625) | mp.rest(duration=0.125, dotted=None) | c.set(0.125, 0) | \
                       mp.rest(duration=0.125, dotted=None)
            else:
                pass
    return v


"""
this function randomly converts
chords into a suspended 2 chord
"""
def mutate_sus2(solution):
    length = len(solution)
    probability = 1 / length
    v = solution.copy()

    for i in range(1, length):
        if probability >= rnd.uniform(0, 1):
            v[i] = v[i].sus(2)

    return v


"""
this function randomly converts
chords into a suspended 4 chord
"""
def mutate_sus4(solution):
    length = len(solution)
    probability = 1 / length
    v = solution.copy()

    for i in range(1, length):
        if probability >= rnd.uniform(0, 1):
            v[i] = v[i].sus(4)

    return v


"""
this function randomly converts
chords into a dominant 7th chord
"""
def mutate_add_7(solution):
    length = len(solution)
    probability = 1 / length
    random_choice = rnd.choice(range(len(solution)))
    v = solution.copy()
    triad = v[random_choice]
    triad_root = triad[0]

    if probability >= rnd.uniform(0, 1) and len(triad) <= 3:
        seven_chord = triad_root('7')
        v[random_choice] = seven_chord.set(0.75, 0) | mp.rest(duration=1 / 4, dotted=None)

    return v


"""
this function randomly converts
chords into the first inversion
of that chord
"""
def mutate_first_inversion(solution):
    length = len(solution)
    probability = 1 / length
    v = solution.copy()

    for i in range(1, length):
        if probability >= rnd.uniform(0, 1):
            v[i] = v[i] / 1
    return v


"""
this function randomly
moves chords one tone up
in pitch
"""
def mutate_move_one_tone(solution):
    length = len(solution)
    probability = 1 / length
    v = solution.copy()

    for i in range(1, length):
        if probability >= rnd.uniform(0, 1):
            v[i] = v[i] + 1
    return v


"""
this function randomly converts
major triads into minor triads
and vice versa
"""
def mutate_flip_quality(solution):
    length = len(solution)
    probability = 1 / length
    v = solution.copy()

    for i in range(1, length):
        if probability >= rnd.uniform(0, 1):
            # these degree checks convert the notes to MIDI values to
            # determine the interval between the two notes
            if (v[i][0].degree - v[i][1].degree) * -1 == database.minor_third:
                v[i][1] = v[i][1] + 1
            elif (v[i][0].degree - v[i][1].degree) * -1 == database.major_third:
                v[i][1] = v[i][1] - 1
            else:
                pass
    return v


"""
this function randomly moves
one bass note up in pitch if
it is on an even index, and
down in pitch if on odd index
"""
def bass_mutate_move_tone(bass_solution):
    length = len(bass_solution)
    probability = 1 / length
    v = bass_solution.copy()

    for i in range(0, length):
        random_no = rnd.uniform(0, 1)
        if probability >= random_no:
            if random_no % 2 == 0:
                v[i] = v[i] + 1
            else:
                v[i] = v[i] - 1

    return v


"""
this function randomly chooses a note
that happened on the first beat of a bar
and repeats it four times
"""
def bass_mutate_repeat_tone(bass_solution):
    length = len(bass_solution)
    # probability = 1 / length
    probability = 10
    v = bass_solution.copy()
    random_index = rnd.choice(range(len(v)))
    while random_index % 4 != 0 and not random_index <= len(bass_solution)-4:
        random_index = rnd.choice(range(len(v)))

    if probability >= rnd.uniform(0, 1):
        repeated_note = v[random_index]
        for i in range(0, 4):
            v[random_index+i] = repeated_note

    return v


"""
list of bass functions that are randomly applied to solutions
"""
def bass_mutate(bass_solution):
    func_list = [bass_mutate_move_tone, bass_mutate_repeat_tone]
    return rnd.choice(func_list)(bass_solution)
