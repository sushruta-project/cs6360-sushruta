from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
import customtkinter
from tkcalendar import Calendar
from dateutil.parser import parse
from datetime import datetime

conn = pymysql.connect(host="127.0.0.1",user="root",password="1234567890",database="dbproject")
c = conn.cursor()

#---------------------------------------------------------------Login Function --------------------------------------
def clear():
	userentry.delete(0,END)
	passentry.delete(0,END)

def close():
	win.destroy()	


def login():
	if user_name.get()=="" or password.get()=="":
		messagebox.showerror("Error","Enter User Name And Password",parent=win)	
	else:
		try:
			con = pymysql.connect(host="127.0.0.1",user="root",password="1234567890",database="dbproject")
			cur = con.cursor()

			cur.execute("select * from patient where username=%s and password = %s",(user_name.get(),password.get()))
			row = cur.fetchone()

			if row==None:
				messagebox.showerror("Error" , "Invalid User Name And Password", parent = win)

			else:
				messagebox.showinfo("Success" , "Successfully Login" , parent = win)
				close()
				deshboard()
			con.close()
		except Exception as es:
			messagebox.showerror("Error" , f"Error Due to : {str(es)}", parent = win)

#---------------------------------------------------------------End Login Function ---------------------------------

#---------------------------------------------------- DeshBoard Panel -----------------------------------------
def deshboard():

	def book():
		date = getCustomDate(cal)
		print("selected date is", date)
		print(parse(date).strftime("%Y-%m-%d"))
		if docter_var.get() =="" or date =="":
			messagebox.showerror("Error" , "All Fields Are Required" , parent = des)

		else:
			con = pymysql.connect(host="127.0.0.1",user="root",password="1234567890",database="dbproject")
			cur = con.cursor()
			cur.execute("select * from doctor where first_name = %s", (docter_var.get()))
			doc = cur.fetchone()
			doc_id = doc[0]
			doc_fees = doc[7]
			print(type(id))
			print(type(date))
			apt_date = parse(date).strftime("%Y-%m-%d")
			print(type(apt_date))

			cur.execute("select * from patient where username = %s",user_name.get())
			patient = cur.fetchone()
			patient_id = patient[0]

			new_status = 'Upcoming'
			modified_date = datetime.today().strftime('%Y-%m-%d')
			cur.execute("insert into appointment(patient_id,doctor_id,date_time,status,payment_amt,rating_by_patient,patient_feedback,doctor_comments, modified_date) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
		    (patient_id,doc_id,apt_date,new_status,doc_fees,'','','',modified_date))

			# c.execute("insert into appointment values (11,2,'2023-01-04','Upcoming','70$','','','')")
			#TODO
			# cur.execute("update appointment set docter ='" + doc_id + "', day ='" +  day.get() + "', month = '" + month.get() + "', year = '" + year.get() + "' where username ='"+ user_name.get() +"'")
			con.commit()	
			con.close()
			messagebox.showinfo("Success" , f"Booked Appointment, paid doctor fees - {doc_fees}" , parent = des)
	
	def getCustomDate(cal):
		print("custom date --",cal.get_date())	
		return cal.get_date()


	des = Tk()
	des.title("Patient Profile")	
	des.maxsize(width=1000 ,  height=1000)
	des.minsize(width=1000 ,  height=1000)		

	#heading label
	heading = Label(des , text = f"User Name : {user_name.get()}" , font = 'Arial 16')
	heading.place(x=220 , y=50)

	f=Frame(des,height=1,width=1000,bg="black")
	f.place(x=0,y=95)

	# menu bar
	Chooser = Menu()
	itemone = Menu()
	Chooser.add_cascade(label='Edit Appointment', command=editAppointment)
	# itemone.add_command(label='Inside Edit Appointment')
	Chooser.add_cascade(label='Search Medicine', command=lambda: searchMedicine())
	Chooser.add_cascade(label='Raise an Issue')
	Chooser.add_cascade(label='Logout', command=lambda: logout(des))

	des.config(menu=Chooser)

	con = pymysql.connect(host="127.0.0.1",user="root",password="1234567890",database="dbproject")
	cur = con.cursor()

	cur.execute("select * from patient where username ='"+ user_name.get() + "'")
	row = cur.fetchall()

	a=Frame(des,height=1,width=1000,bg="black")
	a.place(x=0,y=600)

	b=Frame(des,height=505,width=1,bg="black")
	b.place(x=455,y=96)

	user_details = Label(des, text= "User details:", font='Arial 12 underline')
	user_details.place(x=20,y=100)

	for data in row: 
		first_name = Label(des, text= f"First Name : {data[1]}", font='Arial 10')
		first_name.place(x=20,y=140)

		last_name = Label(des, text= f"Last Name : {data[2]}", font='Arial 10')
		last_name.place(x=20,y=170)

		
		age = Label(des, text= f"Age : {data[3]}" , font='Arial 10')
		age.place(x=20,y=200)

		id = Label(des, text= f"ID : {data[0]}" , font='Arial 10')
		id.place(x=250,y=140)

		'''
		city = Label(des, text= f"City : {data[5]}" , font='Verdana 10 bold')
		city.place(x=250,y=130)

		add = Label(des, text= f"Address : {data[6]}" , font='Verdana 10 bold')
		add.place(x=250,y=160)
		'''

		gender = Label(des, text = f"Gender : {data[4]}" , font = 'Arial 10')
		gender.place(x=250, y = 170)

		phone_num = Label(des, text = f"Phone no : {data[5]}" , font = 'Arial 10')
		phone_num.place(x=250, y = 200)

		med_hist = Label(des, text=f"Medical History : {data[6]}" , font = 'Arial 10')
		med_hist.place(x=20, y = 230)

	# Book Docter Appointment App #TODO
	heading = Label(des , text = "Book Appointment" , font = 'Arial 12 underline')
	heading.place(x=470 , y=100)	

	# Book DocterLabel 
	Docter= Label(des, text= "Doctor:" , font='Arial 10')
	Docter.place(x=480,y=145)
	'''
	Day = Label(des, text= "Day:" , font='Arial 10')
	Day.place(x=480,y=175)

	Month = Label(des, text= "Month:" , font='Arial 10')
	Month.place(x=480,y=205)

	Year = Label(des, text= "Year:" , font='Arial 10')
	Year.place(x=480,y=245)
	'''

	# Book Docter Entry Box

	docter_var = tk.StringVar()
	day = StringVar()
	month = tk.StringVar()
	year = StringVar()

	appointment_date = StringVar()

	Docter_box= ttk.Combobox(des, width=30, textvariable= docter_var, state='readonly')
	cur.execute("select first_name from doctor where availability = 'Yes'")
	rows = cur.fetchall()
	doc_names = []
	for doc in rows:
		doc_names.append(doc)
	#Docter_box['values']=['Andy','Charlie','Shetal','Danish','Sunil']
		Docter_box['values'] = doc_names
	Docter_box.current(0)
	Docter_box.place(x=550,y=145)
	'''
	Day = Entry(des, width=33 , textvariable = day)
	Day.place(x=650 , y=225)

	Month_Box= ttk.Combobox(des, width=30, textvariable=month, state='readonly')
	Month_Box['values']=('January','February','March','April','May','June','July','August','September','October','November','December')
	Month_Box.current(0)
	Month_Box.place(x=650,y=260)

	Year = Entry(des, width=33 , textvariable = year)
	Year.place(x=650 , y=300)
	'''
	appointment_date = Label(des, text= "Appointment Date:" , font='Arial 10')
	appointment_date.place(x=480,y=185)

	#changed 

	cal = Calendar(des, selectmode = 'day', date_pattern = 'yyyy-mm-dd')
 
	cal.place(x=600, y=215)

	# button 

	btn= Button(des, text = "Book" ,font='Arial 12', width = 20, command = book)
	btn.place(x=553, y=500) #295 without datepicker

	# btn= customtkinter.CTkButton(des, text = "Book", width = 20) #command = book)
	# btn.place(x=553, y=275)

	con = pymysql.connect(host="127.0.0.1",user="root",password="1234567890",database="dbproject")
	cur = con.cursor()

	cur.execute("select * from patient where username=%s and password = %s",(user_name.get(),password.get()))
	row = cur.fetchone()
	id = row[0]

	cur.execute("select * from appointment where patient_id =%s order by modified_date desc", id)
	rows = cur.fetchall()
	print("Appointments")
	print(rows)
	#changed
	# book Appointment Details
	# heading = customtkinter.CTkButton(des , text = f"{user_name.get()} Appointments")
	heading = Label(des, text= "Appointments:", font='Arial 12 underline')
	heading.place(x=20 , y=610)	

	# for book in rows:
	# 	cur.execute("select * from doctor where doctor_id = %s", book[1])
	# 	docRow = cur.fetchone()
	# 	docFname = docRow[1]
	# 	docLname = docRow[2]
	# 	#d1 = customtkinter.CTkButton(des, text= f"Docter: {docFname} {docLname}" )
	# 	d1 = last_name = Label(des, text= f"Doctor : {docFname} {docLname}", font='Arial 10')
	# 	d1.place(x=20,y=300)

	# 	#d2 = customtkinter.CTkButton(des, text= f"Date & Time {book[2]}" )
	# 	d2 = Label(des, text= f"Appointment Date : {book[2]}", font='Arial 10')
	# 	d2.place(x=20,y=330)

	# 	#d3 = customtkinter.CTkButton(des, text= f"Status: {book[3]}" )
	# 	d3 = Label(des, text= f"Status : {book[3]}", font='Arial 10')
	# 	d3.place(x=20,y=360)

	# 	#d4 = customtkinter.CTkButton(des, text= f"Payment amount: {book[4]}")
	# 	d4 = Label(des, text= f"Payment Amount : {book[4]}", font='Arial 10')
	# 	d4.place(x=20,y=390)
	
	cols = ['Doctor', 'Appointment Date', 'Status', 'Payment Amount']
	listBox = ttk.Treeview(des, columns=cols, show='headings')
	
	style = ttk.Style(des)
	style.configure('Treeview.Heading', foreground='black')
	style.configure('Treeview', rowheight=40)
	for col in cols:
		listBox.heading(col, text=col)    
		listBox.grid(row=1, column=0, columnspan=2)
	
	for appt in rows:
		cur.execute("select * from doctor where doctor_id = %s", appt[1])
		docRow = cur.fetchone()
		docFname = docRow[1]
		docLname = docRow[2]
		docName = docFname + ' ' + docLname
		listBox.insert("", "end", values=(docName, appt[2], appt[3], appt[4]))

	# for pharm in list_of_pharm:
	# 	c.execute("select * from pharmacy where store_id = %s", (pharm[1]))
	# 	pharm_det = c.fetchone()
	# 	listBox.insert("", "end", values=(pharm_det[1], pharm_det[2], pharm[2], pharm[3], pharm[4]))	

	listBox.place(x=70, y = 650)


		
