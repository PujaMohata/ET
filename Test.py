import mysql.connector
from datetime import date, datetime
import calendar

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

def MontoTxt(month): # Function to convert month from digit to word
	if(month == '01'):
		a = 'January'
	elif(month == '02'):
		a = 'February'
	elif(month == '03'):
		a = 'March'
	elif(month == '04'):
		a = 'April'
	elif(month == '05'):
		a = 'May'
	elif(month == '06'):
		a = 'June'
	elif(month == '07'):
		a = 'July'
	elif(month == '08'):
		a = 'August'
	elif(month == '09'):
		a = 'September'
	elif(month == '10'):
		a = 'October'
	elif(month == '11'):
		a = 'November'
	elif(month == '12'):
		a = 'December'
	return a
	

save = 0 # Savings var
print("Enter 1 to add details \n")
user = int(input())

#Entering details as user pressed 1 to add details option 
if (user == 1):
	datee = input("Add Expenses date in the format YYYY-MM-DD : ")
	if not datee: # If date not given take the current date as default
		today = date.today()
		datee = today.strftime("%Y-%m-%d")
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
   
 