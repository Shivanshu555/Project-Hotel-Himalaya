import mysql.connector
from datetime import date
from tabulate import tabulate

db='Hotel' #input('Enter Name of your database: ')

#Connecting to MySQL
mydb=mysql.connector.connect(host='localhost',user='root',password='88951')
mycursor=mydb.cursor()

#Entering into Database
mycursor.execute('CREATE DATABASE if not exists '+db+';')
mycursor.execute('USE '+db)
print('Connection to the Database Succesfull...')
mycursor=mydb.cursor()

#Entering into the Table
TableName='Rooms' #input('Enter the table name: ')
query="CREATE TABLE IF NOT EXISTS "+TableName+"\
(RoomNo int PRIMARY KEY,\
Price_per_day float,\
Person_Name varchar(15),\
Contact_No varchar(14),\
From_Date date,\
To_Date date,\
Bill float,\
Status varchar(10));"
mycursor.execute(query)
print('Entered to table '+TableName+' succesfully...\n\n')


#Now the options available is displayed
print('===============================')
print('Welcome to the Hotel Himalaya')
print('===============================')

def options():
    print('''

1. Book a room
2. Delete booking of room
3. See the details of all the room
4. See the details of a room
5. Add Room
6. Delete Room
7. Exit''')
    what=int(input('\n What do you want to do: '))
    print('\n')
    if what==1:
        Book()
    elif what==2:
        Delete()
    elif what==3:
        Rooms()
    elif what==4:
        RoomDetails()
    elif what==5:
        AddRoom()
    elif what==6:
        DeleteRoom()
    elif what==7:
        exit()
    else:
        print('Incorrect Choice!\n')
        options()

def AddRoom():
    '''It adds a room to the table Rooms'''
    
    rn=int(input('Enter Room No.: '))
    p=float(input('Enter the price per day: '))
    mycursor.execute("INSERT INTO {} VALUES({},{},NULL,NULL,NULL,NULL,NULL,'NOT BOOKED')".format(TableName,rn,p))
    mydb.commit()
    print('Room {} added succefully...'.format(rn))
    options()

def DeleteRoom():
    '''It deletes a room in the table Rooms'''
    
    rn=int(input('Enter the Room No. to delete: '))
    mycursor.execute("DELETE FROM {} WHERE RoomNo={};".format(TableName,rn))
    mydb.commit()
    print('Room {} deleted succefully...'.format(rn))
    options()

def Book():
    '''To see the rooms available and do booking'''

    # Show Available Rooms
    print('Rooms available are: ')
    mycursor.execute("SELECT RoomNo, Price_per_day FROM {} WHERE Status='NOT BOOKED'".format(TableName))
    available_rooms=mycursor.fetchall()
    print(tabulate(available_rooms,headers=['Room Number','Price Per Day (in Rs)'],tablefmt='fancy_grid'))
    
    # Book a room
    if len(available_rooms)==0:
        print('No room is available!')
        options()
    try:
        rn=int(input('\nEnter Room No. to book: '))
    except ValueError:
        options()
        
    for i in available_rooms:
        if i[0]==rn:
            price_per_day=i[1]
            break
        
    n=input('Enter the Name of person: ')
    cont=input('Enter the contact no: ')
    from_date1=input('Enter the Booking date (dd-mm-yyyy format): ')
    to_date1=input('Enter the ending date (dd-mm-yyyy format): ')
    
    fd,fm,fy=[int(i) for i in from_date1.split('-')]
    from_date=str(fy)+'-'+str(fm)+'-'+str(fd)
    td,tm,ty=[int(i) for i in to_date1.split('-')]
    to_date=str(ty)+'-'+str(tm)+'-'+str(td)
    no_of_days=date(ty,tm,td)-date(fy,fm,fd)
    bill=no_of_days.days*price_per_day
    print('\nAmount to pay: Rs '+str(bill))
    pd=input('Is the amount paid (y/n): ')
    if pd.lower()=='y':        
        mycursor.execute("UPDATE {} \
    SET Person_Name='{}',Contact_No='{}',From_Date='{}',To_Date='{}',Bill={},Status='BOOKED'\
    WHERE RoomNo={}".format(TableName,n,cont,from_date,to_date,bill,rn))

        mydb.commit()
        print('Booked Room No. {} succesfully...'.format(rn))
        print('''
                    Payment Slip...
                    --------------------------------------------
                                   HIMALAYA HOTELS

                       Room No: {}             Price Per Day: {}
                          Name: {}
                          From: {}
                            To: {}             
                    No of days: {}
                    Total payment made: Rs {}/        Paid

                    Happy Stay!
                    -----------------------------------------------
'''.format(rn,price_per_day,n,from_date1,to_date1,no_of_days.days,bill))

    else:
        print('Booking Unsuccessfull!')
    options()

def Delete():
    rn=int(input('Enter the Room No. to delete booking: '))
    mycursor.execute("UPDATE {} \
SET Person_Name=NULL,Contact_No=NULL,From_Date=NULL,To_Date=NULL,Bill=NULL,Status='NOT BOOKED'\
WHERE RoomNo={}".format(TableName,rn))
    mydb.commit()
    print("Booking of Room No. {} deleted successfully.".format(rn))
    options()

def Rooms():
    mycursor.execute('SELECT * FROM Rooms;')
    data=mycursor.fetchall()
    print(tabulate(data,headers=['R.No','Price','Name','Physics Wallah.lnk','From','To','Bill','Status'],tablefmt='fancy_grid'))
    options()

def RoomDetails():
    rn=int(input('Enter the Room No. whose details you want: '))
    mycursor.execute('SELECT * FROM {} WHERE RoomNo={}'.format(TableName,rn))
    data=mycursor.fetchall()
    print(tabulate(data,headers=['Room No','Price','Name','Contact','From','To','Bill','Status'],tablefmt='fancy_grid'))
    options()


options()




