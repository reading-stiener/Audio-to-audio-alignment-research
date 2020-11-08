import librosa
import random
import numpy as np
import pprint
# contains the defs to stretch and shrink audio

def modify_snippet(snippet, rate):
    signal_snippet = librosa.effects.time_stretch(
        y=snippet,
        rate=rate
    )
    return signal_snippet

def modify_signal(signal, sr):
    start_idx = 0
    end_idx = signal.shape[0]
    start_mod_idx = 0
    snippet_lengths = [2, 3, 4, 5, 6, 7, 8, 9]
    modified_sig = []
    changes_dict = []
    while start_idx < end_idx:
        snippet_length = random.choice(snippet_lengths) * sr
        rate = random.random() * 3
        if start_idx + snippet_length <= end_idx:
            mod_snippet = modify_snippet( 
                    snippet = signal[start_idx:start_idx+snippet_length],
                    rate=rate
                )
            modified_sig.append(
                mod_snippet
            )
            changes_dict.append(
                {
                    "original_start_time": round(start_idx/sr, 2),
                    "original_delta_time": round(snippet_length/sr, 2),
                    "modified_start_time": round(start_mod_idx/sr, 2),
                    "modified_delta_time": round(mod_snippet.shape[0]/sr, 2),
                    "rate": rate
                }
            )
            start_idx += snippet_length 
        else:
            mod_snippet = modify_snippet( 
                    snippet = signal[start_idx:end_idx],
                    rate=rate
                )
            modified_sig.append(
                mod_snippet
            )
            changes_dict.append(
                {
                    "original_start_time": round(start_idx/sr, 2),
                    "original_delta_time": round(snippet_length/sr, 2),
                    "modified_start_time": round(start_mod_idx/sr, 2),
                    "modified_delta_time": round(mod_snippet.shape[0]/sr, 2),
                    "rate": rate
                }
            )
            start_idx = end_idx
        start_mod_idx += mod_snippet.shape[0]
    return np.concatenate(modified_sig), changes_dict

if __name__ == "__main__": 
    filename = "/home/camel/Documents/Honors Thesis Research/Audio-to-audio-alignment-research/URMP/01_Jupiter_vn_vc/AuMix_01_Jupiter_vn_vc.wav"
    signal, sr = librosa.load(
        path = filename
    )
    print(signal)
    signal_modified, changes = modify_signal(signal, sr)
    pprint.pprint(changes)
    