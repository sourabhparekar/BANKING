import mysql.connector as sql
from mysql import *

class Bankdb:
    def __init__(self):
        self.conn=sql.connect(database="sbidb",user="root",password="admin",charset='utf8')
    def addAcc(self,nm,bl):
        cmd="insert into accmaster(name,balance) values(%s,%s)"
        cur=self.conn.cursor()
        cur.execute(cmd,[nm,bl])

        cmd="select max(accno) from accmaster"
        cur=self.conn.cursor()
        cur.execute(cmd)
        row=cur.fetchone()
        an=row[0]
        
        self.addtrans(an,bl,"D")
        self.conn.commit()
        return an

    def deposit(self,an,amt):
        cmd="update accmaster set balance=balance+%s where accno=%s"
        cur=self.conn.cursor()
        cur.execute(cmd,[amt,an])
        if cur.rowcount==1:
            self.addtrans(an,amt,"D")
            self.conn.commit()
            return True
        return False

    def withdraw(self,an,amt):
        bal=self.getbalance(an)
        if bal==-1:
            return False
        if amt>bal:
            return None
        cmd="update accmaster set balance=balance-%s where accno=%s"
        cur=self.conn.cursor()
        cur.execute(cmd,[amt,an])
        if cur.rowcount==1:
            self.addtrans(an,amt,"W")
            self.conn.commit()
            return True

    def getbalance(self,an):
        cmd="select balance from accmaster where accno=%s"
        cur=self.conn.cursor()
        cur.execute(cmd,[an])
        row=cur.fetchone()
        if row==None:
            return -1
        return row[0]

    def list(self):
        cmd="select * from accmaster"
        cur=self.conn.cursor()
        cur.execute(cmd)
        lst=cur.fetchall()
        return lst

    def passbook(self,an):
        cmd="select * from trans where accno=%s"
        cur=self.conn.cursor()
        cur.execute(cmd,[an])
        lst=cur.fetchall()
        return lst
    
    def addtrans(self,an,amt,ttype):
        cmd="insert into trans(accno,amt,ttype) values(%s,%s,%s)"
        cur=self.conn.cursor()
        cur.execute(cmd,[an,amt,ttype])        

db=Bankdb()
while True:
    menu="\n1:New Acc\n2:Deposit\n3:Withdraw\n4:List\n5:Passbook\n8:Exit"
    print(menu)
    ch=int(input("Enter Choice:"))
    if ch==1:
        nm=input("Enter Name:")
        bl=int(input("Enter Amount:"))
        an=db.addAcc(nm,bl)
        print("New Account No is:",an)
    if ch==2:
        an=int(input("Enter AccNo:"))
        amt=int(input("Enter Amount:"))
        if db.deposit(an,amt):
            print("Amount Deposited..")
        else:
            print("Accno Not Found..")
    if ch==3:
        an=int(input("Enter AccNo:"))
        amt=int(input("Enter Amount:"))
        res=db.withdraw(an,amt)
        if res==True:
            print("Amount Withdrawn..")
        elif res==False:
            print("AccNo Not Found..")
        else:
            print("InSufficient Balance..")

    if ch==4:
        lst=db.list()
        print("-"*37)
        for an,nm,bl in lst:
            an=str(an).rjust(5)
            nm=nm.ljust(20)
            bl=str(bl).rjust(8)
            print(f"|{an}|{nm}|{bl}|")
        print("-"*37)

    if ch==5:
        an=int(input("Enter AccNo:"))
        bal=db.getbalance(an)
        if bal==-1:
            print("AccNo Not Found..")
        else:
            print("Balance :",bal)
            lst=db.passbook(an)
            print("-"*30)
            print("|Date      |Deposit |Withdraw|")
            print("-"*30)
            for tid,dt,an,amt,ttype in lst:
                dt=dt.strftime("%d-%m-%Y")
                if ttype=="D":
                    damt=str(amt).rjust(8)
                    wamt=" "*8
                else:
                    wamt=str(amt).rjust(8)
                    damt=" "*8
                print(f"|{dt}|{damt}|{wamt}|")
            print("-"*30)
    if ch==8:
        break