#------------------------------------------------------------------Logout---------------------------------------------------------------
# function to close the top window
	def logout(parent):
		MsgBox = tk.messagebox.askquestion('Logout Application','Are you sure you want to logout?', icon='warning')
		if MsgBox == 'yes':
		# self.path = self.name + ".jpg"
			print("parent is ", parent)
			parent.destroy()
			login()

#-----------------------------------------------------End Deshboard Panel -------------------------------------

def editAppointment():
	'''
	if sys.platform.startswith('Linux'):
		os.system("python3 update.py")
	elif sys.platform.startswith('win32'):
		os.system("python update.py" + user_name.get())
	'''

	#creating the object
	editApp = tk.Tk()
	# b = App(root)
	# root.geometry("640x620+100+50")
	# root.resizable(False, False)
	# root.title("Update Appointment")

	editApp.title('Edit Appointment')	
	editApp.maxsize(width=1000 ,  height=1000)
	editApp.minsize(width=1000 ,  height=1000)	
	f=Frame(editApp,height=1,width=1000)
	f.place(x=95,y=95)

	# heading label
	heading = Label(editApp, text="Update Appointments",  fg='black', font=('arial 18'))
	heading.place(x=180, y=40)

    # search criteria -->name 
	name = Label(editApp, text="Enter Doctor's Name", font=('arial 12'))
	name.place(x=70, y=100)

    # entry for  the name
	namenet = Entry(editApp, width=30)
	namenet.place(x=300, y=100)

    # search button
	search = Button(editApp, text="Search", width=12, height=1, bg='steelblue', command=lambda: search_db(editApp, namenet))
	search.place(x=230, y=150)

