import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from time import gmtime, strftime
import cx_Oracle
from datetime import datetime

now = datetime.now()
datestr = now.strftime("%d-%b-%Y %I:%M:%S")

print(datestr) 

kyc=('FIRSTNAME','LASTNAME','LOCATION_ADDRESS','DIGITAL_ADDRESS','CONTACT_NUMBER','EMAIL','GENDER','AGE','MARITAL_STATUS','NAME_OF_SPOUSE','OCCUPATION','EMPLOYER','ANNUALSALARY','CLIENTID','PASSWORD','RE_TYPE_PASSWORD') # create account

GUARANTORS=('G.FULL_NAME','G.EMAIL','G.PHONE','G.LOACTION_ADDRESS','RELATIONSHIP','BANK','ACCOUNT_NUMBER','ACCOUNT_NAME','BRANCH')

payment_fields=('LOAN NUMBER','CLIENT ID','AMOUNT PAID','DATE PAID')

Lnform_field = ('ClientId','Gurantor name','Amount','Period') #apply loan table

loanschedule = ('Loan number','Client id','Loan Duration')

account_info = () 
row = []
field = []
loan_info = ()


#validate pin
def home_return(master):
	master.destroy()
	Main_Menu()


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
	entries['G.FULL_NAME'].insert(0,gurantorname)
	entries['G.FULL_NAME'].configure(state='disabled')
	entries['G.EMAIL'].insert(0,"Linos@gmail")
	entries['G.PHONE'].insert(0,"543309781")
	entries['G.LOACTION_ADDRESS'].insert(0,"Syi")
	entries['RELATIONSHIP'].insert(0,"Bro")
	entries['BANK'].insert(0,"Ecobank")
	entries['ACCOUNT_NUMBER'].insert(0,1234586)
	entries['ACCOUNT_NAME'].insert(0,"Linos")
	entries['BRANCH'].insert(0,"Sunyani")
	return entries


'''Loan Repayment fields'''
def payloan(win, payLnFields):
	global payloanwn,datestr
	payloanwn=tk.Tk()
	payloanwn.geometry("900x500")
	payloanwn.title("Credit Amount")
	payloanwn.configure(bg="powder blue")
	Tops=tk.Frame(payloanwn,width=600,height=500,bd=8,bg="powder blue")
	Tops.pack(side=tk.TOP)
	l_title=tk.Label(Tops,text="Efiekuma Holdings",relief="raised",fg="white",bg="blue",justify="center",anchor="center")
	l_title.config(font=("Courier","50","bold"))
	l_title.pack(side='top')
	l_title2=tk.Label(Tops,text="Loan repayment",justify="center")
	l_title2.config(font=("Courier","20","bold"))
	l_title2.pack(side="bottom")
	entries = {}
	for field in payment_fields:
		print(field)
		row = tk.Frame(payloanwn,width=600,height=100,bg="powder blue")
		row.pack(side=tk.TOP)
        
        # **********Label Widget****************
		inputV=tk.Label(row,width=15,text=field +": ",font=('arial',16,'bold'),bd=20,fg="black",bg="powder blue")
		inputV.grid(row=0,column=0)
        
        # # **********Entry Widget****************
		ent = tk.Entry(row,font=('arial',14),bd=16,width=22,justify='left')
		ent.grid(row=0,column=1)
		entries[field] = ent
  
	#calling submit function
	button_fr=tk.Frame(payloanwn,width=300,height=250,bd=8,bg="powder blue")
	button_fr.pack(side='bottom',ipadx=5,ipady=5)
	b=tk.Button(button_fr,text="PAY",relief="raised",bd=8,font=('arial',16,'bold'),bg="powder blue",command=lambda:submitpay(payloanwn,entries))
	b.pack(side="right",padx=10,ipadx=10)
	payloanwn.bind("<Return>",lambda x:submitpay(payloanwn,entries))
 
	# state='disabled'
	entries['LOAN NUMBER'].insert(0,0)
	entries['CLIENT ID'].insert(0,'Enter Client\'s Id')
	entries['AMOUNT PAID'].insert(0,0)
	entries['DATE PAID'].insert(0,datestr)
	return entries



'''APPLY LOAN Fields'''
def applyloan(win, Lnform_field):
	global applyloanwn,Loantype
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
		inputV=tk.Label(row,width=15,text=field +": ",font=('arial',16,'bold'),bd=5,fg="black",bg="powder blue")
		inputV.grid(row=0,column=0)
        
        # # **********Entry Widget****************
		ent = tk.Entry(row,font=('arial',14),width=22,justify='left')
		ent.grid(row=0,column=1)
		entries[field] = ent

	
	typelabel= tk.Label(row, text = "Loan Type: ", 
          font=('arial',16,'bold'),width=15,bg="powder blue")
	typelabel.grid(row = 1,column = 0) #(column = 0, row = 5, padx = 10, pady = 25) 
	Loantype = ttk.Combobox(row,font=('arial',14),width = 20)
	Loantype.grid(row = 1,column = 1) 
	Loantype['values'] = ('Personal loan',  
                          'Education loan', 
                          'Special loan' )
	# return Loantype
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
	entries['Amount'].insert(0,2000)
	entries['Period'].insert(0,2)
	return entries


