# Adobe-Gensolve-Hackathon

Curvetopia: A Journey into the World of Curves
==============================================

Welcome to Curvetopia, where we bring order and beauty to the world of 2D curves! This project aims to identify, regularize, and beautify various types of curves. Dive into the world of curves with us and explore symmetry, completeness, and more.

Project Overview
----------------

**Curvetopia** is designed to work with 2D curves defined by sequences of points. The project involves processing polylines to identify geometric shapes, detect symmetries, and complete curves with natural continuations. The final output includes visualizations in SVG format and analysis results.

### Objective

The mission is to transform a set of polylines into a set of regularized, symmetric, and completed curves. Our focus is on:

1.  **Curve Regularization:** Identifying regular shapes such as lines, circles, ellipses, rectangles, rounded rectangles, polygons, and stars.
    
2.  **Symmetry Detection:** Finding reflection and rotational symmetries in curves.
    
3.  **Curve Completion:** Filling gaps and connecting disjoint parts of curves.
    

### Problem Description

The project starts with an input set of polylines and aims to:

*   **Regularize Curves:** Detect and classify different geometric shapes.
    
*   **Explore Symmetry:** Identify reflection and rotational symmetries.
    
*   **Complete Incomplete Curves:** Fill gaps and complete curves that are partially occluded or disconnected.
    

### Input

*   **CSV Files:** Polylines are represented as CSV files where each file contains a sequence of points for each path.
    

### Expected Output

*   **Images:** Composite images of the detected shapes.
    
*   **SVG Files:** Visualizations of the processed paths in SVG format.
    
*   **Console Output:** Details about detected shapes, symmetries, and completed curves.
    

Installation
------------

To run this project, you need to install the following Python libraries:

*   numpy
    
*   opencv-python
    
*   matplotlib
    
*   scikit-learn
    
*   svgwrite
    

You can install them using pip:

```bash
pip install numpy opencv-python matplotlib scikit-learn svgwrite
```

1.  **Read CSV Files:**Use the read\_csv function to load polylines from CSV files.
    
2.  **Create Composite Image:**Use the composite\_shapes function to generate an image from the polylines.
    
3.  **Detect Shapes:**Use the detect\_shapes function to identify different geometric shapes in the composite image.
    
4.  **Detect Symmetry:**Use the detect\_symmetry and detect\_rotational\_symmetry functions to find reflection and rotational symmetries.
    
5.  **Complete Curves:**Use the complete\_curve function to fit a polynomial curve to the given points.
    
6.  **Save SVG Files:**Use the polylines2svg function to save the processed paths as an SVG file.
    

### Example Code

Here's an example of how to use the functions:

## Main Function

The `main` function in the script handles the entire workflow of processing polylines, detecting shapes, analyzing symmetries, and saving the results. Here's how it works:

```python
def main():
    csv_path = "occlusion2.csv"
    paths_XYs = read_csv(csv_path)

    # Determine the shape of the image based on the maximum coordinates
    img_shape = (int(np.max([XY[:, 1].max() for XYs in paths_XYs for XY in XYs])) + 1,
                 int(np.max([XY[:, 0].max() for XYs in paths_XYs for XY in XYs])) + 1)

    # Create a composite image of the shapes
    shape_order = range(len(paths_XYs))
    composite_img = composite_shapes(paths_XYs, img_shape, shape_order)
    
    # Save the composite image
    cv2.imwrite('composite_image.png', composite_img)

    # Detect shapes in the composite image
    shapes = detect_shapes(composite_img)
    
    print("Detected shapes:")
    for shape_type, detected in shapes.items():
        print(f"{shape_type.capitalize()}: {detected}")

    # Analyze symmetries for each path
    for i, path_XYs in enumerate(paths_XYs):
        reflection_symmetric, axis = detect_symmetry(np.vstack(path_XYs))
        rotational_symmetric, angle = detect_rotational_symmetry(np.vstack(path_XYs))
        
        print(f"Path {i} Reflection Symmetry: {reflection_symmetric}, Axis: {axis}")
        print(f"Path {i} Rotational Symmetry: {rotational_symmetric}, Angle: {angle}")
    
    # Complete curves
    for i, path_XYs in enumerate(paths_XYs):
        complete_curve(np.vstack(path_XYs))
    
    # Save the processed paths as an SVG file
    polylines2svg(paths_XYs, "output.svg")

if __name__ == "__main__":
    main()
```

