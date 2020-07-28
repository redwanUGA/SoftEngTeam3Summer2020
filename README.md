# SoftEngTeam3Summer2020
# instruction to run the application 

1. Extract the items in the folder. 
2. run finaldb.sql in MySQL Workbench. 
3. go to the folder where the app.py folder is 
4. run the following command in cmd 

`python app.py`

Note : following packages are needed to run the application 
* Flask
* flask-mysqldb
* flask-mail
* flask-uploads
* cryptography

also downgrade werkzeug to version 0.6.0 since it conflicts with flask-uploads
