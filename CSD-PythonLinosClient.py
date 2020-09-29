import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from time import gmtime, strftime
import cx_Oracle
from datetime import datetime

now = datetime.now()
datestr = now.strftime("%d-%b-%Y %I:%M:%S")

L_payement= ('LOAN_NUM', 'CLIENT_ID', 'AMOUNT_PAID', 'DATE_PAID')#Loan_repayement

kyc=('FIRST_NAME','LAST_NAME','LOCATION_ADDRESS','DIGITAL_ADDRESS','CONTACT_NUMBER','EMAIL','GENDER','AGE','MARITAL_STATUS','NAME_OF_SPOUSE','OCCUPATION','EMPLOYER','ANNUALSALARY','CLIENTID','PASSWORD','RE_TYPE_PASSWORD') # create account

GUARANTORS=('G.FULL_NAME','G.EMAIL','G.PHONE','G.LOACTION_ADDRESS','RELATIONSHIP','BANK','ACCOUNT_NUMBER','ACCOUNT_NAME','BRANCH')
Lnform_field = ('ClientId','Gurantor name','Amount','Period') #apply loan table

account_info = () #get Kyc values into this
loan_info = () #get loan applied

def home_return(master):
	master.destroy()
	Main_Menu()

#This function creates a gurantor forms, the function is located in side procced function which is called when the proceed button is clicked
def gurantor_info(win, kyc):
	win=tk.Tk()
	win.geometry("1000x700")
	win.title("Gurantor Info")
	win.configure(bg="powder blue")
	Tops=tk.Frame(win,width=600,height=100,bd=8,bg="powder blue")
	Tops.pack(side=tk.TOP)

	l_title2=tk.Label(Tops,text="Fill Gurantor details",justify="center",relief="raised")
	l_title2.config(font=("Courier","15","bold"))
	l_title2.pack(side="bottom")
	global field
	global row
	entries = {}
	for field in GUARANTORS:
		print(field)
		row = tk.Frame(win,width=500,height=300,bg="powder blue")
		row.pack(side=tk.TOP)
  
        
        # **********Label Widget****************
		inputV=tk.Label(row,width=22,text=field +": ",font=('arial',13,'bold'),bd=15,fg="black",bg="powder blue")
		inputV.grid(row=0,column=0)
        
        # # **********Entry Widget****************
		ent = tk.Entry(row,font=('arial',12),bd=15,width=22,justify='left')
		ent.grid(row=0,column=1)
        
		entries[field] = ent
	button_fr=tk.Frame(win,width=300,bg="powder blue")
	button_fr.pack(fill=tk.X,ipadx=5,ipady=5)
	b=tk.Button(button_fr,width=20,text="Submit",bd=20,relief="raised",font=('arial',14,'bold'),bg="powder blue",command=lambda:submit(win,entries))
	b.pack(side="top",pady=20,ipadx=10)
	win.bind("<Return>",lambda x:submit(win,entries))
       
        # insert values 
	entries['G.FULL_NAME'].insert(0,"gurantor full name")
	# entries['G.FULL_NAME'].configure(state='disabled')
	entries['G.EMAIL'].insert(0,"name@gmail.com")
	entries['G.PHONE'].insert(0,"phone number")
	entries['G.LOACTION_ADDRESS'].insert(0,"Gh-post/Town/Region")
	entries['RELATIONSHIP'].insert(0,"How are you related to the persone?")
	entries['BANK'].insert(0,"name of bank")
	entries['ACCOUNT_NUMBER'].insert(0,"Guarantor's account number")
	entries['ACCOUNT_NAME'].insert(0,"Account's name")
	entries['BRANCH'].insert(0,"Bank's branch")
	return entries