'''proceed Button in Applyloan function call this when clicked.
it get the values in the Applyloan field and store it in the loan_info
and again calls the gurantor_info Function
'''
def proceed(win,entries):
	global loan_info,gurantorname
	gurantorname = entries['Gurantor name'].get()
	try:#('G.FULL_NAME','G.EMAIL','G.PHONE','G.LOACTION_ADDRESS','RELATIONSHIP')
		
		print(loan_info)
		loan_info = ((entries['ClientId'].get()),
					(entries['Gurantor name'].get()),
                    (float(entries['Amount'].get())),
                    int(entries['Period'].get()),
                    Loantype.get()
                    )
	except Exception as e:
		print('Invalid value entered',e)
	try:  
		print(loan_info)
		gurantor_info(win, GUARANTORS) #win parameter from proceed parameter(applyloanwn)
		applyloanwn.destroy()
	except Exception as e:
		print('Guarantor error',e)



'''when this fn inside gurantor_info is click it submit application to db'''
def submit(Master,entries):
	try:#('G.FULL_NAME','G.EMAIL','G.PHONE','G.LOACTION_ADDRESS','RELATIONSHIP')	
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
#   'BANK','ACCOUNT_NUMBER','ACCOUNT_NAME','BRANCH')
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
			INSERT INTO Loan_Applications(CLIENT_ID,GURANTOR_FULL_NAME,AMOUNT_REQUESTED,LOAN_TENOR,LOAN_TYPE) values(:1,:2,:3,:4,:5)
					'''
			var1 = '''
			INSERT INTO GUARANTORS(FULL_NAME,EMAIL,PHONE,LOACTION_ADDRESS,RELATIONSHIP,BANK,ACCOUNT_NUMBER,ACCOUNT_NAME,BRANCH  ) values(:1,:2,:3,:4,:5,:6,:7,:8,:9)
				'''
			c.execute(var,loan_info)
			c.execute(var1,gurantor_info)
		except Exception as e:
			print('Error in inserting data',e)
			messagebox.showinfo("Error","Invalid Credentials\nPlease try again.")
			Master.destroy()
		else:
			messagebox.showinfo("Successful",'Client Id: '+str(loan_info[0])+'\n'
                       						'Amount Requested: '+str(loan_info[2])+'\n'
                       						'Duration: '+str(loan_info[3])+'\n')
			print('row inserted')
			conn.commit()
			Master.destroy()     
	finally:
		c.close()
		conn.close()
		print(loan_info)
		print(gurantor_info)

'''The calculate fn is called the the calculate buttom in applyloan page'''
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


'''called by pay buttom inside the payment form/page'''
def submitpay(Master,entries):
	try:	
		payment_info = ((entries['LOAN NUMBER'].get()),
      				(entries['CLIENT ID'].get()),
					(int(entries['AMOUNT PAID'].get())),
                    ((entries['DATE PAID'].get())),  
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
			INSERT INTO loan_repayments(Loan_Num,CLIENT_ID,AMOUNT_PAID,DATE_PAID) values(:1,:2,:3,:4)
					'''
			response = messagebox.askokcancel("Confirm payment", "Press OK to Confirm payment\n\tPayment details:\nAre you sure you want to pay "+"GHC"+str(payment_info[1])+".00"+"\nto a client with id "+str(payment_info[0]))
			print(response)
			if response == True:
				c.execute(var,payment_info)
				messagebox.showinfo("Succesful", 'Payment is Successful\ndetail below:\n'
                       						'\nCLIENT ID: '+str(payment_info[0])+'\n'
                       						'AMOUNT PAID: '+str(payment_info[1])+'\n'
                       						'DATE PAID: '+str(payment_info[2])+'\n')
			else:
				messagebox.showinfo("Cancell payment","Payment Cancelled Successful")

		except Exception as e:
			print('Error in inserting data',e)
			messagebox.showinfo("Error","Invalid Credentials\nPlease try again.")
			Master.destroy()
		else:
			print('row inserted')
			conn.commit()
			Master.destroy()      
	finally:
		c.close()
		conn.close()
		print(loan_info)
		print(gurantor_info)

'''Inside account'''
def logged_in_menu(cid,password,jtitle):
	global penfr,win,homefr,rootwn
	rootwn=tk.Tk()
	rootwn.geometry("1300x750")
	rootwn.title("Efiekuma Holdings-"+emp_id) # cid to be change
	rootwn.configure(background='powder blue')
    
	win=tk.Frame(rootwn)
	fr1=tk.Frame(rootwn)
	fr1.pack(side="top")
	l_title=tk.Message(rootwn,text="Efiekuma Holdings \n"+jobtitle,relief="raised",width=2000,padx=600,pady=0,fg="white",bg="blue",justify="center",anchor="center")
	l_title.config(font=("Courier","50","bold"))
	l_title.pack(side="top")

 
	dashboardfr=tk.Frame(rootwn,width=300,bg='powder blue')
	dashboardfr.pack()
    
	label=tk.Label(text="Logged in as: "+cid,relief="raised",bg="blue",fg="white",anchor="center",justify="center")
	label.pack(side="top")
    
	homefr=tk.Frame(rootwn,width=300,bg='powder blue')
	homefr.pack(side='bottom')
    
	penfr=tk.Frame(rootwn)
	penfr.pack(side='top')
 

	#buttons
	homebtn=tk.Button(dashboardfr,text='HOME',bd=5,command=lambda: homepage(),relief="raised")
	homebtn.pack(side='left')
    
	pendingbtn=tk.Button(dashboardfr,text='PENDING LOANS',bd=5,command=lambda:pendingloans(),relief="raised")
	pendingbtn.pack(side='left')
 
	recbtn=tk.Button(dashboardfr,text='ALL RECEIVABLES',bd=5,command=lambda: actual_receivables(),relief="raised")
	recbtn.pack(side='left')
 
	paybtn=tk.Button(dashboardfr,text='PAYMENTS',bd=5,command=lambda: payments(),relief="raised")
	paybtn.pack(side='left')
	# defbtn=tk.Button(dashboardfr,text='DEFAULTER',bd=5,command=lambda: None,relief="raised")
	# defbtn.pack(side='left')
	homepage()
       

