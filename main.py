from tkinter import Tk, Button, Label
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw

canvas = None
minus_counter = 0
pixel_counter = 0
safe_area_visible = False
blue_square_visible = False

def import_image():
    try:
        file_path = filedialog.askopenfilename()
        if file_path:
            image = Image.open(file_path)
            width, height = image.size

            global canvas, minus_counter, pixel_counter, safe_area_visible, blue_square_visible
            canvas = Image.new("RGB", (width, height), color="black")
            canvas.paste(image, (0, 0))

            update_preview()

            shrink_border_button.config(state='normal')
            expand_border_button.config(state='normal')
            reset_border_button.config(state='normal')
            export_button.config(state='normal')
            plus_bleed_button.config(state='normal')
            minus_bleed_button.config(state='normal')
            toggle_safe_area_button.config(state='normal')

            minus_counter = 0
            pixel_counter = 0
            completion_label.config(text="")

            # Reset the visibility of the red and blue lines
            safe_area_visible = False
            blue_square_visible = False

    except Exception as e:
        completion_label.config(text="Error: Failed to import image.")

def shrink_border():
    try:
        global canvas, minus_counter, pixel_counter
        if canvas:
            width, height = canvas.size
            if width > 2 and height > 2:
                canvas = canvas.crop((1, 1, width - 1, height - 1))
                minus_counter += 1
                pixel_counter += 1  # Increment pixel_counter
                update_preview()
                enable_minus_bleed_button()

    except Exception as e:
        completion_label.config(text="Error: Failed to shrink border.")

def reset_border():
    try:
        global canvas, pixel_counter
        if canvas:
            original_image = canvas.copy()
            original_width, original_height = original_image.size
            expanded_width = original_width + 2 * pixel_counter  # Use pixel_counter for expansion
            expanded_height = original_height + 2 * pixel_counter  # Use pixel_counter for expansion
            expanded_canvas = Image.new("RGB", (expanded_width, expanded_height), color="black")

            offset_x = (expanded_width - original_width) // 2
            offset_y = (expanded_height - original_height) // 2

            expanded_canvas.paste(original_image, (offset_x, offset_y))
            canvas = expanded_canvas
            update_preview()

            pixel_counter = 0  # Reset pixel_counter to 0

    except Exception as e:
        completion_label.config(text="Error: Failed to reset border.")

def expand_border():
    try:
        global canvas, minus_counter, pixel_counter
        if canvas:
            original_image = canvas.copy()
            original_width, original_height = original_image.size
            if original_width > 2 and original_height > 2:
                canvas = Image.new("RGB", (original_width + 2, original_height + 2), color="black")
                canvas.paste(original_image, (1, 1))
                minus_counter -= 1
                pixel_counter -= 1
                update_preview()
                if minus_counter <= 0:
                    minus_bleed_button.config(state='disabled')
                enable_minus_bleed_button()  # Enable the button

    except Exception as e:
        completion_label.config(text="Error: Failed to expand border.")

def calculate_bleed_pixels(width, height):
    try:
        dpi = 300
        bleed_dots = dpi // 8
        bleed_pixels = bleed_dots * width // dpi
        return bleed_pixels

    except Exception as e:
        completion_label.config(text="Error: Failed to calculate bleed pixels.")

def add_bleed_edge():
    try:
        global canvas
        if canvas:
            original_image = canvas.copy()
            original_width, original_height = original_image.size
            bleed_pixels = calculate_bleed_pixels(original_width, original_height)
            expanded_width = original_width + bleed_pixels
            expanded_height = original_height + bleed_pixels
            expanded_canvas = Image.new("RGB", (expanded_width, expanded_height), color="black")
            offset_x = bleed_pixels // 2
            offset_y = bleed_pixels // 2
            expanded_canvas.paste(original_image, (offset_x, offset_y))
            canvas = expanded_canvas
            update_preview()

    except Exception as e:
        completion_label.config(text="Error: Failed to add bleed edge.")

