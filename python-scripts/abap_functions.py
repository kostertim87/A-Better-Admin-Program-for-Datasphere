from hdbcli import dbapi # To connect to SAP HANA Database underneath SAP Datasphere to fetch Remote Table metadata
import pandas as pd
import PySimpleGUI as sg
import subprocess
import os.path
import os
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import pytz
import datetime


icon_path = r"C:\Users\TimKoster\OneDrive\Python\ABAP for Datasphere.ico"


# This file contains all the CLI functions needed for the GUI

def dsp_name_is_filled(dsp_name): 
    if dsp_name: 
        return True
    sg.popup_error("Please fill in the URL of your tenant")
    return False

def secret_path_is_filled(secrets_file):
    if secrets_file: 
        return True
    sg.popup_error("Please give the path to your secretsfile")
    return False

def ds_logout(dsp_host): 
    command = f'datasphere logout --host {dsp_host}'
    print(command)
    subprocess.run(command, shell=True)
    print("Logged Out")

def ds_login(dsp_host, secrets_file):
    print(dsp_host)
    command = f'datasphere login --host {dsp_host} --secrets-file {secrets_file}'
    print(command)
    subprocess.run(command, shell=True)
    print("Logged In")

def no_process_selected(): 
	sg.popup("No process was selected")

def process_already_ended(): 
	sg.popup("Process already ended")

def are_you_sure(process): 
	answer = sg.popup_yes_no("Are you sure you want to kill process:", f'{process}')
	return answer

def are_you_sure_disconnect(user): 
	answer = sg.popup_yes_no("Are you sure you want to disconnect user:", f'{user}')
	return answer

def connect_hdb(hdb_address, hdb_port, hdb_user, hdb_password): 
	conn = dbapi.connect(
		address=hdb_address,
		port=hdb_port,
		user=hdb_user,
		password=hdb_password
	)
	cursor = conn.cursor()

	return cursor


def active_connections(hdb_address, hdb_port, hdb_user, hdb_password):
# Connect to HANA Database
	conn = dbapi.connect(
		address=hdb_address,
		port=hdb_port,
		user=hdb_user,
		password=hdb_password
	)
	cursor = conn.cursor()

	st = f''' SELECT 
		"ACTIVE"."CONNECTION_ID",
		CONN.CLIENT_APPLICATION,
		CONN.CLIENT_TYPE,
		CONN.CREATED_BY,
		CONN.USER_NAME,
        MDX."APPLICATION_USER_NAME" AS USER,
		"ACTIVE"."STATEMENT_STRING",
		("ACTIVE"."ALLOCATED_MEMORY_SIZE"/1048576) as Allocated_Memory,
		"ACTIVE"."LAST_EXECUTED_TIME",
		"ACTIVE"."LAST_ACTION_TIME"
	FROM "M_ACTIVE_STATEMENTS" AS ACTIVE
		LEFT JOIN "M_CONNECTIONS" CONN ON ACTIVE."CONNECTION_ID" = CONN."CONNECTION_ID"
        LEFT JOIN 
        (SELECT DISTINCT "STATEMENT_ID", "APPLICATION_USER_NAME" FROM "M_SERVICE_THREADS") AS MDX ON MDX."STATEMENT_ID" = ACTIVE."STATEMENT_ID"
	WHERE ACTIVE."STATEMENT_STATUS" = 'ACTIVE'
    ORDER BY MDX."APPLICATION_USER_NAME", ACTIVE."CONNECTION_ID", ACTIVE."ALLOCATED_MEMORY_SIZE" DESC;'''

	columns = ["Connection ID", "Client Application", "Client Type", "Created By", "User Name", "User",  
			"Statement String", "Allocated Memory Size (MB)", "Last Executed Time", "Last Action Time"]

	#print(st)

	cursor.execute(st)

	data = cursor.fetchall()

	df = pd.DataFrame(data, columns=columns)   

	#print(df)

	data = df.values.tolist()
	header_list = columns
	data = df.values.tolist()

	return data, header_list

def get_id_data(user_setting, id):
    return user_setting[id]

