import mysql.connector
from datetime import date, datetime
import calendar
import sys
# import numpy as np
import pandas as pd

# MySQL connection Block 
# THIS FILE IS ON PUBLIC REPO SO BETTER CHANGE THIS BEFORE HOSTING IT
mydb = mysql.connector.connect(
  host="localhost",
  user="puja",
  password="eEOhur45omZsdIno",
  database="test"
)
# MySQL Block ends here 

mycursor = mydb.cursor() # Defining global mycursor var here
b = ''
def MontoTxt(month): # Function to convert month from digit to word
	if(month == '01'):
		b = 'January'
	elif(month == '02'):
		b = 'February'
	elif(month == '03'):
		b = 'March'
	elif(month == '04'):
		b = 'April'
	elif(month == '05'):
		b = 'May'
	elif(month == '06'):
		b = 'June'
	elif(month == '07'):
		b = 'July'
	elif(month == '08'):
		b = 'August'
	elif(month == '09'):
		b = 'September'
	elif(month == '10'):
		b = 'October'
	elif(month == '11'):
		b = 'November'
	elif(month == '12'):
		b = 'December'
	return b
	

save = 0 # Savings var
datee = ""
def getdate():
	global datee
	datee = input("Enter date in the format YYYY-MM-DD : ")
	t = date.today()
	d = t.strftime("%Y-%m-%d")
	if not datee: # If date not given take the current date as default
		today = date.today()
		datee = today.strftime("%Y-%m-%d")
	elif datee > d:
		print("Sorry I can't travel to future")
		sys.exit()
	
print("Enter 1 to add details \n")
print("Enter 2 to view details \n")
print("Enter 3 to edit details \n")

user = int(input())

#Entering details as user pressed 1 to add details option 
if (user == 1):
	getdate()
	income = 0 # define income as 0 for later use in calc last day expenditure
	if (datee[8:10] == '01'): # Take income only if it's the first day of the month 
		income = int(input("Enter your monthly income: "))
	rent = int(input("Add your monthly rent expense : ") or 0) 
	grocery = int(input("Add your monthly grocery expense : ") or 0)
	travel = int(input("Add your travel expense for the day : ") or 0)
	internet = int(input("Add your monthly internet charges : ") or 0)
	dailyitem = int(input("Add your daily item expenses : ") or 0)
	misc = int(input("Add your daily miscellaneous expenses : ") or 0)
	#income = int(input("Enter your monthly income: "))
	total = rent + grocery + travel + internet + dailyitem + misc
	print("Your Total Expense for the day is : ",total) # Printing Total expense every day after entering data
	
	#weekly expenditure of the current week starting from Monday and ending on Sunday 
	if (datetime.today().isoweekday() == 7):
		calcweek(date1)
		today = date.today()
		date1 = today.strftime("%Y-%m-%d")
		a = "%v"
		sql = "SELECT SUM(Rent)+ SUM(Grocery) + SUM(Travel)+SUM(Internet)+SUM(DailyItem)+SUM(Miscellaneous) FROM `expenses` WHERE DATE_FORMAT(`Date`, '%s') = DATE_FORMAT('%s', '%s')" % (a,date1,a)
		mycursor.execute(sql, date1)
		result = mycursor.fetchone()
		result1 = result[0] + rent + grocery + travel + internet + dailyitem + misc
		print("Your this Week's Expenditure is %s" % result1)

	#2020-08-31 
	# 31 == lastdateof 2020 08
	
	if (int(datee[8:10]) == int(calendar.monthrange(int(datee[:4]),int(datee[6:7]))[1])):
		#2020-08-01
		#'%-08-%'
		value ="%-"+ datee[5:7] +"-%"
		sql = "SELECT SUM(Rent) + SUM(Grocery) + SUM(Travel) + SUM(Internet) + SUM(DailyItem) + SUM(Miscellaneous) FROM `expenses` WHERE `Date` LIKE '%s'" % value
		mycursor.execute(sql, value)
		res = mycursor.fetchone()
		#Printing Monthly expenditure for the current month
		print("Your Monthly Expenditure for %s is %s" %(MontoTxt(datee[5:7]),res[0]))
		val = "%-"+datee[5:7] +"-01"
		sql = "SELECT `Income` FROM expenses WHERE `Date` LIKE '%s'" % val
		#val = (datee[4:10])
		mycursor.execute(sql, val)
		income1 = mycursor.fetchone()
		print(type(income1[0]))
		if(int(income1[0]) != 0):
			save = income1[0] - res[0]
			print(save)
			print("Your Monthly Savings for %s is %s" %(MontoTxt(datee[5:7]),save))
			
		else:
			print("You didn't Enter your income for the month")
			income = int(input("Enter Your Income for the month : "))
			save = income - res[0]
			print("Your Monthly Savings for %s is %s" %(MontoTxt(datee[5:7]),save))

	#Inserting Values after working through the above lines
	sql = "INSERT INTO expenses (Date,Rent,Grocery,Travel,Internet,DailyItem,Miscellaneous,Income,Saving) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	val = (datee, rent, grocery, travel, internet, dailyitem, misc, income,save)
	mycursor.execute(sql, val)

	mydb.commit()

	print(mycursor.rowcount, "record inserted.") # print for fun 
   
if (user == 2):
	getdate()
	print("Enter the category of which you wanna view the data")
	print("Eg. Rent, Grocery,Travel, Internet, DailyItem, Misc,ALL or Everything")
	a = input()
	a = a.capitalize()
	if a == 'Dailyitem':
		a = 'DailyItem'
	 
	elif a == 'Tt':
	# 2019-08-19.... 2019-08-01 till today
		val = datee[:7] + "-01"
		sql = "SELECT * FROM `expenses` WHERE `Date` BETWEEN '%s' AND '%s'" %(val, datee)
		mycursor.execute(sql,val)
		res2 = mycursor.fetchall()
		#print(res2)
		df = pd.DataFrame(res2,columns=['Date','Rent','Grocery','Travel','Internet','Daily Item','Miscellaneous','Income','Savings'])
		print(df)
		#sys.exit()
		
	
	# start date till end date 
	# 2020-08-03 till 2020-08-12
	elif  a == 'Range':
		val = "%-"+datee[5:7]+ "-%" +datee[8:10]# %-08-% 
		h = "%-"+datee[5:7]+ "-%" +datee[8:10]
		sql = "SELECT * FROM expenses WHERE `Date` LIKE '%s' AND '%s'" % (val,h)
		mycursor.execute(sql,val)
		myresult = mycursor.fetchall()
		print(myresult)
		df = pd.DataFrame(myresult,columns=['Date','Rent','Grocery','Travel','Internet','Daily Item','Miscellaneous','Income','Savings'])
		print(df)
		#data = np.array([['Date','Rent','Grocery'],
                #[myresult[0][0],myresult[0][1],myresult[0][2]],
                #[myresult[1][0],myresult[1][1],myresult[1][2]]])
		
		#print(pd.DataFrame(data=data[1:,1:],
                  #index=data[1:,0],
                  #columns=data[0,1:]))
			
			
	else:
		val = "%-"+datee[5:7]+ "-%" # %-08-%
		sql = "SELECT SUM(%s) FROM expenses WHERE `Date` LIKE '%s'" %(a,val)
		#val = (datee[4:10])
		mycursor.execute(sql, val)
		value = mycursor.fetchone()
		print(value[0])
		
if (user == 3):
	getdate()
	print("Wanna Edit Your Expense of any day?")
	
		
	