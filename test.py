import pretty_midi

midi_filename = "URMP/01_Jupiter_vn_vc/Sco_01_Jupiter_vn_vc.mid"
midi_object =  pretty_midi.PrettyMIDI(midi_filename)
print(midi_object)
X_midi = midi_object.synthesize(fs=22050)
