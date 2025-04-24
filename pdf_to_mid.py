import os, subprocess, glob, shutil, threading
from music21 import converter, tempo
import customtkinter as ctk
from tkinter import filedialog, messagebox

# --- Core Conversion Functions ---

def pdf_to_images(pdf_path, images_dir, base_name):
    try:
        output_prefix = os.path.join(images_dir, base_name)
        cmd = ["pdftoppm", "-png", "-rx", "300", "-ry", "300", pdf_path, output_prefix]
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        raise Exception(f"PDF to images failed: {e.stderr.decode()}")

def process_image_with_audiveris(image_path, output_dir, audiveris_executable):
    try:
        cmd = [audiveris_executable, "-batch", "-export", "-output", output_dir, image_path]
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        raise Exception(f"Audiveris failed: {e.stderr.decode()}")

def find_exported_file(output_dir):
    candidates = glob.glob(os.path.join(output_dir, "**", "*.mxl"), recursive=True) + \
                 glob.glob(os.path.join(output_dir, "**", "*.musicxml"), recursive=True)
    return candidates[0] if candidates else None

def convert_xml_to_midi(xml_path, midi_output_path, desired_tempo=120):
    try:
        score = converter.parse(xml_path)
        for mark in score.flat.getElementsByClass(tempo.MetronomeMark):
            mark.activeSite.remove(mark)
        score.insert(0, tempo.MetronomeMark(number=desired_tempo))
        score.write('midi', fp=midi_output_path)
    except Exception as e:
        raise Exception(f"Music21 conversion failed: {str(e)}")

# --- GUI Setup ---

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class PDFToMIDIConverter(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Batch PDF to MIDI Converter")
        self.geometry("700x450")
        self.pdf_files = []
        self.audiveris_var = ctk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        header = ctk.CTkLabel(self, text="Batch PDF to MIDI Converter", font=("Arial", 24, "bold"))
        header.pack(pady=10)

        ctk.CTkButton(self, text="Select PDF Files", command=self.browse_pdfs).pack(pady=5)
        self.pdf_label = ctk.CTkLabel(self, text="No PDFs selected", wraplength=600)
        self.pdf_label.pack(pady=5)

        ctk.CTkButton(self, text="Select Audiveris Executable", command=self.browse_audiveris).pack(pady=5)
        self.audiveris_label = ctk.CTkLabel(self, text="No Audiveris path selected")
        self.audiveris_label.pack(pady=5)

        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.pack(pady=10, fill='x', padx=20)
        self.progress_bar.set(0)

        self.convert_button = ctk.CTkButton(self, text="Convert PDFs to MIDI", command=self.start_conversion)
        self.convert_button.pack(pady=20)

    def browse_pdfs(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        if files:
            self.pdf_files = files
            self.pdf_label.configure(text=f"Selected {len(files)} PDFs")

    def browse_audiveris(self):
        file_path = filedialog.askopenfilename(filetypes=[("BAT Files", "*.bat")])
        if file_path:
            self.audiveris_var.set(file_path)
            self.audiveris_label.configure(text=file_path)

    def start_conversion(self):
        self.convert_button.configure(state="disabled")
        threading.Thread(target=self.convert_pdfs_to_midi, daemon=True).start()

    def convert_pdfs_to_midi(self):
        try:
            if not self.pdf_files:
                raise Exception("No PDF files selected")
            audiveris_path = self.audiveris_var.get().strip()
            if not os.path.isfile(audiveris_path):
                raise Exception("Invalid Audiveris path")
            
            total_files = len(self.pdf_files)
            for index, pdf_file in enumerate(self.pdf_files, start=1):
                base_dir = os.path.dirname(pdf_file)
                base_filename = os.path.splitext(os.path.basename(pdf_file))[0]
                clean_filename = base_filename.replace(" ", "_")

                temp_dirs = {
                    "images": os.path.join(base_dir, "TempImages"),
                    "audiveris": os.path.join(base_dir, "AudiverisOutput")
                }
                for d in temp_dirs.values():
                    os.makedirs(d, exist_ok=True)

                self.progress_bar.set((index - 1) / total_files)
                pdf_to_images(pdf_file, temp_dirs["images"], clean_filename)
                image_files = sorted(glob.glob(os.path.join(temp_dirs["images"], "*.png")))

                for i, image_path in enumerate(image_files, 1):
                    process_image_with_audiveris(image_path, temp_dirs["audiveris"], audiveris_path)
                    xml_file = find_exported_file(temp_dirs["audiveris"])
                    if xml_file:
                        midi_path = os.path.join(base_dir, f"{clean_filename}-{i}.mid")
                        convert_xml_to_midi(xml_file, midi_path)

                shutil.rmtree(temp_dirs["images"], ignore_errors=True)
                shutil.rmtree(temp_dirs["audiveris"], ignore_errors=True)
                
            messagebox.showinfo("Success", "All PDFs converted to MIDI successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.progress_bar.set(0)
            self.convert_button.configure(state="normal")

if __name__ == "__main__":
    app = PDFToMIDIConverter()
    app.mainloop()