def search_db(editApp, namenet):
	print("In search db method")
	input = namenet.get()
	print(user_name.get() + ' ' + '***')
	c.execute("select id from patient where username = %s", (user_name.get()))
	patientid = c.fetchone()
	print(patientid[0])
	print("Input ---- " + input)
	
	c.execute("select doctor_id from doctor where first_name like '%" + input + "%'")
	doctor_id = c.fetchone()[0]
	print(doctor_id)
	c.execute("select * from appointment where doctor_id = %s and patient_id = %s order by modified_date desc", (doctor_id, patientid))
	appointment = c.fetchone()    
	print(appointment)

	if appointment == None:
	 	messagebox.showerror("Error" , f"No appointment with : {input}", parent = editApp)
		# raise Exception("No appointment with : {input}")

	#for row in appointment:
	c.execute("select * from patient where id = %s", (patientid))
	patient = c.fetchone()
	print(patient)
	print(appointment)
	name = patient[1] + ' ' + patient[2]
	age = patient[3]
	gender = patient[4]
	appointment_date = appointment[2]
	status = appointment[3]
	payment_amt = appointment[4]
	patient_rating = appointment[5]
	patient_feedback = appointment[6]
	doctor_feedback = appointment[7]

	c.execute("select medicine_id from prescription where patient_id = %s and doctor_id = %s and date_time = %s", (patientid, doctor_id, appointment_date))
	medicine_id = c.fetchone()
	medicine_name = ''
	suggestion = ''
	if medicine_id:
		c.execute("select name from medicine where medicine_id = %s", (medicine_id))
		medicine = c.fetchone() 
		medicine_name = medicine[0]

		c.execute("select suggestions from prescription where patient_id = %s and doctor_id = %s and date_time = %s", (patientid, doctor_id, appointment_date))
		suggestion_list = c.fetchone()
		suggestion = suggestion_list[0]

	 # creating the update form
	uname = Label(editApp, text= f"Patient's Name : {name}", font=('arial 12'))
	uname.place(x=70, y=220)

	uage = Label(editApp, text= f"Age : {age}", font=('arial 12'))
	uage.place(x=70, y=260)

	ugender = Label(editApp, text= f"Gender : {gender}", font=('arial 12'))
	ugender.place(x=70, y=300)

	ulocation = Label(editApp, text=f"Appointment Date : {appointment_date}", font=('arial 12'))
	ulocation.place(x=70, y=340)

	utime = Label(editApp, text=f"Status : {status}", font=('arial 12'))
	utime.place(x=70, y=380)
	
	uphone = Label(editApp, text=f"Payment : {payment_amt}", font=('arial 12'))
	uphone.place(x=70, y=420)

	upatient_rating = Label(editApp, text="Rating : ", font=('arial 12'))
	upatient_rating.place(x=70, y=460)

	upatient_feedback = Label(editApp, text="Feedback : ", font=('arial 12'))
	upatient_feedback.place(x=70, y=500)

	udoctor_feedback = Label(editApp, text=f"Doctor Feedback : {doctor_feedback}", font=('arial 12'))
	udoctor_feedback.place(x=70, y=540)

	uprescription = Label(editApp, text = "Prescription", font= ('arial 14 underline'))
	uprescription.place(x=70, y=580)

	umedicine = Label(editApp, text = f"Prescribed medicine: {medicine_name}", font= ('arial 12'))
	umedicine.place(x=70, y=620)

	usuggestion = Label(editApp, text = f"suggestion: {suggestion}", font= ('arial 12'))
	usuggestion.place(x=70, y=660)

	# entries for each labels==========================================================
        # ===================filling the search result in the entry box to update
	upatient_rating = Label(editApp, text="Patient Rating", font=('arial 12'))
	upatient_rating.place(x=70, y=460)

	# patient_name = Label(editApp, text= f"City : {data[5]}" , font='Verdana 10 bold')
	# city.place(x=250,y=130)

	ent1 = Entry(editApp, width=30)
	ent1.place(x=300, y=460)
	ent1.insert(END, str(patient_rating))
	
	ent2 = Entry(editApp, width=30)
	ent2.place(x=300, y=500)
	ent2.insert(END, str(patient_feedback))

	# button to execute update
	update = Button(editApp, text="Update", width=20, height=2, bg='lightblue', command=lambda: update_db(editApp, appointment[0], appointment[1], ent1, ent2))
	update.place(x=150, y=800)

	cancel = Button(editApp, text="Cancel", width=20, height=2, bg='orange red', command=lambda: cancel_db(editApp, appointment[0], appointment[1], ent1, ent2))
	cancel.place(x=450, y=800)
	

