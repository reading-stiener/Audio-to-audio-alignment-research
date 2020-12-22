from modify_audio import modify_signal, write_files
from modify_video import modify_video
import glob
import os
import re
import librosa

def create_dataset(root_dir):
    """
    Creates a workable dataset for DTW for the URMP dataset (maybe the LSTM dataset too)
    """
    # base directory for dataset
    base_dir = "DTW_dataset"
    inst_label = {
        'violin' : '_vn',
        'flute' : '_fl',
        'trumpet' : '_tpt', 
        'clarinet' : '_cl',
        'cello' : '_vc',
        'saxophone' : '_sax', 
        'tuba' : '_tba',
        'viola' : '_va',
        'trombone' : '_tbn', 
        'bassoon' :  '_bn',
        'horn' : '_hn', 
        'double_bass' : '_db', 
        'oboe' : '_ob'
    }
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
    # Traverse through the directories (BFS traversal)
    for r_dir, sub_dir_list, file_list in os.walk(root_dir):
        if re.match(r"^(URMP)(/\w+)$", r_dir): 
            print("root_dir ", r_dir)
            file_folder = r_dir.split("/")[-1]
            for file_name in file_list:
                if re.match(r"^(AuSep)", file_name):
                    for inst, key in inst_label.items():
                        if key in file_name:
                            inst_folder_path = os.path.join(base_dir, inst)
                            if not os.path.exists(inst_folder_path):
                                os.mkdir(inst_folder_path)
                            file_path = os.path.join(r_dir, file_name)
                            print("file ", file_path)
                            if not os.path.exists(os.path.join(inst_folder_path, file_name)):
                                signal, sr = librosa.load(
                                    path = file_path
                                )
                                signal_modified, changes = modify_signal(signal, sr)
                                write_files(
                                    folder=inst_folder_path,
                                    filename=file_name[:-4],
                                    signal=signal_modified, 
                                    sr=sr,
                                    mod_dict=changes
                                )
                                video_filepath = os.path.join(r_dir, "Vid_"+file_folder+".mp4")
                                modify_video(
                                    folder=inst_folder_path, 
                                    filename=video_filepath,
                                    mod_dict=changes,
                                    audio_file=file_name
                                )
                            else:
                                print("File already exists")

if __name__ == "__main__":
    create_dataset(root_dir="URMP")