# APPLY LOAN FORMS and interface called by apply loan button
def applyloan(win, Lnform_field):
	global applyloanwn
	applyloanwn=tk.Tk()
	applyloanwn.geometry("900x500")
	applyloanwn.title("Credit Amount")
	applyloanwn.configure(bg="powder blue")

	Tops=tk.Frame(applyloanwn,width=600,height=500,bd=8,bg="powder blue")
	Tops.pack(side=tk.TOP)
	l_title=tk.Label(Tops,text="Efiekuma Holdings",relief="raised",fg="white",bg="blue",justify="center",anchor="center")

	l_title.config(font=("Courier","50","bold"))
	l_title.pack(side='top')
	l_title2=tk.Label(Tops,text="Loan Application",justify="center")
	l_title2.config(font=("Courier","20","bold"))
	l_title2.pack(side="bottom")
	entries = {}
	
	for field in Lnform_field:
		print(field)
		row = tk.Frame(applyloanwn,width=600,height=100,bg="powder blue")
		row.pack(side=tk.TOP)
        
        # **********Label Widget****************
		inputV=tk.Label(row,width=15,text=field +": ",font=('arial',16,'bold'),bd=20,fg="black",bg="powder blue")
		inputV.grid(row=0,column=0)
        
        # # **********Entry Widget****************
		ent = tk.Entry(row,font=('arial',14),bd=16,width=22,justify='left')
		ent.grid(row=0,column=1)
		entries[field] = ent
  
	#calling submit function
	button_fr=tk.Frame(applyloanwn,width=300,height=250,bd=8,bg="powder blue")
	button_fr.pack(side='bottom',ipadx=5,ipady=5)
	b=tk.Button(button_fr,text="proceed",relief="raised",bd=8,font=('arial',16,'bold'),bg="powder blue",command=lambda:proceed(applyloanwn,entries))
	b.pack(side="right",padx=10,ipadx=10)
	applyloanwn.bind("<Return>",lambda x:proceed(applyloanwn,entries))
 
	#calling calucalte function
	b=tk.Button(button_fr,text="Calculate",relief="raised",bd=8,font=('arial',16,'bold'),bg="powder blue",command=lambda:calculate(entries))
	b.pack(side="right",padx=10,ipadx=10)
	applyloanwn.bind("<Return>",lambda x:calculate(entries))
	# state='disabled'
	entries['ClientId'].insert(0,c_id)
	entries['ClientId'].configure(state='disabled')
	entries['Gurantor name'].insert(0,'Linos Nouwoto')
	entries['Amount'].insert(0,2000)
	entries['Period'].insert(0,2)
	return entries


# proceed Button in Applyloan function call this when click
def proceed(win,entries):
	global loan_info,gurantorname
	gurantorname = entries['Gurantor name'].get()
	try:
		print(loan_info)
		loan_info = ((entries['ClientId'].get()),
					(entries['Gurantor name'].get()),
                    (float(entries['Amount'].get())),
                    int(entries['Period'].get()),
                    )
	except Exception as e:
		print('Invalid value entered',e)
	try:  
		gurantor_info(win, GUARANTORS) #win parameter from proceed parameter(applyloanwn)
		applyloanwn.destroy()
	except Exception as e:
		print('Guarantor error',e)


#inside apply loan to submit application to db
def submit(Master,entries):
	try:
		gurantor_info = ((entries['G.FULL_NAME'].get()),
					(entries['G.EMAIL'].get()),
                    (int(entries['G.PHONE'].get())),
                    (entries['G.LOACTION_ADDRESS'].get()),
                    (entries['RELATIONSHIP'].get()),
                    (entries['BANK'].get()),
                    (entries['ACCOUNT_NUMBER'].get()),
                    (entries['ACCOUNT_NAME'].get()),
                    (entries['BRANCH'].get())
                    )

	except Exception as e:
		print('Invalid value entered',e)
	try:
		conn = cx_Oracle.connect('Linos/Linos2020@//localhost:1521/xe')
	except  Exception as e:
		print("Error while Connecting to database",e)
	else:
		try:
			c = conn.cursor()
			var = '''
			INSERT INTO Loan_Applications(CLIENT_ID,GURANTOR_FULL_NAME,AMOUNT_REQUESTED,LOAN_TENOR) values(:1,:2,:3,:4)
					'''
			var1 = '''
			INSERT INTO GUARANTORS(FULL_NAME,EMAIL,PHONE,LOACTION_ADDRESS,RELATIONSHIP,BANK,ACCOUNT_NUMBER,ACCOUNT_NAME,BRANCH  ) values(:1,:2,:3,:4,:5,:6,:7,:8,:9)
				'''
			c.execute(var,loan_info)
			c.execute(var1,gurantor_info)
		except Exception as e:
			print('Error in inserting data',e)
			messagebox.showinfo("Error","Invalid Credentials\nPlease try again.")
			# f2.destroy()
			Master.destroy()
		else:
			# if entries['ClientId'].get != c_id:
					# print('Invalid username')
			# else:
			messagebox.showinfo("Successful",'Client Id: '+str(loan_info[0])+'\n'
                       						'Amount Requested: '+str(loan_info[2])+'\n'
                       						'Duration: '+str(loan_info[3])+'\n')
	
			print('row inserted')
			conn.commit()
			Master.destroy()
			# win.destroy()       
	finally:
		c.close()
		conn.close()
		print(loan_info)
		print(gurantor_info)
		# Master.destroy()