def update_db(editApp, patient_id, doctor_id, ent1, ent2):
	patient_rating = ent1.get()
	patient_feedback = ent2.get()
	print(patient_feedback)
	c.execute("update appointment set rating_by_patient = %s, patient_feedback = %s where patient_id = %s and doctor_id = %s", (patient_rating, patient_feedback, patient_id, doctor_id))
	conn.commit()
	messagebox.showinfo("Updated", "Successfully Updated.", parent = editApp)
	editApp.destroy()

def cancel_db(editApp, patient_id, doctor_id, ent1, ent2):
	print("in cancel appt")
	print(patient_id, doctor_id)
	c.execute("delete from appointment where patient_id = %s and doctor_id = %s", (patient_id, doctor_id))
	conn.commit()
	messagebox.showinfo("Cancelled", "Appointment Cancelled.", parent = editApp)
	editApp.destroy()

#changed
#search pharmacy-----------------------------
def searchMedicine():
	print("in search medicine")
		#creating the object
	searchMed = tk.Tk()
	# b = App(root)
	# root.geometry("640x620+100+50")
	# root.resizable(False, False)
	# root.title("Update Appointment")

	searchMed.title('Search Pharmacy')	
	searchMed.maxsize(width=1200 ,  height=1000)
	searchMed.minsize(width=1200 ,  height=1000)	
	f=Frame(searchMed,height=1,width=1000)
	f.place(x=95,y=95)

	# heading label
	heading = Label(searchMed, text="Search Pharmacy",  fg='black', font=('arial 18'))
	heading.place(x=180, y=40)

    # search criteria -->name 
	name = Label(searchMed, text="Enter Medicine Name", font=('arial 12'))
	name.place(x=70, y=100)

    # entry for  the name
	namenet = Entry(searchMed, width=30)
	namenet.place(x=320, y=100)

    # search button
	search = Button(searchMed, text="Search", width=12, height=1, bg='steelblue', command=lambda: search_pharmacy(searchMed, namenet))
	search.place(x=230, y=150)

