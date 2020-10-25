from typing import List
from copy import copy

class MergeType:
    BEFORE = 1
    ZIP_BEFORE = 2
    ZIP_AFTER = 3
    AFTER = 4

def deduce_local_centers(line_centers, merge_type: MergeType):
    all_centers = []
    for line1 in line_centers:
        for line2 in line_centers:
            if line1 == line2:
                continue
            new_center = list(set(line1['center']).intersection(set(line2['center'])))
            # bisher ist das nur MergeType.BEFORE
            new_lines = []
            if merge_type == MergeType.BEFORE:
                new_lines = copy(line1['lines'])
                new_lines.extend(copy(line2['lines']))
            elif merge_type == MergeType.AFTER:
                new_lines = copy(line2['lines'])
                new_lines.extend(copy(line1['lines'])) 
            elif merge_type == MergeType.ZIP_BEFORE:
                for i in range(max(len(line1['lines']), len(line2['lines']))):
                    if i < len(line1['lines']):
                        new_lines.append(line1['lines'][i])
                    if i < len(line2['lines']):
                        new_lines.append(line2['lines'][i])
            elif merge_type == MergeType.ZIP_AFTER:
                for i in range(max(len(line1['lines']), len(line2['lines']))):
                    if i < len(line2['lines']):
                        new_lines.append(line2['lines'][i])
                    if i < len(line1['lines']):
                        new_lines.append(line1['lines'][i])
            all_centers.append({'lines': new_lines, 'center': new_center})

    result = []
    already_inserted_lines = set()
    for line_center in sorted(all_centers, key=lambda el: len(el['center']), reverse=True):
        already_treated = already_inserted_lines.intersection(set(line_center['lines']))
        if len(already_treated) > 0:
            continue
        for line in line_center['lines']:
            already_inserted_lines.add(line)
        result.append(line_center)

    for line_center in line_centers:
        already_treated = already_inserted_lines.intersection(set(line_center['lines']))
        if len(already_treated) > 0:
            continue
        result.append(line_center)

    return result

class TimeTable:
    def __init__(self, lines: List['Line'], merge_type: MergeType):
        # it is assumed that all the input lines have a common center
        self.lines = lines
        self.merge_type = merge_type
        self.sort()

    def sort(self):
        result = [{'lines': [line], 'center': line.all_stations } for line in self.lines]
        prev_size = len(result)*2
        while len(result) >= 1 and prev_size != len(result):
            for r in result:
                print([line.name for line in r['lines']])
                print(len(r['center']))
            print()
            prev_size = len(result)
            result = deduce_local_centers(result, self.merge_type)
            