"""Procedurally drawn 6x13 Powerline glyphs (U+E0A0-E0A3, U+E0B0-E0BF).

The separators are generated from simple geometry so they tile edge to edge with
neighbouring cells; the four symbol glyphs (branch, line number, lock, column)
are drawn by hand.  All output is rows of '#'/'.' strings, 6 wide x 13 tall.
"""
W, H = 6, 13


def _grid(fn):
    return ["".join("#" if fn(x, y) else "." for x in range(W)) for y in range(H)]


def _mirror(rows):
    return [r[::-1] for r in rows]


def _tri_count(y):
    return max(1, round(W * (1 - abs(y - 6) / 7)))


def _round_count(y):
    return max(1, round(W * (1 - ((y - 6) / 6.5) ** 2) ** 0.5))


def _solid(count):
    return _grid(lambda x, y: x < count(y))


def _tri_diag_lower_left(y):
    return round((y + 1) * W / H)


def _tri_diag_upper_left(y):
    return round((H - y) * W / H)


SYMBOLS = {
    # branch
    0xE0A0: """
        ......
        .##.##
        .##.##
        .#..#.
        .#.##.
        .#.#..
        .###..
        .#....
        .#....
        .#....
        ###...
        ###...
        ......
    """,
    # line number (LN)
    0xE0A1: """
        ......
        #.....
        #..#.#
        #..##.
        #..#.#
        ####..
        ......
        #..#.#
        #..#.#
        #..###
        ......
        ......
        ......
    """,
    # lock
    0xE0A2: """
        ......
        ......
        .###..
        #...#.
        #...#.
        #####.
        #####.
        ##.##.
        ##.##.
        #####.
        #####.
        ......
        ......
    """,
    # column
    0xE0A3: """
        ......
        .#.#..
        .#.#..
        .#.#..
        ##.##.
        .#.#..
        .#.#..
        .#.#..
        ##.##.
        .#.#..
        .#.#..
        .#.#..
        ......
    """,
}


def _hand(s):
    rows = [r.strip() for r in s.strip().splitlines()]
    assert len(rows) == H and all(len(r) == W for r in rows), rows
    return rows


def _outline_diag_ll():
    return _grid(lambda x, y: x == round(y * (W - 1) / (H - 1)))


def glyphs():
    out = {}
    for cp, art in SYMBOLS.items():
        out[cp] = _hand(art)

    right_tri = _solid(_tri_count)
    right_tri_edge = _grid(lambda x, y: x == _tri_count(y) - 1)
    out[0xE0B0] = right_tri
    out[0xE0B1] = right_tri_edge
    out[0xE0B2] = _mirror(right_tri)
    out[0xE0B3] = _mirror(right_tri_edge)

    right_round = _solid(_round_count)
    right_round_edge = _grid(lambda x, y: x == _round_count(y) - 1 or
                             (y in (0, H - 1) and x < _round_count(y)))
    out[0xE0B4] = right_round
    out[0xE0B5] = right_round_edge
    out[0xE0B6] = _mirror(right_round)
    out[0xE0B7] = _mirror(right_round_edge)

    ll = _grid(lambda x, y: x < _tri_diag_lower_left(y))
    ul = _grid(lambda x, y: x < _tri_diag_upper_left(y))
    back = _outline_diag_ll()          # '\'
    slash = _mirror(back)              # '/'
    out[0xE0B8] = ll
    out[0xE0B9] = back
    out[0xE0BA] = _mirror(ll)
    out[0xE0BB] = slash
    out[0xE0BC] = ul
    out[0xE0BD] = slash
    out[0xE0BE] = _mirror(ul)
    out[0xE0BF] = back
    return out


if __name__ == "__main__":
    for cp, rows in sorted(glyphs().items()):
        print("U+%04X" % cp)
        print("\n".join(rows))
        print()
