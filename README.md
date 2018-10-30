# Project 1 - Parsing | EDA
    Part 1: Parsing Foxtrot.com.ua    
    Part 2: Some EDA, Data Preprocessing, Interactive subplots with Plotly    

# Project 2 - Dash Only    
    "gtd.zip" - archive with data    
    "for_dash.py" - prepared massive for dashboards    
    Plots for test - Data Preprocessing and charts with Plotly
    Folders "Dashes - single app" and "sub_dashes" - folders with dashboard (use Dash+Plotly)    
    full_dash.py - three static dashboards with tabs    
    maps_interactive.py - interactive dashboard with dropbox, year rangeslider and radiobuttons.    

You can clone or download this repo:
https://github.com/amyard/Parsing-Dashboards.git

Then cd into the repo:

    cd Parsing-Dashboards

Now create and activate a virtualenv (noting the python runtime):
On a mac:

    virtualenv -p <python version> venv
    source venv/bin/activate

On a Windows:

    virtualenv -p <python version> venv
    venv/Scripts/activate

Now that virtualenv is setup and active we can install the dependencies:

    pip install -r requirements.txt

Once the dependencies have been installed, cd into the project.
For Project 1 and some files from Project 2 use jupyter notebook.

For Project 2 -> file "full_dash.py" / "maps_interactive.py" type in console:

    python <name of file>.py

Then visit http://127.0.0.1:8050/