def login_window(): 
    user_data = sg.UserSettings('user_data_datasphere.json')
    user_data = user_data.get_dict()
    profiles_list = list(user_data.keys())
    print(profiles_list)
    layout = [
        [sg.Combo(values=profiles_list, size=(50,1), key="-COMBO-")],
        [sg.Button('Add new profile'), sg.Button('Load Profile'), sg.Button('Exit')],
    ]
    return layout

def add_new_window():    
    
    INPUT_SIZE = (50, 1)
    
    layout = [
        [sg.Text('Profile', justification='left'), sg.Push(), sg.Input(key='-ID-', size=INPUT_SIZE, justification='left') ],
        [sg.Text('DataSpehere Host Name (Database User)'), sg.Push(), sg.Input(key='-URL-', size=INPUT_SIZE)],
        [sg.Text('Database User'), sg.Push(), sg.InputText(key='-DBUSER-', size=INPUT_SIZE)],
        [sg.Text('Database User Password'), sg.Push(), sg.InputText(key='-DBPASSWORD-', password_char='*' ,size=INPUT_SIZE)],
        [sg.Text('DataSphere URL'), sg.Push(), sg.InputText(key='-DSURL-', size=INPUT_SIZE)],
        [sg.Text("Path to Secrets File"), sg.Push(), sg.In(size=(50,1), enable_events=True, key="-SECFILE-"),sg.FileBrowse()],
        [sg.Text("Path for Export Files"), sg.Push(), sg.In(size=(50,1), enable_events=True, key="-EXPORTPATH-"),sg.FolderBrowse()],
        [sg.Button('Add/Update'), sg.Button('Return'), sg.Push(), sg.Button('Create new secrets file'),],
        ]
    return sg.Window('Add new profile', layout, finalize=True, resizable=True, icon=icon_path, titlebar_icon=icon_path)
           

def create_new_secrets_file_window():
    
    INPUT_SIZE = (50, 1)
    
    layout = [
        [sg.Text('Filename', justification='left'), sg.Push(), sg.Input(key='-FILENAME-', size=INPUT_SIZE, justification='left') ],
        [sg.Text('Client ID', justification='left'), sg.Push(), sg.Input(key='-CLIENT_ID-', size=INPUT_SIZE, justification='left') ],
        [sg.Text('Client Secret'), sg.Push(), sg.Input(key='-CLIENT_SECRET-', size=INPUT_SIZE)],
        [sg.Text('Authorization URL'), sg.Push(), sg.InputText(key='-AUTH_URL-', size=INPUT_SIZE)],
        [sg.Text('Token URL'), sg.Push(), sg.InputText(key='-TOKEN_URL-', size=INPUT_SIZE)],
        [sg.Text('Folder to store file'), sg.Push(), sg.InputText(key='-FOLDER-', size=INPUT_SIZE), sg.FolderBrowse()],
        [sg.Button('Create Secrets File'), sg.Button('Return')],       
    ]    

    return sg.Window('Create new secrets file', layout, finalize=True, resizable=True, icon=icon_path, titlebar_icon=icon_path)

def create_new_secrets_file(client_id, client_secret, auth_url, token_url, folder, filename):
    
    auth_data = {
        "client_id": f'{client_id}',
        "client_secret": f'{client_secret}',
        "auth_url": f'{auth_url}',
        "token_url": f'{token_url}'
    }
    
    filename = f'{filename}.json'
    
    #define the file path
    file_path = os.path.join(f'{folder}', f'{filename}')
    
    with open(file_path, 'w') as file: 
        json.dump(auth_data, file, indent=4)
        
    sg.Popup(f'Secrets file {filename} created in {folder}')

def create_new_user_copy(): 
    
    INPUT_SIZE = (50, 1)

    layout = [ 
        [sg.Text('User Name', justification='left'), sg.Push(), sg.Input(key='-USERNAME-', size=INPUT_SIZE, justification='left')],
        [sg.Text('First Name', justification='left'), sg.Push(), sg.Input(key='-FIRSTNAME-', size=INPUT_SIZE, justification='left') ],
        [sg.Text('Last Name', justification='left'), sg.Push(), sg.Input(key='-LASTNAME-', size=INPUT_SIZE, justification='left')],
        [sg.Text('Display Name', justification='left'), sg.Push(), sg.Input(key='-DISPLAYNAME-', size=INPUT_SIZE, justification='left')],
        [sg.Text('Email', justification='left'), sg.Push(), sg.Input(key='-EMAIL-', size=INPUT_SIZE, justification='left')],
        [sg.Button('Create User'), sg.Button('Cancel')], 
    ]

    return sg.Window('Create new user', layout, finalize=True, resizable=True, icon=icon_path, titlebar_icon=icon_path)

