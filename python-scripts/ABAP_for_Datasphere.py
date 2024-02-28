# -----------------------------------------------------------
# Package import
# -----------------------------------------------------------
import os
os.environ['PySimpleGUI_license'] = 'ehyBJjMbaLWiNlljbLn3Nll5VBHGluwZZUShIs6rIfkRRWpccZ36RxyKaHWBJa16dyGwlbvObIixItsHIok8xZpFYD2EVXuZcB2NVKJGRoC0Ir6LM4TDc6wLOXTGEjwLNRjZYO0vOwCAwTinTqGGljjXZYWL5uztZgUSR9lacPGkx0vNeyWe1LlFbAnkRwWyZ9XUJDzlaUWq9xuQI5jHofiPN5SH4mwxIfiMwkixTqmZFBtDZOUbZxpWcsn2Nf0sIojjoxi1VZGNlMtsICiawBiWTjmVFEtdZRUSxVhsce3TQuiHO4iNJ6L0bj3xNX0rZqXeIPiqL9CdJWDab62i19wWYBWN5k5VI5j7ogibS5W05200ZhXDJokfb52bJRzeIhi4w5icQF30VUz2dfGx9ttlZvXFJxJ6R3CvIr6hIsjZIux3Njzgg0iPLLCjJSEYY6XVRjlQSRXHNlzadSWKVSkKIRjgoQiVMpjkA7yKNhCk0cwKMoid08ySOCC1I0shInksRlhIdNGfVPF3e1HXBHpXcOmAVRzlISjCo2iJMrjLAoyhNVSX0SwnMriS07xyNRivIvsrIVk3VwtGYYWUlHshQoWaRkkUc6mpVzzhcOyTIn6CIkn8RHpSb6SG5Cr4bF3CNh0xZPXqJUAAafWF5T0HZKXHJykAbO27JjzWLrmL5KsRILigwkizSKVQBuBLZUGARNyIZiX0NEzPItjVoPioNDzzcSuOMHTacKxILBjsEVwgMeSv4YygMWTGUvi8fnQv=h=M447800b1ae8f333f0912ed4e8fd6d555d3e0516232f5fff3f938afc075961665df27d4e8f40376584e279145feb07fe7476f18a1e38c73bba31b04c442225e83d745dd1327ff31ccd716a289bf79e3ec30203b77dcd02f38c51a57e6f250120fc9ceac4385386bf9bde2657ee86a1afff9994d16df96e277ccacb79f18bf9523c2dedd972726c20be13bc2486de35cdf374c53683ae71ed14f71cff4febec637c069f148d9d3e5f4d8bc640a1d0170f0b413cd50e72c32cb96ac91accbe8ee768912c3f74fffa4ddd63ee9d0d984c4ea5fb7bafb69c213a7629376244afda7730f0b520b7289d92e046cda6321294c4e899e9cc7e5e432b6240b71f1943de2c317a919a348196527cb48700abc6b58099aca511b1428d4d6616551afd2aa4c3fc6ac422bfff779b40aab7c28555763ace65580a7e7ec0670370b9a7e4da256f0174a5fe238006959ca2f97fffc6c42deb0706645af01e928007a81b79c9edf31c66d2f1d4dff58c56d028342765ab4c79a071f548ac01bc8e1c9dcc864e9c193ffde58af2fe1a354b2ce17d3ef171df9b67f9e3880959634fe8aba7049170c9823a60d95d52d64a527134627acc87ea08a101da78ed855bc2b227d067d000bad488a9d1050ae1353277f1a26f7f643efc3d447edd0018b9ff94bcbcfde6414ba9bd640e1da8d95126dd5e00f96dac6f691819ddace456920f48b0e78e1fea9d6'
import PySimpleGUI as sg
import subprocess # For OS commands on DSP CLI
import json # For handling the CSN files which are in JSON format
import time # For wait function to let an object deploy finish before starting the following
import csv
import os.path
import abap_functions as af
from hdbcli import dbapi # To connect to SAP HANA Database underneath SAP Datasphere to fetch Remote Table metadata
import pandas as pd
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pytz
import datetime
import openpyxl
import matplotlib.figure as Figure



## Global variables

data = []
header_list = ["Connection ID", "Client Application", "Client Type", "Created By", "User Name", "User",  
			"Statement String", "Allocated Memory Size (MB)", "Last Executed Time", "Last Action Time"]

user_data = sg.UserSettings('user_data_datasphere.json')
user_data = user_data.get_dict()
profiles_list = list(user_data.keys())
spaces = []
spaces_prod = []
users = []
removal_list = [] 
cleaned_spaces = []
combined_multiple_user_info = []
current_wd = os.path.dirname(os.path.realpath(__file__))
icon_file = r"\ABAP for Datasphere.ico"
icon_path = current_wd + icon_file
logged_in = 'Not logged in'
dev_views = []
cross_temp_list_prod = ['Please add views to transport']
temp_list = ['Please select a development space']
temp_list_prod = ['Please add views to transport']
dev_space = []
cross_temp_list_prod_graphical = []
size=(1450, 650)
canvas_cpu = sg.Canvas(key='-CPUchart-', expand_x=True, expand_y=True)
canvas_memory = sg.Canvas(key='-MEMORYchart-', expand_x=True, expand_y=True)


## End of Global Variables

## Start of the Menu 

menu_def = [['&File', ['&Open     Ctrl-O', '&Save       Ctrl-S', '&Properties', '&Exit']],
                ['&Help', ['&About...']], ]

## Start of Tab Layouts

