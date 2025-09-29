import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def generate_clipart():
    text = text_entry.get()
    if not text:
        messagebox.showerror("Missing text!")
        return

    # Font setup
    try:
        font = ImageFont.truetype("arial.ttf", 120)
    except:
        font = ImageFont.load_default()

    # Measure total text width
    total_width = 0
    letter_widths = []
    for char in text:
        bbox = font.getbbox(char)
        width = bbox[2] - bbox[0]
        letter_widths.append(width)
        total_width += width + 5
    total_width -= 5  # remove extra spacing after last letter

    # Canvas with balanced margins
    margin = 50
    canvas_width = total_width + margin * 2
    canvas_height = 300
    img = Image.new('RGBA', (canvas_width, canvas_height), (255,255,255,255))
    draw = ImageDraw.Draw(img)

    fill_color = (79, 136, 198)  # blue
    outline_color = (0,0,0)      # black

    # Starting position
    x = margin
    y = 100

    # Draw each letter with thick outline
    for i, char in enumerate(text):
        letter_width = letter_widths[i]

        # Draw thick outline by multiple offsets around the letter
        outline_thickness = 5
        for dx in range(-outline_thickness, outline_thickness+1):
            for dy in range(-outline_thickness, outline_thickness+1):
                if dx !=0 or dy !=0:
                    draw.text((x+dx, y+dy), char, font=font, fill=outline_color)

        # Draw main blue fill
        draw.text((x, y), char, font=font, fill=fill_color)

        # Move x for next letter
        x += letter_width + 5  # tight spacing

    # Slight smoothing
    img = img.filter(ImageFilter.SMOOTH_MORE)

    # Save
    save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png")])
    if save_path:
        img.save(save_path)
        messagebox.showinfo("File saved", f"ClipArt saved : {save_path}")

# GUI
root = tk.Tk()
root.title("ClipArt Generator")

tk.Label(root, text="Enter the text :", font=("Arial", 14)).pack(pady=10)
text_entry = tk.Entry(root, width=30, font=("Arial", 16))
text_entry.pack(pady=5)

generate_btn = tk.Button(root, text="Generate ClipArt", command=generate_clipart, font=("Arial", 14))
generate_btn.pack(pady=20)

root.mainloop()
