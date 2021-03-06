def print_cols(lines):
    cols = zip(*lines)
    col_widths = [max(len(str(word)) for word in col) + 2 for col in cols]
    for line in lines:
        print("".join(str(word).ljust(col_widths[i]) for i, word in enumerate(line)))


def merge(ranges):
    if not ranges:
        return []
    saved = list(ranges[0])
    for lower, upper in sorted([sorted(t) for t in ranges]):
        if lower <= saved[1] + 1:
            saved[1] = max(saved[1], upper)
        else:
            yield tuple(saved)
            saved[0] = lower
            saved[1] = upper
    yield tuple(saved)


def align(value, page_size=4096):
    m = value % page_size
    f = page_size - m
    aligned_size = value + f
    return aligned_size


def remove_range(old_range, to_remove):
    old_lower, old_upper = old_range
    remove_lower, remove_upper = to_remove
    if old_lower == remove_lower and old_upper == remove_upper:
        return []
    if old_lower < remove_lower and old_upper > remove_upper:
        # deleted range is inside old range
        return [(old_lower, remove_lower - 1), (remove_upper + 1, old_upper)]
    if remove_lower <= old_lower and old_upper > remove_upper:
        # only deleted range upper limit is inside old range
        return [(remove_upper + 1, old_upper)]
    if old_lower < remove_lower and remove_upper >= old_upper:
        # only lower limit is inside old range
        return [(old_lower, remove_lower - 1)]
    # range unaffected
    return [(old_lower, old_upper)]