# This function get info from applyloan form and calculate the loan interest and repayment_amount,called by calcute button inside applyloan func
def calculate(entries):
    win = tk.Tk()
    win.title("Linos")
    
    f2=tk.Frame(win,width=300,height=700,bd=8,bg="powder blue")
    f2.pack(side=tk.RIGHT)
    
    global frame
    try:
        rate = 0.1
        rate1 = '10% /mon'
        loan_amt = float(entries['Amount'].get())
        per =  float(entries['Period'].get())
        int_amt = rate * loan_amt
        rep_amt = int_amt + loan_amt
        print('Interest on Loan: '+ str(int_amt))
        print('Repayment Amount: '+ str(rep_amt))
        loanslip=tk.Label(f2,text='Loan details',font=('arial',21,'bold'),fg="red",bg="powder blue")
        loanslip.grid(row=0,column=0)
        
        txtloan_details =tk.Text(f2,height=22,width=34,bd=16,font=('arial',13,'bold'),fg="green",bg="powder blue")
        txtloan_details.grid(row=1,column=0)
        
        txtloan_details.insert(tk.END,'\t'+'**********************'+'\n')
        txtloan_details.insert(tk.END,"principal loan:\t"+ '\t\t'+ str('%.2f'%loan_amt)+'\n')
        txtloan_details.insert(tk.END,"Duration in months:\t"+'\t\t' +str('%i'%per)+'\n')
        txtloan_details.insert(tk.END,"Interest rate:\t"+'\t\t'+ str('%.2f'%rate)+'\n')
        txtloan_details.insert(tk.END,"Interest rate:\t"+'\t\t'+(rate1)+'\n')
        txtloan_details.insert(tk.END,"Interest Amount:\t"+ '\t\t'+str('%.2f'%int_amt)+'\n')
        txtloan_details.insert(tk.END,"repayment_amount:\t"+ '\t\t'+str('%.2f'%rep_amt)+'\n')
    except Exception as e:
        print('Invalid value',e)
        feedback=tk.Label(f2,text='Loan details',font=('arial',21,'bold'),fg="red",bg="powder blue")
        feedback.grid(row=0,column=0)
        
        txterror_feedback =tk.Text(f2,height=22,width=34,bd=16,font=('arial',13,'bold'),fg="green",bg="powder blue")
        txterror_feedback.grid(row=1,column=0)
        txterror_feedback.insert(tk.END,'You did not enter a valid value.'+'\n')
        txterror_feedback.insert(tk.END,'Please check and enter a valid value.'+'\n')



'''check Transaction history function'''
def myloan_hist():
	disp_wn=tk.Tk()
	disp_wn.geometry("900x600")
	disp_wn.title("Transaction History")
	disp_wn.configure(bg="powder blue")

	l_title=tk.Message(disp_wn,text="Efiekuma Holdings",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="blue",justify="center",anchor="center")
	l_title.config(font=("Courier","50","bold"))
	l_title.pack(side="top")

	fr1=tk.Frame(disp_wn,bg="powder blue")
	fr1.pack(side="top",anchor="center")
	l1=tk.Message(fr1,text="Your Transaction History:",padx=300,pady=20,width=1000,bg="blue",fg="orange",relief="raised")
	l1.pack(side="top")
	# l1.grid(row=0,column=0)
 
	title_row=tk.Frame(fr1,padx=160,bg="powder blue")
	title_row.pack(side="top",anchor="w")
	c1=tk.Message(title_row,text="Date",font=('Arial',12,'bold'),padx=30,pady=5,width=250,bg="light blue",fg="orange")
	c1.grid(row=0,column=0)
 
	cs=tk.Message(title_row,text=" ",font=('Arial',12,'bold'),padx=30,pady=5,width=250,bg="light blue",fg="orange")
	cs.grid(row=0,column=1)
 
	c2=tk.Message(title_row,text="LoanType",font=('Arial',12,'bold'),padx=30,pady=5,width=250,bg="light blue",fg="orange")
	c2.grid(row=0,column=2)
	c3=tk.Message(title_row,text="Amount",font=('Arial',12,'bold'),padx=30,pady=5,width=250,bg="light blue",fg="orange")
	c3.grid(row=0,column=3)
	c4=tk.Message(title_row,text="Duration",font=('Arial',12,'bold'),padx=15,pady=5,width=200,bg="light blue",fg="orange")
	c4.grid(row=0,column=4)
	
	cs=tk.Message(title_row,text="  ",font=('Arial',12,'bold'),pady=5,width=250,bg="light blue",fg="orange")
	cs.grid(row=0,column=5)
 
	c5=tk.Message(title_row,text="status",font=('Arial',12,'bold'),padx=15,pady=5,width=200,bg="light blue",fg="orange")
	c5.grid(row=0,column=6)
	# c1.pack(side="right")
 
	fr2=tk.Frame(disp_wn)
	fr2.pack(side="top")
	
	try:
		conn = cx_Oracle.connect('Linos/Linos2020@//localhost:1521/xe')
	except  Exception as e:
		print("Error while connecting to database",e)
	else:
		try:
			c = conn.cursor()
			var = '''
			SELECT TO_CHAR(APPLYDATE,'DD/MM/YY HH24:MI'),LOAN_TYPE,AMOUNT_REQUESTED,LOAN_TENOR,LOAN_STATUS FROM Loan_Applications where CLIENT_ID = :c_id
			'''
			c.execute(var,{'c_id':c_id})
			res = c.fetchall()
			print(res)
			totalrow=len(res)
			totalcols=len(res[0])
			rows = tk.Frame(fr1,padx=160,bg="powder blue")
			rows.pack(side="top",anchor="w")
			for R in range(totalrow):
				for C in range(totalcols):

					l1=tk.Entry(rows,width=15,bd=1,font=('courier',11),bg="powder blue",fg='black')
					l1.grid(row=R, column=C,sticky='w')
					l1.insert(tk.END, res[R][C])
					l1.configure(state='disabled')

		except Exception as e:
			print('Error in selecting data data',e)
		else:
			print('rows fetched successfully')
			conn.commit()
	finally:
		c.close()
		conn.close() 
  
	#QUIT BUTTON
	b=tk.Button(disp_wn,bd=15,width=15,bg="powder blue",text="Quit",relief="raised",command=disp_wn.destroy)
	b.pack(side="top")
	

