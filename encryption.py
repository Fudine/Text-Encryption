import sqlite3
import customtkinter as ctk

# Database setup
def setup_database():
    conn = sqlite3.connect("encryption.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_text TEXT,
            encrypted_text TEXT,
            shift INTEGER
        )
    """)
    conn.commit()
    conn.close()

# Save a message to the database
def save_to_database(original_text, encrypted_text, shift):
    conn = sqlite3.connect("encryption.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO messages (original_text, encrypted_text, shift)
        VALUES (?, ?, ?)
    """, (original_text, encrypted_text, shift))
    conn.commit()
    conn.close()

# Retrieve all messages from the database
def get_messages():
    conn = sqlite3.connect("encryption.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Caesar Cipher encryption and decryption functions
def encrypt_text(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isupper():
            encrypted_text += chr((ord(char) + shift - 65) % 26 + 65)
        elif char.islower():
            encrypted_text += chr((ord(char) + shift - 97) % 26 + 97)
        elif char.isdigit():
            encrypted_text += chr((ord(char) + shift - 48) % 10 + 48)
        else:
            encrypted_text += char  # Non-alphanumeric characters remain unchanged
    return encrypted_text

def decrypt_text(encrypted_text, shift):
    return encrypt_text(encrypted_text, -shift)

# GUI Application using customtkinter
def run_gui():
    setup_database()

    # Create main window
    app = ctk.CTk()
    app.title("Text Encryption Generator")
    app.geometry("400x450")
    app.configure(fg_color="#461c81")

    # Define input fields
    original_text_entry = ctk.CTkEntry(app, placeholder_text="Enter text to encrypt/decrypt", width=300)
    original_text_entry.pack(pady=10)

    shift_entry = ctk.CTkEntry(app, placeholder_text="Enter shift (1-25)", validate="key", width=300)
    shift_entry.pack(pady=10)

    encrypted_text_label = ctk.CTkLabel(app, text="Encrypted/Decrypted text will appear here", width=300)
    encrypted_text_label.pack(pady=10)

    # Function to encrypt the message
    def encrypt_action():
        text = original_text_entry.get()
        try:
            shift = int(shift_entry.get())
            if 1 <= shift <= 25:
                encrypted_text = encrypt_text(text, shift)
                encrypted_text_label.configure(text=f"Encrypted Text: {encrypted_text}")
                # Save to database
                save_to_database(text, encrypted_text, shift)
            else:
                encrypted_text_label.configure(text="Shift must be between 1 and 25")
        except ValueError:
            encrypted_text_label.configure(text="Invalid shift value. Please enter a number between 1 and 25.")

    # Function to decrypt the message
    def decrypt_action():
        text = original_text_entry.get()
        try:
            shift = int(shift_entry.get())
            if 1 <= shift <= 25:
                decrypted_text = decrypt_text(text, shift)
                encrypted_text_label.configure(text=f"Decrypted Text: {decrypted_text}")
            else:
                encrypted_text_label.configure(text="Shift must be between 1 and 25")
        except ValueError:
            encrypted_text_label.configure(text="Invalid shift value. Please enter a number between 1 and 25.")

    # Encrypt button
    encrypt_button = ctk.CTkButton(app, text="Encrypt", command=encrypt_action, width=200)
    encrypt_button.pack(pady=10)

    # Decrypt button
    decrypt_button = ctk.CTkButton(app, text="Decrypt", command=decrypt_action, width=200)
    decrypt_button.pack(pady=10)

    # Function to view saved messages
    def view_saved_messages():
        messages = get_messages()
        if not messages:
            messages_window = ctk.CTkToplevel(app)
            messages_window.title("Saved Messages")
            no_message_label = ctk.CTkLabel(messages_window, text="No messages found.", width=300)
            no_message_label.pack(padx=20, pady=20)
            return

        messages_window = ctk.CTkToplevel(app)
        messages_window.title("Saved Messages")
        
        for message in messages:
            msg = f"ID: {message[0]}, Original: {message[1]}, Encrypted: {message[2]}, Shift: {message[3]}"
            label = ctk.CTkLabel(messages_window, text=msg, width=300)
            label.pack(padx=20, pady=5)

    # View saved messages button
    view_button = ctk.CTkButton(app, text="View Saved Messages", command=view_saved_messages, width=200)
    view_button.pack(pady=10)

    # Run the application
    app.mainloop()

# Run the GUI
if __name__ == "__main__":
    run_gui()
