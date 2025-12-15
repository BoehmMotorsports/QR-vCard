import customtkinter as ctk
import qrcode
from PIL import Image
from tkinter import filedialog
import os

# 1. Setup Theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class VCardApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Initialize variable to hold the generated image
        self.current_qr_image = None

        # Window Configuration
        self.title("vCard QR Generator")
        #self.geometry("700x550") # Made slightly taller for the extra button
        self.grid_columnconfigure(1, weight=1) 

        # --- LEFT SIDE: INPUTS ---
        self.frame_inputs = ctk.CTkFrame(self)
        self.frame_inputs.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.entries = {}
        fields = [
            ("First Name", "John"),
            ("Last Name", "Doe"),
            ("Phone", "+15551234567"),
            ("Email", "john.doe@example.com"),
            ("Organization", "Example Corp"),
            ("Website", "https://www.example.com")
        ]

        for i, (label_text, default_val) in enumerate(fields):
            label = ctk.CTkLabel(self.frame_inputs, text=label_text, anchor="w")
            label.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w")
            
            entry = ctk.CTkEntry(self.frame_inputs, width=250)
            entry.grid(row=i, column=1, padx=10, pady=(10, 0))
            entry.insert(0, default_val)
            self.entries[label_text] = entry

        # --- BUTTONS ---
        
        # Button 1: Generate Preview
        self.btn_generate = ctk.CTkButton(
            self.frame_inputs, 
            text="Generate Preview", 
            command=self.generate_preview,
            height=40,
            fg_color="#1f538d", # Standard Blue
            hover_color="#14375e"
        )
        self.btn_generate.grid(row=len(fields)+1, column=0, columnspan=2, padx=10, pady=(30, 10), sticky="ew")

        # Button 2: Save Image (Initially Disabled)
        self.btn_save = ctk.CTkButton(
            self.frame_inputs, 
            text="Save Image", 
            command=self.save_image,
            height=40,
            state="disabled",        # Start disabled
            fg_color="gray",         # Grayed out look
            text_color_disabled="lightgray" 
        )
        self.btn_save.grid(row=len(fields)+2, column=0, columnspan=2, padx=10, pady=(0, 20), sticky="ew")

        # Status Label
        self.status_label = ctk.CTkLabel(self.frame_inputs, text="Ready", text_color="gray")
        self.status_label.grid(row=len(fields)+3, column=0, columnspan=2)

        # --- RIGHT SIDE: PREVIEW ---
        self.frame_preview = ctk.CTkFrame(self, fg_color="transparent", width=250)
        self.frame_preview.grid_propagate(False) 
        self.frame_preview.pack_propagate(False)
        self.frame_preview.grid(row=0, column=1, padx=(0,20), pady=20, sticky="nsew")
        
        self.lbl_preview_title = ctk.CTkLabel(self.frame_preview, text="QR Preview", font=("Arial", 16, "bold"))
        self.lbl_preview_title.pack(pady=10)

        self.lbl_image = ctk.CTkLabel(self.frame_preview, text="")
        self.lbl_image.pack(pady=10)

    def generate_preview(self):
        # 1. Get Data
        data = {key: entry.get() for key, entry in self.entries.items()}
        
        # 2. Format vCard
        vcard_payload = f"""BEGIN:VCARD
VERSION:3.0
N:{data['Last Name']};{data['First Name']};;;
FN:{data['First Name']} {data['Last Name']}
ORG:{data['Organization']}
TEL;TYPE=CELL:{data['Phone']}
EMAIL;TYPE=WORK,INTERNET:{data['Email']}
URL:{data['Website']}
END:VCARD"""

        # 3. Create QR Object
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(vcard_payload)
        qr.make(fit=True)

        # 4. Create Image (Store in self)
        # We use .get_image() to ensure it's a standard PIL object
        self.current_qr_image = qr.make_image(fill_color="black", back_color="white").get_image()

        # 5. Update UI Preview
        preview_img = ctk.CTkImage(light_image=self.current_qr_image, dark_image=self.current_qr_image, size=(250, 250))
        self.lbl_image.configure(image=preview_img)
        self.lbl_image.image = preview_img
        
        # 6. Enable the Save Button
        self.btn_save.configure(state="normal", fg_color="green", hover_color="darkgreen")
        self.status_label.configure(text="Preview Generated!", text_color="cyan")

    def save_image(self):
        if not self.current_qr_image:
            return

        # 1. Get Default Filename
        fname = self.entries["First Name"].get()
        lname = self.entries["Last Name"].get()
        default_name = f"{fname}_{lname}_vcard.png"

        # 2. Open Save Dialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All Files", "*.*")],
            initialfile=default_name
        )

        # 3. Save
        if file_path:
            self.current_qr_image.save(file_path)
            self.status_label.configure(text=f"Saved: {os.path.basename(file_path)}", text_color="cyan")
        else:
            self.status_label.configure(text="Save cancelled", text_color="orange")

if __name__ == "__main__":
    app = VCardApp()
    app.mainloop()