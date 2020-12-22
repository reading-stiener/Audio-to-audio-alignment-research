from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx
from moviepy.video.fx.speedx import speedx
from pprint import pprint
import os
import json

def modify_video(folder, filename, mod_dict, audio_file=None):
    with VideoFileClip(filename, audio=False) as videoclip:
        cliplist = []
        for changes in mod_dict:
            ta, tb, rate = changes["original_start_time"], changes["original_start_time"]+changes["original_delta_time"], changes["rate"]
            snippet = videoclip.subclip(ta, tb)
            # applying speed effect and appending to clip list
            cliplist.append(snippet.fx(speedx, rate))
        modified_clip = concatenate_videoclips(cliplist)
        inputfolder, inputfile = os.path.split(filename)
        if audio_file:
            modified_clip.write_videofile(os.path.join(folder, inputfile[:-4]+ "_"+ audio_file.split("_")[1]) + ".mp4")
        else:
            modified_clip.write_videofile(os.path.join(folder, inputfile))
if __name__ == "__main__":
    filename = "/home/camel/Documents/Honors Thesis Research/Audio-to-audio-alignment-research/LSTM_dataset_4/violin/01_Jupiter_vn_vc/violin_1.mp4"
    folder = "annotations"
    with open("annotations/Jupiter_vn_vc.json") as f:
        mod_dict = json.load(fp=f)
    modify_video(folder, filename, mod_dict)
    