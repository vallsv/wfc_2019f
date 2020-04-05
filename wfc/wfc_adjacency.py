"""Convert input data to adjacency information"""
from collections import Counter
import numpy as np

import pdb

def adjacency_extraction(pattern_grid, pattern_catalog, direction_offsets, pattern_size=[2, 2]):
    """Takes a pattern grid and returns a list of all of the legal adjacencies found in it."""
    dimensions = (1,0)
    not_a_number = -1
    def is_valid_overlap_xy(adjacency_direction, pattern_1, pattern_2):
        """Given a direction and two patterns, find the overlap of the two patterns
        and return True if the intersection matches."""

        #TODO: can probably speed this up by using the right slices, rather than rolling the whole pattern...
        #shifted = np.roll(np.pad(pattern_catalog[pattern_2], max(pattern_size), mode='constant', constant_values = not_a_number), adjacency_direction, dimensions)
        #compare = shifted[pattern_size[0] : pattern_size[0] + pattern_size[0], pattern_size[1] : pattern_size[1] + pattern_size[1]]

        left = max(0, 0, + adjacency_direction[0])
        right = min(pattern_size[0], pattern_size[0] + adjacency_direction[0])
        top = max(0, 0 + adjacency_direction[1])
        bottom = min(pattern_size[1], pattern_size[1] + adjacency_direction[1])
        a = pattern_catalog[pattern_1][top:bottom, left:right]
        b = compare[top:bottom, left:right]
        res = np.array_equal(a, b)
        return res

    def is_valid_overlap_xy_fast(adjacency_direction, pattern_1, pattern_2):

        return True

    print("===PATTERN GRID===")
    print(pattern_grid)

    def is_found_in_source(adjacency_direction, pattern_1, pattern_2):
        """Is the combination found in the wild in the pattern grid? Some legal adjacencies won't have examples in the data."""
        # for index, pat in np.ndenumerate(pattern_grid):
        #     offset = np.add(index, adjacency_direction)
        #     not_offset = np.add(index, [0,0])
        #     try:
        #         #print(pattern_grid.shape)
        #         #print(max(pattern_grid.shape))
        #         print(f"{index} + {adjacency_direction} = {offset} : {pat} ~ {not_offset}")
        #         print(pattern_grid[offset])
        #         print(pattern_grid[index])
        #         print(pattern_grid[not_offset])
        #         raise Error
        #         #print(pat)
        #         #print(np.equal(pat, pattern_grid[offset]))
        #     except IndexError:
        #         pass

        return True # TODO



    pattern_list = list(pattern_catalog.keys())
    legal = []
    countpat = 0
    for direction_index, direction in direction_offsets:
        left = max(0, 0, + direction[0])
        right = min(pattern_size[0], pattern_size[0] + direction[0])
        top = max(0, 0 + direction[1])
        bottom = min(pattern_size[1], pattern_size[1] + direction[1])
        pattern_1_array = [False] * len(pattern_list)
        for p1_index, pattern_1 in enumerate(pattern_list):
            pattern_1_array[p1_index] = pattern_catalog[pattern_1][top:bottom, left:right]
        pattern_1_array = np.array(pattern_1_array)
        for pattern_2 in pattern_list:
            countpat += 1
            print(f"{pattern_2} : {countpat} of {len(pattern_list)}")
            shifted = np.roll(np.pad(pattern_catalog[pattern_2], max(pattern_size), mode='constant', constant_values = not_a_number), direction, dimensions)
            compare = shifted[pattern_size[0] : pattern_size[0] + pattern_size[0], pattern_size[1] : pattern_size[1] + pattern_size[1]]
            b = compare[top:bottom, left:right]
            comparison = pattern_1_array == b
            for p1_index, pattern_1 in enumerate(pattern_list):
                a = pattern_1_array[p1_index]
                res = np.array_equal(a, b)
                if res:
                    if not np.all(comparison[p1_index]):
                        print(f"res and comparison mismatch at {p1_index}: {res} vs {comparison[p1_index]}")
                    legal.append((direction, pattern_1, pattern_2))
                else:
                    if np.all(comparison[p1_index]):
                        print(f"comparison and res mismatch at {p1_index}: {res} vs {comparison[p1_index]}")

            if countpat >= 5:
                countpat = 0
                break
    print(legal)
    return legal



def test_adjacency_extraction():
    from wfc_tiles import make_tile_catalog
    from wfc_patterns import make_pattern_catalog
    import imageio

    # TODO: generalize this to more than the four cardinal directions
    direction_offsets = list(enumerate([(0, -1), (1, 0), (0, 1), (-1, 0)]))


    filename = "../images/samples/Red Maze.png"
    img = imageio.imread(filename)
    tile_size = 1
    pattern_width = 2
    rotations = 0
    tile_catalog, tile_grid, code_list, unique_tiles = make_tile_catalog(img, tile_size)
    pattern_catalog, pattern_weights, pattern_list, pattern_grid = make_pattern_catalog(tile_grid, pattern_width, rotations)
    adjacency_relations = adjacency_extraction(pattern_grid, pattern_catalog, direction_offsets)
    assert(((0, -1), -6150964001204120324, -4042134092912931260) in adjacency_relations)
    assert(((-1, 0), -4042134092912931260, 3069048847358774683) in adjacency_relations)
    assert(((1, 0), -3950451988873469076, -3950451988873469076) in adjacency_relations)
    assert(((-1, 0), -3950451988873469076, -3950451988873469076) in adjacency_relations)
    assert(((0, 1), -3950451988873469076, 3336256675067683735) in adjacency_relations)
    assert(not ((0, -1), -3950451988873469076, -3950451988873469076) in adjacency_relations)
    assert(not ((0, 1), -3950451988873469076, -3950451988873469076) in adjacency_relations)


if __name__ == "__main__":
    test_adjacency_extraction()