## TAB 1 -- LOGIN
login_tab  = [
        [sg.Combo(values=profiles_list, size=(50,1), key="-PROFILES-")],
        [sg.Button('Add new profile'), sg.Button('Update Profile'), sg.Button('Load Profile'), ],		 
		[sg.Button('Exit')],
        [sg.Text(f'{logged_in}', key='-LOGGED_IN-')],
    ]

## TAB 2 -- PERFORMANCE
monitor_tab = [
    ## "SM50" table
	[sg.Table(values=data,
              headings=header_list, 
              display_row_numbers=True, 
              auto_size_columns=False,
              enable_events=True,
			  expand_x=True,
			  expand_y=True,
              enable_click_events=True,           # Comment out to not enable header and other clicks
              num_rows=min(25, len(data)), 
			  key='-TAB2_TABLE-')],
	[sg.Button('Cancel Process',enable_events=True, key='-TAB2_CANCEL-'), 
	sg.Button('Disconnect User',enable_events=True, key='-TAB2_DISCONNECT-'), 
	sg.Button('Refresh',enable_events=True, key='-TAB2_REFRESH-')]
]

## TAB 3 -- Space Management

performance_monitor_tab = [
  	[sg.Text('Data is refreshed every 10 seconds in database'), 
	 sg.Text('                                                                                                                                                                                                               '),
	 sg.Text('Show the last'), sg.InputText(key='-TIME-', size=(10, 1)), sg.Text('minutes')],
	[sg.Frame("CPU Usage", [[canvas_cpu]], size=(700,530), element_justification='left', title_location=sg.TITLE_LOCATION_TOP), 
  		sg.Frame("Memory Usage", [[canvas_memory]], size=(700,530), element_justification='left', title_location=sg.TITLE_LOCATION_TOP)],
	[sg.Button('Refresh', key='-TAB3_REFRESH-')],	
]

## TAB 4 -- User Management
user_management_tab = [
	[sg.Text('User to be copied:'), sg.Combo(values=users, key="-TAB4_USER_LIST-", size=30)],
	[sg.Button('Copy User to Single User', key='-TAB4_COPY_SINGLE_USER-'), sg.Button('Copy User to Multiple Users', key='-TAB4_COPY_MULTIPLE_USERS-')], 
	[sg.HorizontalSeparator()],
	[sg.Text('Remove User from System')],
	[sg.Combo(values=users, key="-TAB4_REMOVE_USER_LIST-", size=30)],
	[sg.Button('Remove User', key='-TAB4_REMOVE_USER-')],
	[sg.HorizontalSeparator()],
	[sg.Text('Remove Multiple Users from System:')],
  	[sg.Listbox(values=users, size=(55,10), key = '-TAB4_REMOVE_MULTI_USER-'), sg.Listbox(values=users, size=(55,10), key='-TAB4_REMOVE_MULTI_USERS_LISTBOX-')], 
	[sg.Button('Add User to Remove List', key='-TAB4_ADD_USER_TO_REMOVE_LIST-'), sg.Text('                                                           '), sg.Button('Remove User from List', key='-TAB4_REMOVE_USER_FROM_LIST-'), sg.Button('Remove List of Users from System', key='-TAB4_REMOVE_USERS_FROM_SYSTEM-')],
	
]

## TAB 5 -- Same Tenant Transporting

column_left = [
	[sg.Text('Development Space'), sg.Combo(values=spaces, key="-TAB5_DEV_SPACE_LIST-", size=25),sg.Button('Get Objects', key="-TAB5_GET_VIEWS-")],
	[sg.Listbox(values=temp_list, size=(95, 25), key="-TAB5_DEV_VIEWS-", enable_events=True)], 
	[sg.Button('Add View', key='-TAB5_ADD_VIEW-'), sg.Button('Add Views from File', key='-TAB5_VIEWS_FROM_FILE-')]] 


column_right = [
	[sg.Text('Production Space'), sg.Combo(values=spaces, key="-TAB5_PROD_SPACE_LIST-", size=25), sg.Button('Transport', key='TAB5_TRANSPORT')],
	[sg.Listbox(values=temp_list_prod, size=(95, 25), key="-TAB5_PROD_VIEWS-", enable_events=True)],
	[sg.Button('Remove from Transport List', key='-REMOVE_FROM_TRANSPORT-')],
]

same_tenant_transporting_tab = [[sg.Pane([sg.Column(column_left, expand_x=True, size=145), sg.Column(column_right, expand_x=True, size=145)], orientation='h', expand_x=True, expand_y=True, size=(1000, 500))]]

## TAB 6 -- Cross Tenant Transporting

column_left = [
	[sg.Text('This only works for non-graphical views', font=("bold"))],
 	[sg.Text('Development Space'), sg.Combo(values=spaces, key="-TAB6_DEV_SPACE_LIST-", size=25),sg.Button('Get Objects', key="-TAB6_GET_VIEWS-")],
	[sg.Listbox(values=dev_views, size=(95, 25), key="-TAB6_DEV_VIEWS-", enable_events=True)],
	[sg.Button('Add View', key='-TAB6_ADD_VIEW-'), sg.Button('Add Views from File', key='-TAB6_VIEWS_FROM_FILE-')], 
	# [sg.HorizontalSeparator()], 
	# [sg.Text('Please use this part for Graphical Calculation views', font=("bold"))],
 	# [sg.Text('For Graphical Views, download the CSN from tenant and please select the folder with CSN files')], 
    # [sg.InputText(key='-TAB6_CSN_FOLDER-', size=(60, 1)), sg.FolderBrowse('Browse')],
    # [sg.Button('Add Views', key='-TAB6_VIEWS_FROM_FOLDER-')],
 ]