#search pharmacy for medicine -------------

def search_pharmacy(searchMed, medName):
	print("in search pharm")
	c.execute("select * from medicine where name like '%" + medName.get() +"%'")
	med = c.fetchone()

	if type(med) == 'NoneType':
		med_id = med[0]

		c.execute("select * from availability where medicine_id = %s and availability = %s", (med_id, 1))
		list_of_pharm = c.fetchall()
		print(list_of_pharm)

		pharm_list = Label(searchMed, text="Medicine available in pharmacies", font=('arial 12'))
		pharm_list.place(x=70, y = 210)
	# for pharm in list_of_pharm:


	# Add the rowheight
		cols = ['Pharmacy Name', 'Location', 'Availability', 'Count', 'Price']
		listBox = ttk.Treeview(searchMed, columns=cols, show='headings')
		style = ttk.Style(searchMed)
		style.configure('Treeview.Heading', foreground='black')
		style.configure('Treeview', rowheight=40)
		for col in cols:
			listBox.heading(col, text=col)    
			listBox.grid(row=1, column=0, columnspan=2)
		
		for pharm in list_of_pharm:
			c.execute("select * from pharmacy where store_id = %s", (pharm[1]))
			pharm_det = c.fetchone()
			listBox.insert("", "end", values=(pharm_det[1], pharm_det[2], pharm[2], pharm[3], pharm[4]))	

		listBox.place(x=70, y = 210)
	
	else:
		messagebox.showerror("Error" , f"No medicine starting with name - {medName.get()}", parent = searchMed)





#----------------------------------------------------------- Signup Window --------------------------------------------------