def homepage():
    img2=tk.PhotoImage(homefr,file="Apply_LoanBtn.gif")
    myimg2=img2.subsample(1,1)
    img3=tk.PhotoImage(homefr,file="enter payment.gif")
    myimg3=img3.subsample(1,1)
    img5=tk.PhotoImage(homefr,file="View_loan_HistoryBtn.gif")
    myimg5=img5.subsample(1,1)
    imgc1=tk.PhotoImage(homefr,file="new.gif")
    myimgc1=imgc1.subsample(2,2)
    
	
     	#Create Account
    bc=tk.Button(image=myimgc1,command=lambda:Create())
    bc.image=myimgc1
    
    #apply button
    applybtn=tk.Button(image=myimg2,command=lambda: applyloan(win,Lnform_field))
    applybtn.image=myimg2
        
    	#button Enter payment
    b3=tk.Button(image=myimg3,command=lambda: payloan(win,payments))
    b3.image=myimg3
      
    img6=tk.PhotoImage(file="logout.gif")
    myimg6=img6.subsample(2,2)
          
    b6=tk.Button(image=myimg6,relief="raised",command=lambda: logout(rootwn))
    b6.image=myimg6
      
    bc.place(x=500,y=300)  
    applybtn.place(x=100,y=300)
    b3.place(x=900,y=300)
    b6.place(x=600,y=400)


