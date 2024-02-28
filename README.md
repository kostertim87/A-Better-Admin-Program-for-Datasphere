# A Better Admin Program for SAP Datasphere
![ABAP for Datasphere (341 x 318)](https://github.com/kostertim87/A-Better-Admin-Program-for-Datasphere/assets/50547693/2d901eb1-3687-4500-871a-180607ea828a)

# Introduction to A Better Admin Program for SAP Datasphere

A Better Admin Program for SAP Datasphere is developed to enhance your experience with SAP Datasphere as an admin user. Performing several tasks within SAP Datasphere might be a bit more cumbersome than necessary. I have used my 5 years experience as a Datasphere developer to make some of these tasks simpler. A Better Admin Program for SAP Datasphere will unlock some functionalities in your Datasphere tenant that are not as easily accesible as ABAP for Datasphere will make it.

# Prerequisites
There is a few things you need before you can actually start using A Better Admin Program for SAP Datasphere. 

## Installation of software
- You need to install node.js via this url: [https://nodejs.org/en/](https://nodejs.org/en/)
- After this you can install the SAP Datasphere Command Line Interface (CLI). You can follow the instructions for this via this [SAP page](https://help.sap.com/docs/SAP_DATASPHERE/d0ecd6f297ac40249072a44df0549c1a/f7d5eddf20a34a1aa48d8e2c68a44e28.html)
- Don't worry about the creation of a secrets file or setting a host value, A Better Admin Program will help you with creating it.

## Creating a Database User
We need a database user to perform most of the operations in A Better Admin Program for SAP Datasphere. 
You can create one via: System -> Configuration -> Database Access -> Database Analysis Users -> Create. Please make sure you check the "Enable Space Schema Access" and set the "expires in" to Never (see below screenshot). 

![image](https://github.com/kostertim87/A-Better-Admin-Program-for-Datasphere/assets/50547693/a239e379-ef3f-43f0-b642-a2d40a18cb25)

After creation of the user, edit that same user and note down the User Name, Host Name, the Port and Password. 

![image](https://github.com/kostertim87/A-Better-Admin-Program-for-Datasphere/assets/50547693/19bd595a-2eb1-409b-9a48-ea628bfe395d)

## Creating an OAuth Client
An OAuth Client is needed to be able to write back some of the things that we can manipulate through A Better Admin Program for SAP Datasphere (i.e. Users Lists, Views, etc.). 
To create an OAuth Client go to: System -> Administration -> App Integration and click "Add a New OAuth Client". Give the new client a name, leave the purpose on Interactive Usage and click Add to generate a secret. 
Note down the OAuth Client ID and Secret.  

![image](https://github.com/kostertim87/A-Better-Admin-Program-for-Datasphere/assets/50547693/16447c8d-69f0-46d2-8c71-d1c5aa4d53f9)

When you close down the window, also note down the Authorization URL and Token URL.

![image](https://github.com/kostertim87/A-Better-Admin-Program-for-Datasphere/assets/50547693/c66f0c15-0e39-48a5-9903-b9ea165e2dca)

## Deploying Monitoring Views
Please follow the SAP documentation to set-up a [monitoring space](https://help.sap.com/docs/SAP_DATASPHERE/9f804b8efa8043539289f42f372c4862/9cd0691c44a74f2aa47b52f615f74433.html)
After the set-up has been done, you need to deploy a view tables in the monitoring space: 
- M_LOAD_HISTORY_HOST
- M_ACTIVE_STATEMENTS
- M_CONNECTIONS
- M_SERVICE_THREADS

# Using A Better Admin Program for SAP Datasphere for the first time
You can use ABAP for SAP Datasphere in two ways: 
- Executing the Python Script
- Using the Executable

When you are executing the Python Script don't forget to install all the used packages, which are obviously listed at the top of the Python Script. 

## Creating a Profile
The first time you run the program you have to create a profile. Click the "Add new profile" button. 
Fill in the fields based on the Database User you created in earlier steps. 

![image](https://github.com/kostertim87/A-Better-Admin-Program-for-Datasphere/assets/50547693/e2dee91e-4f87-4a9e-b81e-ffbb6ffecff8)

Since this is the first time you are using ABAP for SAP Datasphere you probably also need to generate a Secrets File. For this you can click the button "Create New Secrets File" in the bottom right. 
Give the file a name and fill in the fields with the information you noted down earlier. Click "Create Secrets File" when you are done and then click "Return", where you can select the secrets file via the "Browse" button.  

![image](https://github.com/kostertim87/A-Better-Admin-Program-for-Datasphere/assets/50547693/ee0bb72b-7287-4094-a192-2453b86c3b51)

After everything is filled in you can click "Add/Update" to create your profile (multiple profiles can be created), click "Return" to return to the login screen. 

## Load a Profile 
Select a profile that you want to load and click "Load Profile". If you filled all the fields correctly it will start loading your profile and logging in. 
You will see that a new browser window will be opened by CLI to log you in into SAP Datasphere. You can do this with your normal credentials (or the login goes automatically when you saved your profile in the browser). 

**Sometimes the login says succeeded, but the program crashes. This is probably caused by a discrepancy between the profile you are trying to load and the user you are logging in with (i.e. when you have different users on different systems and you are still logged in with a different user while trying to load a different profile). Try logging out of Datasphere and then try to load the profile again.**

# System Monitor
In the System Monitor you can see the active statements that are running in your SAP Datasphere tenant. The table is automatically sorted by the Application User Name and the Memory Used. 
![image](https://github.com/kostertim87/A-Better-Admin-Program-for-Datasphere/assets/50547693/2e4bc842-7354-4efc-8fdf-7a9c2f20e813)

If you want to kill a certain task, you can simply select the task in the table and click "Cancel Process". This will send a request to Datasphere to cancel the process. If the system is quite busy it may take some time to actually kill the task you selected. Whenever a user is flooding your system, or maybe there are some zombie loads on a certain user, you may decide to just disconnect the user completely. This will cancel all the running workprocesses that are connected to that user. 

# Performance Monitor
In the Performance Monitor you can see the performance system historically. By default 10 minutes of history is shown, but you can expand this if you like. By clicking the refresh button the program will get the latest CPU / Memory from the system. Be aware that this data is stored only every 10 seconds in the system, so if you click the refresh button multiple times within those ten seconds the chart will not change. 

![image](https://github.com/kostertim87/A-Better-Admin-Program-for-Datasphere/assets/50547693/d426e817-b2bc-4077-9d66-b48b49a09ce6)

# User Management 
The User Management tab is where you can easily copy users and remove users from your system. 

## Copy a user
In the User Management tab you can easily copy a user to a new user. First select the user you want to copy and click the "Copy to Single User" button. 

![image](https://github.com/kostertim87/A-Better-Admin-Program-for-Datasphere/assets/50547693/5cbc2467-ed25-40f5-9383-dc490e41d7dc)

You can now fill in the fields for the new user, click the "Create User" button, and the user will get a welcome mail for SAP Datasphere! 
![image](https://github.com/kostertim87/A-Better-Admin-Program-for-Datasphere/assets/50547693/9767a8b7-e6c5-41d4-923d-f2ce60b36ce4)

If you want to copy a user to multiple new users you can use the "Copy User to Multiple Users" button. This will open a window where you can provide the file that contains the new users and their information. Please use the template that is generated by A Better Admin Program for SAP Datasphere to create this list. To create the template just click "Create template file" and a template file will be created at the export path you provided in your profile. 

![image](https://github.com/kostertim87/A-Better-Admin-Program-for-Datasphere/assets/50547693/a3bcbe19-ff18-4755-9d47-7faa7b46aa82)

## Remove a user
Just select the user that you want to remove from the system in the drop-down list and click the "Remove User" button. 

![image](https://github.com/kostertim87/A-Better-Admin-Program-for-Datasphere/assets/50547693/94f845d6-d94b-432d-a030-807f803bbeb0)

## Remove multiple users
To remove multiple users from the system you can add users by selecting 1 user and clicking on the "Add User to Remove List" button. When your selection is complete you can click the "Remove List of Users from System" button to remove them from the system. 

![image](https://github.com/kostertim87/A-Better-Admin-Program-for-Datasphere/assets/50547693/c3b69bcc-a083-4859-b2e4-b4123087c52a)

# Same Tenant Transporting
Through the Same Tenant Transporting tab you can easily transport non-graphical views from one space to another. First select the space where you want to transport from and click "Get Objects". 
You can add views by clicking the "Add View" button or you can use the "Add Views from File" button to select a list of views that you want to add to the transport list. 

![image](https://github.com/kostertim87/A-Better-Admin-Program-for-Datasphere/assets/50547693/9ccbdac9-d6ea-4cef-807f-ced59ed50b8a)

When you are ready to transport, select a space you want to transport to and click the "Transport" button.
**If you transport a graphical view through this method it will actually get the CSN from the back-end and change the view into a SQL View, so I advice against using this method of transporting for graphical views.**

# Cross Tenant Transporting
Cross Tenant Transporting works the same as Same Tenant Transporting, but as an extra step you need to login to the production tenant (which is a profile that needs to be generated first in the Login Tab). 

![image](https://github.com/kostertim87/A-Better-Admin-Program-for-Datasphere/assets/50547693/a09e8692-d049-4081-ba8f-94741d57c0db)


**Unfortunately at this time it is only possible to do a cross tenant transport when the user name / password is the same for the development tenant as the production tenant, as the cookie that is stored when logged in can not be removed. You might be able to do a cross tenant transport when you manually log off in the development tenant and then re-login via the "Login" button in the Cross Tenant Transporting Tab, but I have not tested that yet.**


# Donating
A Better Admin Program for SAP Datasphere is absolutely free to use. If however you want to support the project feel free to do a donation. 

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/donate/?business=GHJJDER887YUC&no_recurring=0&item_name=Although+A+Better+Admin+Program+for+SAP+Datasphere+is+absolutely+free+to+use%2C+donations+are+always+welcome%21+&currency_code=EUR)