def signup():
	# signup database connect 
	def action():
		selected_gender = ''
		print("gender is",gender.get())
		if gender.get() == 0:
			selected_gender = 'Male'
		else:
			selected_gender = 'Female'
		print(selected_gender)
		if first_name.get()=="" or last_name.get()=="" or age.get()=="" or selected_gender == "" or phone_no.get()=="" or medical_hist.get()=="" or user_name.get()=="" or password.get()=="" or very_pass.get()=="":
			messagebox.showerror("Error" , "All Fields Are Required" , parent = winsignup)
		elif password.get() != very_pass.get():
			messagebox.showerror("Error" , "Password & Confirm Password Should Be Same" , parent = winsignup)
		else:
			try:
				con = pymysql.connect(host="127.0.0.1",user="root",password="1234567890",database="dbproject")
				cur = con.cursor()
				cur.execute("select * from patient where username=%s",user_name.get())
				row = cur.fetchone()
				if row!=None:
					messagebox.showerror("Error" , "User Name Already Exits", parent = winsignup)
				else:
					print(medical_hist.get(), phone_no.get())
					cur.execute("insert into patient(first_name,last_name,age,gender,phone_no,medical_history,username,password) values(%s,%s,%s,%s,%s,%s,%s,%s)",
						(
						first_name.get(), 
						last_name.get(),
						age.get(),
						selected_gender,
						phone_no.get(),
						medical_hist.get(),
						user_name.get(),
						password.get()
						))
					con.commit()
					con.close()
					messagebox.showinfo("Success" , "Registration Successfull" , parent = winsignup)
					clear()
					switch()
				
			except Exception as es:
				messagebox.showerror("Error" , f"Error Due to : {str(es)}", parent = winsignup)

	# close signup function			
	def switch():
		winsignup.destroy()

	# clear data function
	def clear():
		first_name.delete(0,END)
		last_name.delete(0,END)
		age.delete(0,END)
		var.set("Male")
		phone_no.delete(0,END)
		medical_hist.delete(0,END)
		user_name.delete(0,END)
		password.delete(0,END)
		very_pass.delete(0,END)


	# start Signup Window	

	customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
	customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

	winsignup = customtkinter.CTk()
	winsignup.title("Sushruta - Signup Page")
	winsignup.maxsize(width=750 ,  height=750)
	winsignup.minsize(width=750 ,  height=750)


	#heading label
	#heading = Label(winsignup , text = "Sign UP")
	#heading.place(x=80 , y=60)
	
	heading = customtkinter.CTkButton(winsignup , text = "SIGN UP PAGE")
	heading.place(x=80 , y=60)

	# form data label
	'''
	first_name = Label(winsignup, text= "First Name :")
	first_name.place(x=80,y=130)
	'''
	first_name = customtkinter.CTkButton(winsignup, text= "First Name :")
	first_name.place(x=80,y=130)

	#last_name = Label(winsignup, text= "Last Name :" , font='Verdana 10 bold')
	#last_name.place(x=80,y=160)

	last_name = customtkinter.CTkButton(winsignup, text= "Last Name :")
	last_name.place(x=80,y=160)

	#age = Label(winsignup, text= "Age :" , font='Verdana 10 bold')
	#age.place(x=80,y=190)

	age = customtkinter.CTkButton(winsignup, text= "Age :")
	age.place(x=80,y=190)

	#Gender = Label(winsignup, text= "Gender :" , font='Verdana 10 bold')
	#Gender.place(x=80,y=220)

	Gender = customtkinter.CTkButton(winsignup, text= "Gender :" )
	Gender.place(x=80,y=220)

	#city = Label(winsignup, text= "City :" , font='Verdana 10 bold')
	#city.place(x=80,y=260)

	# city = customtkinter.CTkButton(winsignup, text= "City :")
	# city.place(x=80,y=250)

	#add = Label(winsignup, text= "Address :" , font='Verdana 10 bold')
	#add.place(x=80,y=290)

	phone_no = customtkinter.CTkButton(winsignup, text= "Phone no :" )
	phone_no.place(x=80,y=250)

	#medical history
	medical_hist = customtkinter.CTkButton(winsignup, text= "Medical History :")
	medical_hist.place(x=80,y=280)

	#user_name = Label(winsignup, text= "User Name :" , font='Verdana 10 bold')
	#user_name.place(x=80,y=320)

	user_name = customtkinter.CTkButton(winsignup, text= "User Name :")
	user_name.place(x=80,y=310)

	#password = Label(winsignup, text= "Password :" , font='Verdana 10 bold')

	#password.place(x=80,y=350)

	password = customtkinter.CTkButton(winsignup, text= "Password :")
	password.place(x=80,y=340)

	#very_pass = Label(winsignup, text= "Verify Password:" , font='Verdana 10 bold')
	#very_pass.place(x=80,y=380)

	very_pass = customtkinter.CTkButton(winsignup, text= "Verify Password:")
	very_pass.place(x=80,y=370)

	# Entry Box ------------------------------------------------------------------

	first_name = StringVar()
	last_name = StringVar()
	age = IntVar(winsignup, value='0')
	var= StringVar()
	medical_hist= StringVar()
	phone_no = StringVar()
	user_name = StringVar()
	password = StringVar()
	very_pass = StringVar()
	gender = IntVar(winsignup, value=0)

	first_name = Entry(winsignup, width=40 , textvariable = first_name)
	first_name.place(x=300 , y=165)
	
	last_name = Entry(winsignup, width=40 , textvariable = last_name)
	last_name.place(x=300 , y=205)
	
	age = Entry(winsignup, width=40, textvariable=age)
	age.place(x=300 , y=245)
	
	#changed
	
	radio_male = ttk.Radiobutton(winsignup,text='Male', value=0, variable = gender)
	radio_male.place(x= 300 , y= 280)
	
	radio_female = ttk.Radiobutton(winsignup,text='Female', value=1, variable = gender)
	radio_female.place(x= 400 , y= 280)

	phone_no = Entry(winsignup, width=40,textvariable = phone_no)
	phone_no.place(x=300 , y=320)
	
	medical_hist = Entry(winsignup, width=40 , textvariable = medical_hist)
	medical_hist.place(x=300 , y=360)

	
	user_name = Entry(winsignup, width=40,textvariable = user_name)
	user_name.place(x=300 , y=395)

	
	password = Entry(winsignup, width=40, textvariable = password)
	password.place(x=300 , y=432)

	
	very_pass= Entry(winsignup, width=40 ,show="*" , textvariable = very_pass)
	very_pass.place(x=300 , y=470)


	# button login and clear

	#btn_signup = Button(winsignup, text = "Signup" ,font='Verdana 10 bold', command = action)
	#btn_signup.place(x=200, y=413)

	btn_signup = customtkinter.CTkButton(winsignup, text = "SIGN UP", command = action)
	btn_signup.place(x=150, y=450)

	#btn_login = Button(winsignup, text = "Clear" ,font='Verdana 10 bold' , command = clear)
	#btn_login.place(x=280, y=413)
	
	btn_login = customtkinter.CTkButton(winsignup, text = "CLEAR" , command = clear)
	btn_login.place(x=350, y=450)

	#sign_up_btn = Button(winsignup , text="Switch To Login" , command = switch )
	#sign_up_btn.place(x=350 , y =20)

	sign_up_btn = customtkinter.CTkButton(winsignup , text="SWITCH TO LOGIN PAGE", command = switch )
	sign_up_btn.place(x=350 , y =20)

	winsignup.mainloop()
