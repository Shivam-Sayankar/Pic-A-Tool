import customtkinter as ctk

def confirmation_popup(root, title, message):
    popup = ctk.CTkToplevel(root)
    popup.geometry("450x320")
    popup.title("Confirmation")

    popup.update()
    popup.grab_set()

    # Title question
    label = ctk.CTkLabel(popup, text=title)
    label.pack(pady=10, padx=10)

    # Texbox for message
    preview_box = ctk.CTkTextbox(popup)
    preview_box.insert("end", message)
    preview_box.pack(padx=10, expand=True, fill="both")

    response = ctk.StringVar(value="None")

    def confirm():
        response.set("Yes")
        popup.destroy()

    def cancel():
        response.set("No")
        popup.destroy()

    yes_button = ctk.CTkButton(popup, text="Yes", command=confirm)
    no_button = ctk.CTkButton(popup, text="No", command=cancel)

    yes_button.pack(side="left", padx=10, pady=10)
    no_button.pack(side="right", padx=10, pady=10)

    popup.wait_window()
    # print(response.get(), type(response.get()))
    return response.get() == "Yes"