column_right = [
    [sg.Text('', font = ("bold"))],
    [sg.Text('Production Tenant'), sg.Combo(values=profiles_list, size=20, key='-TAB6_PROD_PROFILE-'), sg.Button('Login', key='-TAB6_LOGIN_PROD-'), sg.Text('Production Space'), sg.Combo(values=spaces_prod, key="-TAB6_PROD_SPACE_LIST-", size=20), sg.Button('Transport', key='-TAB6_TRANSPORT-')],
	[sg.Listbox(values=cross_temp_list_prod, size=(95, 25), key="-TAB6_PROD_VIEWS-", enable_events=True)],
 	[sg.Button('Remove from Transport List', key='-TAB6_REMOVE_FROM_TRANSPORT-')],
	# [sg.HorizontalSeparator()], 
	# [sg.Text('Production Tenant'), sg.Combo(values=profiles_list, size=20, key='-TAB6_PROD_PROFILE_GRAPH-'), sg.Button('Login', key='-TAB6_LOGIN_PROD_GRAPH-'), sg.Text('Production Space'), sg.Combo(values=spaces_prod, key="-TAB6_PROD_SPACE_LIST_GRAPHICAL-", size=20)],	
	# [sg.Listbox(values=cross_temp_list_prod_graphical, size=(110, 10), key="-TAB6_PROD_VIEWS_GRAPHICAL-", enable_events=True)],
 	# [sg.Button('Remove from List', key='-TAB6_REMOVE_FROM_LIST_GRAPH-' ), sg.Button('Transport', key='-TAB6_TRANSPORT_GRAPHICAL-')],
]
  
cross_tenant_transporting_tab = [
    			[sg.Text('Currently only works if Datasphere User is the same for Development and Production tenant', font=("bold"))],
                [sg.Pane([sg.Column(column_left, expand_x=True, size=100), sg.Column(column_right, expand_x=True, size=170)], orientation='h', expand_x=True, expand_y=True, size=(1000, 500))]
                ]

## End of Tab Layouts


## Start of Tab Group Layouts and Window Layout
tab_group_layout = [
	[sg.Tab('Login Tab', login_tab, key="-TAB1-", expand_x=True, expand_y=True)],
	[sg.Tab('System Monitor', monitor_tab, key="-TAB2-", visible=False, expand_x=True, expand_y=True,)], 
	[sg.Tab('Performance Monitor', performance_monitor_tab, key="-TAB3-", visible=False, expand_x=True, expand_y=True,)],
	#[sg.Tab('Space Management', space_management_tab, key="-TAB3-",visible=False,expand_x=True, expand_y=True,)],
	[sg.Tab('User Management', user_management_tab, key="-TAB4-",visible=False,expand_x=True, expand_y=True,)],
	[sg.Tab('Same Tenant Transporting', same_tenant_transporting_tab, key="-TAB5-", visible=False, expand_x=True, expand_y=True,)],
	[sg.Tab('Cross Tenant Transporting', cross_tenant_transporting_tab, key="-TAB6-", visible=False, expand_x=True, expand_y=True,)]	
	]
 	

layout = [
	[[sg.TabGroup(tab_group_layout, expand_x=True, key='-TABGROUP-', expand_y = True)]]
]

window = sg.Window(f'A Better Admin Program for Datasphere -- {logged_in}', layout, grab_anywhere=False, resizable=True, finalize=True, 
				   icon=icon_path, titlebar_icon=icon_path, size=size)

window1 = window
window2 = None
window3 = None
window4 = None
window5 = None
window6 = None

## End of Tab Group Layouts and Window Layout

# Eventloop

counter = 1

while True:
	window, event, values = sg.read_all_windows()
	
	if window == window1 and event in (sg.WIN_CLOSED, 'Exit'):
		break
 
