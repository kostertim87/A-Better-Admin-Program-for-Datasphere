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

# Donating
A Better Admin Program for SAP Datasphere is absolutely free to use. If however you want to support the project feel free to do a donation. 

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/donate/?business=GHJJDER887YUC&no_recurring=0&item_name=Although+A+Better+Admin+Program+for+SAP+Datasphere+is+absolutely+free+to+use%2C+donations+are+always+welcome%21+&currency_code=EUR)

