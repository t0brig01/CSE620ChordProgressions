TEMPLATE = r"""global = {
  \key $key \$grade
  \time 4/4
}
\parallelMusic #'(voiceA voiceB voiceC voiceD) {
  % Bar 1
$notes
  % Bar 2 ...
}
\score {
  \new PianoStaff <<
     \new Staff {
       \global
       <<
         \voiceA
         \\
         \voiceB
       >>
     }
     \new Staff {
       \global \clef bass
       <<
         \voiceC
         \\
         \voiceD
       >>
     }
  >>
  \layout{}
  \midi{}
}"""

import os

lily_file_name = os.sys.argv[1]
output_name = os.sys.argv[2]
os.system("lilypond -dbackend=eps {}".format(lily_file_name))
if '/' in lily_file_name:
    lily_file_name = lily_file_name[lily_file_name.index('/')+1:]
os.system("convert -density 1000x1000 {}eps {}".format(lily_file_name[:-2], output_name))
os.system("rm {}-*".format(lily_file_name[:-3]))
os.system("rm {}.eps".format(lily_file_name[:-3]))
os.system("rm {}.pdf".format(lily_file_name[:-3]))
os.system("convert {0}.jpg -crop x7000 {0}.jpg".format(output_name[:-4]))
os.system("convert -trim {}-0.jpg {}".format(output_name[:-4], output_name))
os.system("rm {}-*".format(output_name[:-4]))
if not os.path.isdir("img"):
    os.system("mkdir img")
os.system("mv {0} img/{0}".format(output_name))


def transform_lilypond(ton, indiv):
    """Take one list of chords and print the it in lilypond notation"""
    note_map = dict()
    if ton[-1] == 'M':
        note_map = {0: 'c',
                    1: 'cis',
                    2: 'd',
                    3: 'dis',
                    4: 'e',
                    5: 'f',
                    6: 'fis',
                    7: 'g',
                    8: 'gis',
                    9: 'a',
                    10: 'ais',
                    11: 'b'
                    }
    else:
        note_map = {0: 'c',
                    1: 'des',
                    2: 'd',
                    3: 'ees',
                    4: 'e',
                    5: 'f',
                    6: 'ges',
                    7: 'g',
                    8: 'aes',
                    9: 'a',
                    10: 'bes',
                    11: 'b'
                    }
    voces = [[], [], [], []]

    for chord in indiv:
        for note, voce in zip(chord, voces):

            octave = (note // 12) - 4
            name_lily = note_map[note % 12]
            if octave < 0:
                name_lily += ',' * (octave * -1)
            elif octave > 0:
                name_lily += "'" * octave
            voce.append(name_lily)
    form_txt = '{}|\n{}|\n{}|\n{}|\n'
    print(form_txt.format(*(' '.join(voce) for voce in reversed(voces))))