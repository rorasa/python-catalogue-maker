from weasyprint import HTML
import os, tempfile, sys
from subprocess import call
import Tkinter as tk
import tkFileDialog
from shutil import copyfile

EDITOR = os.environ.get('EDITOR','vim')
BASENAME = os.path.dirname(os.path.abspath(__file__))+"/"
list_tempfiles = []

# Ask for contents

collection_id = raw_input('Please enter a collection ID: ')
print('Creating a page for ID:', collection_id)

title = raw_input("Please insert the item's title: ")
description = raw_input("Please insert the description (1 line): ")
infotext = "This is the catalogue page for "+collection_id+"."

raw_input("Please enter the description in the editor. (Press enter to continue)")
with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
    tf.write(infotext)
    tf.flush()
    call([EDITOR, tf.name])
    with open(tf.name) as tf:
        tf.seek(0)
        infotext = tf.read()

# Open dialog to get input files
root = tk.Tk()
root.withdraw()

file_path = tkFileDialog.askopenfilename()
print("Please select the file for Photo 1: ")
print(file_path+" is used as Photo 1")
file_name, file_extension = os.path.splitext(file_path)
dst = BASENAME+'img1'+file_extension
copyfile(file_path,dst)
list_tempfiles.append(dst)

file_path = tkFileDialog.askopenfilename()
print("Please select the file for Photo 2: ")
print(file_path+" is used as Photo 2")
file_name, file_extension = os.path.splitext(file_path)
dst = BASENAME+'img2'+file_extension
copyfile(file_path,dst)
list_tempfiles.append(dst)

# open template file for editing
template_file = open(BASENAME+'template.html','r')
template = template_file.read()

# parsing template parameters
template = template.replace("{{collection-id}}",collection_id)
template = template.replace("{{title}}", title)
template = template.replace("{{description}}", description)
template = template.replace("{{info}}",infotext)

template = template.replace("{{photo-1}}",'<img src="'+list_tempfiles[0]+'" alt="photo1">')
template = template.replace("{{photo-2}}",'<img src="'+list_tempfiles[1]+'" alt="photo2">')

# save processed html source
source_file = open(BASENAME+'source.html','w')
source_file.write(template)
source_file.close()
list_tempfiles.append(BASENAME+'source.html')

# Creating PDF output
output_filename = collection_id + '.pdf'
HTML(BASENAME+'source.html').write_pdf(output_filename);
print('Page saved as '+ output_filename)

# Remove temp files
for filename in list_tempfiles:
    os.remove(filename)