def pendingloans():
	global pen,lnstatus,rows,R,approveres
	pen=tk.Tk()
	pen.geometry("1300x700")
	pen.title("Transaction History")
	pen.configure(bg="powder blue")
	fr1=tk.Frame(pen,bg="blue")
	l_title=tk.Message(pen,text="Efiekuma Holdings",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="blue",justify="center",anchor="center")
	l_title.config(font=("Courier","50","bold"))
	l_title.pack(side="top")

	fr1=tk.Frame(pen,bg="powder blue")
	fr1.pack(side="top",anchor="center")
	l1=tk.Message(fr1,text="Your Transaction History:",padx=200,pady=20,width=1000,bg="blue",fg="orange",relief="raised")
	l1.pack(side="top")
  
    
	title_row=tk.Frame(fr1,padx=160,width=200,bg="powder blue")#padx=500
	title_row.pack(side="top",anchor="w")
	c0=tk.Message(title_row,text="Loan num",font=('Arial',12,'bold'),padx=15,pady=5,width=100,bg="light blue",fg="orange")
	c0.grid(row=0,column=0)
 
	c0=tk.Message(title_row,text="Client id",font=('Arial',12,'bold'),padx=20,pady=5,width=100,bg="light blue",fg="orange")
	c0.grid(row=0,column=1)
 
	# to create space row,column
	cs=tk.Message(title_row,text="",font=('Arial',12,'bold'),padx=10,pady=5,bg="light blue",fg="orange")
	cs.grid(row=0,column=2)
    
	c1=tk.Message(title_row,text="Date",font=('Arial',12,'bold'),padx=15,pady=5,width=100,bg="light blue",fg="orange")
	c1.grid(row=0,column=3)
    
    # space row,column
	cs=tk.Message(title_row,text="",font=('Arial',12,'bold'),padx=30,pady=5,bg="light blue",fg="orange")
	cs.grid(row=0,column=4)
    
	c2=tk.Message(title_row,text="Loan Type ",font=('Arial',12,'bold'),padx=15,pady=5,width=100,bg="light blue",fg="orange")
	c2.grid(row=0,column=5)
	c3=tk.Message(title_row,text=" Amount",font=('Arial',12,'bold'),padx=15,pady=5,width=100,bg="light blue",fg="orange")
	c3.grid(row=0,column=6)

	# space btn Amount duration row,column  
	cs=tk.Message(title_row,text="",font=('Arial',12,'bold'),padx=15,pady=5,bg="light blue",fg="orange")
	cs.grid(row=0,column=7)
 
	c4=tk.Message(title_row,text="Duration",font=('Arial',12,'bold'),padx=15,pady=5,width=100,bg="light blue",fg="orange")
	c4.grid(row=0,column=8)
      
    # space btn duration and status row,column  
	cs=tk.Message(title_row,text="",font=('Arial',12,'bold'),padx=15,pady=5,width=100,bg="light blue",fg="orange")
	cs.grid(row=0,column=9)
    
	c5=tk.Message(title_row,text="status",font=('Arial',12,'bold'),padx=15,pady=5,width=100,bg="light blue",fg="orange")
	c5.grid(row=0,column=10)
        # c1.pack(side="right")
    
	fr2=tk.Frame(pen)
	fr2.pack(side="top")
        
	try:
		conn = cx_Oracle.connect('Linos/Linos2020@//localhost:1521/xe')
	except  Exception as e:
		print("Error while connecting to database",e)
	else:
		try:
			c = conn.cursor()
			var = '''
			SELECT Loan_Num,CLIENT_ID,APPLYDATE,LOAN_TYPE,AMOUNT_REQUESTED,LOAN_TENOR,LOAN_STATUS FROM Loan_Applications where LOAN_STATUS='Pending'
			'''
			c.execute(var)
			res = c.fetchall()
			try:
				totalrow=len(res)
				totalcols=len(res[0])
			except Exception as e:
				print("No data",e)
				l1=tk.Message(fr1,text="No records:",padx=200,pady=20,width=1000,fg="black",relief="raised")
				l1.pack(side="top")
			else:
				rows = tk.Frame(fr1,padx=160,bg="powder blue",width=1000)
				rows.pack(side="top",anchor="center")
				approveres = []
				# partial
				for R in range(totalrow):
					btn=tk.Button(rows,text='Approve',width=8,bd=5,font=('courier',11),bg="green",command=lambda approveres=res[R]:approvalprocess(approveres[0]))
					btn1=tk.Button(rows,text='Disapprove',width=9,bd=5,font=('courier',11),bg="red",command=lambda approveres=res[R]:disapproval(approveres[0]))
					for C in range(totalcols):

						l1=tk.Entry(rows,width=15,bd=1,font=('courier',10),bg="powder blue")
						# l1.grid(row=0,column=0,)
						l1.grid(row=R,column=C,sticky='w')
						l1.insert(tk.END, res[R][C])
						# btn=tk.Button(rows,text='Approve',width=8,bd=5,font=('courier',11),bg="powder blue",command=print_selection)
						btn.grid(row=R,column=C+1)
						btn1.grid(row=R,column=C+2)
				
				print(res[R][C])

				'''
				for i,line in enumerate(res):
					# print('{i}:{r}')
					rows = tk.Frame(fr1,width=300,padx=100,bg="blue")
					rows.pack(side="top")
					
					l1=tk.Message(rows,text=line,padx=50,width=500,bd=1,font=('courier',11),anchor="center",bg="powder blue")
					l1.pack(side='left')
					# lnstatus.insert(tk.END,line)
					tk.Checkbutton(rows, text = "Machine",onvalue = 1, offvalue=0).pack(side='right')
					
					# l1=tk.Label(rows,padx=10,width=2000,bd=1,font=('courier',11),anchor="center",bg="powder blue")
					# l1.pack(side='left')
			
					# l1.grid(row=0,column=1,sticky='w')
			
				#     ls=tk.Message(rows,text='  ',padx=5,bd=1,font=('courier',11),bg="powder blue")#,relief="raised"
				#     ls.pack(side='left')
				#     # ls.grid(row=0,column=1,sticky='w')
			
				#     l2=tk.Message(rows,text=line[1],padx=5,width=1000,bd=1,font=('courier',11),bg="powder blue",anchor="e")
				#     l2.pack(side='left')
				#     # l2.grid(row=0,column=2,sticky='w')
			
				#     ls=tk.Message(rows,text='  ',padx=5,bd=1,font=('courier',11),bg="powder blue")#,relief="raised"
				#     ls.pack(side='left')
				#     # ls.grid(row=0,column=3,sticky='w')
			
				#     l3=tk.Message(rows,text=line[2],padx=5,width=500,bd=1,font=('courier',11),bg="powder blue",anchor="e")
				#     l3.pack(side='left')
				#     # l3.grid(row=0,column=4,sticky='w')

				#     ls=tk.Message(rows,text='     ',padx=5,bd=1,font=('courier',11),bg="powder blue")#,relief="raised"
				#     ls.pack(side='left')
				#     # ls.grid(row=0,column=5,sticky='w')
			
				#     l4=tk.Message(rows,text=line[3],padx=5,width=500,bd=1,font=('courier',11),bg="powder blue",anchor="e")
				#     l4.pack(side='left')
				#     # l4.grid(row=0,column=6,sticky='w')

				#     ls=tk.Message(rows,text='  ',bd=1,font=('courier',11),bg="powder blue",anchor="e")#,relief="raised"
				#     ls.pack(side='left')
				#     # ls.grid(row=0,column=7,sticky='e')
			
				#     l5=tk.Message(rows,text=str(line[4])+' Month(s)',padx=5,width=500,bd=1,font=('courier',11),bg="powder blue",anchor="e")
				#     l5.pack(side='left')
				#     # l5.grid(row=0,column=8,sticky='e')
			
				#     ls=tk.Message(rows,text=' ',padx=5,bd=1,font=('courier',11),bg="powder blue")#,relief="raised"
				#     ls.pack(side='left')
				#     # ls.grid(row=0,column=9,sticky='w')
					
					# loan status field
					# l5=tk.Message(rows,text=line[5],padx=5,width=500,bd=1,font=('courier',11),bg="powder blue",anchor="e")
					# lnstatus = tk.Listbox(width=9,height=1,bd=1,relief="raised",bg="powder blue")#listvariable=line[5]
					# lnstatus.insert(0, line[5])
					# lnstatus.pack(side='right')
					
					# pendingList.append(lnstatus)
					
				#     # l6.grid(row=0,column=10,sticky='e')
					
				#     ls=tk.Message(rows,text=' ',padx=5,bd=1,font=('courier',11),bg="powder blue")
				#     # ls.grid(row=0,column=11,sticky='w')
				#     ls.pack(side='left')
					
					# approvement button
					# btn=tk.Button(rows,text='Approve',width=8,bd=5,font=('courier',11),bg="powder blue",anchor="center",command=print_selection)
					# btn.pack(side='left')
					
					# # btn.grid(row=0,column=12,sticky='w')
					# btn1=tk.Button(rows,text='Disapprove',width=9,bd=5,font=('courier',11),bg="powder blue",anchor="center")
					# btn1.pack(side='left')
					# print(res[i])
				
				
				# lnstatus = tk.Listbox(rows,width=9,height=i+1,bd=1,relief="raised",bg="blue")
				# lnstatus.pack(side='top')
				
				# statusfr=tk.Frame(rows)
				# statusfr.pack(side='top')
				# lnstatus = tk.Listbox(rows,width=9,height=i+1,bd=1,relief="raised",bg="blue")
				# lnstatus.pack(side='left')
				# for line in res:   
				#     print(res[i])
				#     lnstatus.insert(0, line[5])
				'''      
		except Exception as e:
			print('Error in selecting data data',e)
		else:
			print('rows fetched successfully')
			conn.commit()
	finally:
		c.close() 
		conn.close()
    
     #QUIT BUTTON
	b=tk.Button(pen,bd=15,width=15,bg="powder blue",text="Quit",relief="raised",command=pen.destroy)
	b.pack(side="top")
 
 