def create_multiple_users_copy(): 
    
    INPUT_SIZE = (50, 1)

    layout = [ 
        [sg.Text('Create new users based on user:', justification='left'), sg.Text('', key='-USERTOCOPY-')],
        [sg.Text('Please select the file with users:', justification='left')], [sg.In(size=(50,1), enable_events=True, key="-MASSCREATEFILE-"),sg.FileBrowse()],
        [sg.Button('Create Users'), sg.Button('Create template file'), sg.Button('Cancel')],
    ]

    return sg.Window('Create new multiple users', layout, finalize=True, resizable=True, icon=icon_path, titlebar_icon=icon_path)

def transport_views_from_file(): 
        
        INPUT_SIZE = (50, 1)
    
        layout = [ 
            [sg.Text('Please select the file with views:', justification='left')], [sg.In(size=(60,1), enable_events=True, key="-VIEWFROMFILE-"),sg.FileBrowse()],
            [sg.Button('Add Views to Transport List'), sg.Button('Create template file'), sg.Button('Cancel')],
        ]
    
        return sg.Window('Transport views', layout, finalize=True, resizable=True, icon=icon_path, titlebar_icon=icon_path)

def remove_user_from_system(dsp_host, username):   
    command = f'''datasphere users delete --host {dsp_host} --users {username} --force'''
    print(command)
    subprocess.run(command, shell=True)

def get_user_info_for_copy(users, username):
    for user in users:
            return {
                'manager': user.get('manager', 'Not specified'),
                'roles': user.get('roles', 'Not specified')
            }
    return None  

def read_spaces(dsp_host, secrets_file, file_spaces):
    init = f'datasphere config cache init --host {dsp_host}'
    subprocess.run(init, shell=True)
    command = f'datasphere spaces list --host {dsp_host} --secrets-file {secrets_file} --file-path {file_spaces}'
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)
    spaces = json.loads(result.stdout)
    return spaces

def read_hana_views_in_space(hdb_address, hdb_port, hdb_user, hdb_password, selected_space): 
    conn = dbapi.connect(
		address=hdb_address,
		port=hdb_port,
		user=hdb_user,
		password=hdb_password
	)
    cursor = conn.cursor()

    selected_space = selected_space

    total_statement = f'''SELECT ARTIFACT_NAME FROM (SELECT ID, SCHEMA_NAME, ARTIFACT_NAME, ARTIFACT_VERSION, PLUGIN_NAME, PLUGIN_VERSION, CSN, CMDS, ROW_NUMBER() OVER (PARTITION BY ARTIFACT_NAME ORDER BY ARTIFACT_VERSION DESC) AS ROWNUM FROM
    "{selected_space}$TEC"."$$DeployArtifacts$$" WHERE PLUGIN_NAME in ('InAModel', 'table', 'remoteTable') AND LEFT(ARTIFACT_NAME,2) <> 'D∞' AND LEFT(ARTIFACT_NAME,1) <> '∞' AND LEFT(ARTIFACT_NAME,2) <> 'H∞') WHERE ROWNUM = 1 ORDER BY ARTIFACT_NAME ASC;'''

    #print(total_statement)

    st = total_statement

    columns = ["Artifact_Name"]
    #print(st)

    cursor.execute(st)

    data = cursor.fetchall()

    df = pd.DataFrame(data, columns=columns)   

    #print(df)

    data = df.values.tolist()
    header_list = columns
    data = df.values.tolist()
    
    views = data
    
    return views

# -----------------------------------------------------------
# Find the CSN for the selected view
# -----------------------------------------------------------

