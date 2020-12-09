# CSE620ChordProgressions
Why make music when computers can do it for you?

## Prerequisites ##
* Python 3.x
* Python packages
  * ypstruct
  * pygame
  * abjad
  * numpy
  * midiutil
* Lilypond (For the visual of chord progression)
* Lilypond path added to environment variables 

## How to Run #
After installing the packages and programs above, simply run `python main.py` in cmd.

Make sure sound is on to hear the chord progression that was created!

## Sample Outputs ##
Every iteration, it will output the best cost and worst cost. It is currently set to have 100 iterations every run, and only one run is set right now. This multiple runs was mainly for testing. 

```
Iteration 99: Best Cost = -8.0 / Worst Cost = -6.0
Run 1 done
Max: 30.0
Min: -1.33
Average: -0.133
struct({'chords': [[55, 65], [57, 65], [69, 72], [62, 72], [69, 81], [62, 72], [55, 65], [48, 53]], 'cost': -8})
```
