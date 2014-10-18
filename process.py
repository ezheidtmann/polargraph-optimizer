#!/usr/bin/python
types = {
    'C13': 'pendown',
    'C14': 'penup',
}

def typename(code):
    return types.get(code, 'other')


instructions = []

import fileinput
for line in fileinput.input():
    inst = { 'line': line.rstrip(), 'lineparts': line.rstrip().split(',') }
    inst['typecode'] = inst['lineparts'][0]
    inst['typename'] = typename(inst['typecode'])
    instructions.append(inst)

glyphs = []
glyph = { 'instructions': [] }
for inst in instructions:
    glyph['instructions'].append(inst)
    if inst['typename'] == 'penup':
        if len(glyph['instructions']) > 1:
            glyphs.append(glyph)
        glyph = { 'instructions': [] }

for glyph in glyphs:
    glyph['start_coords'] = glyph['instructions'][0]['lineparts'][1:3]
    glyph['end_coords'] = glyph['instructions'][-2]['lineparts'][1:3]
    print "GLYPH start:%s" % glyph['start_coords']
    print "GLYPH end:%s" % glyph['end_coords']
    for inst in glyph['instructions']:
        if inst['typename'] != 'other':
            print inst['typename']
        else:
            print inst['line']

# nearest neighbor
for glyph in glyphs:
    pass   
