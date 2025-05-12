import sys
import time
import pygame


if len(sys.argv) > 1:
    file_path = sys.argv[1]
else:
    file_path = input("Enter the path to the MIDI file: ")


try:
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)

    print(f"Playing {file_path}...")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)  # Keep the script alive while music is playing
    print("Finished playing.")

except pygame.error as e:
    print(f"Error playing MIDI file: {e}")

except FileNotFoundError:
    print(f"Error: MIDI file not found at {file_path}")

finally:
    pygame.mixer.quit()
    pygame.quit()