####### Here comes all the logic for the first tab. ######
	if window == window1:
		if event == 'Load Profile':
			user_data = sg.UserSettings('user_data_datasphere.json')
			user_data = user_data.get_dict()
			user = values['-PROFILES-']
			data = user_data[user]
			#print(data)
			dev_dsp_host = data['-url-']
			dev_dsp_user = data['-dbuser-']
			dev_dsp_password = data['-dbpassword-']
			dev_dsp_url = data['-dsurl-']
			dev_dsp_secrets_file = data['-secfile-']
			dev_export_folder_path = data['-exportpath-']
			file_spaces = dev_export_folder_path + '/spaces.json'
			cursor = af.connect_hdb(dev_dsp_host, '443', dev_dsp_user, dev_dsp_password)
			ds_logout = af.ds_logout(dev_dsp_url)
			ds_login = af.ds_login(dev_dsp_url, dev_dsp_secrets_file)
			if cursor != None: 
				print('Connected to HDB')
				logged_in = 'Logged in @ ' + dev_dsp_url
				window['-LOGGED_IN-'].update(f'{logged_in}')
				window.set_title(f'A Better Admin Program for Datasphere -- {logged_in}')
				window.refresh()
				data2, header_list = af.active_connections(dev_dsp_host, '443', dev_dsp_user, dev_dsp_password)
				window['-TAB2_TABLE-'].update(values=data2, num_rows=min(25, (len(data2))))
				counter = counter + 1
				spaces = af.read_spaces(dev_dsp_url, dev_dsp_secrets_file, file_spaces)
				file_export_users = af.get_users_from_dsp_tenant(dev_dsp_url, dev_export_folder_path)
				print(file_export_users)
				print('File Exported')	

				# Read the list of users into a data object
				with open(file_export_users, encoding='utf-8') as file: 
					data_json = json.load(file)

				extracted_info = []
				for user in data_json:
					user_info = {
						"userName": user["userName"]
					}
					extracted_info.append(user_info)
				
				user_list = pd.DataFrame(extracted_info)
				number_of_users = len(user_list.index)
				
				user_list = user_list.values.tolist()
				seconds = 600

				# Get the CPU data and draw chart. 
				time, cpu = af.processor_usage(dev_dsp_host, '443', dev_dsp_user, dev_dsp_password, seconds)
				af.draw_figure(window['-CPUchart-'].TKCanvas, af.create_plot_cpu(time, cpu))
				
				# Get the Memory Data and draw chart. 
				time, memory = af.memory_usage(dev_dsp_host, '443', dev_dsp_user, dev_dsp_password, seconds)
				af.draw_figure(window['-MEMORYchart-'].TKCanvas, af.create_plot_memory(time, memory))

				#print(number_of_users)

				window['-TAB4_USER_LIST-'].update(values=user_list)
				window['-TAB4_REMOVE_USER_LIST-'].update(values=user_list)
				window['-TAB4_REMOVE_MULTI_USER-'].update(values=user_list)
				window.refresh()
				window['-TIME-'].update(value=10)

				#print(spaces)
				#spaces_str = str(spaces)
				#window['-TAB3_SPACES_LIST-'].update(values=spaces)
				window['-TAB5_DEV_SPACE_LIST-'].update(values=spaces)
				window['-TAB5_PROD_SPACE_LIST-'].update(values=spaces)
				window['-TAB6_DEV_SPACE_LIST-'].update(values=spaces)
				window['-TAB2-'].update(visible=True)
				window['-TAB3-'].update(visible=True)
				window['-TAB4-'].update(visible=True)
				window['-TAB5-'].update(visible=True)
				window['-TAB6-'].update(visible=True)	
				window.refresh()
			
   
		if  event == 'Add new profile': 
			window.hide()
			window2 = af.add_new_window()

		if event == 'Update Profile':
			profile = values['-PROFILES-']
			data = user_data[profile]
			user_data = sg.UserSettings('user_data_datasphere.json')
			data_map = {'-url-': '-URL-', '-dbuser-': '-DBUSER-', '-dbpassword-': '-DBPASSWORD-', '-dsurl-': '-DSURL-', '-secfile-': '-SECFILE-', '-exportpath-': '-EXPORTPATH-'}
			print(data)
			window.hide()			
			window2 = af.add_new_window()
			for setting_key, values_key in data_map.items():
				value = data[setting_key] if data is not None else ''
				window2[values_key].update(value)

	
	if window == window2:
		if event == 'Add/Update' :
			print(event)
			data_map = {'-url-': '-URL-', '-dbuser-': '-DBUSER-', '-dbpassword-': '-DBPASSWORD-', '-dsurl-': '-DSURL-', '-secfile-': '-SECFILE-', '-exportpath-': '-EXPORTPATH-'}
			user_data = sg.UserSettings('user_data_datasphere.json')
			user = values['-ID-']
			data = {}
			for setting_key, values_key in data_map.items():
				data[setting_key] = values[values_key]
			user_data[user] = data
			sg.popup(f'Data saved for {user}')
		if (event == 'Create new secrets file' and window == window2):
			#window2.hide()
			window3 = af.create_new_secrets_file_window()  
		elif event == 'Return' or event == sg.WIN_CLOSED:
			window2.close()
			window2 = None
			user_data = sg.UserSettings('user_data_datasphere.json')
			user_data = user_data.get_dict()
			profiles_list_upd = list(user_data.keys())
			window1["-PROFILES-"].update(values=profiles_list_upd)
			window1.refresh()
			window1.un_hide()
    
	if window == window3: 
		if event == 'Create Secrets File':                
			af.create_new_secrets_file(values['-CLIENT_ID-'], values['-CLIENT_SECRET-'], values['-AUTH_URL-'], values['-TOKEN_URL-'], values['-FOLDER-'], values['-FILENAME-'])
		elif event == 'Return' or event == sg.WIN_CLOSED:
			window3.close()
			window3 = None
			window2.un_hide()

