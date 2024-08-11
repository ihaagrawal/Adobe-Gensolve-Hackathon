import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

import cv2
import numpy as np

def detect_shapes(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    shape_info = []

    for contour in contours:
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        num_vertices = len(approx)

        if num_vertices == 2:
            shape = "Line"
        elif num_vertices == 3:
            shape = "Triangle"
        elif num_vertices == 4:
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = w / float(h)
            shape = "Square" if 0.95 <= aspect_ratio <= 1.05 else "Rectangle"
        elif num_vertices == 5:
            shape = "Pentagon"
        elif num_vertices == 6:
            shape = "Hexagon"
        elif num_vertices >= 7 and num_vertices <= 12:
            # Detect polygons with 7 to 12 sides
            shape = f"Polygon ({num_vertices} sides)"
        else:
            # Detecting star-like shapes (simple heuristic for demonstration)
            if num_vertices > 12:
                shape = "Star"
            else:
                shape = "Circle"

        cv2.drawContours(image, [approx], 0, (0, 255, 0), 2)
        cv2.putText(image, shape, (approx[0][0][0], approx[0][0][1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        shape_info.append(shape)

    return image, shape_info


def find_symmetry(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        contour = contour[:, 0, :]
        M = cv2.moments(contour)
        if M["m00"] == 0:
            continue
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)
        cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)

        cv2.line(image, (cX, 0), (cX, image.shape[0]), (0, 255, 0), 3)  # Thickness set to 3

        symmetry = True
        for i in range(len(contour)):
            x1, y1 = contour[i]
            x2, y2 = contour[-i % len(contour)]
            if abs(x1 - x2) > 10 or abs(y1 - y2) > 10:
                symmetry = False
                break

        if symmetry:
            cv2.putText(image, "Symmetric", (cX - 30, cY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    return image



def complete_curves(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((5, 5), np.uint8)
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=3)
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros_like(image)

    for contour in contours:
        cv2.drawContours(mask, [contour], 0, (255), thickness=cv2.FILLED)

    completed_image = cv2.bitwise_or(thresh, mask)
    completed_image = cv2.bitwise_not(completed_image)
    final_result = cv2.bitwise_and(image, completed_image)

    return final_result

class ShapeDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shape Detection Application")

        # Set window size
        self.root.geometry("1400x900")

        # Main Frame
        self.main_frame = tk.Frame(root, bg='#f0f0f0')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Grid Configuration
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=3)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=4)

        # Title Label
        self.title_label = tk.Label(self.main_frame, text="Shape Detection Application", font=("Arial", 24), bg='#f0f0f0')
        self.title_label.grid(row=0, column=1, pady=20, sticky='n')

        # Left Frame for buttons
        self.left_frame = tk.Frame(self.main_frame, bg='#f0f0f0', width=250)
        self.left_frame.grid(row=1, column=0, sticky='ns', padx=10, pady=10)

        # Image Display Frame
        self.image_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        self.image_frame.grid(row=1, column=1, sticky='nsew')

        # Buttons
        self.upload_button = tk.Button(self.left_frame, text="Upload Image", command=self.upload_image, font=("Arial", 14), bg="#4CAF50", fg="white", relief="flat", padx=10, pady=5)
        self.upload_button.grid(row=0, column=0, pady=10)

        self.detect_shapes_button = self.create_nav_button("Detected Shapes", self.show_detected_shapes)
        self.detect_shapes_button.grid(row=1, column=0, pady=10, padx=10)

        self.symmetry_detection_button = self.create_nav_button("Symmetry Detection", self.show_symmetry_detection)
        self.symmetry_detection_button.grid(row=2, column=0, pady=10, padx=10)

        self.curve_completion_button = self.create_nav_button("Curve Completion", self.show_curve_completion)
        self.curve_completion_button.grid(row=3, column=0, pady=10, padx=10)

        # Canvas for image display
        self.canvas = tk.Canvas(self.image_frame, bg='white')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.v_scrollbar = tk.Scrollbar(self.image_frame, orient="vertical", command=self.canvas.yview)
        self.v_scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)

        self.h_scrollbar = tk.Scrollbar(self.image_frame, orient="horizontal", command=self.canvas.xview)
        self.h_scrollbar.pack(side="bottom", fill="x")
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set)

        self.image_path = None
        self.current_section = None

    def create_nav_button(self, text, command):
        button = tk.Button(self.left_frame, text=text, command=command, font=("Arial", 14), bg="#4CAF50", fg="white", relief="flat", padx=10, pady=5)
        button.config(width=20)
        return button

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if not self.image_path:
            messagebox.showinfo("No File Selected", "No file was selected. Please select an image file.")
            return

        print(f"Selected image path: {self.image_path}")  # Debug: Print the selected file path

        try:
            # Test if the file exists
            with open(self.image_path, 'rb') as f:
                pass
        except FileNotFoundError:
            messagebox.showerror("Error", "The selected file was not found.")
            return

        self.show_detected_shapes()

    def process_image(self):
        print("Processing image...")  # Debug: Print when processing starts
        try:
            shapes_image, _ = detect_shapes(self.image_path)
            symmetry_image = find_symmetry(self.image_path)
            completed_image = complete_curves(self.image_path)
            print("Image processing completed.")  # Debug: Print when processing is done
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            return None, None, None

        return shapes_image, symmetry_image, completed_image

    def show_detected_shapes(self):
        print("Showing detected shapes...")  # Debug: Print when this method is called
        self.current_section = 'shapes'
        shapes_image, _, _ = self.process_image()
        if shapes_image is not None:
            self.display_image_on_canvas(shapes_image)
        else:
            print("Failed to process image.")  # Debug: Print if processing fails

    def show_symmetry_detection(self):
        print("Showing symmetry detection...")  # Debug: Print when this method is called
        self.current_section = 'symmetry'
        _, symmetry_image, _ = self.process_image()
        if symmetry_image is not None:
            self.display_image_on_canvas(symmetry_image)
        else:
            print("Failed to process image.")  # Debug: Print if processing fails

    def show_curve_completion(self):
        print("Showing curve completion...")  # Debug: Print when this method is called
        self.current_section = 'curves'
        _, _, completed_image = self.process_image()
        if completed_image is not None:
            self.display_image_on_canvas(completed_image)
        else:
            print("Failed to process image.")  # Debug: Print if processing fails
    
    def resize_image(image, max_width=800, max_height=600):
        img_width, img_height = image.size
        if img_width > max_width or img_height > max_height:
            scaling_factor = min(max_width / img_width, max_height / img_height)
            new_width = int(img_width * scaling_factor)
            new_height = int(img_height * scaling_factor)
            image = image.resize((new_width, new_height), Image.ANTIALIAS)
        return image


    def display_image_on_canvas(self, image):
        print("Displaying image on canvas...")  # Debug: Print when displaying image

        # Convert image from BGR to RGB and then to PIL image
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)

        # Get image dimensions
        img_width, img_height = image.size

        # Update canvas size
        self.canvas.config(scrollregion=(0, 0, img_width, img_height))
        self.canvas.config(width=min(img_width, self.canvas.winfo_width()))
        self.canvas.config(height=min(img_height, self.canvas.winfo_height()))

        # Create an image object for the canvas
        image = ImageTk.PhotoImage(image)

        # Clear the canvas and display the image
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=image)
        self.canvas.image = image  # Keep a reference to avoid garbage collection


if __name__ == "__main__":
    root = tk.Tk()
    app = ShapeDetectionApp(root)
    root.mainloop()
