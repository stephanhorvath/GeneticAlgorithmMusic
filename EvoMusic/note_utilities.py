def compare_without_octave(note_a, note_b) -> True | False:
    a = note_a.degree % 12
    b = note_b.degree % 12
    return a == b


def compute_degree_separation(note_a, note_b):
    degree_of_separation = note_a.degree - note_b.degree
    if degree_of_separation < 0:
        degree_of_separation = degree_of_separation * -1
    return degree_of_separation