####### Here comes all the logic for the second tab. ######
			
	# The refresh event, refreshes the table on click. 
	if event == '-TAB2_REFRESH-':
			data2, header_list = af.active_connections(dev_dsp_host, '443', dev_dsp_user, dev_dsp_password)
			window['-TAB2_TABLE-'].update(values=data2, num_rows=min(25, (len(data2))))
			counter = counter + 1
			seconds = int(values['-TIME-'])*60
			time, cpu = af.processor_usage(dev_dsp_host, '443', dev_dsp_user, dev_dsp_password, seconds)
			af.draw_figure(window['-CPUchart-'].TKCanvas, af.create_plot_cpu(time, cpu))
			time, memory = af.memory_usage(dev_dsp_host, '443', dev_dsp_user, dev_dsp_password, seconds)
			af.draw_figure(window['-MEMORYchart-'].TKCanvas, af.create_plot_memory(time, memory))
	# The Table event shows the table and makes the processes in that table clickable. 
	if event == '-TAB2_TABLE-':
		try: 
			if counter == 1:
				selected_process = [data[row] for row in values[event]]
				#print(selected_process[0][0])
			if counter > 1:
				selected_process = [data2[row] for row in values[event]]
				#print(selected_process[0][0])
		except: 
				print('')
	# When a user clicks the kill button it will pick up the selected process and kill that process. 			
	if event == '-TAB2_CANCEL-':
		try: 
			cursor = af.connect_hdb(dev_dsp_host, '443', dev_dsp_user, dev_dsp_password)
			process = selected_process[0][0]
			answer = af.are_you_sure(process)
			if answer == 'Yes':
				st_kill_process = '''CALL "DWC_GLOBAL"."STOP_RUNNING_STATEMENT"''' + '''('CANCEL', ''' + ' ' + f'{process}' +')' 
				print(st_kill_process)	
				cursor.execute(f'{st_kill_process}')		
			if answer == 'No': 
				print('No')			
		except Exception as e: 
				message = e
				error_message = f'{message}'
				print(error_message)
				first5 = error_message[1:6]
				if first5 == '11000': 
					af.process_already_ended()
				else: 
					af.no_process_selected()
	# When a user clicks the disconnect button it will pick up the selected process and disconnect the user.
	if event == '-TAB2_DISCONNECT-':
		try: 
			cursor = af.connect_hdb(dev_dsp_host, '443', dev_dsp_user, dev_dsp_password)
			user = selected_process[0][5]
			process = selected_process[0][0]
			answer = af.are_you_sure_disconnect(user)
			if answer == 'Yes':
				st_disconnect_user = '''CALL "DWC_GLOBAL"."STOP_RUNNING_STATEMENT"''' + '''('DISCONNECT', ''' + ' ' + f'{process}' +')' 
				print(st_disconnect_user)	
				cursor.execute(f'{st_disconnect_user}')		
			if answer == 'No': 
				print('No')			
		except Exception as e: 
				message = e
				error_message = f'{message}'
				print(error_message)
				first5 = error_message[1:6]
				if first5 == '11000': 
					af.process_already_ended()
				else: 
					af.no_process_selected()

## Here comes all the logic for the Third Tab.

	if event == '-TAB3_REFRESH-':
		seconds = int(values['-TIME-'])*60
		print(seconds)
		time, cpu = af.processor_usage(dev_dsp_host, '443', dev_dsp_user, dev_dsp_password, seconds)
		af.draw_figure(window['-CPUchart-'].TKCanvas, af.create_plot_cpu(time, cpu))
		time, memory = af.memory_usage(dev_dsp_host, '443', dev_dsp_user, dev_dsp_password, seconds)
		af.draw_figure(window['-MEMORYchart-'].TKCanvas, af.create_plot_memory(time, memory))


