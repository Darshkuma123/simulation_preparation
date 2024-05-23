import asyncio
import tkinter
import time
from random import randint
import pika as pk
from tkinter import *
import threading
import pymongo.mongo_client
from xmlschema_design import load_schema
from tkinter import messagebox
from pubsub import sub
from tkinter import filedialog,ttk
import generator as gen
import line as li
import Iso
import load
import feeder
import transformer
import network as nk
import xml.etree.ElementTree as ET
import os
import pymongo
from asyncua import Client
global host
global port
global network_para
attributes={"Generator":"GeneratorAttribute","line":"LineAttributes"}
Generation_dict={}
lines_dict={}
iso_dict={}
load_dict={}
transformer_dict={}
Feeder_dict={}
# #tkinter(screenName="Substation",  baseName=None,  className=None,  useTk=1)
m= tkinter.Tk()
m.title("substation display")
m.config(width=400,height=200)
# button=tkinter.Button(m,text="host", width=25)
# button.pack()
url = "opc.tcp://localhost:4840/freeopcua/server/"
namespace = "http://examples.freeopcua.github.io"
# t=Label(m,text="ip").place(x=0,y=100)
# s=Label(m,text="host").place(x=0,y=200)
# e1=Entry(m)
# e2=Entry(m)
# e1.place(x=20,y=100)
# e2.place(x=30,y=200)
db=pymongo.MongoClient("localhost", 27017)
db_network=db["network"]
get_network_values=db_network["Network_values"]
selection_menu=ttk.Combobox(state="readonly",values=["Network","OPC","61850 suite"])
selection_menu.place(x=20,y=20)
print(selection_menu.get())

