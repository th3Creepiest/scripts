import os


def count_files(directory: str) -> int:
    """Counts the number of files in the specified directory tree."""
    file_count = 0
    for _, _, files in os.walk(directory):
        file_count += len(files)
    return file_count


if __name__ == "__main__":
    directory = input("Enter directory path: ")
    print(f"Number of files in {directory}: {count_files(directory)}")