def get_csn_for_object(hdb_address, hdb_port, hdb_user, hdb_password, selected_space, selected_space_push, view_name): 
    conn = dbapi.connect(
		address=hdb_address,
		port=hdb_port,
		user=hdb_user,
		password=hdb_password
	)
    cursor = conn.cursor()

    total_statement = f'''SELECT CSN FROM (SELECT ID, SCHEMA_NAME, ARTIFACT_NAME, ARTIFACT_VERSION, PLUGIN_NAME, PLUGIN_VERSION, CSN, CMDS, ROW_NUMBER() OVER (PARTITION BY ARTIFACT_NAME ORDER BY ARTIFACT_VERSION DESC) AS ROWNUM FROM
    "{selected_space}$TEC"."$$DeployArtifacts$$" WHERE ARTIFACT_NAME ='{view_name}' AND PLUGIN_NAME = 'InAModel') WHERE ROWNUM = 1;'''

    print(selected_space)
    print(total_statement)

    st = total_statement
    
    cursor.execute(st)

    view_csn = cursor.fetchall()
    
    df = pd.DataFrame(view_csn)

    view_csn_new = df.iloc[0,0]

        # Parse the string to a JSON object
    if isinstance(view_csn_new, str):
        try:
            view_csn_new = json.loads(view_csn_new)
        except json.JSONDecodeError:
            print("Error: The CSN data is not a valid JSON string.")
            return None

    space_csn = {selected_space_push: view_csn_new}
    
    return space_csn

# -----------------------------------------------------------
# Add Space Definition to CSN for Graphical CSN file
# -----------------------------------------------------------

def create_graphical_csn_file(csn_file, selected_space_push): 
    with open(csn_file, 'r') as f:
        csn = json.load(f)
    #print(csn)
    csn_pretty = json.dumps(csn, indent=4)
    
    space_csn = {selected_space_push: csn_pretty}
    
    return space_csn

# -----------------------------------------------------------
# Write the csn to DSP with space definition csn as input
# -----------------------------------------------------------
def write_space_csn(space_csn, export_folder_path, dsp_space, view_name):
    
    space_csn_pretty = json.dumps(space_csn, indent=4)
    
    space_csn_file = f'{export_folder_path}{dsp_space}_{view_name}.csn'
    
    print(space_csn_file)
    with open(space_csn_file, 'w') as f:
        f.write(space_csn_pretty)
    return space_csn_file

# -----------------------------------------------------------
# Push view csn to DSP with space definition csn as input
# -----------------------------------------------------------
def push_space_csn_to_DSP(space_csn_file, dsp_host, dsp_space):
    command = f'datasphere spaces create --host {dsp_host} --space {dsp_space} --file-path {space_csn_file} --force-definition-deployment --verbose'
    print(command)
    subprocess.run(command, shell=True)

def flatten_list(nested_list):
    flattened_list = []
    for item in nested_list:
        # Check if the item is a list
        if isinstance(item, list):
            # If the item is a list, extend the flattened list with the first element of this item
            flattened_list.extend(item[0])
        else:
            # If the item is not a list, just append it to the flattened list
            flattened_list.append(item)
    return flattened_list    

def get_users_from_dsp_tenant(dsp_url, export_folder_path):
    command = f'datasphere users list --host {dsp_url} --accept application/vnd.sap.datasphere.space.users.details+json --output {export_folder_path}/users.json'
    print(command)
    subprocess.run(command, shell=True)
    file = f'{export_folder_path}/users.json'
    print(file)
    return file

def processor_usage(hdb_address, hdb_port, hdb_user, hdb_password, seconds):
    conn = dbapi.connect(
        address=hdb_address,
        port=hdb_port,
        user=hdb_user,
        password=hdb_password
    )
    cursor = conn.cursor()

    st = f'''SELECT 
    SUBSTRING("TIME", 12, 8) as TIME, 
    CPU
    FROM M_LOAD_HISTORY_HOST
    WHERE TO_DATE(LEFT(TIME,10)) = LEFT(NOW(),10) AND 
    TIME > ADD_SECONDS(NOW(), -{seconds})
    ;'''

    columns = [ "Time", "CPU"]
         
    cursor.execute(st)

    data = cursor.fetchall()

    df = pd.DataFrame(data, columns=columns)  
    time = df['Time'].values.tolist()
    cpu = df['CPU'].values.tolist()  

    timezone = pytz.timezone('UTC')
    timezone_aware_datetimes = []

    for time_str in time: 
    # Parse the time string into a datetime object
        naive_datetime = datetime.datetime.strptime(time_str, '%H:%M:%S')
    # Make it timezone-aware
        aware_datetime = timezone.localize(naive_datetime)
        timezone_aware_datetimes.append(aware_datetime)

    time = timezone_aware_datetimes

    return time, cpu