#checking loan schedule function
def myloan_schedule():
	disp_wn=tk.Tk()
	disp_wn.geometry("900x600")
	disp_wn.title("Transaction History")
	disp_wn.configure(bg="powder blue")
	# fr1=tk.Frame(disp_wn,bg="blue")
	l_title=tk.Message(disp_wn,text="Efiekuma Holdings",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="blue",justify="center",anchor="center")
	l_title.config(font=("Courier","50","bold"))
	l_title.pack(side="top")

	fr1=tk.Frame(disp_wn,bg="powder blue")
	fr1.pack(side="top",anchor="center")
	l1=tk.Message(fr1,text="Your Transaction History:",padx=300,pady=20,width=1000,bg="blue",fg="orange",relief="raised")
	l1.pack(side="top")
	
 
	title_row=tk.Frame(fr1,padx=50,bg="powder blue")
	title_row.pack(side="top",anchor="center")
 


	c1=tk.Message(title_row,text="RepaymentDate",font=('Arial',12,'bold'),padx=10,pady=5,width=90,bg="light blue",fg="orange")
	c1.grid(row=0,column=1)
 
	c2=tk.Message(title_row,text="MonthlyRepays",font=('Arial',12,'bold'),padx=10,pady=5,width=70,bg="light blue",fg="orange")
	c2.grid(row=0,column=2)


	c3=tk.Message(title_row,text="AmountPaid",font=('Arial',12,'bold'),padx=10,pady=5,width=100,bg="light blue",fg="orange")
	c3.grid(row=0,column=3)

 
	c4=tk.Message(title_row,text="DatePaid",font=('Arial',12,'bold'),padx=10,pady=5,width=100,bg="light blue",fg="orange")
	c4.grid(row=0,column=4)
	

 
	fr2=tk.Frame(disp_wn)
	fr2.pack(side="top")
	
	try:
		conn = cx_Oracle.connect('Linos/Linos2020@//localhost:1521/xe')
	except  Exception as e:
		print("Error while connecting to database",e)
	else:
		try:
			c = conn.cursor()
			var = '''
				SELECT TO_CHAR(REPAYMENT_DATE,'Mon fmDD,YYYY')REPAYMENT_DATE,MONTHLY_REPAY,AMOUNT_PAID,NVL(TO_CHAR(DATE_PAID, 'fmDD Month YYYY'),'-') DATE_PAID
				from loan_schedule where CLIENT_ID =:CLIENT_ID
				order BY 1 desc
				'''
			c.execute(var,{'CLIENT_ID':c_id})
			res = c.fetchall()
			print(res)
			totalrow=len(res)
			totalcols=len(res[0])
			rows = tk.Frame(fr1,padx=50,bg="powder blue")
			rows.pack(side="top",anchor="center")
			for R in range(totalrow):
				for C in range(totalcols):

					l1=tk.Entry(rows,width=11,bd=1,font=('courier',11),bg="powder blue",fg='black')
					# l1.grid(row=0,column=0,)
					l1.grid(row=R, column=C,sticky='w')
					l1.insert(tk.END, res[R][C])
					l1.configure(state='disabled')
		except Exception as e:
			print('Error in selecting data data',e)
		else:
			print('rows fetched successfully')
			conn.commit()
	finally:
		c.close() 
		conn.close() 
  
	#QUIT BUTTON
	b=tk.Button(disp_wn,bd=15,width=15,bg="powder blue",text="Quit",relief="raised",command=disp_wn.destroy)
	b.pack(side="top")


