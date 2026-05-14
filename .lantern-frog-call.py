import pygame, time
pygame.mixer.init()
pygame.mixer.music.load(r"C:\Users\alexp\.lantern\sounds\Frogs_croak_calling_chorus_at_night.ogg")
pygame.mixer.music.set_volume(0.9)
pygame.mixer.music.play()
print("PLAYING: Frogs_croak_calling_chorus_at_night.ogg")
# Hold the process for the duration of the file so playback doesn't get GC'd.
while pygame.mixer.music.get_busy():
    time.sleep(0.5)
print("DONE")