#---------------------------------------------------------------------------End Singup Window-----------------------------------	


	

#------------------------------------------------------------ Login Window -----------------------------------------
import customtkinter

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


win = customtkinter.CTk()  # create CTk window like you do with the Tk window

# app title
win.title("Sushruta - Medicare For All")

# window size
win.maxsize(width=750 ,  height=750)
win.minsize(width=750 ,  height=750)


#heading label

button = customtkinter.CTkButton(master=win, text="User Login Below ")
button.place(x=60,y=125)


username = customtkinter.CTkButton(master=win, text="User Name : ")
username.place(x=60,y=175)

userpass = customtkinter.CTkButton(master=win, text="Password : ")
userpass.place(x=60,y=225)

# Entry Box
user_name = StringVar()
password = StringVar()
	
userentry = Entry(win, width=40 , textvariable = user_name)
userentry.focus()
userentry.place(x=260 , y=223)

passentry = Entry(win, width=40, show="*" ,textvariable = password)
passentry.place(x=260 , y=285)


# button login and clear
'''
btn_login = Button(win, text = "Login" ,font='Verdana 10 bold',command = login)
btn_login.place(x=200, y=293)
'''

btn_login = customtkinter.CTkButton(win, text = "Login",command = login)
btn_login.place(x=200, y=275)

'''
btn_login = Button(win, text = "Clear" ,font='Verdana 10 bold', command = clear)
btn_login.place(x=260, y=293)
'''
btn_login = customtkinter.CTkButton(win, text = "Clear" ,command = clear)
btn_login.place(x=350, y=275)

# signup button

sign_up_btn = customtkinter.CTkButton(win , text="GO TO SIGN UP PAGE" , command = signup )
sign_up_btn.place(x=350 , y =20)

win.mainloop()

#-------------------------------------------------------------------------- End Login Window --------------------------------------------------