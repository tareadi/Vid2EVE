import datatable as dtable
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from IPython.display import HTML
from Events import Event
from gen_vis import event_agg
from media_info import all_media_detail

if __name__ == "__main__":
    pic_file ,time_stamp, image_width , image_height = all_media_detail('/Users/adityatare/Vid2EVE/tennis.mp4')
    print("Generating Events......")
    model = Event(image_width,image_height,fixed_thres=0.4,adapt_thres_coef_shift=0.05)
    model.generate_events(pic_file,time_stamp)
    file = dtable.fread("/Users/adityatare/Vid2EVE/events.text",sep = " ").to_pandas()
    file.columns = ["timestamp","x","y","polarity"]
    file["polarity"] *= 1
    t_r = 0.01
    M = file['x'].max() + 1
    N = file['y'].max() + 1
    timestamp = np.array(file['timestamp'].values)
    x = np.array(file['x'].values)
    y = np.array(file['y'].values)
    polarity = np.array(file['polarity'].values)
    print("Generating Superframes.......")
    superframes = event_agg(timestamp, x, y, polarity, t_r, M, N)
    frames = [] # for storing the generated images
    fig = plt.figure()
    for i in range(len(superframes)):
        frames.append([plt.imshow(superframes[i], animated = True)])

    ani = animation.ArtistAnimation(fig, frames, interval = 50, blit = False, repeat_delay = 1000)
    ani.save('video.gif')
    HTML(ani.to_jshtml())