'''payments page'''
def payments():
	global pen,lnstatus,rows,R,approveres
	pen=tk.Tk()
	pen.geometry("1300x700")
	pen.title("Transaction History")
	pen.configure(bg="powder blue")
	fr1=tk.Frame(pen,bg="blue")
	l_title=tk.Message(pen,text="Efiekuma Holdings",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="blue",justify="center",anchor="center")
	l_title.config(font=("Courier","50","bold"))
	l_title.pack(side="top")

	fr1=tk.Frame(pen,bg="powder blue")
	fr1.pack(side="top",anchor="center")
	l1=tk.Message(fr1,text="Your Transaction History:",padx=200,pady=20,width=1000,bg="blue",fg="orange",relief="raised")
	l1.pack(side="top")
  
    
	title_row=tk.Frame(fr1,padx=160,width=200,bg="powder blue")#padx=500
	title_row.pack(side="top",anchor="w")
	c0=tk.Message(title_row,text="Loan num",font=('Arial',12,'bold'),padx=15,pady=5,width=100,bg="light blue",fg="orange")
	c0.grid(row=0,column=0)
 
	c0=tk.Message(title_row,text="Client id",font=('Arial',12,'bold'),padx=20,pady=5,width=100,bg="light blue",fg="orange")
	c0.grid(row=0,column=1)
 
	# to create space row,column
	cs=tk.Message(title_row,text="",font=('Arial',12,'bold'),padx=10,pady=5,bg="light blue",fg="orange")
	cs.grid(row=0,column=2)
    
	c1=tk.Message(title_row,text="Amount paid",font=('Arial',12,'bold'),padx=15,pady=5,width=100,bg="light blue",fg="orange")
	c1.grid(row=0,column=3)
    
	c5=tk.Message(title_row,text="Payment date",font=('Arial',12,'bold'),padx=15,pady=5,width=150,bg="light blue",fg="orange")
	c5.grid(row=0,column=4)
    
	fr2=tk.Frame(pen)
	fr2.pack(side="top")
        
	try:
		conn = cx_Oracle.connect('Linos/Linos2020@//localhost:1521/xe')
	except  Exception as e:
		print("Error while connecting to database",e)
	else:
		try:
			c = conn.cursor()
			var = '''
			SELECT Loan_Num,CLIENT_ID,AMOUNT_PAID,DATE_PAID FROM loan_repayments
			'''
			c.execute(var)
			res = c.fetchall()
			try:
				totalrow=len(res)
				totalcols=len(res[0])
			except Exception as e:
				print("No data",e)
				l1=tk.Message(fr1,text="No records:",padx=200,pady=20,width=1000,fg="black",relief="raised")
				l1.pack(side="top")
			else:
				rows = tk.Frame(fr1,padx=160,bg="powder blue",width=1000)
				rows.pack(side="top",anchor="center")
				approveres = []
				# partial
				for R in range(totalrow):
					btn=tk.Button(rows,text='Approve',width=8,bd=5,font=('courier',11),bg="green",command=lambda approveres=res[R]:delpayment(approveres[0]))
					btn1=tk.Button(rows,text='Delete',width=9,bd=5,font=('courier',11),bg="red",command=lambda approveres=res[R]:delpayment(approveres[3]))
					for C in range(totalcols):

						l1=tk.Entry(rows,width=15,bd=1,font=('courier',10),bg="powder blue")
						l1.grid(row=R,column=C,sticky='w')
						l1.insert(tk.END, res[R][C])

						btn.grid(row=R,column=C+1)
						btn1.grid(row=R,column=C+2)
			
					print(res[R][C])
		except Exception as e:
			print('Error in selecting data data',e)
		else:
			print('rows fetched successfully')
			conn.commit()
	finally:
		c.close() 
		conn.close() 
	# Quit Button
	b=tk.Button(pen,bd=15,width=15,bg="powder blue",text="Quit",relief="raised",command=pen.destroy)
	b.pack(side="top")


