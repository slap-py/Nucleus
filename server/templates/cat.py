import tkinter as tk

window = tk.Tk()

def uplink():
  toUplink = data.get()
  data.set('')
  submit['state'] = tk.DISABLED



nbL = tk.Label(text="NEBULUS EMERGENCY SERVICE")
nbL.pack()

data = tk.Entry()
data.pack()

submit = tk.Button(text="UPLINK MESSAGE",command=uplink)
submit.pack()
window.mainloop()