def memory_usage(hdb_address, hdb_port, hdb_user, hdb_password, seconds):
    conn = dbapi.connect(
        address=hdb_address,
        port=hdb_port,
        user=hdb_user,
        password=hdb_password
    )
    cursor = conn.cursor()

    st = f'''SELECT 
    SUBSTRING("TIME", 12, 8) as TIME, 
    ROUND(MEMORY_USED / MEMORY_ALLOCATION_LIMIT * 100,2) as Memory
    FROM M_LOAD_HISTORY_HOST
    WHERE TO_DATE(LEFT(TIME,10)) = LEFT(NOW(),10) AND 
    TIME > ADD_SECONDS(NOW(), -{seconds})
    ORDER BY TIME ASC
    ;'''

    columns = [ "Time", "Memory"]
         
    cursor.execute(st)

    data = cursor.fetchall()

    df = pd.DataFrame(data, columns=columns)  
    time = df['Time'].values.tolist()
    memory = df['Memory'].values.tolist()  

    timezone = pytz.timezone('UTC')
    timezone_aware_datetimes = []

    for time_str in time: 
    # Parse the time string into a datetime object
        naive_datetime = datetime.datetime.strptime(time_str, '%H:%M:%S')
    # Make it timezone-aware
        aware_datetime = timezone.localize(naive_datetime)
        timezone_aware_datetimes.append(aware_datetime)

    time = timezone_aware_datetimes

    return time, memory
        

def create_plot_cpu(time, cpu):
    # Create a figure object
    fig = Figure()
    # Create a canvas and associate it with the figure
    canvas = FigureCanvas(fig)
    # Add an axes to the figure
    ax = fig.add_subplot(111)
    
    # Plot the data
    ax.plot(time, cpu, color='red')
    # Set the title and labels
    ax.set_xlabel('Time', fontsize=10)
    ax.set_ylabel('CPU', fontsize=10)
    # Enable grid
    ax.grid(True)
    
    # Format the x-axis to display dates properly
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    fig.autofmt_xdate()  # Rotate date labels to fit
    ax.set_ylim(0, 100)
    
    return fig

def create_plot_memory(time, memory):
    # Create a figure object
    fig = Figure()
    # Create a canvas and associate it with the figure
    canvas = FigureCanvas(fig)
    # Add an axes to the figure
    ax = fig.add_subplot(111)
    
    # Plot the data
    ax.plot(time, memory, color='red')
    # Set the title and labels
    ax.set_xlabel('Time', fontsize=10)
    ax.set_ylabel('Memory %', fontsize=10)
    # Enable grid
    ax.grid(True)
    
    # Format the x-axis to display dates properly
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    fig.autofmt_xdate()  # Rotate date labels to fit
    ax.set_ylim(0, 100)
    
    return fig

def draw_figure(canvas, figure):
    # Check if the canvas already has a figure drawn on it and clear it
    if hasattr(canvas, 'figure_canvas_agg'):
        # This assumes 'figure_canvas_agg' is the FigureCanvasTkAgg instance from a previous draw
        # We need to destroy the old canvas widget and create a new one
        canvas.figure_canvas_agg.get_tk_widget().destroy()
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    # Pack the new figure in the canvas
    figure_canvas_agg.get_tk_widget().pack(side='left', expand=1)
    # Store the new figure canvas agg to allow it to be cleared next time
    canvas.figure_canvas_agg = figure_canvas_agg
    return figure_canvas_agg

def push_userdata_to_dsp(new_user_file, dsp_host):
    command = f'datasphere users create --host {dsp_host} --file-path {new_user_file} --verbose'
    print(command)
    subprocess.run(command, shell=True)