### Detailed Description of Functions

*   **read\_csv(csv\_path)**: Reads polylines from a CSV file and returns a list of paths where each path is a list of points.
    
*   **create\_blank\_image(img\_shape)**: Creates a blank white image with the specified shape.
    
*   **composite\_shapes(paths\_XYs, img\_shape, shape\_order)**: Composites shapes from polylines onto a blank image.
    
*   **detect\_shapes(image)**: Identifies lines, circles, ellipses, rectangles, rounded rectangles, stars, and polygons in an image.
    
*   **detect\_symmetry(path\_XYs)**: Checks for reflection symmetry in the set of points.
    
*   **detect\_rotational\_symmetry(path\_XYs)**: Checks for rotational symmetry at 90, 180, and 270 degrees.
    
*   **complete\_curve(path\_XYs, degree=3, num\_points=100)**: Fits a polynomial curve to a set of points and visualizes it.
    
*   **polylines2svg(paths\_XYs, filename)**: Converts paths to SVG format for visualization.
    
## GUI Integration with `gui.py`

The `gui.py` file provides a graphical user interface (GUI) to interact with the polylines processing script. It allows users to visualize and manage polylines, detect shapes, and analyze symmetries in a user-friendly manner. Below is an overview of its functionalities:

### Features

- **Load and Display Polylines:**
  - The GUI enables users to load polylines from a CSV file.
  - It visualizes these polylines in a graphical window, allowing users to see the shapes and their arrangements.

- **Create and Save Composite Image:**
  - Users can generate a composite image of the loaded polylines.
  - The GUI provides options to save this image, which can be useful for visual inspection or documentation.

- **Shape Detection:**
  - The GUI includes functionality to detect various shapes within the composite image.
  - Detected shapes are displayed and categorized, making it easy to analyze the composition of the polylines.

- **Symmetry Analysis:**
  - Users can analyze reflection and rotational symmetries of the polylines.
  - The results are displayed in the GUI, providing insights into the geometric properties of the shapes.

- **Curve Completion:**
  - The GUI allows for the completion of curves in the polylines, enhancing the visual representation and analysis.

- **Export to SVG:**
  - The processed polylines can be exported as an SVG file directly from the GUI.
  - This feature is useful for further manipulation or presentation of the shapes.

### Code Overview

Here is a simplified overview of how `gui.py` is structured:

```python
import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np

# Define the GUI class
class PolylineGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Polyline Processor")
        self.create_widgets()

    def create_widgets(self):
        # Define GUI components here
        pass

    def load_file(self):
        # Load CSV file and update display
        pass

    def save_image(self):
        # Save the composite image
        pass

    def detect_shapes(self):
        # Perform shape detection and update GUI
        pass

    def analyze_symmetry(self):
        # Perform symmetry analysis and update GUI
        pass

    def complete_curve(self):
        # Complete the curves in the polylines
        pass

    def export_svg(self):
        # Export polylines to SVG format
        pass

# Run the GUI application
if __name__ == "__main__":
    root = tk.Tk()
    app = PolylineGUI(root)
    root.mainloop()
```

### Usage

1.  **Running the GUI:**
    
    *   Execute gui.py to launch the GUI application.
        
    *   Interact with the various buttons and options to load polylines, analyze shapes, and perform symmetry checks.
        
2.  **Loading Data:**
    
    *   Use the "Load File" option to import polylines from a CSV file.
        
3.  **Processing and Analysis:**
    
    *   Use the provided buttons to process the polylines, detect shapes, and analyze symmetries.
        
4.  **Saving and Exporting:**
    
    *   Save the composite image or export the polylines as an SVG file using the respective options in the GUI.
        

Feel free to customize and extend the gui.py file according to your specific requirements. The GUI serves as an interactive tool to enhance the usability and accessibility of the polylines processing functionality.


Testing
-------

To test the implementation, use the provided example CSV files and verify the output images and SVG files.

Contributing
------------

Feel free to contribute to this project by opening issues, submitting pull requests, or providing feedback.

Acknowledgements
----------------

This project was created for the Adobe Gensolve Hackathon. Special thanks to the hackathon organizers for the opportunity to work on this challenge.