####### Here comes all the logic for the User Management Tab ######
	if event == '-TAB4_COPY_SINGLE_USER-':
		if values['-TAB4_USER_LIST-'] == '': 
			sg.popup('Please select a user to copy')
		else:
			user_to_copy = values['-TAB4_USER_LIST-']
			window.hide()
			window4 = af.create_new_user_copy()
	
	if window == window4:
		if event == 'Cancel' or event == sg.WIN_CLOSED:
			window4.close()
			window4 = None
			window1.refresh()
			window1.un_hide()

		if event == 'Create User':
			username = user_to_copy
			with open(file_export_users, encoding='utf-8') as file: 
					users_data_json = json.load(file)
			username = values['-USERNAME-']
			username = username.replace(' ', '')
			username = username.upper()
			
			firstname = values['-FIRSTNAME-']
			lastname = values['-LASTNAME-']
			displayname = values['-DISPLAYNAME-']
			email = values['-EMAIL-']
			new_user_info = f'''"userName": "{username}", "firstName": "{firstname}", "lastName": "{lastname}", "displayName": "{displayname}", "email": "{email}"'''
			new_user_info = '{' + new_user_info + '}'
			new_user_info_json = json.loads(new_user_info, )
			user_info = af.get_user_info_for_copy(users_data_json, username)
			combined_user_info = {**new_user_info_json, **user_info}
			combined_user_info_array = [combined_user_info]
			print(combined_user_info_array)
			new_user_json_file = dev_export_folder_path + '/newuser.json'
			with open(new_user_json_file, 'w') as file: 
				json.dump(combined_user_info_array, file, indent=4)
			af.push_userdata_to_dsp(new_user_json_file, dev_dsp_url)
			sg.popup('User created')
			window4.close()
			window4 = None
			window1.refresh()
			window1.un_hide()

	if event  == '-TAB4_REMOVE_USER-':
		user_to_be_removed = values['-TAB4_REMOVE_USER_LIST-']
		print(user_to_be_removed)
		user_to_be_removed_str = user_to_be_removed[0]
		user_to_be_removed_str = user_to_be_removed_str.replace('[', '')
		user_to_be_removed_str = user_to_be_removed_str.replace(']', '')
		user_to_be_removed_str = "'" + user_to_be_removed_str + "'"
		print(user_to_be_removed_str)
		answer = sg.popup_yes_no("Are you absolutely sure you want to remove user:", f'{user_to_be_removed_str}')
		if answer == 'Yes':
			af.remove_user_from_system(dev_dsp_url, user_to_be_removed_str)
			sg.popup('User removed')
		if answer == 'No':
			print('No')		

	if event == '-TAB4_COPY_MULTIPLE_USERS-':
		if values['-TAB4_USER_LIST-'] == '': 
			sg.popup('Please select a user to copy')
		else:
			user_to_copy = values['-TAB4_USER_LIST-']
			user_to_copy_str = str(user_to_copy)
			user_to_copy_str = user_to_copy_str.replace('[', '')
			user_to_copy_str = user_to_copy_str.replace(']', '')	
			user_to_copy_str = user_to_copy_str.replace("'", '')
			window.hide()
			window5 = af.create_multiple_users_copy()
			window5['-USERTOCOPY-'].update(value=user_to_copy_str)

	if window == window5:
		if event == 'Cancel' or event == sg.WIN_CLOSED:
			window5.close()
			window5 = None
			window1.refresh()
			window1.un_hide()

		if event == 'Create template file': 
			columns = ['userName', 'firstName', 'lastName', 'displayName', 'email']	
			df = pd.DataFrame(columns=columns)
			excel_file_path = dev_export_folder_path + '/mass_user_creation_template.xlsx'
			df.to_excel(excel_file_path, index=False, engine='openpyxl')
			sg.popup(f'Template file created in location: {excel_file_path}')

		if event == 'Create Users':
			excel_file_path = values['-MASSCREATEFILE-']
			users_to_create = pd.read_excel(excel_file_path)
			username = user_to_copy
			with open(file_export_users, encoding='utf-8') as file: 
					users_data_json = json.load(file)
			user_info = af.get_user_info_for_copy(users_data_json, username)
			
			for index, row in users_to_create.iterrows():
				userName = row['userName']
				userName = userName.replace(' ', '')
				userName = userName.upper()
				firstName = row['firstName']
				lastName = row['lastName']
				displayName = row['displayName']
				email = row['email']
				new_user_info = f'''"userName": "{userName}", "firstName": "{firstName}", "lastName": "{lastName}", "displayName": "{displayName}", "email": "{email}"'''
				new_user_info = '{' + new_user_info + '}'
				new_user_info_json = json.loads(new_user_info, )
				combined_user_info = {**new_user_info_json, **user_info}
				combined_multiple_user_info.append(combined_user_info)

			new_multi_users_json_file = dev_export_folder_path + '/multinewusers.json'
			
			with open(new_multi_users_json_file, 'w') as file: 
				json.dump(combined_multiple_user_info, file, indent=4)
			af.push_userdata_to_dsp(new_multi_users_json_file, dev_dsp_url)
			
			file_export_users = af.get_users_from_dsp_tenant(dev_dsp_url, dev_export_folder_path)
			with open(file_export_users, encoding='utf-8') as file: 
					data_json = json.load(file)
			extracted_info = []
			for user in data_json:
				user_info = {
					"userName": user["userName"]
				}
				extracted_info.append(user_info)
				
			user_list = pd.DataFrame(extracted_info)

			user_list = user_list.values.tolist()

			window1['-TAB4_USER_LIST-'].update(values=user_list)
			window1['-TAB4_REMOVE_USER_LIST-'].update(values=user_list)
			window1['-TAB4_REMOVE_MULTI_USER-'].update(values=user_list)
			window.refresh()
			sg.popup('Users created')
			window5.close()
			window5 = None
			window1.refresh()
			window1.un_hide()

	if event == '-TAB4_ADD_USER_TO_REMOVE_LIST-':
		remove_user = values['-TAB4_REMOVE_MULTI_USER-']	
		remove_user_str = str(remove_user)
		remove_user_str = remove_user_str.replace('[', '')
		remove_user_str = remove_user_str.replace(']', '')
		remove_user_str = remove_user_str.replace("'", '')
		removal_list.append(remove_user_str)
		window['-TAB4_REMOVE_MULTI_USERS_LISTBOX-'].update(values=removal_list)

			
	if event == '-TAB4_REMOVE_USER_FROM_LIST-':
		remove_user_from_list = values['-TAB4_REMOVE_MULTI_USERS_LISTBOX-']
		remove_user_from_list_str = str(remove_user_from_list)
		remove_user_from_list_str = remove_user_from_list_str.replace('[', '')
		remove_user_from_list_str = remove_user_from_list_str.replace(']', '')
		remove_user_from_list_str = remove_user_from_list_str.replace("'", '')
		removal_list.remove(remove_user_from_list_str)
		window['-TAB4_REMOVE_MULTI_USERS_LISTBOX-'].update(values=removal_list)
		
		print(remove_user_from_list_str)

	if event == '-TAB4_REMOVE_USERS_FROM_SYSTEM-': 
		removal_list_str = str(removal_list)
		removal_list_str = removal_list_str.replace('[', '')
		removal_list_str = removal_list_str.replace(']', '')
		removal_list_str = removal_list_str.replace("'", '')
		answer = sg.popup_yes_no("Are you absolutely sure you want to remove these users:", f'{removal_list_str}')
		if answer == 'Yes':
			for user in removal_list: 
				user = "'" + user + "'"
				af.remove_user_from_system(dev_dsp_url, user)
			removal_list = []
			window['-TAB4_REMOVE_MULTI_USERS_LISTBOX-'].update(values=removal_list)
			file_export_users = af.get_users_from_dsp_tenant(dev_dsp_url, dev_export_folder_path)
			with open(file_export_users, encoding='utf-8') as file: 
					data_json = json.load(file)
			extracted_info = []
			for user in data_json:
				user_info = {
					"userName": user["userName"]
				}
				extracted_info.append(user_info)
				
			user_list = pd.DataFrame(extracted_info)

			user_list = user_list.values.tolist()

			window['-TAB4_USER_LIST-'].update(values=user_list)
			window['-TAB4_REMOVE_USER_LIST-'].update(values=user_list)
			window['-TAB4_REMOVE_MULTI_USER-'].update(values=user_list)
			window.refresh()				

			sg.popup('Users removed')
		if answer == 'No':
			print('No')