'''Check Loan Statement'''
def myloan_statement():
	disp_wn=tk.Tk()
	disp_wn.geometry("1000x600")
	disp_wn.title("Transaction History")
	disp_wn.configure(bg="powder blue")
	# fr1=tk.Frame(disp_wn,bg="blue")
	l_title=tk.Message(disp_wn,text="Efiekuma Holdings",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="blue",justify="center",anchor="center")
	l_title.config(font=("Courier","50","bold"))
	l_title.pack(side="top")

	fr1=tk.Frame(disp_wn,bg="powder blue")
	fr1.pack(side="top",anchor="center")
	l1=tk.Message(fr1,text=c_id +" Current Loans Statement as at\n\t"+datestr,padx=300,pady=20,width=1000,bg="white",relief="raised",font=('Arial',12,'bold'))
	l1.pack(side="top")
	# l1.grid(row=0,column=0)
 
	title_row=tk.Frame(fr1,padx=80,bg="powder blue")
	title_row.pack(side="top",anchor="w")
	c1=tk.Message(title_row,text="Loan Number",font=('Arial',12,'bold'),pady=5,width=200,bg="light blue",fg="orange")
	c1.grid(row=0,column=0)
 
	c1=tk.Message(title_row,text="DateDisbursed",font=('Arial',12,'bold'),pady=5,width=170,bg="light blue",fg="orange")
	c1.grid(row=0,column=1)
 

 
	c2=tk.Message(title_row,text="Pri. Amount",font=('Arial',12,'bold'),pady=5,width=200,bg="light blue",fg="orange")
	c2.grid(row=0,column=3)

	c3=tk.Message(title_row,text="Interest",font=('Arial',12,'bold'),pady=5,width=200,bg="light blue",fg="orange")
	c3.grid(row=0,column=4)
 
	c3=tk.Message(title_row,text="Repayments",font=('Arial',12,'bold'),padx=60,pady=5,width=190,bg="light blue",fg="orange")
	c3.grid(row=0,column=5)
 
	c3=tk.Message(title_row,text="Balance",font=('Arial',12,'bold'),pady=5,width=200,bg="light blue",fg="orange")
	c3.grid(row=0,column=6,sticky='e') 
 
	c4=tk.Message(title_row,text="LoanEnd Date",font=('Arial',12,'bold'),pady=5,width=200,bg="light blue",fg="orange")
	c4.grid(row=0,column=7)
	
	cs=tk.Message(title_row,text="  ",font=('Arial',12,'bold'),width=250,bg="light blue",fg="orange")
	cs.grid(row=0,column=8)
 
	fr2=tk.Frame(disp_wn)
	fr2.pack(side="top")
	
	try:
		conn = cx_Oracle.connect('Linos/Linos2020@//localhost:1521/xe')
	except  Exception as e:
		print("Error while connecting to database",e)
	else:
		try:
			c = conn.cursor()
			var = '''
			SELECT Loan_num,TO_CHAR(Date_Disbursed,'Mon fmDD,YYYY') as Date_Disbursed,Amount,Interest_Amount,Total_Amount_paid AS Payments,Balance,TO_CHAR(REPAYMENT_DATE,'Mon fmDD,YYYY') asRepayment_date
			from ACTUAL_RECEIVABLE_DETAIL
			WHERE CLIENT_ID=:CLIENT_ID
			'''
			c.execute(var,{'CLIENT_ID':c_id})
			res = c.fetchall()
			print(res)
			totalrow=len(res)
			totalcols=len(res[0])
			rows = tk.Frame(fr1,padx=80,bg="powder blue")
			rows.pack(side="top",anchor="center")
			for R in range(totalrow):
				for C in range(totalcols):

					l1=tk.Entry(rows,width=13,bd=1,font=('courier',11),bg="powder blue",fg='black')
					# l1.grid(row=0,column=0,)
					l1.grid(row=R, column=C,sticky='w')
					l1.insert(tk.END, res[R][C])
					l1.configure(state='disabled')
	
		except Exception as e:
			print('Error in selecting data data',e)
		else:
			print('rows fetched successfully')
			conn.commit()
	finally:
		c.close()
		conn.close() 
  
	#QUIT BUTTON
	b=tk.Button(disp_wn,bd=15,width=15,bg="powder blue",text="Quit",relief="raised",command=disp_wn.destroy)
	b.pack(side="top")