def actual_receivables():
	global pen,lnstatus,rows,R,approveres
	pen=tk.Tk()
	pen.geometry("1300x700")
	pen.title("Transaction History")
	pen.configure(bg="powder blue")
	fr1=tk.Frame(pen,bg="blue")
	l_title=tk.Message(pen,text="Efiekuma Holdings",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="blue",justify="center",anchor="center")
	l_title.config(font=("Courier","50","bold"))
	l_title.pack(side="top")

	fr1=tk.Frame(pen,bg="powder blue")
	fr1.pack(side="top",anchor="center")
	l1=tk.Message(fr1,text="Actual Receivables:",padx=200,pady=20,width=1000,bg="blue",fg="orange",relief="raised")
	l1.pack(side="top")
  
    
	title_row=tk.Frame(fr1,padx=70,width=200,bg="powder blue")#padx=500
	title_row.pack(side="top",anchor="w")
	c0=tk.Message(title_row,text="Loan num",font=('Arial',10,'bold'),padx=15,pady=5,width=100,bg="light blue",fg="orange")
	c0.grid(row=0,column=0)
 
	c0=tk.Message(title_row,text="Client id",font=('Arial',10,'bold'),padx=20,pady=5,width=100,bg="light blue",fg="orange")
	c0.grid(row=0,column=1)
 
	# to create space row,column
	cs=tk.Message(title_row,text="",font=('Arial',12,'bold'),padx=10,pady=5,bg="light blue",fg="orange")
	cs.grid(row=0,column=2)

	c1=tk.Message(title_row,text="Amount",font=('Arial',10,'bold'),padx=15,pady=5,width=100,bg="light blue",fg="orange")
	c1.grid(row=0,column=3)

	cs=tk.Message(title_row,text="",font=('Arial',12,'bold'),padx=10,pady=5,bg="light blue",fg="orange")
	cs.grid(row=0,column=4)

	c1=tk.Message(title_row,text="Rate",font=('Arial',10,'bold'),padx=15,pady=5,width=100,bg="light blue",fg="orange")
	c1.grid(row=0,column=5)

	cs=tk.Message(title_row,text="   ",font=('Arial',12,'bold'),padx=10,pady=5,bg="light blue",fg="orange")
	cs.grid(row=0,column=6)
 
	c1=tk.Message(title_row,text="Duration(mon)",font=('Arial',10,'bold'),padx=15,pady=5,width=150,bg="light blue",fg="orange")
	c1.grid(row=0,column=7)

	cs=tk.Message(title_row,text="",font=('Arial',12,'bold'),padx=10,pady=5,bg="light blue",fg="orange")
	cs.grid(row=0,column=8)

	c1=tk.Message(title_row,text="Interest",font=('Arial',10,'bold'),padx=15,pady=5,width=150,bg="light blue",fg="orange")
	c1.grid(row=0,column=9)

	cs=tk.Message(title_row,text="",font=('Arial',12,'bold'),padx=10,pady=5,bg="light blue",fg="orange")
	cs.grid(row=0,column=10)

	c1=tk.Message(title_row,text="Repayment",font=('Arial',10,'bold'),padx=15,pady=5,width=200,bg="light blue",fg="orange")
	c1.grid(row=0,column=11)

	# cs=tk.Message(title_row,text="",font=('Arial',12,'bold'),padx=10,pady=5,bg="light blue",fg="orange")
	# cs.grid(row=0,column=12)
 
	c1=tk.Message(title_row,text="Amount paid",font=('Arial',10,'bold'),padx=15,pady=5,width=200,bg="light blue",fg="orange")
	c1.grid(row=0,column=13)

	# cs=tk.Message(title_row,text="",font=('Arial',12,'bold'),padx=10,pady=5,bg="light blue",fg="orange")
	# cs.grid(row=0,column=14)

	c1=tk.Message(title_row,text="Balance",font=('Arial',10,'bold'),padx=15,pady=5,width=100,bg="light blue",fg="orange")
	c1.grid(row=0,column=15)
 
	cs=tk.Message(title_row,text="",font=('Arial',12,'bold'),padx=10,pady=5,bg="light blue",fg="orange")
	cs.grid(row=0,column=16)

	c1=tk.Message(title_row,text="Date Disbursed",font=('Arial',10,'bold'),padx=15,pady=5,width=150,bg="light blue",fg="orange")
	c1.grid(row=0,column=17)

	c1=tk.Message(title_row,text="End date",font=('Arial',10,'bold'),padx=15,pady=5,width=150,bg="light blue",fg="orange")
	c1.grid(row=0,column=18)
    
	fr2=tk.Frame(pen)
	fr2.pack(side="top")
        
	try:
		conn = cx_Oracle.connect('Linos/Linos2020@//localhost:1521/xe')
	except  Exception as e:
		print("Error while connecting to database",e)
	else:
		try:
			c = conn.cursor()
			var = '''
			SELECT * FROM ACTUAL_RECEIVABLE_DETAIL
			'''
			c.execute(var)
			res = c.fetchall()
			try:
				totalrow=len(res)
				totalcols=len(res[0])
			except Exception as e:
				print("No data",e)
				l1=tk.Message(fr1,text="No records:",padx=200,pady=20,width=1000,fg="black",relief="raised")
				l1.pack(side="top")
			else:
				rows = tk.Frame(fr1,padx=70,bg="powder blue",width=200)
				rows.pack(side="top",anchor="w")
				approveres = []
				for R in range(totalrow):
					# Approve and disapprove btn, not needed in Receivable
					# btn=tk.Button(rows,text='Approve',width=8,bd=5,font=('courier',11),bg="green",command=lambda approveres=res[R]:approvalprocess(approveres[0]))
					# btn1=tk.Button(rows,text='Disapprove',width=9,bd=5,font=('courier',11),bg="red",command=lambda approveres=res[R]:disapproval(approveres[0]))
					for C in range(totalcols):

						l1=tk.Entry(rows,width=13,bd=1,font=('courier',10),bg="powder blue")
						l1.grid(row=R,column=C,sticky='w')
						l1.insert(tk.END, res[R][C])
						l1.configure(state='disabled')
						# btn.grid(row=R,column=C+1)
						# btn1.grid(row=R,column=C+2)
				

		except Exception as e:
			print('Error in selecting data data',e)
		else:
			print('rows fetched successfully')
			conn.commit()
	finally:
		c.close() 
		conn.close()

	# Quit Button
	b=tk.Button(pen,bd=15,width=15,bg="powder blue",text="Quit",relief="raised",command=pen.destroy)
	b.pack(side="top")


