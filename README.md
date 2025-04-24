# PDF-to-MIDI

A gui based python code for converting sheetmusic containing pdf files to midi format, it uses an ocr software called Audiveris, it also a command line argument and may not work the same way in mac, it is only for windows yet, but you can use it in mac doing some changes.

Unfortunately the process of running the code isnt very straight forward, you have to install a lot of dependencies and audiveris software to correctly run the requirements.txt libraries and the code.

-----------------------------------------------------------------------------------------------------------------------------------

Firstly you need to download and install Java :  
👉 https://www.oracle.com/java/technologies/downloads/?er=221886#jdk21-windows  
For audiveris to function you actually just need the JRE but just download the full sdk if you havent already and make sure to add it to the path variables in your windows.  
(make sure to restart your PC or at least your terminal after doing this, or the path variable might not be detected)

Now download the latest version of audiveris from here :  
👉 https://github.com/Audiveris/audiveris/releases  
or Just search "audiveris download" in your browser and download the latest version for your device on github.

Check if it functions and add it to the system path variables.  
It has a relatively mediocre and old style gui, you cannot directly import pdf files into the audiveris software itself, you have to test it using an image.  

> ⚠️ Note the path of the `.bat` file in the Audiveris folder, it is the executable file that's important. You will be selecting this in the app GUI.

-----------------------------------------------------------------------------------------------------------------------------------

After that you need to download and install **Poppler** to convert pdf files to images.  
👉 Link: https://poppler.freedesktop.org/  

After downloading, extract the zip, and **add its `bin` folder to the system path variables**.  
Make sure `pdftoppm.exe` is inside that bin folder — this is what is used for the main part.

-----------------------------------------------------------------------------------------------------------------------------------

### Python Dependencies

Install the required python packages using the following command in your terminal:
```bash
pip install -r requirements.txt