'''Inside account'''
def logged_in_menu(cid,password):
	rootwn=tk.Tk()
	rootwn.geometry("1300x500")
	rootwn.title("Efiekuma Holdings-"+cid) # cid to be change
	rootwn.configure(background='powder blue')
	win=tk.Frame(rootwn)
	fr1=tk.Frame(rootwn)
	fr1.pack(side="top")
	l_title=tk.Message(rootwn,text="Efiekuma Holdings",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="blue",justify="center",anchor="center")
	l_title.config(font=("Courier","50","bold"))
	l_title.pack(side="top")
	label=tk.Label(text="Logged in as: "+cid,relief="raised",bg="blue",fg="white",anchor="e",justify="center")
	label.pack(side="top")
 
	
 
	img2=tk.PhotoImage(file="Apply_LoanBtn.gif")
	myimg2=img2.subsample(1,1)
	img3=tk.PhotoImage(file="Loan_statement.gif")
	myimg3=img3.subsample(1,1)
	img4=tk.PhotoImage(file="CHECK_loan_schedule.gif")
	myimg4=img4.subsample(1,1)
	img5=tk.PhotoImage(file="View_loan_HistoryBtn.gif")
	myimg5=img5.subsample(1,1)
 
 
	#Apply Loan button
	b2=tk.Button(image=myimg2,command=lambda: applyloan(win,Lnform_field))
	b2.image=myimg2
	
	# loan statement button
	b3=tk.Button(image=myimg3,command=lambda: myloan_statement())
	b3.image=myimg3
 
	#  Loan schedule button
	b4=tk.Button(image=myimg4,command=lambda: myloan_schedule())
	b4.image=myimg4
 
	#  display loan history button
	b5=tk.Button(image=myimg5,command=lambda: myloan_hist())
	b5.image=myimg5
	 
	# log out button
	img6=tk.PhotoImage(file="logout.gif")
	myimg6=img6.subsample(2,2)
	
	
	b6=tk.Button(image=myimg6,relief="raised",command=lambda: logout(rootwn))
	b6.image=myimg6

	
	b2.place(x=100,y=150)
	b3.place(x=100,y=220)
	b4.place(x=900,y=150)
	b5.place(x=900,y=220)
	b6.place(x=600,y=400)

	
def logout(master):
	messagebox.showinfo("Logged Out","You Have Been Successfully Logged Out!!")
	master.destroy()
	Main_Menu()



'''Log in frame/page'''
def log_in(master):
	master.destroy()
	loginwn=tk.Tk()
	loginwn.geometry("700x400")
	loginwn.title("Log in")
	loginwn.configure(bg="powder blue")
	fr1=tk.Frame(loginwn,bg="blue")
	l_title=tk.Message(loginwn,text="Efiekuma Holdings",relief="raised",width=700,padx=400,pady=0,fg="white",bg="blue",justify="center",anchor="center")
	l_title.config(font=("Courier","50","bold"))
	l_title.pack(side="top")

	form_structure =tk.Frame(relief=tk.RAISED,borderwidth=5)
	form_structure.pack()

	l1=tk.Label(master=form_structure,text="Client Id:",font=('arial',14,'bold'))
	ClientId=tk.Entry(master=form_structure,width=10,bd=8,font=('arial',16))
	l1.grid(row=0,column=0)
	ClientId.grid(row=0,column=1,sticky='e')
	# ClientId.insert(0, 'Maxone')
 
	l2=tk.Label(master=form_structure,text="Password:",font=('arial',14,'bold'))
	password_box=tk.Entry(master=form_structure,show='*',width=10,bd=8,font=('arial',16))
	l2.grid(row=1,column=0)
	password_box.grid(row=1,column=1,sticky='e')
	# password_box.insert(0, '8024max')


	b=tk.Button(loginwn,relief="raised",bd=8,bg="blue",text="Log in",command=lambda: submitact(loginwn,ClientId.get().strip(),password_box.get().strip()))
	b.pack(side="top")
 
	b1=tk.Button(text="HOME",width=30,relief="raised",font=('arial',12,'bold'),bg="blue",fg="white",bd=8,command=lambda: home_return(loginwn))
	b1.pack(side="bottom")
 
 
	loginwn.bind("<Return>",lambda x:submitact(loginwn,ClientId.get().strip(),password_box.get().strip()))
	return


