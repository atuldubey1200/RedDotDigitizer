
# RedDotDigitizer

**RedDotDigitizer** is a Python-based GUI application designed to digitize data points from graph images. It enables users to load or paste an image of a plot, calibrate both axes, interactively place red dots to mark data points, adjust them by dragging, and export the extracted real-world coordinates to a CSV file.

This tool is especially useful for researchers, engineers, and students who need to retrieve numerical data from printed or scanned plots, journal figures, or legacy graphs.

---

## ✨ Features

- 📁 Load image from file or 📋 paste from clipboard
- 📏 Manual calibration of X and Y axes using real-world values
- 🔴 Drop and drag red dot markers to digitize data
- 🔗 Automatic red line connecting all data points
- ↩️ Delete last point to undo mistakes
- 💾 Export digitized data to `.csv`

---

## 🖥️ Demo Workflow

1. **Load or Paste Graph Image**  
   Load a `.png`, `.jpg`, `.bmp`, etc., or paste directly from clipboard.

2. **Calibrate Axes**  
   - Click "Calibrate X" and mark two points on the X-axis; enter their real X values.
   - Click "Calibrate Y" and mark two points on the Y-axis; enter their real Y values.

3. **Start Data Extraction**  
   - Click on the graph to drop red dots at desired data points.
   - 🔄 **Red dots are draggable**: click and drag any red dot to reposition it.
   - The program automatically updates the real X, Y values and redraws the connecting line.

4. **Delete Last Point**  
   Click "Delete Last Point" if you make a mistake.

5. **Save CSV**  
   Once finished, export all (X, Y) values by clicking "Save CSV".

---

## 📦 Requirements

This program requires the following Python libraries:

- `matplotlib`
- `pillow`
- `pandas`
- `tkinter` (comes pre-installed with most Python distributions)

---

## 💡 Quick Install Tip

If you are new to Python or face import errors, open your terminal or command prompt and run:

```bash
!pip install matplotlib pillow pandas
```

This will install all necessary libraries at once.

---

## 🚀 Run the Program

Save the file as `red_dot_digitizer.py` and execute:

```bash
python red_dot_digitizer.py
```

> 💻 If you're using **Spyder**, make sure to run the script in the **IPython Console** and not the regular Editor-only run mode. GUI programs using `tkinter` require a console that supports event loops.

---

## 📁 Output Format

When you save the CSV, the file contains two columns:

```
X,Y
12.45, 3.67
13.89, 4.01
...
```

These are the real-world coordinates after calibration and dot placement.

---

## 📚 Use Cases

- Extracting data from scanned scientific plots
- Recovering numerical values from journal articles
- Educational use for digital lab reports
- Reconstructing missing experimental data

---

## 📄 License

MIT License © 2025 [Atul Kumar Dubey](https://github.com/yourusername)

---

## 🤝 Contributions

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

---

## 💬 Questions?

Feel free to raise issues in the GitHub repo or contact the developer directly.
