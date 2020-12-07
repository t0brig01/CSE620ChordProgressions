from midiutil.MidiFile import MIDIFile

def run(pop):
    mf = MIDIFile(1)
    track = 0
    time = 0

    mf.addTrackName(track,time,"Sample Track")
    mf.addTempo(track,time,120)

    channel = 0
    volume = 100
    i = 0
    for chord in pop.chords:
        for note in chord:
            mf.addNote(track,channel,note,i,1,volume)
        i += 1
    
    with open ("output.mid",'wb') as outf:
        mf.writeFile(outf)