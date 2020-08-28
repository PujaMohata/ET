import mysql.connector
from datetime import date, datetime
import calendar
import sys
import time
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
c = 0
loop = 'y'
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
val= ""
h= ""
cat = ""
def getdate(): # Function that will enter date as and when required
	global datee
	datee = input("Enter date in the format YYYY-MM-DD : ")
	#2020-09-02
	t = date.today()
	d = t.strftime("%Y-%m-%d")
	format = "%Y-%m-%d"
	try:
	    datetime.strptime(datee, format)
	    return 1
	except ValueError:
	    print("This is the incorrect date string format. It should be YYYY-MM-DD")
	    getdate()
	
	if not datee: # If date not given take the current date as default
		today = date.today()
		datee = today.strftime("%Y-%m-%d")
	elif datee > d:
		print("Sorry I can't travel to future")
		getdate()

def validatedate():
	global val
	global h
	global c
	if c == 0:
		val = input("Enter the Initial date(YYYY-MM-DD) : ")
	
	try:
		#val = input("Enter the Initial date(YYYY-MM-DD) : ")
		datetime.strptime(val,"%Y-%m-%d")
		c = 1
		
	except ValueError:
		print("This is the incorrect initial date string format. It should be YYYY-MM-DD")
		c = 0
		validatedate()
	
	if c == 1:
		h = input("Enter the Final date(YYYY-MM-DD): ")	
	try:
		#h = input("Enter the Final date(YYYY-MM-DD): ")	
		datetime.strptime(h,"%Y-%m-%d")
		
	except ValueError:
		print("This is the incorrect final date string format. It should be YYYY-MM-DD")
		h = ""
		c = 1
		validatedate()

def GetCategory():
	global cat
	List = ['Rent','Grocery','Travel','Internet','Daily Item','Miscellaneous']
	print("Select the category('Rent','Grocery','Travel','Internet','Daily Item','Miscellaneous') in which you wanna edit ")
	cat = input()
	cat = cat.capitalize()
	if a not in List :
		GetCategory()
		

while loop == 'y' :
		

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
		#getdate()
		print("Enter 1 for viewing for a day")
		print("Enter 2 for viewing for a Range of dates")
		print("Enter 3 for viewing for a Range of months")
		a = int(input())
		if (a == 1):
			getdate()
			sql = "SELECT * FROM expenses WHERE `Date` = '%s'" %(datee)
			mycursor.execute(sql)
			myresult = mycursor.fetchall()
			#print (myresult)
			
			df = pd.DataFrame(myresult,columns=['Date','Rent','Grocery','Travel','Internet','Daily Item','Miscellaneous','Income','Savings'])
			print(df)
			
		
		
		elif  a == 2:
			validatedate()
			sql = "SELECT * FROM expenses WHERE `Date` BETWEEN '%s' AND '%s'" % (val,h)
			mycursor.execute(sql)
			myresult = mycursor.fetchall()
			
			df = pd.DataFrame(myresult,columns=['Date','Rent','Grocery','Travel','Internet','Daily Item','Miscellaneous','Income','Savings'])
			print(df)
			
		
		elif a == 3:
			print("select a for Current month")
			print("select b for Last month")
			print("select c for Last 3 months")
			v = input()
			if (v == 'a'):
				r = date.today()
				t = r.strftime("%Y-%m")
				t = t + "-%"
				sql = "SELECT * FROM expenses WHERE `Date` LIKE '%s'" %(t)
				#print(sql)
				mycursor.execute(sql)
				myresult = mycursor.fetchall()
				#print(myresult)
				df = pd.DataFrame(myresult,columns=['Date','Rent','Grocery','Travel','Internet','Daily Item','Miscellaneous','Income','Savings'])
				print(df)
				
			if (v == 'b'):
				today = date.today()
				if today.month == 1:
					one_month_ago = today.replace(year=today.year - 1, month=12)
		
				else:
					one_month_ago = today.replace(month=today.month - 1)
		
				z = one_month_ago.strftime("%Y-%m")
				z= z + "-%" 
				sql = "SELECT * FROM expenses WHERE `Date` LIKE '%s'" %(z)
				mycursor.execute(sql)
				myresult = mycursor.fetchall()
				
				df = pd.DataFrame(myresult,columns=['Date','Rent','Grocery','Travel','Internet','Daily Item','Miscellaneous','Income','Savings'])
				print(df)
				
			if (v == 'c'):
				today = date.today()
				#date_str = '2020-01'
				#today = datetime.strptime(date_str, '%Y-%m').date()
				#today = "2020-02-01"
				#today = time.strptime(today, "%Y-%m")
				y = today.strftime("%Y-%m")
				y += "-31"
				if today.month == 2:
					two_month_ago = today.replace(year=today.year - 1, month=12)
					
				elif today.month == 1:
					two_month_ago = today.replace(year=today.year - 1, month=11)
					
				else:
					two_month_ago = today.replace(month=today.month - 2)
				
				z = two_month_ago.strftime("%Y-%m")
				z = z+ "-01"
				sql = "SELECT * FROM expenses WHERE `Date` BETWEEN '%s' AND '%s'" %(z,y)
				print(sql)
				mycursor.execute(sql)
				myresult = mycursor.fetchall()
				
				df = pd.DataFrame(myresult,columns=['Date','Rent','Grocery','Travel','Internet','Daily Item','Miscellaneous','Income','Savings'])
				print(df)
				
		# else:
			# getdate()
			# val = "%-"+datee[5:7]+ "-%" # %-08-%
			# sql = "SELECT SUM(%s) FROM expenses WHERE `Date` LIKE '%s'" %(a,val)
			# val = (datee[4:10])
			# mycursor.execute(sql, val)
			# value = mycursor.fetchone()
			# print(value[0])
			
	if (user == 3):
		print("select 1 to edit one category for a day")
		print("select 2 to edit all categories for a day")
		a = int(input())
		if (a == 1):
			GetCategory()	
			getdate()
			b = input("Enter the new value : ")     
			sql = "UPDATE expenses SET `%s` = %s WHERE Date = '%s'  " %(a,b,datee)
			#print(sql)
			#sql = "UPDATE expenses SET Rent = %s WHERE Date = %s"
			#val = (b,datee)
			mycursor.execute(sql)

			mydb.commit()

			print(mycursor.rowcount, "record(s) affected")
							
		if (a == 2):
			getdate()
			grocery = int(input("Add your monthly grocery expense : ") or 0)
			travel = int(input("Add your travel expense for the day : ") or 0)
			internet = int(input("Add your monthly internet charges : ") or 0)
			dailyitem = int(input("Add your daily item expenses : ") or 0)
			misc = int(input("Add your daily miscellaneous expenses : ") or 0)
			
			sql = "UPDATE expenses SET Grocery = %s, Travel = %s, Internet = %s, DailyItem = %s, Miscellaneous = %s WHERE Date = '%s' " %(grocery,travel,internet,dailyitem,misc,datee) 
			
			mycursor.execute(sql)
			
			mydb.commit()
			
			print(mycursor.rowcount, "record(s) affected")
	print("Enter Y to continue")
	loop = input()
	loop = loop.lower()	
			
		