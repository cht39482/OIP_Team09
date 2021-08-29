from capture_images import activateCamera
from guizero import App, Text, TextBox, PushButton, Slider, Picture, Combo, Box, info, Window
from time import sleep
import time
import detect_picamera
import serial

try:
    ser = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
except:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    
ser.flush()
app = App(title="Basin Washer", width=800, height=480, bg = "#F5F5F5")
app2 = App(title="Process running", width=800, height=480, bg = "#F5F5F5")
#timer = False
app2.hide()


def selection():
    if process_choice.value == "Wash and Sterilize":
        start_process()
    if process_choice.value == "Sterilizing":
        start_sterilizing()
        
def start_process():
    confirm_message = app.yesno("Confirm", "Do you want run process?")
    if confirm_message == True:
        home_message.value = "Washing..."
        app.update()
        ser.write("process1\n".encode('utf-8'))#Write to arduino to start process 1
        line = ser.readline().decode('utf-8').rstrip()#Read ack from arduino to start washing process
        if line == "ok": #if ack recieved
            ser.flush()
            ser.write("20\n".encode('utf-8')) #write a duration command to arduino start washing
            line = response_message("washing completed") #arduino will send a message once washing is done
            #ML FUNCTION run here
            while(line=="washing completed"):
                activateCamera()
                if(detect_picamera.predictClass("saved_image.jpg")):
                    break
                else:
                    ser.flush
                    ser.write("20\n".encode('utf-8'))
                    line = response_message("washing completed") #arduino will send a message once washing is done
                
            if line == "washing completed": #Start sterilizing process once ack is recieved
                home_message.value = "Sterilizing..."
                app.update()
                line = response_message("sterilization completed")#Awaiting ack from arduino to start the next drying process
                if line == "sterilization completed":#Check if ack is received
                    home_message.value = "Drying..."
                    app.update()
                    ser.write("20\n".encode('utf-8'))#write a duration command to aduino start drying
                    line = response_message("drying completed")#awaiting ack
                    if line == "drying completed":#check if ack is recieved
                        home_message.value = "Drying completed"
                        app.update()
                        extend_drying()#Call method extend drying process
                    
    else:
        process_message.value = ""
        Fan_speed.value = 0
        app.error("Exiting..", "Okay bye...")
        app.show()
        
def response_message(value): #Serial communication to wait for message from arduino
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            if(line == value):
                print(line)
                return line  
            
def start_sterilizing():
    confirm_message = app.yesno("Confirm", "Do you want run process?")
    if confirm_message == True:
        ser.write("process2\n".encode('utf-8'))#Write to arduino to start process 2
        line = ser.readline().decode('utf-8').rstrip()#Awaiting ack from arduino to start process 
        if line == "ok":#Check if ack is recieved 
            ser.flush()
            home_message.value = "Sterilizing..."
            app.update()
            line = response_message("sterilization completed")#awaiting ack from arduino on the completion 
            if line == "sterilization completed":#check if ack is received
                home_message.value = "Drying..."
                app.update()
                ser.write("2\n".encode('utf-8'))#Send duration command to arduino to start drying
                line = response_message("drying completed")#awaiting ack on completion
                if line == "drying completed":
                    home_message.value = "Drying completed"
                    app.update()
                    extend_drying()#Method to extend drying 
                            
    else:
        process_message.value = ""
        Fan_speed.value = 0
        app.error("Exiting..", "Okay bye...")
        app.show()
    
def start_drying():
    confirm_message = app2.yesno("Confirm", "Start drying?")
    if confirm_message == True:

        if Fan_speed.value is "0":#check for invalid user input duration 
            app2.warn("Warning", "Please enter the drying duration!")
        else:
            string_fan = str(Fan_speed.value) + "\n"
            ser.write(string_fan.encode('utf-8'))
            countdown(int(Fan_speed.value))
                
    
def close_app2():
    confirm_message = app.yesno("Confirm", "Do you want end process?")
    if confirm_message == True:
        process_message.value = ""
        Fan_speed.value = 0
        app2.hide()
        home_message.value = "Process completed!"
        app.show()

def countdown(t):
    
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        #timer_message.value = "Drying process running.."
        print(timer, end="\r")
        #app2.info("Timer", "Drying will end in " + timer)
        process_message.value = "Process running at " + timer + "secs"
        app2.update()
        time.sleep(1)
        t -= 1
      
    process_message.value = "Process completed"
    extend_drying()
    
def extend_drying():#process to extend drying duration 
    confirm_message = app2.yesno("Process completed", "Process completed! Extend drying time? ")
    if confirm_message == True:
        home_message.value = "Drying running..."
        app.hide()
        app2.show()
        process_message.value = ""
        Fan_speed.value = 0
        
    else:
        ser.write("0\n".encode('utf-8'))
        home_message.value = "Process completed!"
        process_message.value = ""
        Fan_speed.value = 0
        app2.error("Exiting..", "Okay bye...")
        app2.hide()
        app.show()
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        
    
#User Interface design for app and app1
form_box = Box(app, layout="grid", width="fill", align="form_box", border=True)
syringe = Text(form_box, text="Enter the number of Syringe", grid=[0,0], size=20, font="Times new roman", align="left")
slider_Syringe = Slider(form_box, start=1, end=6, grid=[1,0], height=30, width=430, align="left")
slider_Syringe.bg = "#DCDCDC"
select = Text(form_box, text="Select the process", grid=[0,1], size=20, font="Times new roman", align="left")
process_choice = Combo(form_box, grid=[1,1], options=["Wash and Sterilize", "Sterilizing"], height=3, width=40, align="left")
process_choice.font = "Times new roman"
process_choice.text_size = "17"
process_choice.bg = "#DCDCDC"
form_box3 = Box(app, layout="grid", width="fill", align="form_box", border=True)
form_box3.bg = "#191970"
home_message = Text(form_box3, text="Welcome", size=40, grid=[0,0], font="Times new roman", color="white", align="top")

form_box2 = Box(app2, layout="grid", width="fill", align="form_box", border=True)
fan = Text(form_box2, text="Select the duration for cleaning", grid=[0,0], size=20, font="Times new roman", align="left")
Fan_speed = Combo(form_box2, options=[0, 5, 10], grid=[1,0],height=2, width=30, align="right")
Fan_speed.font = "Times new roman"
Fan_speed.text_size = "15"
Fan_speed.bg = "#DCDCDC"

form_box4 = Box(app2, layout="grid", width="fill", align="form_box", border=True)
form_box4.bg = "#191970"
process_message = Text(form_box4, text="", size=40, grid=[0,0], font="Times new roman", color="white", align="top")

start = PushButton(app, command=selection, text="Start", height = "3", width = "20", align="bottom")
start.text_size =30
start.text_color ="Red"
start.bg = "#B0C4DE"
end_process = PushButton(app2, command=close_app2, text="End process", width=40, height=5, align="bottom")
end_process.text_size =15
end_process.text_color ="Red"
end_process.bg = "#B0C4DE"
start_drying = PushButton(app2, command=start_drying, text="Start Drying", width=40, height=5, align="bottom")
start_drying.text_size =15
start_drying.text_color ="Red"
start_drying.bg = "#B0C4DE"

app.display()
