def is_same_pitch(note_a, note_b) -> bool:
    a = note_a.degree % 12
    b = note_b.degree % 12
    return a == b


def interval_between(note_a, note_b):
    return abs(note_a.degree - note_b.degree)
