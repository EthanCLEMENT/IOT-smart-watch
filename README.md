# Running smart watch project
This is a project that I started in December 2021 and finished in February 2022. 

## Description
The entire watch runs on an arduino uno which displays basic features such as a step counter, the heart rate or even the time. The watch includes a BLE ( bluetooth low energy ) so the watch can send the data from a run to the website which includes a database so each user can track their running stats. A query was built as well so the 
administrators of the website can make requests in the database. 
The BLE is also used to send the data from the watch to an IOS app where the same features displayed on the watch can be found. 

The backend of the website was made in Python with diverse librairies such as Flask or requests whereas the frontend was coded in HTML5 and CSS. The Arduino was entirely coded in C.
Finally the IOS app was coded in Swift.

## Commands
In order to compile the website you will need to import ```flask```, ```flask_sqlalchemy```, ```requests```, ```datetime```.
To do that you need to open a terminal and enter the following command :
```
pip install flask, flask_sqlalchemy, requests, datetime
```
or you can just do :
```
pip install -r requirements.txt
```

To initiate the website you need to type in a terminal : 
```
python main.py
```
Then you can open a web broswer and enter :
```
http://127.0.0.1:5000/
```
The request commands can be accessed by typing :
```
python DatabaseRequests.py
```
The commands that are currently implemented are : userInfo, deleteUser, modifyInfo and some others might be added later. Note that SQL is not required to use the database at all.

To connect the watch to a computer or a phone, you need to turn on the bluetooth on the corresponding device. Eventually an app like nRF Connect will be required on IOS.  

