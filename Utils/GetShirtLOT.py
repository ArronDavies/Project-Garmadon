def GetShirtLOT(Color, Style):  # Get color assigned to IDs in the CDClient
    lot = -1

    Greater34 = {0: 5730, 1: 5736, 3: 5808, 5: 5754, 6: 5760, 7: 5766, 8: 5772, 9: 5778, 10: 5784, 11: 5802, 13: 5796,
                 14: 5802, 15: 5808, 16: 5814, 84: 5820, 96: 5826}
    Less34 = {0: 4049, 1: 4083, 3: 4151, 5: 4185, 6: 4219, 7: 4263, 8: 4287, 9: 4321, 10: 4355, 11: 4389, 13: 4423,
              14: 4457, 15: 4491, 16: 4491, 84: 4559, 96: 4593}

    if Style > 34:
        lot = Greater34[Color]
        lot += Style - 35
    else:
        lot = Less34[Color]
        lot += Style - 1

    return lot
