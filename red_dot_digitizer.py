# -*- coding: utf-8 -*-
"""
Created on Fri Jun 13 11:57:24 2025

@author: atuld
"""

import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.lines import Line2D
from PIL import Image, ImageGrab
import pandas as pd

class GraphDigitizerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Graph Digitizer with Calibration and Editing")

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        # Button frame
        btn_frame = tk.Frame(master)
        btn_frame.pack()

        tk.Button(btn_frame, text="Load Image", command=self.load_image).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Paste Image", command=self.paste_image).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Calibrate X", command=self.calibrate_x).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Calibrate Y", command=self.calibrate_y).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Start Data Extraction", command=self.start_extraction).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Delete Last Point", command=self.delete_last_point).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Save CSV", command=self.save_csv).pack(side=tk.LEFT)

        # State
        self.mode = None
        self.image = None
        self.cal_x = []
        self.cal_y = []
        self.points = []  # List of (x_real, y_real, x_pix, y_pix)
        self.circles = []
        self.line = None

        self.x_transform = lambda x: x
        self.y_transform = lambda y: y

        # Events
        self.canvas.mpl_connect('button_press_event', self.on_click)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.canvas.mpl_connect('button_release_event', self.on_release)

        # Dragging state
        self.dragging_index = None

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")])
        if path:
            self.set_image(Image.open(path).convert("RGB"))

    def paste_image(self):
        img = ImageGrab.grabclipboard()
        if isinstance(img, Image.Image):
            self.set_image(img)
        else:
            messagebox.showerror("Error", "No image in clipboard.")

    def set_image(self, img):
        self.image = img
        self.ax.clear()
        self.ax.imshow(img)
        self.canvas.draw()

        self.points.clear()
        self.circles.clear()
        self.cal_x.clear()
        self.cal_y.clear()
        self.line = None

    def calibrate_x(self):
        self.mode = "cal_x"
        messagebox.showinfo("X Calibration", "Click 2 points on X-axis (left to right)")

    def calibrate_y(self):
        self.mode = "cal_y"
        messagebox.showinfo("Y Calibration", "Click 2 points on Y-axis (bottom to top)")

    def start_extraction(self):
        self.mode = "extract"
        messagebox.showinfo("Data Extraction", "Click on the graph to record points. Drag red dots to adjust.")

    def on_click(self, event):
        if event.xdata is None or event.ydata is None:
            return

        x, y = event.xdata, event.ydata

        # Drag selection logic
        if self.mode == "extract":
            for i, circle in enumerate(self.circles):
                if (circle.center[0] - x)**2 + (circle.center[1] - y)**2 < 16:
                    self.dragging_index = i
                    return

        if self.mode == "cal_x":
            self.cal_x.append((x, y))
            self.ax.plot(x, y, 'go')
            self.canvas.draw()
            if len(self.cal_x) == 2:
                x1_pix, x2_pix = self.cal_x[0][0], self.cal_x[1][0]
                if x1_pix == x2_pix:
                    messagebox.showerror("Error", "X calibration points must differ.")
                    self.cal_x.clear()
                    self.redraw()
                    return
                x1_real = float(simpledialog.askstring("X1", "Enter real X for first point:"))
                x2_real = float(simpledialog.askstring("X2", "Enter real X for second point:"))
                self.x_transform = lambda px: x1_real + (px - x1_pix) * (x2_real - x1_real) / (x2_pix - x1_pix)
                messagebox.showinfo("Done", "X calibration complete.")
                self.mode = None

        elif self.mode == "cal_y":
            self.cal_y.append((x, y))
            self.ax.plot(x, y, 'bo')
            self.canvas.draw()
            if len(self.cal_y) == 2:
                y1_pix, y2_pix = self.cal_y[0][1], self.cal_y[1][1]
                if y1_pix == y2_pix:
                    messagebox.showerror("Error", "Y calibration points must differ.")
                    self.cal_y.clear()
                    self.redraw()
                    return
                y1_real = float(simpledialog.askstring("Y1", "Enter real Y for first point:"))
                y2_real = float(simpledialog.askstring("Y2", "Enter real Y for second point:"))
                self.y_transform = lambda py: y1_real + (py - y1_pix) * (y2_real - y1_real) / (y2_pix - y1_pix)
                messagebox.showinfo("Done", "Y calibration complete.")
                self.mode = None

        elif self.mode == "extract":
            real_x = self.x_transform(x)
            real_y = self.y_transform(y)
            self.points.append((real_x, real_y, x, y))
            circle = Circle((x, y), radius=4, color='red', picker=True)
            self.ax.add_patch(circle)
            self.circles.append(circle)
            self.update_line()
            self.canvas.draw()

    def on_motion(self, event):
        if self.dragging_index is None or event.xdata is None or event.ydata is None:
            return
        x, y = event.xdata, event.ydata
        real_x = self.x_transform(x)
        real_y = self.y_transform(y)
        self.points[self.dragging_index] = (real_x, real_y, x, y)
        self.circles[self.dragging_index].center = (x, y)
        self.update_line()
        self.canvas.draw()

    def on_release(self, event):
        self.dragging_index = None

    def delete_last_point(self):
        if self.points:
            self.points.pop()
            self.circles.pop()
            self.update_line()
            self.redraw()

    def update_line(self):
        if not self.points:
            if self.line:
                self.line.remove()
                self.line = None
            return
        xlist = [p[2] for p in self.points]
        ylist = [p[3] for p in self.points]
        if self.line is None:
            self.line = Line2D(xlist, ylist, color='red', linestyle='-', linewidth=1)
            self.ax.add_line(self.line)
        else:
            self.line.set_data(xlist, ylist)

    def redraw(self):
        self.ax.clear()
        self.ax.imshow(self.image)

        # Redraw calibration
        for x, y in self.cal_x:
            self.ax.plot(x, y, 'go')
        for x, y in self.cal_y:
            self.ax.plot(x, y, 'bo')

        # Redraw extracted points
        for circle in self.circles:
            self.ax.add_patch(circle)

        # Redraw line
        self.update_line()

        self.canvas.draw()

    def save_csv(self):
        if not self.points:
            messagebox.showinfo("Empty", "No points to save.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv")
        if path:
            df = pd.DataFrame([(x, y) for x, y, _, _ in self.points], columns=["X", "Y"])
            df.to_csv(path, index=False)
            messagebox.showinfo("Saved", f"{len(df)} points saved to:\n{path}")

# Run app
def main():
    root = tk.Tk()
    app = GraphDigitizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

