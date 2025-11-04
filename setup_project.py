import os

# Define folder structure
folders = [
    "app",
    "data",
    "notebooks",
    "reports",
]

files = {
    "app": [
        "main.py",
        "ecl_calculator.py",
        "visualization.py",
        "chat_module.py",
        "auth.py",
        "database.py",
        "utils.py",
    ],
    "data": [
        "README.txt"
    ],
    "notebooks": [
        "data_exploration.ipynb"
    ],
    "reports": [],
}

root_dir = os.getcwd()

# Create folders
for folder in folders:
    folder_path = os.path.join(root_dir, folder)
    os.makedirs(folder_path, exist_ok=True)
    print(f"✅ Created folder: {folder}")

    # Create files inside folders
    if folder in files:
        for filename in files[folder]:
            file_path = os.path.join(folder_path, filename)
            if not os.path.exists(file_path):
                with open(file_path, "w") as f:
                    f.write("")  # empty file
                print(f"   📄 Created file: {filename}")

# Create top-level files
top_level_files = ["requirements.txt", "README.md", ".gitignore"]
for filename in top_level_files:
    path = os.path.join(root_dir, filename)
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("")
        print(f"📦 Created: {filename}")

print("\n🎉 Project structure created successfully!")
