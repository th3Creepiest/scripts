import os


def remove_unwanted_files(directory: str):
    """Removes files from the specified directory tree after user confirmation."""

    files_to_delete = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file == ".DS_Store" or file.startswith("._") or file.endswith(".asd"):
                files_to_delete.append(os.path.join(root, file))

    if not files_to_delete:
        print("No unwanted files found.")
        return

    for file in files_to_delete:
        print(file)

    print(f"Found {len(files_to_delete)} unwanted file(s) to remove:")

    confirmation = input("Do you want to delete these files? (yes/no): ").strip().lower()

    if confirmation.startswith("y"):
        for file in files_to_delete:
            os.remove(file)
            print(f"Removed {file}")
        print("Garbage files removed.")
    else:
        print("Operation cancelled. No files were removed.")


if __name__ == "__main__":
    # remove_unwanted_files("C:\\Users\\Creep\\Desktop\\Samples")
    remove_unwanted_files(input("Enter directory path: "))
