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


def mutate_sus2(solution):
    length = len(solution)
    probability = 1 / length
    v = solution.copy()

    for i in range(1, length):
        if probability >= rnd.uniform(0, 1):
            v[i] = v[i].sus(2)

    return v


def mutate_sus4(solution):
    length = len(solution)
    probability = 1 / length
    v = solution.copy()

    for i in range(1, length):
        if probability >= rnd.uniform(0, 1):
            v[i] = v[i].sus(4)

    return v


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


def mutate_first_inversion(solution):
    length = len(solution)
    probability = 1 / length
    v = solution.copy()

    for i in range(1, length):
        if probability >= rnd.uniform(0, 1):
            v[i] = v[i] / 1
    return v


def mutate_move_one_tone(solution):
    length = len(solution)
    probability = 1 / length
    v = solution.copy()

    for i in range(1, length):
        if probability >= rnd.uniform(0, 1):
            v[i] = v[i] + 1
    return v


def mutate_flip_quality(solution):
    length = len(solution)
    probability = 1 / length
    # probability = -1
    v = solution.copy()

    for i in range(1, length):
        if probability >= rnd.uniform(0, 1):
            if (v[i][0].degree - v[i][1].degree) * -1 == database.minor_third:
                v[i][1] = v[i][1] + 1
            elif (v[i][0].degree - v[i][1].degree) * -1 == database.major_third:
                v[i][1] = v[i][1] - 1
            else:
                pass
    return v


def mutate_five_one(solution):
    length = len(solution)
    probability = 1 / length
    random_choice = rnd.choice(range(len(solution)))
    v = solution.copy()
    one_chord = v[random_choice]

    if probability >= rnd.uniform(0, 1) and len(one_chord) <= 6:
        fifth_note = degree_to_note(v[random_choice][0].degree + database.perfect_fifth)
        fifth_chord = C(f'{fifth_note}:7')
        v[random_choice] = fifth_chord.set(0.5, 0) | one_chord.set(0.5, 0)
    return v


def mutate_four_one(solution):
    length = len(solution)
    probability = 1 / length
    random_choice = rnd.choice(range(len(solution)))
    v = solution.copy()
    one_chord = v[random_choice]

    if probability >= rnd.uniform(0, 1) and len(one_chord) <= 6:
        fourth_note = degree_to_note(v[random_choice][0].degree + database.perfect_fourth)
        fourth_chord = C(f'{fourth_note}:maj')
        v[random_choice] = fourth_chord.set(0.5, 0) | one_chord.set(0.5, 0)
    return v


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


def bass_mutate(bass_solution):
    func_list = [bass_mutate_move_tone, bass_mutate_repeat_tone]
    return rnd.choice(func_list)(bass_solution)