def browsefiles():
    filename= filedialog.askopenfile(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files","*.txt"),("all files","*.*")))
    r=m.configure(text="File Opened: "+filename)
def fourth_window(event):
    fourth= tkinter.Tk()
    fourth.config(width=600,height=600)
    close_button= tkinter.Button(fourth,text="clost", command=fourth.destroy)
    close_button.place(x=200,y=200)

def Network():
    load_network()
    nw= tkinter.Tk()
    #nw.geometry(str(network_para.get_x())+'x'+str(network_para.get_y()))
    nw.title("input result")
    nw.resizable(False,False)
    canvas= Canvas(nw,width=int(500),height=int(500))
    canvas.bind("<Button-1>",positon)
    if len(Generation_dict)>0:
        # canvas.create_rectangle(x=float(Generation.get_x),y=float(Generation.get_y),120, 80,
        #     outline="#fb0", fill="#fb0")
        for key,value in Generation_dict.items():
            generator=canvas.create_oval(float(value.x),float(value.y),float(value.length),float(value.width),outline = "black",fill = "white",width = 2,tags=key)
            canvas.tag_bind(generator,"<Button-1>", change_color)
            canvas.create_text(99,112,text="Generator_0")
    if len(lines_dict)>0:
        for key,value in lines_dict.items():
            lines= canvas.create_line(float(value.x),float(value.y),float(value.length),float(value.width),fill = "white",width = 2,tags=key)
            canvas.tag_bind(lines,"<Button-1>",info2)
    if len(iso_dict)>0:
        for key,value in iso_dict.items():
            iso=canvas.create_rectangle(float(value.x),float(value.y),float(value.length),float(value.width),outline = "black",fill = "white",width = 2,tags=key)
            canvas.tag_bind(iso,"<Button-1>",info2)
    if len(Feeder_dict)>0:
        for key,value in Feeder_dict.items():
            feeder_line= canvas.create_line(float(value.x),float(value.y),float(value.length),float(value.width),fill = "white",width = 2,tags=key)
            canvas.tag_bind(feeder_line,"<Button-1>",info2)
            
    if len(load_dict)>0:
        for key,value in load_dict.items():
            load_element=canvas.create_rectangle(float(value.x),float(value.y),float(value.length),float(value.width),outline = "black",fill = "white",width = 2,tags=key)
            canvas.tag_bind(load_element,"<Button-1>",lambda event: getting_canvas(canvas,event))
            canvas.create_text(119,478,text=key)
    if len(transformer_dict)>0:
        for key,value in transformer_dict.items():
            transformer_element=canvas.create_oval(float(value.x),float(value.y),float(value.length),float(value.width),outline = "black",fill = "white",width = 2,tags=key)
            canvas.tag_bind(transformer_element,"<Button-1>",lambda event: getting_canvas(canvas,event))
            canvas.create_text(103,297,text=key)
    close=tkinter.Button(canvas,text="close",command=nw.destroy)        
    canvas.create_text(86,349,text="Bus_2")
    canvas.create_text(255,299,text="Bus_1")
    canvas.create_text(75,223,text="Bus_0")
    close.place(x=337,y=28)
    start_button= tkinter.Button(nw,text="start",command=load_data)
    start_button.place(x=250,y=150)
    canvas.pack()


def getting_canvas(canvas,event):
    print()
    print(event)
    print(canvas)
    print(canvas.gettags("current"))
    current_tag=canvas.gettags("current")
    canvas.itemconfig(current_tag[0],fill='green')


def positon(event):
    print(str(event.x)+" "+str(event.y))
def info2(event):
    print()
    print(event)
    
    messagebox.showinfo("hello","line")

def change_color(event):
    print()
    print(event)
    messagebox.showinfo("hello","hello")
def IEC_61850():
    nw= tkinter.Tk()
    #nw.geometry(str(network_para.get_x())+'x'+str(network_para.get_y()))
    nw.title("input result")
    nw.resizable(False,False)
    canvas= Canvas(nw,width=int(500),height=int(500))
    canvas.bind("<Button-1>",positon)
    loaded_schema= load_schema.Load()
    #print(loaded_schema)
    transformer=loaded_schema['TransFormer']
    genera=loaded_schema['Generator']
    line=loaded_schema['line']
    iso=loaded_schema['ISO']
    feeder=loaded_schema['Feeder']
    Load= loaded_schema['Load']
    if len(genera)>0:
        for g in genera:
            generator=canvas.create_oval(float(g["positionX"][0]),float(g["positionY"][0]),float(g["positionLength"][0]),float(g["positionWidth"][0]),outline = "black",fill = "white",width = 2,tags=g['@id'])
            canvas.tag_bind(generator,"<Button-1>", change_color)
            canvas.create_text(80,108,text="Generator_0")
    if len(line)>0:
        for li in line:
            #print(li['@id'])
            liine_component= canvas.create_line(float(li["positionX"][0]),float(li["positionY"][0]),float(li["positionLength"][0]),float(li["positionWidth"][0]),fill = "white",width = 2,tags=li['@id'])
            canvas.tag_bind(liine_component,"<Button-1>",info2)
    if len(iso)>0:
        for i in iso:
            iso_component=canvas.create_rectangle(float(i["positionX"][0]),float(i["positionY"][0]),float(i["positionLength"][0]),float(i["positionWidth"][0]),outline = "black",fill = "white",width = 2,tags="ISO_"+i['@id'])
            canvas.tag_bind(iso_component,"<Button-1>",lambda event: getting_canvas(canvas,event))
    if len(feeder)>0:
        for f in feeder:
            feeder_line= canvas.create_line(float(f["positionX"][0]),float(f["positionY"][0]),float(f["positionLength"][0]),float(f["positionWidth"][0]),fill = "white",width = 2,tags=f['@id'])
            canvas.tag_bind(feeder_line,"<Button-1>",info2)
    if len(Load)>0:
        for L in Load:
            load_element=canvas.create_rectangle(float(L["positionX"][0]),float(L["positionY"][0]),float(L["positionLength"][0]),float(L["positionWidth"][0]),outline = "black",fill = "white",width = 2,tags="Load_"+L['@id'])
            canvas.tag_bind(load_element,"<Button-1>",lambda event: getting_canvas(canvas,event))
            canvas.create_text(94,478,text="Load_0")
    if len(transformer)>0:
        for g in transformer:
            generator=canvas.create_oval(float(g["positionX"][0]),float(g["positionY"][0]),float(g["positionLength"][0]),float(g["positionWidth"][0]),outline = "black",fill = "white",width = 2,tags=g['@id'])
            canvas.tag_bind(generator,"<Button-1>", change_color)
            canvas.create_text(72,287,text="Transformer_4")
            #canvas.create_text(103,297,text=g['@id'])
        

    canvas.create_text(261,349,text="Bus_2")
    canvas.create_text(73,326,text="Bus_1")
    canvas.create_text(75,223,text="Bus_0")
    stop_button=tkinter.Button(nw,text="close",command=nw.destroy)
    stop_button.place(x=250,y=180)
    label_time_now = Label(canvas)
    label_time_now.place(x=20, y=60)
    start_button= tkinter.Button(nw,text="start",command=load_iec61850)
    start_button.place(x=250,y=150)
    canvas.pack()

async def OPC():
    async with Client(url=url) as client:
        # Find the namespace index
        nsidx = await client.get_namespace_index(namespace)
        print(f"Namespace Index for '{namespace}': {nsidx}")

        # Get the variable node for read / write
        var = await client.nodes.root.get_child(
            f"0:Objects/{nsidx}:MyObject/{nsidx}:MyVariable"
        )
        value = await var.read_value()
        print(f"Value of MyVariable ({var}): {value}")

        new_value = value - 50
        print(f"Setting value of MyVariable to {new_value} ...")
        await var.write_value(new_value)

        # Calling a method
        res = await client.nodes.objects.call_method(f"{nsidx}:ServerMethod", 5)
        print(f"Calling ServerMethod returned {res}")
    pass

def load_iec61850():
    load_data_display=tkinter.Tk()
    load_data_display.title("input result")
    load_data_display.resizable(True,True)
    canvas1_load_data= Canvas(load_data_display,width=int(1000),height=int(500))
    process_input=[]
    tree_load_data= ttk.Treeview(canvas1_load_data, column=("time","attribute","value"),show='headings',height=30)
    tree_load_data.column('#1',anchor=CENTER)
    tree_load_data.heading('#1',text="time")
    tree_load_data.column('#2',anchor=CENTER)
    tree_load_data.heading('#2',text='attribute Name')
    tree_load_data.column('#3',anchor= CENTER)
    tree_load_data.heading('#3',text="value")
    db=pymongo.MongoClient("localhost", 27017)
    db_network=db["network"]
    get_network_values=db_network["iec61850"]
    queried_json=get_network_values.find().sort({"timestamp":pymongo.DESCENDING}).limit(1)
    query_list=list(queried_json)
    time_stamp=query_list[0]['timestamp']
    filtered_values=get_network_values.find({"timestamp":time_stamp})
    v=list(filtered_values)
    #tree.pack()
    for f in v:
        tree_load_data.insert('',tkinter.END,text=f['attribute'],values=(f['timestamp'],"SampleNetwork/MMXU."+f['attribute'],f['value']),iid=f['attribute'])
        print(str(f['timestamp'])+" "+str(f['attribute']))

    close=tkinter.Button(tree_load_data,text="close",command=load_data_display.destroy)
    refresh=tkinter.Button(tree_load_data,text="refresh",command=lambda: update_iec61850_table(tree_load_data))
    tree_load_data.get_children()
    tree_load_data.pack()
    tree_load_data.after(10000,load_iec61850)
    close.place(x=0,y=500)
    refresh.place(x=100,y=500)
    # with open("/Users/darshankumar/Documents/Python AI/simulation_preparation/pubsub/output_iec61850.txt",'r') as output:
    #     result=output.readlines()
    #     if len(result)>0:
    #         for r in result:
    #             body=str(r)
    #             body=body.replace('b','')
    #             body=body.replace('"','')
    #             process_input=body.split(',')
    # e = Entry(canvas1, width=20, fg='blue',
    #                        font=('Arial',16,'bold'))
    # j=0
    # for i in range(0,len(process_input)):
    #     e=Text(canvas1, width=60, height=1) 
    #     e.grid(row=i,column=0)
    #     name=process_input[i].split(':')
    #     e.insert(INSERT,"SampleNetwork/MMXU."+name[0].replace('b','').replace('{','').replace("'",'').strip())
    # for j in range(0,len(process_input)):
    #     e=Text(canvas1, width=60, height=1) 
    #     e.grid(row=j,column=1)
    #     name=process_input[j].split(':')

    #     e.insert(INSERT,name[1].replace('}',''))

    # start_button= tkinter.Button(canvas1,text="refresh",command=load_data)
    # start_button.place(x=250,y=150)
    canvas1_load_data.pack()
def update_iec61850_table(tree):
    db=pymongo.MongoClient("localhost", 27017)
    db_network=db["network"]
    get_network_values=db_network["iec61850"]
    queried_61850_json=get_network_values.find().sort({"timestamp":pymongo.DESCENDING}).limit(1)
    query_list=list(queried_61850_json)
    time_stamp=query_list[0]['timestamp']
    filtered_values=get_network_values.find({"timestamp":time_stamp})
    v=list(filtered_values)
    for f in v:
        tree.item(f['attribute'],text=f['attribute'],values=(f['timestamp'],"SampleNetwork/MMXU."+f['attribute'],f['value']))
    tree.pack()
    #tree.after(10000,update_network_table(tree))
    #tree.after(10000,update_network_table(tree))
    # thread= threading.Thread(target=update_value,args=tree)
    # thread.start()
    pass
def load_data():
    queried_json=[]
    load_data_display=tkinter.Tk()
    load_data_display.title("input result")
    load_data_display.resizable(False,False)
    canvas1_load_data= Canvas(load_data_display,width=int(500),height=int(500))
    process_input=[]
    tree_load_data= ttk.Treeview(canvas1_load_data, column=("time","attribute","value"),show='headings',height=30)
    tree_load_data.column('#1',anchor=CENTER)
    tree_load_data.heading('#1',text="time")
    tree_load_data.column('#2',anchor=CENTER)
    tree_load_data.heading('#2',text='attribute Name')
    tree_load_data.column('#3',anchor= CENTER)
    tree_load_data.heading('#3',text="value")
    db=pymongo.MongoClient("localhost", 27017)
    db_network=db["network"]
    get_network_values=db_network["Network_values"]
    queried_json=get_network_values.find().sort({"timestamp":pymongo.DESCENDING}).limit(1)
    query_list=list(queried_json)
    time_stamp=query_list[0]['timestamp']
    filtered_values=get_network_values.find({"timestamp":time_stamp})
    v=list(filtered_values)
    #tree.pack()
    for f in v:
        tree_load_data.insert('',tkinter.END,text=f['attribute'],values=(f['timestamp'],f['attribute'],f['value']),iid=f['attribute'])
        print(str(f['timestamp'])+" "+str(f['attribute']))

    close=tkinter.Button(tree_load_data,text="close",command=load_data_display.destroy)
    refresh=tkinter.Button(tree_load_data,text="refresh",command=lambda: update_network_table(tree_load_data))
    tree_load_data.get_children()
    tree_load_data.pack()
    #tree_load_data.after(10000,update_network_table(tree_load_data))
    close.place(x=0,y=500)
    refresh.place(x=100,y=500)
    # with open("/Users/darshankumar/Documents/Python AI/simulation_preparation/pubsub/output.txt",'r') as output:
    #     result=output.readlines()
    #     if len(result)>0:
    #         for r in result:
    #             body=str(r)
    #             body=body.replace('b','')
    #             body=body.replace('"','')
    #             process_input=body.split(',')
    # e = Entry(canvas1, width=20, fg='blue',
    #                        font=('Arial',16,'bold'))
    # j=0
    # for i in range(0,len(process_input)):
    #     e=Text(canvas1, width=60, height=1) 
    #     e.grid(row=i,column=0)
    #     name=process_input[i].split(':')
    #     e.insert(INSERT,"SampleNetwork_"+name[0].replace('b','').replace('{','').replace("'",'').strip())
    # for j in range(0,len(process_input)):
    #     e=Text(canvas1, width=60, height=1) 
    #     e.grid(row=j,column=1)
    #     name=process_input[j].split(':')

    #     e.insert(INSERT,name[1].replace('}',''))

    # start_button= tkinter.Button(canvas1,text="refresh",command=load_data)
    # start_button.place(x=250,y=150)
    
    canvas1_load_data.pack()
# def update():
#     print("started listening")
#     Connection= pk.BlockingConnection(pk.ConnectionParameters(host='localhost'))
#     channel= Connection.channel()
#     channel.queue_declare(queue='network')
#     for method_frame, properties, body in channel.consume('network'):
#         print(str(body))
#     channel.close()
#     Connection.close()

#     num=0
    # while num<10:

    #     channel.start_consuming()
    #     num=num+1
    # num=0
    # while num<100:
    #     label_time_now['text']=randint(0,1000)
    #     canvas.after(1000,canvas.update())
    #     num=num+1
    
    # # raw_TS = datetime.now(IST)
    # # date_now = raw_TS.strftime("%d %b %Y")
    # # time_now = raw_TS.strftime("%H:%M:%S %p")
    # # formatted_now = raw_TS.strftime("%d-%m-%Y")
    # label_time_now.config(text = "Update")
    # # label_date_now.after(500, update_clock)
    # label_time_now.config(text = time_now)
    # label_time_now.after(1000, str(i=i+1))
    # return formatted_now
    pass

def update_network_table(tree):

    queried_json=get_network_values.find().sort({"timestamp":pymongo.DESCENDING}).limit(1)
    query_list=list(queried_json)
    time_stamp=query_list[0]['timestamp']
    filtered_values=get_network_values.find({"timestamp":time_stamp})
    v=list(filtered_values)
    for f in v:
        tree.item(f['attribute'],text=f['attribute'],values=(f['timestamp'],f['attribute'],f['value']))
    tree.pack()
    #tree.after(10000,update_network_table(tree))
    #tree.after(10000,update_network_table(tree))
    # thread= threading.Thread(target=update_value,args=tree)
    # thread.start()
    pass

def start_callback(ch,method,properties, body):
        print(body)
        #display(body)
        nw=tkinter.Tk()
        nw.title("input result")
        nw.resizable(False,False)
        canvas1= Canvas(nw,width=int(500),height=int(500))
        canvas1.pack()

        # body=str(body)
        # body=body.replace('b','')
        # body=body.replace('"','')
        # process_input=body.split(',')

        # # e = Entry(canvas1, width=20, fg='blue',
        # #                    font=('Arial',16,'bold'))
        # # for i in range(len(process_input)):
        # #     e.grid(row=i,column=0)
        # #     e.insert(END,process_input[i][0])
        # canvas1.pack()
        # print()

        # for i in range(total_rows):
        #     for j in range(total_columns):
                 
        #         self.e = Entry(root, width=20, fg='blue',
        #                        font=('Arial',16,'bold'))
                 
        #         self.e.grid(row=i, column=j)
        #         self.e.insert(END, lst[i][j])
        #print(body)
def display(body):
    nw=tkinter.Tk()
    nw.title("input result")
    nw.resizable(False,False)
    canvas1= Canvas(nw,width=int(500),height=int(500))

    body=str(body)
    body=body.replace('b','')
    body=body.replace('"','')
    process_input=body.split(',')

        # e = Entry(canvas1, width=20, fg='blue',
        #                    font=('Arial',16,'bold'))
        # for i in range(len(process_input)):
        #     e.grid(row=i,column=0)
        #     e.insert(END,process_input[i][0])
    canvas1.pack()
    print()

def start_simulation():
    messagebox.showinfo("started simulatiom","simulate")

def stop_simulation():
    messagebox.showinfo("started simulatiom","stopped")

def connect_to_db():
    client = pymongo.MongoClient("localhost", 27017)
    db = client.list_database_names()
    print(db)
    
def load_network():
    global network_para
    global Generation
    print(os.getcwd())
    networkpath=os.path.join("/Users/darshankumar/Documents/Python AI/simulation_preparation","sample_network.xml")
    network=ET.parse(networkpath)
    root=network.getroot()
    if root.tag=="Network":
        network_para=nk.NetWork(root.attrib['Id'],root.attrib['Length'],root.attrib['width'])
    for child in root:
        print(child.tag,child.attrib)
        result =attributes.get(child.tag)
        if child.tag=="Generator":
            Generation=gen.Generation(child.attrib['Id'],child.attrib['X'],child.attrib['Y'],child.attrib['Length'],child.attrib['width'])
            #print("generation id "+ str(Generation.get_id()))
            Generation_dict['Generator_'+str(child.attrib['Id'])]=Generation
        if child.tag=="line":
            line=li.Line(id=child.attrib['Id'],x=child.attrib['X'],y=child.attrib['Y'],length=child.attrib['Length'],width=child.attrib['width'])
            lines_dict["line_"+child.attrib['Id']]=line
        if child.tag=="ISO":
            ISo=Iso.ISO(id=child.attrib['Id'],x=child.attrib['X'],y=child.attrib['Y'], length=child.attrib['Length'],width=child.attrib['width'])
            iso_dict["iso_"+child.attrib['Id']]=ISo
        if child.tag=="Load":
            Load=load.Load(child.attrib['Id'],child.attrib['X'],child.attrib['Y'],child.attrib['Length'],child.attrib['width'])
            load_dict["load_"+child.attrib['Id']]=Load
        if child.tag=="Feeder":
            Feeder=feeder.Feeder(child.attrib['Id'],child.attrib['X'],child.attrib['Y'],child.attrib['Length'],child.attrib['width'])
            Feeder_dict["Feeder_"+child.attrib['Id']]=Feeder
        if child.tag=="TransFormer":
            Feeder=transformer.TransFormer(child.attrib['Id'],child.attrib['X'],child.attrib['Y'],child.attrib['Length'],child.attrib['width'])
            transformer_dict["TransFormer_"+child.attrib['Id']]=Feeder
        if  attributes.get(child.tag) is not None:
            for n in root.iter(result):
                print(n.tag, n.attrib)
def call_back():
    # host=e1.get()
    # port=int(e2.get())
    #browsefiles()
    if selection_menu.get() is not NONE:
        if selection_menu.get()=="Network":
            print("selected: "+selection_menu.get())
            Network()
        elif selection_menu.get()=="OPC":
            print("selected: "+selection_menu.get())
            asyncio.run(OPC())
            pass
        elif selection_menu.get()=="61850 suite":
            print("selected: "+selection_menu.get())
            IEC_61850()

            pass
        else:
            messagebox.showinfo("No selection","Please select a option from the list")
            print("No selection made")

    


    # with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    #     s.connect((host,port))
    #     s.sendall(b"hello world")
    #     data=str(s.recv(1024))
    #     messagebox.showinfo("back info",data)

connect_button= tkinter.Button(m,text="connect",command=connect_to_db)
connect_button.place(x=0,y=100)
enter_button= tkinter.Button(m,text="select",command=call_back)
enter_button.place(x=0,y=150)
m.mainloop()
# print(b"received data is ${data}")

# enter_button= tkinter.Button(m,text="submit",command=call_back)
# enter_button.place(x=0,y=400)
# m.mainloop()
#print(e1.get())

# coords=[(100,100,'x'),(40,30,'y')]

# for c in coords:
#     l=Label(m,text=c[2])
#     l.place(x=c[0],y=c[1])
    
#simulation_preparation

#m.mainloop()


host='127.0.0.1'
port=65432
data=''
# with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
#     s.connect((host,port))
#     s.sendall(b"hello world")
#     data=s.recv(1024)


# print(b"received data is ${data}")