'''Fuction to verify log in'''
def submitact(master,cid,password):
	global c_id
	c_id = cid
	pword = password
	try:
		conn = cx_Oracle.connect('Linos/Linos2020@//localhost:1521/xe')
	except  Exception as e:
		print("Error while connecting to database",e)
	else:
		try:
			c = conn.cursor() #open the database
			data =  [c_id,pword]
			try:
				c.callproc("LOGIN",data)
			except Exception as e:
				print("Linos",e)
				messagebox.showinfo("Error","Invalid Credentials\nPlease check Clientid and password and\ntry again.",parent=master)
			else:
				print('Function created successfully')
				master.destroy()
				logged_in_menu(c_id,pword)
				conn.commit()
		except Exception as e:
			print('Error calling Function function',e)
		# else:
		# 	print('Function created successfully')
		# 	master.destroy()
		# 	logged_in_menu(c_id,pword)
		# 	conn.commit()
		finally:
			c.close()
	finally:
		return c_id
		conn.close() 
  

'''Create account function'''
'''Scroll class'''
class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self,width=600,height=500,confine=True,cursor='arrow')
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all",)
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame,anchor="center")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left",fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


'''Function to create loan application form'''
def Create():

	crwn=tk.Tk()
	crwn.title("Create Account")

	Tops=tk.Frame(crwn,width=300,height=500,bd=5, background="powder blue")
	Tops.pack(side=tk.TOP)

	l_title=tk.Label(Tops,text="Efiekuma Holdings",relief="raised",fg="white",bg="blue",justify="center")
	l_title.config(font=("Courier","45","bold"))
	l_title.pack(side="top")
	l_title2=tk.Label(Tops,text="Sign up to Create New Account",justify="center")
	l_title2.config(font=("Courier","20","bold"))
	l_title2.pack(side="bottom")
	entries = {} # all values
	frame = ScrollableFrame(crwn,relief=tk.RAISED)
	for field in kyc:
		# print(field)
		row = tk.Frame(frame.scrollable_frame,relief=tk.RAISED,width=500,height=200,bd=2,bg="powder blue")

		row.pack()


        # **********Label Widget****************
		# ttk.Label(frame.scrollable_frame, text=field).pack()
		inputV=ttk.Label(row,text=field +": ",font=('arial',12,'bold'),width=20,justify='left')
		inputV.grid(row=0,column=0)
        
        # # **********Entry Widget****************
		ent = ttk.Entry(row,font=('arial',16),justify='left',width=30) #,width=10
		# ent.pack(side=tk.RIGHT,expand=tk.YES,fill=tk.X) #,expand=tk.YES
		ent.grid(row=0,column=1)
		entries[field] = ent   
		# ent.insert(0,'Type here')


	frame.pack()
 

	'''Button start'''
	b=tk.Button(frame.scrollable_frame, text='Submit',padx=10,pady=10,bd=5,font=('arial',16,'bold'),
            command=(lambda : getcreateaccount(crwn,entries)))  
	
	b.pack(side="top")

	crwn.bind("<Return>",lambda x:getcreateaccount(crwn,entries['ClientId    '].get().strip(),entries['FirstName'].get().strip(),entries['Email       '].get().strip()))
	return entries