'''Buttom calling function'''
def approvalprocess(ln_num):
	print('Lin',ln_num)
	try:
		conn = cx_Oracle.connect('Linos/Linos2020@//localhost:1521/xe')
	except  Exception as e:
		print("Error while connecting to database",e)
	else:
		try:
			c = conn.cursor()
			var = '''
            UPDATE Loan_Applications 
            Set LOAN_STATUS = 'Approved'
            WHERE Loan_Num =:Loan_Num
            '''    
			var2 = '''
            UPDATE PROPOSED_RECEIVABLES
            Set DATE_DISBURSED = :DATE_DISBURSED 
            WHERE DATE_DISBURSED is null
            '''
			var3='''
            UPDATE PROPOSED_RECEIVABLES
            Set LOAN_STATUS = 'Approved'
            WHERE Loan_Num =:Loan_Num
            '''
			response = messagebox.askokcancel("Confirm Transaction","Are you sure you want to approve this Loan\n",parent=pen)
			if response == True:
				c.execute(var,{'Loan_Num':ln_num})
				c.execute(var2,{'DATE_DISBURSED':datestr}) #,'Loan_Num':ln_num
				c.execute(var3,{'Loan_Num':ln_num})
				messagebox.showinfo("Succesful","Process successfull",parent=pen)
			else:
				messagebox.showinfo("Cancell","Approval process Cancelled",parent=pen)
		except Exception as e:
			print('Error in updated data data data',e)
			messagebox.showinfo("Unsuccessfull","NOT successfull",parent=pen)
		else:
			print('rows updated successfully')
			conn.commit()
	finally:
		c.close() 
		conn.close() 


def disapproval(ln_num):
	print('Lin',ln_num)
	try:
		conn = cx_Oracle.connect('Linos/Linos2020@//localhost:1521/xe')
	except  Exception as e:
		print("Error while connecting to database",e)
	else:
		try:
			c = conn.cursor()
            
			var1 = '''
            UPDATE Loan_Applications 
            Set LOAN_STATUS = 'Disapproved'
            WHERE Loan_Num =:Loan_Num
            '''
			response = messagebox.askokcancel("Confirm Transaction","Are sure you to disapprove this Loan\n",parent=pen)
			if response == True:
				c.execute(var1,{'Loan_Num':ln_num})
				messagebox.showinfo("Succesful","Process successfull",parent=pen)
			else:
				messagebox.showinfo("Cancell","disapproval process Cancelled",parent=pen)
		except Exception as e:
			print('Error in updated data data data',e)
			messagebox.showinfo("Unsuccessfull","NOT successfull",parent=pen)
		else:
			print('rows updated successfully')
			conn.commit()
	finally:
		c.close() 
		conn.close() 


def delpayment(ln_num):
	print('Lin',ln_num)
	try:
		conn = cx_Oracle.connect('Linos/Linos2020@//localhost:1521/xe')
	except  Exception as e:
		print("Error while connecting to database",e)
	else:
		try:
			c = conn.cursor()
			var = '''
            DELETE FROM loan_repayments
            WHERE DATE_PAID =:DATE_PAID
            '''
			response = messagebox.askokcancel("Confirm Transaction","Are sure you to delete this payment\n",parent=pen)
			if response == True:
				c.execute(var,{'DATE_PAID':ln_num})
				messagebox.showinfo("Succesful","Delete successfull",parent=pen)
			else:
				messagebox.showinfo("Cancell","Delete process Cancelled",parent=pen)
		except Exception as e:
			print('Error in updated data data data',e)
			messagebox.showinfo("Unsuccessfull","NOT successfull",parent=pen)
		else:
			print('rows updated successfully')
			conn.commit()
	finally:
		c.close() 
		conn.close() 

	
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

	l1=tk.Label(master=form_structure,text="Administrator id:",font=('arial',14,'bold'))
	empId=tk.Entry(master=form_structure,width=20,font=('arial',16))
	l1.grid(row=0,column=0)
	empId.grid(row=0,column=1,sticky='e')
	empId.insert(0, 'Sylvie')
 
	l2=tk.Label(master=form_structure,text="Password:",font=('arial',14,'bold'))
	password_box=tk.Entry(master=form_structure,show='*',width=20,font=('arial',16))
	l2.grid(row=1,column=0)
	password_box.grid(row=1,column=1,sticky='e')
	password_box.insert(0, 'Sylvie20')
 
	joblabel= tk.Label(master=form_structure, text = "Job Title: ", 
          font=('arial',14,'bold'))
	joblabel.grid(row = 2,column = 0) #(column = 0, row = 5, padx = 10, pady = 25) 
	jobtitleselection = ttk.Combobox(master=form_structure,font=('arial',14),width = 20)
	jobtitleselection.grid(row = 2,column = 1,sticky='e') 
	jobtitleselection['values'] = ('Financial Accountant',  
                          'Loan Officer', 
                          'Manager',
                          'Customer Care')
 
	b=tk.Button(loginwn,relief="raised",bd=15,text="Log in",command=lambda: submitact(loginwn,empId.get().strip(),password_box.get().strip(),jobtitleselection.get().strip()))
	b.pack(side="top")
 
	b1=tk.Button(text="HOME",width=30,relief="raised",font=('arial',12,'bold'),bg="blue",fg="white",bd=15,command=lambda: home_return(loginwn))
	b1.pack(side="bottom")
 
	# b1.pack(side="top")
	# loginwn.bind("<Return>",lambda x:check_log_in(loginwn,ClientId.get().strip(),entries['FirstName'].get().strip(),entries['Email       '].get().strip()))
 
	loginwn.bind("<Return>",lambda x:submitact(loginwn, ClientId.get().strip(),password_box.get().strip(),jobtitleselection.get().strip()))
	return


