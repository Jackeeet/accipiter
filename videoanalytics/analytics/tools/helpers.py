def translated_segment(initial, side, translation):
    match side:
        case 1:  # on top border
            return initial.translated(-1 * translation, vertical=True)
        case 2:  # on right border
            return initial.translated(translation, vertical=False)
        case 3:  # on bottom border
            return initial.translated(translation, vertical=True)
        case 4:  # on left border
            return initial.translated(-1 * translation, vertical=False)
        case _:
            return initial


def connect(initial, translated, reverse=False):
    if reverse:
        return translated.end_to_point(initial.end)
    return initial.start_to_point(translated.start)