####### Here comes all the logic for the Same Tenant Transporting Tab ######
	if event == '-TAB5_GET_VIEWS-': 
		dev_space = values['-TAB5_DEV_SPACE_LIST-']
		dev_views = af.read_hana_views_in_space(dev_dsp_host, '443', dev_dsp_user, dev_dsp_password, dev_space)
		window['-TAB5_DEV_VIEWS-'].update(values=dev_views)
	if event == '-TAB5_ADD_VIEW-': 
		try: 
			temp_list_prod.remove('Please add views to transport')
		except: 
			print('Not available')
		temp_list_prod.append(values['-TAB5_DEV_VIEWS-'])
		temp_list_prod = af.flatten_list(temp_list_prod)
		window['-TAB5_PROD_VIEWS-'].update(values=temp_list_prod)
	if event == 'TAB5_TRANSPORT':
		if temp_list_prod == '' or temp_list_prod == ['Please add views to transport']:
			sg.popup('No Views to Transport were selected')
		else:
			prod_space = values['-TAB5_PROD_SPACE_LIST-']
			if prod_space == '':
				sg.popup('Please select a production space')
			else: 
				for view in temp_list_prod: 
					space_csn = af.get_csn_for_object(dev_dsp_host, '443', dev_dsp_user, dev_dsp_password, dev_space, prod_space, view)
					space_csn_file = af.write_space_csn(space_csn, dev_export_folder_path, prod_space, view)
					af.push_space_csn_to_DSP(space_csn_file, dev_dsp_url, prod_space)
					sg.popup('Views transported')

	if event == '-TAB5_VIEWS_FROM_FILE-':
		if values['-TAB5_DEV_SPACE_LIST-'] == '': 
			sg.popup('Please select a development space')
		else:
			dev_space = values['-TAB5_DEV_SPACE_LIST-']
			window.hide()
			window6 = af.transport_views_from_file()

	if window == window6:
		if event == 'Cancel' or event == sg.WIN_CLOSED:
			window6.close()
			window6 = None
			window1.refresh()
			window1.un_hide()

		if event == 'Add Views to Transport List':
			transport_file = values['-VIEWFROMFILE-']
			df = pd.read_excel(transport_file)
			df = df.sort_values(by=['view'])			
			print(df)
			print(dev_space)
			transport_views = df['view'].tolist()
			#print(transport_views)
			adj_views = []
			views_added = 0
			dev_views = af.read_hana_views_in_space(dev_dsp_host, '443', dev_dsp_user, dev_dsp_password, dev_space)
			for view in dev_views: 
				adj_dev_view = str(view)
				adj_dev_view = adj_dev_view.replace('[', '')
				adj_dev_view = adj_dev_view.replace(']', '')
				adj_dev_view = adj_dev_view.replace("'", '')
				adj_views.append(adj_dev_view)
			#print(adj_views)
						
			for view in transport_views:
				#print(view)
				if view not in adj_views:
					sg.popup(f'{view} is not available in the development space')
				else:
					if temp_list_prod[0] == 'Please add views to transport':
						temp_list_prod.remove('Please add views to transport')
					temp_list_prod.append(view)
					views_added = views_added + 1
			if views_added == 0:
				sg.Popup('No views were added to transport list')
			else:
				sg.Popup(f'{views_added} were added to transport list')
			
			window1.refresh()
			if temp_list_prod[0] == 'Please add views to transport':
				temp_list_prod.remove('Please add views to transport')
			window1['-TAB5_PROD_VIEWS-'].update(values=temp_list_prod)
			window6.close()
			window1.un_hide()
			

		
		if event == 'Create template file': 
			columns = ['view']	
			df = pd.DataFrame(columns=columns)
			excel_file_path = dev_export_folder_path + '/mass_view_transport_template.xlsx'
			df.to_excel(excel_file_path, index=False, engine='openpyxl')
			sg.popup(f'Template file created in location: {excel_file_path}')


	if event == '-REMOVE_FROM_TRANSPORT-': 
		view_to_remove = values['-TAB5_PROD_VIEWS-']
		view_to_remove_str = str(view_to_remove)
		view_to_remove_str = view_to_remove_str.replace('[', '')
		view_to_remove_str = view_to_remove_str.replace(']', '')
		view_to_remove_str = view_to_remove_str.replace("'", '')
		temp_list_prod.remove(view_to_remove_str)
		window['-TAB5_PROD_VIEWS-'].update(values=temp_list_prod)
			
