from flask import Flask, render_template, request, redirect, url_for
import os
import shutil

app = Flask(__name__)

# Global variables
base_path = None  # To store the directory selected by the user
file_type_mapping = {}  # Dictionary to store folder-extension mappings

@app.route('/')
def index():
    """Render the homepage with the directory and mapping form."""
    return render_template('index.html', base_path=base_path, mappings=file_type_mapping)

@app.route('/set_directory', methods=['POST'])
def set_directory():
    """Set the directory to organize."""
    global base_path
    base_path = request.form.get('directory')
    if not os.path.exists(base_path):
        return "Error: Directory does not exist.", 400
    return redirect(url_for('index'))

@app.route('/add_mapping', methods=['POST'])
def add_mapping():
    """Add folder-extension mapping."""
    folder_name = request.form.get('folder_name').strip()
    extensions = request.form.get('extensions').strip().split(',')
    
    if folder_name and extensions:
        file_type_mapping[folder_name] = [ext.strip().lower() for ext in extensions]
    
    return redirect(url_for('index'))

@app.route('/delete_mapping/<folder_name>', methods=['POST'])
def delete_mapping(folder_name):
    """Delete a mapping."""
    if folder_name in file_type_mapping:
        del file_type_mapping[folder_name]
    return redirect(url_for('index'))

@app.route('/organize', methods=['POST'])
def organize_files():
    """Organize files based on mappings."""
    if not base_path or not os.path.exists(base_path):
        return "Error: Base directory is not set or does not exist.", 400
    
    # Create directories
    for folder in file_type_mapping.keys():
        dir_path = os.path.join(base_path, folder)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
    
    # Organize files
    files = [f for f in os.listdir(base_path) if os.path.isfile(os.path.join(base_path, f))]
    
    for file in files:
        file_ext = file.split('.')[-1].lower()
        for folder, extensions in file_type_mapping.items():
            if file_ext in extensions:
                shutil.move(
                    os.path.join(base_path, file),
                    os.path.join(base_path, folder, file)
                )
                break
    
    return "Files organized successfully!"

if __name__ == '__main__':
    app.run(debug=True)
