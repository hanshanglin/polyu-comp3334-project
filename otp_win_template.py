import time
import math
try:
        import Tkinter as tk
        import tkFont
        import ttk
except  ImportError:  # Python 3
        import tkinter as tk
        import tkinter.font as tkFont
        import tkinter.ttk as ttk

class CircularProgressbar(object):
        def __init__(self, canvas, x0, y0, x1, y1, width=2, start_ang=0, full_extent=360):
            self.custom_font = tkFont.Font(family="Helvetica", size=12, weight='bold')
            self.canvas = canvas
            self.x0, self.y0, self.x1, self.y1 = x0+width, y0+width, x1-width, y1-width
            self.tx, self.ty = (x1-x0) / 2, (y1-y0) / 2
            self.width = width
            self.start_ang, self.full_extent = start_ang, full_extent
            # draw static bar outline
            w2 = width / 2
            self.oval_id1 = self.canvas.create_oval(self.x0-w2, self.y0-w2,
                                                    self.x1+w2, self.y1+w2)
            self.oval_id2 = self.canvas.create_oval(self.x0+w2, self.y0+w2,
                                                   self.x1-w2, self.y1-w2)
        def _get_current_interval():
            sec=int(math.floor(time.time()))
            return sec//TickIntervalSeconds
        
        def _get_current_percent():
            sec=int(math.floor(time.time()))
            return (sec%TickIntervalSeconds)/TickIntervalSeconds
        
        def _get_current_passcode(seed):
            tick=_get_current_interval()
            p=tick*tick*seed % (10**PasscodeLength)
            return p
                
        def start(self, interval=100):
            self.interval = interval
            self.increment = self.full_extent / interval
            self.extent = 0
            self.arc_id = self.canvas.create_arc(self.x0, self.y0, self.x1, self.y1,
                                                start=self.start_ang, extent=self.extent,
                                                width=self.width, style='arc')
            percent = str(_get_current_passcode(seed))
            self.label_id = self.canvas.create_text(self.tx, self.ty, text=percent,
                                                   font=self.custom_font)
            self.canvas.after(interval, self.step, self.increment)

        def step(self, delta):
            self.extent = _get_current_percent()*360
            self.canvas.itemconfigure(self.arc_id, extent=self.extent)

            self.canvas.delete(self.label_id)
            percent = str(_get_current_passcode(seed))
            self.label_id = self.canvas.create_text(self.tx, self.ty, text=percent,
                                                       font=self.custom_font)
            self.canvas.after(self.interval, self.step, delta)



class Application(tk.Frame):
       def __init__(self, master=None):
           tk.Frame.__init__(self, master)
           self.grid()
           self.createWidgets()

       def createWidgets(self):
           self.canvas = tk.Canvas(self, width=200, height=200, bg='white')
           self.canvas.grid(row=0, column=0, columnspan=2)

           self.progressbar = CircularProgressbar(self.canvas, 0, 0, 200, 200, 20)

       def start(self):
           self.progressbar.start()
           self.mainloop()


if __name__ == '__main__':
       app = Application()
       app.master.title('OTP')
       app.start()