####### Here comes all the logic for the Cross Tenant Transporting Tab ######
	if event == '-TAB6_GET_VIEWS-': 
		dev_space = values['-TAB6_DEV_SPACE_LIST-']
		dev_views = af.read_hana_views_in_space(dev_dsp_host, '443', dev_dsp_user, dev_dsp_password, dev_space)
		window['-TAB6_DEV_VIEWS-'].update(values=dev_views)
	
	if event == '-TAB6_ADD_VIEW-':
		try: 
			cross_temp_list_prod.remove('Please add views to transport')
		except: 
			print('')
		cross_temp_list_prod.append(values['-TAB6_DEV_VIEWS-'])
		cross_temp_list_prod = af.flatten_list(cross_temp_list_prod)
		window['-TAB6_PROD_VIEWS-'].update(values=cross_temp_list_prod)

	if event == '-TAB6_REMOVE_FROM_TRANSPORT-':
		if values['-TAB6_PROD_VIEWS-'] == '':
			sg.popup('Please select a view to remove')
		else: 
			view_to_remove = values['-TAB6_PROD_VIEWS-']
			view_to_remove_str = str(view_to_remove)
			view_to_remove_str = view_to_remove_str.replace('[', '')
			view_to_remove_str = view_to_remove_str.replace(']', '')
			view_to_remove_str = view_to_remove_str.replace("'", '')
			cross_temp_list_prod.remove(view_to_remove_str)
			if len(cross_temp_list_prod) == 0:
				cross_temp_list_prod = ['Please add views to transport']
			window['-TAB6_PROD_VIEWS-'].update(values=cross_temp_list_prod)

	if event == '-TAB6_LOGIN_PROD-': 
		print(dev_space)
		if dev_space == '' or len(dev_space) == 0:
			sg.Popup('Please select a development space and press the "Get Objects" button, before trying to log in.', title='Please select Dev Space first')
		else:
			#logout development
			af.ds_logout(dev_dsp_host)
			#retrieve production values
			user_data = sg.UserSettings('user_data_datasphere.json')
			user_data = user_data.get_dict()
			user = values['-TAB6_PROD_PROFILE-']
			data = user_data[user]
			#print(data)
			prod_dsp_url = data['-dsurl-']
			prod_dsp_secrets_file = data['-secfile-']
			prod_export_folder_path = data['-exportpath-']
			af.ds_login(prod_dsp_url, prod_dsp_secrets_file)
			prod_spaces = af.read_spaces(prod_dsp_url, prod_dsp_secrets_file, file_spaces)
			window['-TAB6_PROD_SPACE_LIST-'].update(values=prod_spaces)
			
	if event == '-TAB6_TRANSPORT-':
		if cross_temp_list_prod == '' or cross_temp_list_prod == ['Please add views to transport']:
			sg.popup('No Views to Transport were selected')
		else:
			prod_space = values['-TAB6_PROD_SPACE_LIST-']
			if prod_space == '':
				sg.popup('Please select a production space')
			else: 
				for view in cross_temp_list_prod: 
					dev_space = values['-TAB6_DEV_SPACE_LIST-']
					prod_space = values['-TAB6_PROD_SPACE_LIST-']
					space_csn = af.get_csn_for_object(dev_dsp_host, '443', dev_dsp_user, dev_dsp_password, dev_space, prod_space, view)
					space_csn_file = af.write_space_csn(space_csn, prod_export_folder_path, prod_space, view)
					af.push_space_csn_to_DSP(space_csn_file, prod_dsp_url, prod_space)
					sg.popup('Views transported')
    
	if event == '-TAB6_VIEWS_FROM_FOLDER-':
		if values['-TAB6_CSN_FOLDER-'] == '':
			sg.Popup('Please select a folder with CSN files')
		else:
			csn_folder = values['-TAB6_CSN_FOLDER-']
			filenames = [f for f in os.listdir(csn_folder) if os.path.isfile(os.path.join(csn_folder, f))]
			print(filenames)
			for filename in filenames:
				if filename.endswith('.json'):
					filename_new = filename.split('.json')[0]
					cross_temp_list_prod_graphical.append(filename_new)
					window['-TAB6_PROD_VIEWS_GRAPHICAL-'].update(values=cross_temp_list_prod_graphical)
					print(cross_temp_list_prod_graphical)
    
	# if event == '-TAB6_LOGIN_PROD_GRAPH-':	
	# 	user_data = sg.UserSettings('user_data_datasphere.json')
	# 	user_data = user_data.get_dict()
	# 	user = values['-TAB6_PROD_PROFILE_GRAPH-']
	# 	data = user_data[user]
	# 	#print(data)
	# 	prod_dsp_url_gr = data['-dsurl-']
	# 	prod_dsp_secrets_file_gr = data['-secfile-']
	# 	prod_export_folder_path_gr = data['-exportpath-']
	# 	cf.ds_logout(prod_dsp_url_gr)
	# 	cf.ds_login(prod_dsp_url_gr, prod_dsp_secrets_file_gr)
	# 	prod_spaces_gr = cf.read_spaces(prod_dsp_url_gr, prod_dsp_secrets_file_gr, file_spaces)
	# 	window['-TAB6_PROD_SPACE_LIST_GRAPHICAL-'].update(values=prod_spaces_gr)
		
      
	# if event == '-TAB6_REMOVE_FROM_LIST_GRAPH-':
	# 	if values['-TAB6_PROD_VIEWS_GRAPHICAL-'] == '':
	# 		sg.popup('Please select a view to remove')
	# 	else:
	# 		cross_temp_list_prod_graphical.remove(values['-TAB6_PROD_VIEWS_GRAPHICAL-'])
			
	# if event == '-TAB6_TRANSPORT_GRAPHICAL-': 
	# 	if cross_temp_list_prod_graphical == '' or cross_temp_list_prod_graphical == ['Please add views to transport']:
	# 		sg.popup('No Views to Transport were selected')
	# 	else:
	# 		prod_space_gr = values['-TAB6_PROD_SPACE_LIST_GRAPHICAL-']
	# 		if prod_space_gr == '':
	# 			sg.popup('Please select a production space')
	# 		else: 
	# 			for view in cross_temp_list_prod_graphical: 
	# 				dev_space_gr = values['-TAB6_DEV_SPACE_LIST-']
	# 				prod_space_gr = values['-TAB6_PROD_SPACE_LIST_GRAPHICAL-']
	# 				csn_file_path = csn_folder + '/' + view + '.json'
	# 				csn_file = cf.create_graphical_csn_file(csn_file_path, prod_space_gr)
	# 				space_csn_file = cf.write_space_csn(csn_file, prod_export_folder_path_gr, prod_space_gr, view)
	# 				cf.push_space_csn_to_DSP(space_csn_file, prod_dsp_url_gr, prod_space_gr)
	# 				#sg.popup('Views transported')