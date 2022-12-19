################################################################################ 
# Antonio Morelli - 0001060348 
# utils_gui.py - Description: 
# A bunch of code lines that inits the components that will make up the 
# skeleton of the GUI application.   
################################################################################ 
from utils import *
import PySimpleGUI as sg
from PIL import Image, ImageTk
import shutil
import os, io
import pandas as pd

# ------------------------------------------------------------------------------
# Use PIL to read data of one image.
# ------------------------------------------------------------------------------
def get_img_data(f, maxsize=(256, 255), first=False):
    img = Image.open(f)
    img.thumbnail(maxsize)
    if first:                     # Tkinter is inactive the first time
        bio = io.BytesIO()
        img.save(bio, format='PNG')
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)  

# ------------------------------------------------------------------------------
# Check if analysis method selected with radio buttons corresponds to the right 
# folder method to perform the analysis task required by the images in the 
# folder.
# ------------------------------------------------------------------------------
def check_method(folder_method, values, rods_csv):
    if folder_method == '1' and values['r0'] != True:
        # radio_0.update(True)
        rods_csv = None
        return False
    elif folder_method == 'c1' and values['r1'] != True:
        # radio_1.update(True)
        rods_csv = None
        return False
    elif folder_method == 'c2' and values['r2'] != True:
        # radio_2.update(True)
        rods_csv = None
        return False
    elif folder_method == 'c3' and values['r3'] != True:
        # radio_3.update(True)
        rods_csv = None
        return False
    else:
        return True

# ------------------------------------------------------------------------------
# Init the directories' hierarchy.
# ------------------------------------------------------------------------------
def create_dirs():
    # Images
    if not os.path.exists('images'):
        os.mkdir('images')

    # Task 1 folders
    if not os.path.exists(os.path.join('images','1')):
        os.mkdir(os.path.join('images','1'))
    if not os.path.exists(os.path.join('images',os.path.join('1','outputs_th'))):
        os.mkdir(os.path.join('images',os.path.join('1','outputs_th')))
    else:
        shutil.rmtree(os.path.join('images',os.path.join('1','outputs_th')))
        os.mkdir(os.path.join('images',os.path.join('1','outputs_th')))
    if not os.path.exists(os.path.join('images',os.path.join('1','outputs'))):
        os.mkdir(os.path.join('images',os.path.join('1','outputs')))
    else:
        shutil.rmtree(os.path.join('images',os.path.join('1','outputs')))
        os.mkdir(os.path.join('images',os.path.join('1','outputs')))
        
    # Task 2 folders
    if not os.path.exists(os.path.join('images','2')):
        os.mkdir(os.path.join('images','2'))

    # Task 2 Change 1 folders
    if not os.path.exists(os.path.join('images',os.path.join('2','c1'))):
        os.mkdir(os.path.join('images',os.path.join('2','c1')))
    if not os.path.exists(os.path.join('images',os.path.join('2',os.path.join('c1','outputs_th')))):
        os.mkdir(os.path.join('images',os.path.join('2',os.path.join('c1','outputs_th'))))
    else:
        shutil.rmtree(os.path.join('images',os.path.join('2',os.path.join('c1','outputs_th'))))
        os.mkdir(os.path.join('images',os.path.join('2',os.path.join('c1','outputs_th'))))
    if not os.path.exists(os.path.join('images',os.path.join('2',os.path.join('c1','outputs')))):
        os.mkdir(os.path.join('images',os.path.join('2',os.path.join('c1','outputs'))))
    else:
        shutil.rmtree(os.path.join('images',os.path.join('2',os.path.join('c1','outputs'))))
        os.mkdir(os.path.join('images',os.path.join('2',os.path.join('c1','outputs'))))

    # Task 2 Change 2 folders
    if not os.path.exists(os.path.join('images',os.path.join('2','c2'))):
        os.mkdir(os.path.join('images',os.path.join('2','c2')))
    if not os.path.exists(os.path.join('images',os.path.join('2',os.path.join('c2','outputs_th')))):
        os.mkdir(os.path.join('images',os.path.join('2',os.path.join('c2','outputs_th'))))
    else:
        shutil.rmtree(os.path.join('images',os.path.join('2',os.path.join('c2','outputs_th'))))
        os.mkdir(os.path.join('images',os.path.join('2',os.path.join('c2','outputs_th'))))
    if not os.path.exists(os.path.join('images',os.path.join('2',os.path.join('c2','outputs')))):
        os.mkdir(os.path.join('images',os.path.join('2',os.path.join('c2','outputs'))))
    else:
        shutil.rmtree(os.path.join('images',os.path.join('2',os.path.join('c2','outputs'))))
        os.mkdir(os.path.join('images',os.path.join('2',os.path.join('c2','outputs'))))
        
    # Task 2 Change 3 folders
    if not os.path.exists(os.path.join('images',os.path.join('2','c3'))):
        os.mkdir(os.path.join('images',os.path.join('2','c3')))
    if not os.path.exists(os.path.join('images',os.path.join('2',os.path.join('c3','outputs_th')))):
        os.mkdir(os.path.join('images',os.path.join('2',os.path.join('c3','outputs_th'))))
    else:
        shutil.rmtree(os.path.join('images',os.path.join('2',os.path.join('c3','outputs_th'))))
        os.mkdir(os.path.join('images',os.path.join('2',os.path.join('c3','outputs_th'))))
    if not os.path.exists(os.path.join('images',os.path.join('2',os.path.join('c3','outputs')))):
        os.mkdir(os.path.join('images',os.path.join('2',os.path.join('c3','outputs'))))
    else:
        shutil.rmtree(os.path.join('images',os.path.join('2',os.path.join('c3','outputs'))))
        os.mkdir(os.path.join('images',os.path.join('2',os.path.join('c3','outputs'))))

