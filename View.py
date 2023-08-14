#! python
# -*- coding: utf-8 -*-

# GUI fuer Thermosycler 

from tkinter import *
#from tkinter.tix import *
from PIL import Image, ImageTk
from Controller import *
from threading import *
import atexit
import time
import logging
import pickle
import sys

data = ""

class Gui():
    def __init__(self, root):
        """Do GUI stuff and attach to ObserverPattern"""
        self.root = root
        #label_frame = Frame(root, height = 100, width=200, borderwidth=3, relief=RIDGE)
        #label_frame.place (x= 550, y = 300)
        #tip = Balloon(root)
        #tip.bind_widget(witghet, balloonmsg="The time of Medium-1")
        #self.label_com_status = Label(root, text="False", relief = GROOVE, fg = "red", width = 6)
        #self.canvas = Canvas(root, width=250, height=250)
        #img = ImageTk.PhotoImage(Image.open("WatersystemSmall.png").resize((250, 250), Image.ANTIALIAS))
        #self.canvas.background = img  # Keep a reference in case this code is put in a function.
        #bg = self.canvas.create_image(0, 0, anchor=NW, image=img)
        #self.canvas.place (x= 170, y = 400)

        #Root Window
        self.root.title ("Thermocycling")
        self.root.geometry("1100x700+0+0")
        #Menu
        self.menu =     Menu(root)
        self.filemenu = Menu(self.menu)
        self.filemenu.add_command(label="Sichern", command = self.connection_status_changed)
        self.filemenu.add_command(label="Laden", command = self.connection_status_changed)
        self.filemenu.add_command(label="Beenden", command = self.connection_status_changed)
        self.menu.add_cascade(label="Datei",menu = self.filemenu)
        self.root.config(menu=self.menu)
        
        #*************************  Left  ******************************
        self.label_kalt_warm =          Label(root, text="Kalt-Warm-Zyklen")
        self.label_reinigungszeit =     Label(root, text="Reinigungszeit")
        self.label_dauer =              Label(root, text="Dauer", relief=GROOVE)
        self.label_dauer_links =        Label(root, text="Links")
        self.label_dauer_rechts =       Label(root, text="Rechts")
        self.label_solltemp =           Label(root, text="Solltemperatur erfassen - für Auswertung", relief=GROOVE)
        self.label_solltemp_links =     Label(root, text="Links")
        self.label_solltemp_rechts =    Label(root, text="Rechts")
        self.label_optional =           Label(root, text="Optional", relief=GROOVE)
        self.label_logfile =            Label(root, text="Logfile erstellen, Dateiname")
        self.label_bericht =            Label(root, text="Bericht per E-mail senden an")
        #Entries
        self.entry_zyklen =             Entry(root, width = 10)
        self.entry_reinigungszeit =     Entry(root, width = 10)
        self.entry_dauer_links =        Entry(root, width = 10)
        self.entry_dauer_rechts =       Entry(root, width = 10)
        self.entry_solltemp_links =     Entry(root, width = 10)
        self.entry_solltemp_rechts =    Entry(root, width = 10)
        self.entry_logfile =            Entry(root, width = 30)
        self.entry_email =              Entry(root, width = 30)
        #Units
        self.label_einheit_zyklen =     Label(root, text="1-1000")   
        self.label_einheit_reinigung =  Label(root, text="Sek.")
        self.label_einheit_dauer_L =    Label(root, text="Sek.")
        self.label_einheit_dauer_R =    Label(root, text="Sek.")
        self.label_einheit_temp_L =     Label(root, text="°C")
        self.label_einheit_temp_R =     Label(root, text="°C")
        self.label_einheit_dateiendung =Label(root, text=".log")
        #Buttons
        self.button_start =               Button(root, text="Start",     fg="blue",command=self.start_test, width = 20)
        self.button_abbrechen =           Button(root, text="Abbrechen", fg="red" ,command=self.start_test, width = 20)

        #***  Place label Left  ***
        space = 40
        self.label_kalt_warm.place           (x= 10,  y = space*1)
        self.label_reinigungszeit.place      (x= 10,  y = space*2)
        self.label_dauer.place               (x= 10,  y = space*3)
        self.label_dauer_links.place         (x= 10,  y = space*4)
        self.label_dauer_rechts.place        (x= 250, y = space*4)
        self.label_solltemp.place            (x= 10,  y = space*5)
        self.label_solltemp_links.place      (x= 10,  y = space*6)
        self.label_solltemp_rechts.place     (x= 250, y = space*6)
        self.label_optional.place            (x= 10,  y = space*7)
        self.label_logfile.place             (x= 10,  y = space*8)
        self.label_bericht.place             (x= 10,  y = space*9)
        #Entries
        self.entry_zyklen.place              (x= 150, y = space*1)
        self.entry_reinigungszeit.place      (x= 150, y = space*2)
        self.entry_dauer_links.place         (x= 100, y = space*4)
        self.entry_dauer_rechts.place        (x= 350, y = space*4)
        self.entry_solltemp_links.place      (x= 100, y = space*6)
        self.entry_solltemp_rechts.place     (x= 350, y = space*6)
        self.entry_logfile.place             (x= 200, y = space*8)
        self.entry_email.place               (x= 200, y = space*9)
        #Units
        self.label_einheit_zyklen.place      (x= 250, y = space*1)
        self.label_einheit_reinigung.place   (x= 250, y = space*2)
        self.label_einheit_dauer_L.place     (x= 200, y = space*4)
        self.label_einheit_dauer_R.place     (x= 450, y = space*4)
        self.label_einheit_temp_L.place      (x= 200, y = space*6)
        self.label_einheit_temp_R.place      (x= 450, y = space*6)
        self.label_einheit_dateiendung.place (x= 450, y = space*8)
        #Buttons
        self.button_start.place              (x= 10, y = space*10)
        self.button_abbrechen.place          (x= 250, y = space*10)
               
        #*************************  Right  ******************************   
        self.label_messwerte =          Label(root, text="Aktuelle Messwerte" , relief=GROOVE)
        self.label_temperatur =         Label(root, text="Temperatur", relief=GROOVE)        
        self.label_probenbehaelter =    Label(root, text="Probenbehaelter")
        self.label_isttemp_L =          Label(root, text="Links")
        self.label_isttemp_R =          Label(root, text="Rechts")
        self.label_abg_zyklen =         Label(root, text="Abgeschlossene Zyklen")
        self.label_verlauf =            Label(root, text="Verlauf", relief=GROOVE)
        #Label measurements
        self.label_messwert_proben =    Label(root, text="24.1", relief = GROOVE, fg = "green", width = 6)
        self.label_messwert_temp_L =    Label(root, text="25.2", relief = GROOVE, fg = "green", width = 6)
        self.label_messwert_temp_R =    Label(root, text="26.3", relief = GROOVE, fg = "green", width = 6)
        self.label_messwert_zyklen =    Label(root, text="0030", relief = GROOVE, fg = "green", width = 6)
        #Textbox
        self.text_verlauf =             Text(root, width=30, height=4)
        #Units
        self.label_ein_mess_temp_proben =Label(root, text="°C")
        self.label_ein_mess_temp_L =     Label(root, text="°C")
        self.label_ein_mess_temp_R =     Label(root, text="°C")   

        #****  Place Right ***
        self.label_messwerte.place           (x= 600, y = space*1)
        self.label_temperatur.place          (x= 600, y = space*2)       
        self.label_probenbehaelter.place     (x= 600, y = space*3)
        self.label_isttemp_L.place           (x= 600, y = space*4)
        self.label_isttemp_R.place           (x= 800, y = space*4)
        self.label_abg_zyklen.place          (x= 600, y = space*5)
        self.label_verlauf.place             (x= 600, y = space*6)
        #Label measurements
        self.label_messwert_proben.place     (x= 800, y = space*3)
        self.label_messwert_temp_L.place     (x= 700, y = space*4)
        self.label_messwert_temp_R.place     (x= 900, y = space*4)
        self.label_messwert_zyklen.place     (x= 800, y = space*5)
        #Textbox
        self.text_verlauf.place              (x= 600, y = space*7)
        #Units
        self.label_ein_mess_temp_proben.place(x= 900, y = space*3)
        self.label_ein_mess_temp_L.place     (x= 750, y = space*4)
        self.label_ein_mess_temp_R.place     (x= 950, y = space*4)  
        #Picture
        self.canvas = Canvas(root, width=450, height=250)
        img = ImageTk.PhotoImage(Image.open("WatersystemSmall.png").resize((450, 250), Image.ANTIALIAS))
        self.canvas.background = img  # Keep a reference in case this code is put in a function.
        bg = self.canvas.create_image(0, 0, anchor=NW, image=img)
        self.canvas.place (x= 600, y = 400)

        root.bind('<Motion>',self.mouse)

        self.controller = Controller()
        self.controller.attach(Controller.EVT_CONNECTION_STATUS, self.connection_status_changed)
  
    def mouse(self, e):
        x= e.x
        y= e.y
        print("Pointer is currently at %d, %d" %(x,y))

    def cleanup(self):
        """Close UART and Close GUI"""
        print("Clean-Up")
        self.uart.close()
        self.root.destroy()

    def start_test(self):
        print("view")
        self.controller.start_test(True)

    def connection_status_changed(self, status):
        """Set Connect/Disconect Button State"""
        if status:
            self.button_start.configure(state = DISABLED)
           
        else:
            self.button_start.configure(state = NORMAL)


if __name__ == "__main__":

    root=Tk()
    gui = Gui(root)
    atexit.register(gui.cleanup)
    root.mainloop()