def remove_bleed_edge():
    try:
        global canvas
        if canvas:
            original_image = canvas.copy()
            original_width, original_height = original_image.size
            bleed_pixels = calculate_bleed_pixels(original_width, original_height)
            cropped_width = original_width - bleed_pixels
            cropped_height = original_height - bleed_pixels
            cropped_canvas = original_image.crop(
                (bleed_pixels // 2, bleed_pixels // 2, bleed_pixels // 2 + cropped_width, bleed_pixels // 2 + cropped_height)
            )
            canvas = Image.new("RGB", (cropped_width, cropped_height), color="black")
            canvas.paste(cropped_canvas, (0, 0))
            update_preview()

    except Exception as e:
        completion_label.config(text="Error: Failed to remove bleed edge.")

def enable_minus_bleed_button():
    try:
        minus_bleed_button.config(state='normal')

    except Exception as e:
        completion_label.config(text="Error: Failed to enable minus bleed button.")

def export_image():
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg")
        if file_path:
            global safe_area_visible, blue_square_visible
            safe_area_visible = False  # Make the red square invisible
            blue_square_visible = False  # Make the blue square invisible

            canvas_with_outline = canvas.copy()
            if safe_area_visible:
                draw = ImageDraw.Draw(canvas_with_outline)
                red_outline_size = (281, 411)  # Set the red outline size to 281x411 pixels
                preview_size = (336, 468)
                red_offset = ((preview_size[0] - red_outline_size[0]) // 2, (preview_size[1] - red_outline_size[1]) // 2)
                draw.rectangle([(red_offset[0], red_offset[1]), (red_offset[0] + red_outline_size[0], red_offset[1] + red_outline_size[1])], outline="red", width=1)

            if blue_square_visible:
                draw = ImageDraw.Draw(canvas_with_outline)
                blue_outline_size = (303, 435)  # Set the blue outline size to 303x435 pixels
                preview_size = (336, 468)
                blue_offset = ((preview_size[0] - blue_outline_size[0]) // 2, (preview_size[1] - blue_outline_size[1]) // 2)
                draw.rectangle([(blue_offset[0], blue_offset[1]), (blue_offset[0] + blue_outline_size[0], blue_offset[1] + blue_outline_size[1])], outline="blue", width=1)

            canvas_with_outline.save(file_path)
            completion_label.config(text="Operation complete.")

            update_preview()  # Update the preview

    except Exception as e:
        completion_label.config(text="Error: Failed to export image.")

def update_preview():
    try:
        if canvas:
            preview_image = canvas.resize((336, 468))

            preview_image_with_outline = preview_image.copy()
            if safe_area_visible:
                draw = ImageDraw.Draw(preview_image_with_outline)
                red_outline_size = (281, 411)  # Set the red outline size to 281x411 pixels
                preview_size = (336, 468)
                red_offset = ((preview_size[0] - red_outline_size[0]) // 2, (preview_size[1] - red_outline_size[1]) // 2)
                draw.rectangle([(red_offset[0], red_offset[1]), (red_offset[0] + red_outline_size[0], red_offset[1] + red_outline_size[1])], outline="red", width=1)

            if blue_square_visible:
                draw = ImageDraw.Draw(preview_image_with_outline)
                blue_outline_size = (303, 435)  # Set the blue outline size to 303x435 pixels
                preview_size = (336, 468)
                blue_offset = ((preview_size[0] - blue_outline_size[0]) // 2, (preview_size[1] - blue_outline_size[1]) // 2)
                draw.rectangle([(blue_offset[0], blue_offset[1]), (blue_offset[0] + blue_outline_size[0], blue_offset[1] + blue_outline_size[1])], outline="blue", width=1)

            preview_image_tk = ImageTk.PhotoImage(preview_image_with_outline)
            preview_label.config(image=preview_image_tk)
            preview_label.image = preview_image_tk

    except Exception as e:
        completion_label.config(text="Error: Failed to update preview.")

def toggle_safe_area():
    global safe_area_visible, blue_square_visible
    safe_area_visible = not safe_area_visible
    blue_square_visible = safe_area_visible
    update_preview()

root = Tk()
root.title("Proxy Border Editor")

button_style = {"font": ("Arial", 12), "width": 15, "height": 2}
label_style = {"font": ("Arial", 12), "padx": 10, "pady": 10}

import_button = Button(root, text="Import", command=import_image, **button_style)
import_button.grid(row=0, column=0, padx=10, pady=10)

export_button = Button(root, text="Export", command=export_image, state='disabled', **button_style)
export_button.grid(row=0, column=1, padx=10, pady=10)

toggle_safe_area_button = Button(root, text="Toggle Safe Area", command=toggle_safe_area, state='disabled', **button_style)
toggle_safe_area_button.grid(row=0, column=2, padx=10, pady=10)

plus_bleed_button = Button(root, text="+ Bleed Edge", command=add_bleed_edge, state='disabled', **button_style)
plus_bleed_button.grid(row=0, column=3, padx=10, pady=10)

shrink_border_button = Button(root, text="Shrink Border", command=shrink_border, state='disabled', **button_style)
shrink_border_button.grid(row=1, column=0, padx=10, pady=5)

expand_border_button = Button(root, text="Expand Border", command=expand_border, state='disabled', **button_style)
expand_border_button.grid(row=1, column=1, padx=10, pady=5)

reset_border_button = Button(root, text="Reset Border", command=reset_border, state='disabled', **button_style)
reset_border_button.grid(row=1, column=2, padx=10, pady=5)

minus_bleed_button = Button(root, text="- Bleed Edge", command=remove_bleed_edge, state='disabled', **button_style)
minus_bleed_button.grid(row=1, column=3, padx=10, pady=5)

preview_label = Label(root, **label_style)
preview_label.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

completion_label = Label(root, text="", **label_style)
completion_label.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

root.mainloop()
