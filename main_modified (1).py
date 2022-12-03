from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
import customtkinter

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
			con = pymysql.connect(host="localhost",user="root",password="123456",database="docterapp")
			cur = con.cursor()

			cur.execute("select * from user_information where username=%s and password = %s",(user_name.get(),password.get()))
			row = cur.fetchone()

			if row==None:
				messagebox.showerror("Error" , "Invalid User Name And Password", parent = win)

			else:
				messagebox.showinfo("Success" , "Successfully Login" , parent = win)
				close()
				deshboard()
			con.close()
		except Exception as es:
			messagebox.showerror("Error" , f"Error Dui to : {str(es)}", parent = win)

#---------------------------------------------------------------End Login Function ---------------------------------

#---------------------------------------------------- DeshBoard Panel -----------------------------------------
def deshboard():

	def book():
		if docter_var.get() =="" or day.get() =="" or month.get() == "" or year.get() == "":
			messagebox.showerror("Error" , "All Fields Are Required" , parent = des)

		else:
			con = pymysql.connect(host="localhost",user="root",password="123456",database="docterapp")
			cur = con.cursor()

			cur.execute("update user_information set docter ='" + docter_var.get() + "', day ='" +  day.get() + "', month = '" + month.get() + "', year = '" + year.get() + "' where username ='"+ user_name.get() +"'")
			con.commit()	
			con.close()
			messagebox.showinfo("Success" , "Booked Appointment " , parent = des)

	des = Tk()
	des.title("Profile")	
	des.maxsize(width=1000 ,  height=1000)
	des.minsize(width=1000 ,  height=1000)		

		#heading label
	heading = Label(des , text = f"User Name : {user_name.get()}" , font = 'Verdana 20 bold')
	heading.place(x=220 , y=50)

	f=Frame(des,height=1,width=1000,bg="black")
	f.place(x=0,y=95)

	con = pymysql.connect(host="localhost",user="root",password="123456",database="docterapp")
	cur = con.cursor()

	cur.execute("select * from user_information where username ='"+ user_name.get() + "'")
	row = cur.fetchall()

	a=Frame(des,height=1,width=450,bg="black")
	a.place(x=0,y=225)

	b=Frame(des,height=140,width=1,bg="black")
	b.place(x=450,y=90)

	for data in row: 
		first_name = customtkinter.CTkButton(des, text= f"First Name : {data[1]}")
		first_name.place(x=20,y=80)

		last_name = customtkinter.CTkButton(des, text= f"Last Name : {data[2]}")
		last_name.place(x=20,y=110)

		age = customtkinter.CTkButton(des, text= f"Age : {data[3]}")
		age.place(x=20,y=140)

		gender = customtkinter.CTkButton(des, text= f"ID : {data[0]}")
		gender.place(x=200,y=80)

		city = customtkinter.CTkButton(des, text= f"City : {data[5]}")
		city.place(x=200,y=110)

		add = customtkinter.CTkButton(des, text= f"Address : {data[6]}" )
		add.place(x=200,y=140)

	# Book Docter Appointment App
	heading = customtkinter.CTkButton(des , text = "Book Appointment")
	heading.place(x=470 , y=100)	

	# Book DocterLabel 
	Docter= customtkinter.CTkButton(des, text= "Doctor:")
	Docter.place(x=375,y=145)

	Day = customtkinter.CTkButton(des, text= "Day:")
	Day.place(x=375,y=175)

	Month = customtkinter.CTkButton(des, text= "Month:")
	Month.place(x=375,y=205)

	Year = customtkinter.CTkButton(des, text= "Year:")
	Year.place(x=375,y=235)


	# Book Docter Entry Box

	docter_var = tk.StringVar()
	day = StringVar()
	month = tk.StringVar()
	year = StringVar()

	Docter_box= ttk.Combobox(des, width=30, textvariable= docter_var, state='readonly')
	Docter_box['values']=('Andy','Charlie','Shetal','Danish','Sunil')
	Docter_box.current(0)
	Docter_box.place(x=650,y=185)

	Day = Entry(des, width=33 , textvariable = day)
	Day.place(x=650 , y=225)

	Month_Box= ttk.Combobox(des, width=30, textvariable=month, state='readonly')
	Month_Box['values']=('January','February','March','April','May','June','July','August','September','October','November','December')
	Month_Box.current(0)
	Month_Box.place(x=650,y=260)

	Year = Entry(des, width=33 , textvariable = year)
	Year.place(x=650 , y=300)

	# button 

	btn= customtkinter.CTkButton(des, text = "Book", width = 20) #command = book)
	btn.place(x=553, y=275)

	con = pymysql.connect(host="localhost",user="root",password="123456",database="docterapp")
	cur = con.cursor()

	cur.execute("select * from user_information where username ='"+ user_name.get() + "'")
	rows = cur.fetchall()
	# book Appoitment Details
	heading = customtkinter.CTkButton(des , text = f"{user_name.get()} Following Appointments")
	heading.place(x=20 , y=250)	

	for book in rows:
		d1 = customtkinter.CTkButton(des, text= f"Docter: {book[9]}" )
		d1.place(x=20,y=300)

		d2 = customtkinter.CTkButton(des, text= f"Day: {book[10]}" )
		d2.place(x=20,y=330)

		d3 = customtkinter.CTkButton(des, text= f"Month: {book[11]}" )
		d3.place(x=20,y=360)

		d4 = customtkinter.CTkButton(des, text= f"Year: {book[12]}")
		d4.place(x=20,y=390)		

					
