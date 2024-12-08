# Pic-A-Tool 
<!-- [Logo]   -->
*A tool for managing and modifying image metadata effortlessly.*



## 📝 About  

**Pic-A-Tool** is a Python-based application designed to simplify image metadata management.  
With features like timestamp adjustments, file renaming, and offers additional tools for enhanced functionality. 


## ✨ Features 

### 1. Pic-A-Time
- **Timestamp Adjustment:** Automatically update timestamps based on filenames containing date and time.

- **Smartphone Support:** Modify metadata for images captured by the following smartphone brands, including screenshots:
    - Google, Huawei, iQOO, Motorola, OnePlus, OPPO, POCO/Redmi/Xiaomi, Realme, Samsung, Vivo.

- **Batch Processing:** Modify timestamps for multiple images in one go.

- **Preview Matches:** View a sample of images that match your criteria before applying changes or restoring from a backup file

- **Restore Changes:** Revert modifications using backups created by the app.


### 2. Settings
- **Appearance Customization:** Toggle between `System`, `Dark`, and `Light` modes.

- **Color Themes:** Select from various themes like `Blue`, `Green`, and `Dark Blue`.

- **Backup Settings:** Configure automatic backups before modifications, and set a custom folder for storing them.

### 3. Future Tabs (Coming Soon)
- **Pic-A-Name:** Bulk rename images using customizable naming schemes based on timestamps.
- **Pic-A-Tool:** Additional tools, like removing location data from EXIF metadata.


## 🛠 Installation  

### Prerequisites  
- Python 3.7 or higher.  
- Required libraries (install via `requirements.txt`).  

### Steps  
1. **Clone the repository:**
   ```bash  
   git clone https://github.com/Shivam-Sayankar/Pic-A-Tool.git
   ```
2. **Navigate to the project folder:**
   ```bash
   cd Pic-A-Tool
   ```
3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Run the App:**
    ```bash
    python app.pyw
    ```


## 📖 Usage

### Pic-A-Time
- Open the `Pic-A-Time` tab.
- Select the desired images or folder.
- Modify timestamps using the provided options.
- Preview the changes before applying.
- Restore changes using the Restore option.


### Settings
- Navigate to the `Settings` tab.
- Customize the appearance and color theme.
- Enable or disable automatic backups.
- Select backup folder



## 🔄 Backup & Restore

### Backup:

- Automatically saves image metadata before modifications.
- Stored in a Pickle file format for quick access.

### Restore:

- Load a backup file and preview its contents.
- Revert metadata changes with a single click.

<!-- 
---

## Screenshots

-->