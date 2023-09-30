import csv
import numpy as np
import os 
# ten files test_cloud_1.txt, test_cloud2.txt, ..., test_cloud10.txt
file_names = ['./test_clouds/test_cloud0.txt', 'test_clouds/test_cloud1.txt', './test_clouds/test_cloud2.txt', './test_clouds/test_cloud3.txt', './test_clouds/test_cloud4.txt', './test_clouds/test_cloud5.txt', './test_clouds/test_cloud6.txt', './test_clouds/test_cloud7.txt', './test_clouds/test_cloud8.txt', './test_clouds/test_cloud9.txt', './test_clouds/test_cloud10.txt']

# now convert all of these to csv files, delimter is space
for file_name in file_names:
    with open(file_name, 'r') as in_file:
        stripped = (line.strip() for line in in_file)
        lines = (line.split() for line in stripped if line)
        with open(file_name + '.csv', 'w') as out_file:
            writer = csv.writer(out_file)
            writer.writerows(lines)
            
# move all of these csv files to a new folder called csv_files outside of test_clouds folder 
for file_name in file_names:
    os.rename(file_name + '.csv', './csv_files/' + file_name[14:] + '.csv')

import pandas as pd
# put all of these csvs into a list of dataframes
df_master_list = []
for file_name in os.listdir('./csv_files/'):
    df_master_list.append(pd.read_csv('./csv_files/' + file_name, header=None))


# for each dataframe, add the label column x,y,z and scale 
for df in df_master_list:
    df.drop([3], axis=1, inplace=True)

# export all of these dataframes to csv files again and call them revised
for i in range(len(df_master_list)):
    df_master_list[i].to_csv('./revised_csv_files/test_cloud' + str(i+1) + '.csv', index=False)


import pandas as pd
# put all of these csvs into a list of dataframes
df_master_list = []
for file_name in os.listdir('./revised_csv_files/'):
    df_master_list.append(pd.read_csv('./revised_csv_files/' + file_name, header=None))

# now, using this list of dataframes, create a 3d scatter plot


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.animation import FuncAnimation

# create an animation of each of these dataframes, and show them 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# from all these dataframes, find max and min of x,y,z
min_x = 10000000
max_x = -10000000
min_y = 10000000
max_y = -10000000
min_z = 10000000
max_z = -10000000
for df in df_master_list:
    for i in range(len(df)):
        if df[0][i] < min_x:
            min_x = df[0][i]
        if df[0][i] > max_x:
            max_x = df[0][i]
        if df[1][i] < min_y:
            min_y = df[1][i]
        if df[1][i] > max_y:
            max_y = df[1][i]
        if df[2][i] < min_z:
            min_z = df[2][i]
        if df[2][i] > max_z:
            max_z = df[2][i]
    
print(min_x, max_x, min_y, max_y, min_z, max_z)



# Create a function to update the 3D scatter plot for each frame
def update_3d_scatter(frame):
    ax.clear()
    df = df_master_list[frame]
    x = df[0]
    y = df[1]
    z = df[2]
    ax.scatter(x, y, z, c='b', marker='o')  # Customize the marker and color as needed
    
    # Set fixed axis limits for all frames
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)
    ax.set_zlim(min_z, max_z)
    
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    ax.set_title(f'Frame {frame+1}')

# Create a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Set up the animation
ani = FuncAnimation(fig, update_3d_scatter, frames=len(df_master_list), repeat=False)

# You can adjust the frames, interval, and other animation settings as needed.

# To display the animation, you can use a suitable viewer or save it as a video, e.g., MP4 or GIF.
# To save the animation as an MP4 video (requires FFmpeg), you can use the following line:
ani.save('animation.gif', writer='ffmpeg', fps=10)
