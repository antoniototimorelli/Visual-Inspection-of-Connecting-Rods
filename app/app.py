################################################################################ 
# Antonio Morelli - 0001060348 
# app.py - Description: 
# Main loop run by the GUI application.
################################################################################ 
from utils import *
from utils_gui import *
import os

window = sg.Window('VIMCR', layout, return_keyboard_events=True,
                   location=(100, 100), use_default_focus=False, icon='images' + os.sep + 'icon.ico', size=(1100,850))

# ------------------------------------------------------------------------------
# Loop reading the user input and displaying image, filename
# ------------------------------------------------------------------------------
i = 0
# last_saved = ''
while True:
    # Read the form
    event, values = window.read()
 
    # Perform button and keyboard operations
    if event == sg.WIN_CLOSED:
        break
    elif event == '-FOLDER-':
        i = 0
        folder = values['-FOLDER-']
        if not folder:
            sg.popup_cancel('Cancelling', icon='images' + os.sep + 'icon.ico', size=(1100,850))   
            raise SystemExit()

        # Get list of files in folder
        flist0 = os.listdir(folder)

        folder_method = folder.split('/')[len(folder.split('/'))-1]
        
        if folder_method not in ('1','c1','c2','c3'):
            sg.popup(\
                '\t\tWARNING!\nPlease choose a folder between:\n\t-./1\n\t-./2/c1\n\t-./2/c2;\n\t-./2/c3', icon='images' + os.sep + 'icon.ico', size=(1100,850))
            continue
        elif folder_method == '1':
            radio_0.update(True)
        elif folder_method == 'c1':
            radio_1.update(True)
        elif folder_method == 'c2':
            radio_2.update(True)
        elif folder_method == 'c3':
            radio_3.update(True)
            
        # Create sub list of image files (no sub folders, no wrong file types)
        fnames = [f for f in flist0 if os.path.isfile(
            os.path.join(folder, f)) and f.lower().endswith(img_types)]

        num_files = len(fnames)                # Number of images found
        if num_files == 0:
            sg.popup('No files in folder', icon='images' + os.sep + 'icon.ico', size=(1100,850))
            raise SystemExit()

        del flist0                             # No longer needed

        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []
        fnames = [f for f in file_list if os.path.isfile(os.path.join(folder, f)) and f.lower().endswith(img_types)]
        
        window['listbox'].update(fnames)

    elif event in ('Next', 'MouseWheel:Down', 'Down:40', 'Next:34'):
        i += 1
        if i >= num_files:
            i -= num_files
        filename = os.path.join(folder, fnames[i])

        folder_method = folder.split('/')[len(folder.split('/'))-1]
        
        if not check_method(folder_method, values, rods_csv):
            image_elem.update(data=get_img_data(os.path.join('images', 'missing.png'), first=True))
            image_elem_th.update(data=get_img_data(os.path.join('images', 'missing.png'), first=True))
            image_elem_o.update(data=get_img_data(os.path.join('images', 'missing.png'), first=True))
            filename_display_elem.update('Something went wrong, try to change the analysis method.')
            table.update(values=[])
            continue

                
        filename_th = os.path.join(folder, os.path.join('outputs_th', fnames[i]))
        filename_o = os.path.join(folder, os.path.join('outputs', fnames[i]))  
        if values['r0']:
            rods_csv = task1(filename, filename_th, filename_o)
        elif values['r1']:
            rods_csv = task2_c1(filename, filename_th, filename_o)
        elif values['r2']:
            rods_csv = task2_c2(filename, filename_th, filename_o)
        elif values['r3']:
            rods_csv = task2_c3(filename, filename_th, filename_o)

    elif event in ('Prev', 'MouseWheel:Up', 'Up:38', 'Prior:33'):
        i -= 1
        if i < 0:
            i = num_files + i
        filename = os.path.join(folder, fnames[i])
      
        folder_method = folder.split('/')[len(folder.split('/'))-1]
        
        if not check_method(folder_method, values, rods_csv):
            image_elem.update(data=get_img_data(os.path.join('images', 'missing.png'), first=True))
            image_elem_th.update(data=get_img_data(os.path.join('images', 'missing.png'), first=True))
            image_elem_o.update(data=get_img_data(os.path.join('images', 'missing.png'), first=True))
            filename_display_elem.update('Something went wrong, try to change the analysis method.')
            table.update(values=[])
            continue

        filename_th = os.path.join(folder, os.path.join('outputs_th', fnames[i]))
        filename_o = os.path.join(folder, os.path.join('outputs', fnames[i]))  
        if values['r0']:
            rods_csv = task1(filename, filename_th, filename_o)
        elif values['r1']:
            rods_csv = task2_c1(filename, filename_th, filename_o)
        elif values['r2']:
            rods_csv = task2_c2(filename, filename_th, filename_o)
        elif values['r3']:
            rods_csv = task2_c3(filename, filename_th, filename_o)
        

    elif event == 'listbox':            # Something from the listbox
        f = values['listbox'][0]            # Selected filename
        filename = os.path.join(folder, f)  # Read this file

        folder_method = folder.split('/')[len(folder.split('/'))-1]
        
        if not check_method(folder_method, values, rods_csv):
            image_elem.update(data=get_img_data(os.path.join('images', 'missing.png'), first=True))
            image_elem_th.update(data=get_img_data(os.path.join('images', 'missing.png'), first=True))
            image_elem_o.update(data=get_img_data(os.path.join('images', 'missing.png'), first=True))
            filename_display_elem.update('Something went wrong, try to change the analysis method.')
            table.update(values=[])
            continue
            
        filename_th = os.path.join(folder, os.path.join('outputs_th', fnames[i]))
        filename_o = os.path.join(folder, os.path.join('outputs', fnames[i]))  

        if values['r0']:
            rods_csv = task1(filename, filename_th, filename_o)
        elif values['r1']:
            rods_csv = task2_c1(filename, filename_th, filename_o)
        elif values['r2']:
            rods_csv = task2_c2(filename, filename_th, filename_o)
        elif values['r3']:
            rods_csv = task2_c3(filename, filename_th, filename_o)

        i = fnames.index(f)                 # Update running index

    elif event == 'Export':
        path =  sg.popup_get_folder('', default_path=os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'), no_window=True, icon = 'images' + os.sep + 'icon.ico')
        try:
            save_analysis(filename_th, filename_o, path, filename.split(os.sep)[len(filename.split(os.sep))-1], rods_csv, header_csv)
            sg.popup(f'Exported correctly to:\n{path}.', icon='images' + os.sep + 'icon.ico')
        except:
            sg.popup('Cannot export the file!', icon='images' + os.sep + 'icon.ico')

        continue
    else:
        continue
    
    # Update window with filename and images
    if rods_csv:     
        image_elem.update(data=get_img_data(filename, first=True))
        image_elem_th.update(data=get_img_data(filename_th, first=True))
        image_elem_o.update(data=get_img_data(filename_o, first=True))
        filename_display_elem.update(filename.split(os.sep)[len(filename.split(os.sep))-1])

        rods_csv_i = invert_csv(rods_csv)
        table.update(values=rods_csv_i)
    else:
        image_elem.update(data=get_img_data(os.path.join('images', 'missing.png'), first=True))
        image_elem_th.update(data=get_img_data(os.path.join('images', 'missing.png'), first=True))
        image_elem_o.update(data=get_img_data(os.path.join('images', 'missing.png'), first=True))
        filename_display_elem.update('Something went wrong, try to change the analysis method.')
        table.update(values=[])
        continue

    # Update page display
    file_num_display_elem.update('File {} of {}'.format(i+1, num_files))

window.close()