'''Creating account-function Get value from entry and insert into database'''
def getcreateaccount(master,entries):
	global account_info
   
	try:
		print(account_info)
		account_info = ((entries['FIRSTNAME'].get()),
						(entries['LASTNAME'].get()),
						(entries['LOCATION_ADDRESS'].get()),
      					(entries['DIGITAL_ADDRESS'].get()),
           				(entries['CONTACT_NUMBER'].get()),
               			(entries['EMAIL'].get()),
						(entries['GENDER'].get()),
      					(entries['AGE'].get()),
           				(entries['MARITAL_STATUS'].get()),
               			(entries['NAME_OF_SPOUSE'].get()),
						(entries['OCCUPATION'].get()),
      					(entries['EMPLOYER'].get()),
           				(entries['ANNUALSALARY'].get()),
						(entries['CLIENTID'].get()),
      					(entries['PASSWORD'].get()),
           				(entries['RE_TYPE_PASSWORD'].get()))
	except Exception as e:
			print('Invalid value entered',e)
        
	try:
		conn = cx_Oracle.connect('Linos/Linos2020@//localhost:1521/xe')
	except  Exception as e:
		print("Error while inserting data",e)
	else:
		try:
			print(account_info)
			c = conn.cursor()
			var = '''
            INSERT INTO KYC(FIRSTNAME,LASTNAME,LOCATION_ADDRESS,DIGITAL_ADDRESS,CONTACT_NUMBER,EMAIL,GENDER,AGE,MARITAL_STATUS,NAME_OF_SPOUSE,OCCUPATION,EMPLOYER,ANNUALSALARY,CLIENT_ID,PASS_WORD,RE_TYPE_PASSWORD)  values(:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15,:16)
            '''
			c.execute(var,account_info)
		except Exception as e:
			print('Error in inserting data',e)
			messagebox.showinfo("Error","Invalid Credentials\nPlease try again.",parent=master)
		else:
			messagebox.showinfo("Details","Account created\nLog in with your username\nYour username is:"+str(entries['CLIENTID'].get()))
			print('row inserted')
			conn.commit()
            
	finally:     
		print('Linos')
		c.close()
		conn.close()
	return


def Main_Menu():
	global datestr
	rootwn=tk.Tk()
	rootwn.geometry("1300x700")
	rootwn.title("Efiekuma Holdings")
	rootwn.configure(background='powder blue')
 
	fr1=tk.Frame(rootwn)
	fr1.pack(side="top")
	bg_image = tk.PhotoImage(file ="Publication2.gif")
	x = tk.Label (image = bg_image)
	x.place(y=200, x= 0)
 
	l_title=tk.Message(text="LOAN MANAGEMENT\n SYSTEM",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="blue",justify="center",anchor="center")
	l_title.config(font=("Courier","50","bold"))
	l_title.pack(side="top")
	imgc1=tk.PhotoImage(file="new.gif")
	imglo=tk.PhotoImage(file="login.gif")
	imgc=imgc1.subsample(2,2)
	imglog=imglo.subsample(2,2)

	b1=tk.Button(image=imgc,command=Create)
	b1.image=imgc
	b2=tk.Button(image=imglog,command=lambda: log_in(rootwn))
	b2.image=imglog
	img6=tk.PhotoImage(file="drawButton.png")
	myimg6=img6.subsample(2,2)

	b6=tk.Button(image=myimg6,command=rootwn.destroy)
	b6.image=myimg6
	
	b1.place(x=800,y=300)
	b2.place(x=800,y=200)	
	b6.place(x=920,y=400)

	rootwn.mainloop()
def Create():
    
	crwn=tk.Tk()
	crwn.title("Create Account")

	Tops=tk.Frame(crwn,width=300,height=500,bd=5, background="powder blue")
	Tops.pack(side=tk.TOP)

	l_title=tk.Label(Tops,text="Efiekuma Holdings",relief="raised",fg="white",bg="blue",justify="center")
	l_title.config(font=("Courier","45","bold"))
	l_title.pack(side="top")
	l_title2=tk.Label(Tops,text="Sign up to Create New Account",justify="center")
	l_title2.config(font=("Courier","20","bold"))
	l_title2.pack(side="bottom")
	entries = {} # all values
	frame = ScrollableFrame(crwn,relief=tk.RAISED)
	for field in kyc:
		# print(field)
		row = tk.Frame(frame.scrollable_frame,relief=tk.RAISED,width=500,height=200,bd=2,bg="powder blue")

		row.pack()


        # **********Label Widget****************
		# ttk.Label(frame.scrollable_frame, text=field).pack()
		inputV=ttk.Label(row,text=field +": ",font=('arial',12,'bold'),width=20,justify='left')
		inputV.grid(row=0,column=0)
        
        # # **********Entry Widget****************
		ent = ttk.Entry(row,font=('arial',16),justify='left',width=30) #,width=10
		# ent.pack(side=tk.RIGHT,expand=tk.YES,fill=tk.X) #,expand=tk.YES
		ent.grid(row=0,column=1)
		entries[field] = ent   
		# ent.insert(0,'Type here')


	frame.pack()
 

	'''Button start'''
	b=tk.Button(frame.scrollable_frame, text='Submit',padx=10,pady=10,bd=5,font=('arial',16,'bold'),
            command=(lambda : getcreateaccount(crwn,entries)))  
	
	b.pack(side="top")

	crwn.bind("<Return>",lambda x:getcreateaccount(crwn,entries['ClientId    '].get().strip(),entries['FirstName'].get().strip(),entries['Email       '].get().strip()))
	return entries

							# LOAN Payement

Main_Menu()