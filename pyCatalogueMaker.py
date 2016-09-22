from weasyprint import HTML
import os, tempfile, sys
from subprocess import call
import Tkinter as tk
import tkFileDialog
from shutil import copyfile

class  Content:
    collection_id = ''
    title = ''
    description = ''
    info = ''
    image1_enabled = False
    image1_filename = ''
    image2_enabled = False
    image2_filename = ''

def makeSourceFile(contents):
    # parsing template.html to source.html using infomation from
    # contents object

    template_filename = BASENAME+'template.html'
    source_filename = BASENAME+'source.html'

    # open template file for editing
    template_file = open(template_filename,'r')
    template = template_file.read()

    # parsing template parameters
    template = template.replace("{{collection-id}}",contents.collection_id)
    template = template.replace("{{title}}", contents.title)
    template = template.replace("{{description}}", contents.description)
    template = template.replace("{{info}}",contents.info)

    if contents.image1_enabled:
        template = template.replace("{{photo-1}}",'<img src="'+contents.image1_filename+'" alt="photo1">')
    else:
        template = template.replace("{{photo-1}}",'')
    if contents.image2_enabled:
        template = template.replace("{{photo-2}}",'<img src="'+contents.image2_filename+'" alt="photo2">')
    else:
        template = template.replace("{{photo-2}}",'')

    # save processed html source
    source_file = open(source_filename,'w')
    source_file.write(template)
    source_file.close()
    
    return source_filename

def getTextFromEditor(text):
    # Call up interactive text editor to get multi-line input
    with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
        tf.write(text)
        tf.flush()
        call([EDITOR, tf.name])
        with open(tf.name) as tf:
            tf.seek(0)
            text = tf.read()
    return text

def importPhotoFromDialog(order):
    file_path = tkFileDialog.askopenfilename()
    print(file_path+" is used as Photo "+order)
    file_name, file_extension = os.path.splitext(file_path)
    dst = BASENAME+'img'+order+file_extension
    copyfile(file_path,dst)
    return dst

def askForInputs(contents):
    contents.collection_id = raw_input('Please enter a collection ID: ')
    print('Creating a page for ID: '+ contents.collection_id)

    contents.title = raw_input("Please insert the item's title: ")
    contents.description = raw_input("Please insert the description (1 line): ")
    contents.info = "This is the catalogue page for "+contents.collection_id+"."
    
    raw_input("Please enter the description in the editor. (Press enter to continue)")
    contents.info = getTextFromEditor(contents.info)

    # Open dialog to get input files
    root = tk.Tk()
    root.withdraw()

    if raw_input('Would you like to insert Photo 1 [y/n]: ')=='y':
        print("Please select the file for Photo 1: ")
        photo1 = importPhotoFromDialog('1') 
        contents.image1_enabled = True
        contents.image1_filename = photo1
        list_tempfiles.append(photo1)
    if raw_input('Would you like to insert Photo 2 [y/n]: ')=='y':
        print("Please select the file for Photo 2: ")
        photo2 = importPhotoFromDialog('2')
        contents.image2_enabled = True
        contents.image2_filename = photo2
        list_tempfiles.append(photo2)

    return contents

def generatePDF(contents, source):
    # Generage PDF using WeasyPrint HTML class
    output_filename = contents.collection_id + '.pdf'
    HTML(source).write_pdf(output_filename)
    print('Page saved as '+output_filename)
    return output_filename

# Setting
EDITOR = os.environ.get('EDITOR','vim')
BASENAME = os.path.dirname(os.path.abspath(__file__))+"/"

# Initialisation
list_tempfiles = []
contents = Content()

# Get user inputs
print('==================================================')
print('Starting pyCatalogMaker')
print('==================================================')
contents = askForInputs(contents)

# Generate source.html file from contents
src_file = makeSourceFile(contents)
list_tempfiles.append(src_file)

# Creating PDF output
generatePDF(contents, src_file)

# Remove temp files
for filename in list_tempfiles:
    os.remove(filename)

print('Finished successfully')
print('==================================================')