'''Fuction to verify log in, information gt from Log in frame/page'''
def submitact(master,P_emp_id,password,title):
	global emp_id,jobtitle
	emp_id = P_emp_id
	pword = password
	jobtitle = title
	try:
		conn = cx_Oracle.connect('Linos/Linos2020@//localhost:1521/xe')
	except  Exception as e:
		print("Error while connecting to database",e)
	else:
		try:
			c = conn.cursor() #open the database
			data =  [emp_id,pword,jobtitle]
			var = c.callproc("admlogin",data)
			print(var)
		except Exception as e:
			print('Error creating function',e)
		else:
			print('Function called successfully')
			master.destroy()
			logged_in_menu(emp_id,pword,jobtitle)
			conn.commit()
		finally:
			c.close()
	finally:
		# return emp_id,jobtitle
		conn.close() 

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
	# global field
	# global entries
	# global row
	crwn=tk.Tk()
	# crwn.geometry("650x500")
	crwn.title("Create Account")
	# crwn.configure(bg="orange")

 
	Tops=tk.Frame(crwn,width=600,height=500,bd=8)
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
		# row = tk.Frame(crwn,width=600,height=300,bd=20,bg="powder blue") 
  		#width=20,height=20,
		row.pack()
		# row.pack(side=tk.RIGHT,padx=5 ,pady=5,fill=tk.X)

        # **********Label Widget****************
		# ttk.Label(frame.scrollable_frame, text=field).pack()
		inputV=ttk.Label(row,text=field +": ",font=('arial',12,'bold'),width=20,justify='right')
		inputV.grid(row=0,column=0)
		# inputV.pack(side=tk.LEFT)
        
        # # **********Entry Widget****************
		ent = ttk.Entry(row,font=('arial',16),justify='left',width=30) #,width=10
		# ent.pack(side=tk.RIGHT,expand=tk.YES,fill=tk.X) #,expand=tk.YES
		ent.grid(row=0,column=1)
		entries[field] = ent   
		ent.insert(0,'Try')
        # insert values
	# entries['Firstname'].insert(0,"try")
	# entries['ClientId    '].insert(0,"User Id")
	# entries['FirstName'].insert(0,"fn")
	# entries['Email       '].insert(0,"em")
	frame.pack()
 

	'''Button start'''
	b=tk.Button(frame.scrollable_frame, text='Submit',padx=16,pady=16,bd=8,font=('arial',16,'bold'),
            command=(lambda : write(crwn,entries)))  
	b.pack(side="top")

	crwn.bind("<Return>",lambda x:write(crwn,entries['ClientId    '].get().strip(),entries['FirstName'].get().strip(),entries['Email       '].get().strip()))
	return entries


'''function Get value from entry and insert into database'''
def write(master,entries):
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
			messagebox.showinfo("Details","Account created\nnusername is:"+str(entries['CLIENTID'].get()))
			print('row inserted')
			conn.commit()
            
	finally:     
		print('Linos')
		c.close()
		conn.close()
	return


def Main_Menu():
	rootwn=tk.Tk()
	rootwn.geometry("1200x650")
	rootwn.title("Efiekuma Holdings")
	rootwn.configure(background='powder blue')
	fr1=tk.Frame(rootwn)
	fr1.pack(side="top")
	bg_image = tk.PhotoImage(file ="Admin.gif")
	x = tk.Label (image = bg_image)
	x.place(y=200, x=0)
	l_title=tk.Message(text="LOAN MANAGEMENT SYSTEM\nADMINISTRATOR",relief="raised",width=2000,padx=600,pady=0,fg="white",bg="blue",justify="center",anchor="center")
	l_title.config(font=("Courier","50","bold"))
	l_title.pack(side="top")
	# imgc1=tk.PhotoImage(file="new.gif")
	imglo=tk.PhotoImage(file="login.gif")
	# imgc=imgc1.subsample(2,2)
	imglog=imglo.subsample(2,2)

	# b1=tk.Button(image=imgc,command=Create)
	# b1.image=imgc
	b2=tk.Button(image=imglog,command=lambda: log_in(rootwn))
	b2.image=imglog                                             
	img6=tk.PhotoImage(file="drawButton.png")
	myimg6=img6.subsample(2,2)

	b6=tk.Button(image=myimg6,command=rootwn.destroy)
	b6.image=myimg6
	# b1.place(x=800,y=300)
	b2.place(x=800,y=200)	
	b6.place(x=920,y=400)

	rootwn.mainloop()

Main_Menu()