# ------------------------------------------------------------------------------
# Save analysis as .csv
# ------------------------------------------------------------------------------
def save_analysis(filename_th, filename_o, path, filename, rods_csv, header_csv):    
    filename_save_img = ''.join(filename.split('.')[:len(filename.split('.'))-1])
    new_dir = path + '/' + filename_save_img

    if not os.path.exists(new_dir):
        os.mkdir(new_dir)

    df = pd.DataFrame(rods_csv, columns = header_csv)
    df.to_csv(new_dir + '/' + filename_save_img + '.csv', sep = ';', index=False)
   
    cv2.imwrite(new_dir + '/' + filename_save_img + '_th.png', cv2.imread(filename_th))
    cv2.imwrite(new_dir + '/' + filename_save_img + '_o.png', cv2.imread(filename_o))

# ------------------------------------------------------------------------------
# Invert a .csv file for visualization purposes.
# ------------------------------------------------------------------------------
def invert_csv(rods_csv):
    inverted = []
    for idx in range(2,len(rods_csv[0])):
        inverted.append([header_csv[idx]] + list(list(zip(*rods_csv))[idx]))
        
    return inverted

# ------------------------------------------------------------------------------
# Init variables.
# ------------------------------------------------------------------------------
header_csv = ['filename', 'id', 'type', 'MER', 'centre', 'width', 'length',\
'centre_w', 'theta','color', 'hole_1_centre','hole_1_d_1','hole_1_d_2',\
'hole_2_centre','hole_2_d_1','hole_2_d_2']

create_dirs()

# Theme
theme = 'Material2'
sg.change_look_and_feel(theme) 

# Home folder
folder = os.path.join(os.getcwd(), os.path.join('images','1'))

# PIL supported image types
img_types = ('.png', '.jpg', 'jpeg', '.tiff', '.bmp')

# Get list of files in folder
flist0 = os.listdir(folder)

# Create sub list of image files (no sub folders)
fnames = [f for f in flist0 if os.path.isfile(
    os.path.join(folder, f)) and f.lower().endswith(img_types)]

num_files = len(fnames)                # Number of iamges found
if num_files == 0:
    sg.popup('No files in folder', icon='images' + os.sep + 'icon.ico', size=(1100,850))
    raise SystemExit()
  
# Make these 2 elements outside the layout as we want to "update" them later and
# initialize to the first file in the list
filename = os.path.join(folder, fnames[0])  # Name of first file in list
filename_th = os.path.join(os.path.join(folder,'outputs_th'), fnames[0])  # Name of first file in list
filename_o = os.path.join(os.path.join(folder,'outputs'), fnames[0])  # Name of first file in list

# Execute an analysis of the first image of the folder.
image_elem = sg.Image(data=get_img_data(filename, first=True))
rods_csv = task1(filename, filename_th, filename_o)

if rods_csv:
    image_elem_th = sg.Image(data=get_img_data(filename_th, first=True))
    image_elem_o = sg.Image(data=get_img_data(filename_o, first=True))
    filename_display_elem = sg.Text(filename.split(os.sep)[len(filename.split(os.sep))-1])
else:
    filename_display_elem = sg.Text('Something went wrong, try to change the analysis method.')


# File number in the folder list
file_num_display_elem = sg.Text('File 1 of {}'.format(num_files), size=(15, 1))

# Radio buttons to select analysis method
radio_0 = sg.Radio('First Task', 'task', default=True, key = 'r0')
radio_1 = sg.Radio('Second Task - Change 1', 'task', default=False, key = 'r1')
radio_2 = sg.Radio('Second Task - Change 2', 'task', default=False, key = 'r2')
radio_3 = sg.Radio('Second Task - Change 3', 'task', default=False, key = 'r3')

# Button that saves a '.csv' file containing current analysis 
save_as = sg.Button('Export')

# Build the three columns of the layout 
logo = sg.Image(data=get_img_data('images' + os.sep + 'logo.png', first=True, maxsize=(120,120)))
# File Browser 
col_files = [
            [sg.Column([[logo]], justification='center')],
            [sg.Text('Image Folder'), sg.In(size=(20, 1), enable_events=True, key='-FOLDER-'), sg.FolderBrowse(initial_folder='images')],
            [radio_0],
            [radio_1],
            [radio_2],
            [radio_3],
            [sg.Listbox(values=fnames, change_submits=True, size=(30, 30), key='listbox')],
            [sg.Button('Next', size=(8, 2)), sg.Button('Prev', size=(8, 2)), file_num_display_elem]]

# Analysis Displaying
col = [
      [filename_display_elem, save_as],
      [image_elem], 
      [image_elem_th], 
      [image_elem_o]]


# Analysis CSV Table
rods_csv_i = invert_csv(rods_csv)
table = sg.Table(values=rods_csv_i, headings=['Feature'] + [str(i-1) for i in range(1,len(rods_csv_i[0]))],\
                    auto_size_columns=True,max_col_width=12,\
                    justification='center', background_color='White',\
                    text_color='Black', alternating_row_color='#ccd8ff',\
                    vertical_scroll_only=False, size=(10, 50), key = 'table')
col_csv = [[table]]

# Define layout
layout = [[sg.Column(col_files), sg.VerticalSeparator(color = '#004ea1'), sg.Column(col), sg.Column(col_csv)]]