#-----------------------------------------------------End Deshboard Panel -------------------------------------
#----------------------------------------------------------- Signup Window --------------------------------------------------

def signup():
	# signup database connect 
	def action():
		if first_name.get()=="" or last_name.get()=="" or age.get()=="" or city.get()=="" or add.get()=="" or user_name.get()=="" or password.get()=="" or very_pass.get()=="":
			messagebox.showerror("Error" , "All Fields Are Required" , parent = winsignup)
		elif password.get() != very_pass.get():
			messagebox.showerror("Error" , "Password & Confirm Password Should Be Same" , parent = winsignup)
		else:
			try:
				con = pymysql.connect(host="localhost",user="root",password="123456",database="docterapp")
				cur = con.cursor()
				cur.execute("select * from user_information where username=%s",user_name.get())
				row = cur.fetchone()
				if row!=None:
					messagebox.showerror("Error" , "User Name Already Exits", parent = winsignup)
				else:
					cur.execute("insert into user_information(first_name,last_name,age,gender,city,address,username,password) values(%s,%s,%s,%s,%s,%s,%s,%s)",
						(
						first_name.get(),
						last_name.get(),
						age.get(),
						var.get(),
						city.get(),
						add.get(),
						user_name.get(),
						password.get()
						))
					con.commit()
					con.close()
					messagebox.showinfo("Success" , "Registration Successfull" , parent = winsignup)
					clear()
					switch()
				
			except Exception as es:
				messagebox.showerror("Error" , f"Error Dui to : {str(es)}", parent = winsignup)

	# close signup function			
	def switch():
		winsignup.destroy()

	# clear data function
	def clear():
		first_name.delete(0,END)
		last_name.delete(0,END)
		age.delete(0,END)
		var.set("Male")
		city.delete(0,END)
		add.delete(0,END)
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

	city = customtkinter.CTkButton(winsignup, text= "City :")
	city.place(x=80,y=250)

	#add = Label(winsignup, text= "Address :" , font='Verdana 10 bold')
	#add.place(x=80,y=290)

	add = customtkinter.CTkButton(winsignup, text= "Address :" )
	add.place(x=80,y=280)

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
	city= StringVar()
	add = StringVar()
	user_name = StringVar()
	password = StringVar()
	very_pass = StringVar()


	first_name = Entry(winsignup, width=40 , textvariable = first_name)
	first_name.place(x=300 , y=165)


	
	last_name = Entry(winsignup, width=40 , textvariable = last_name)
	last_name.place(x=300 , y=205)

	
	age = Entry(winsignup, width=40, textvariable=age)
	age.place(x=300 , y=245)

	
	Radio_button_male = ttk.Radiobutton(winsignup,text='Male', value="Male", variable = var).place(x= 300 , y= 280)
	Radio_button_female = ttk.Radiobutton(winsignup,text='Female', value="Female", variable = var).place(x= 400 , y= 280)


	city = Entry(winsignup, width=40,textvariable = city)
	city.place(x=300 , y=320)


	
	add = Entry(winsignup, width=40 , textvariable = add)
	add.place(x=300 , y=360)

	
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