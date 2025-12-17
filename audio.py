import pygame

class Audio:
    def __init__(self, volume=1.0):
        self._main_music = pygame.mixer.Sound("Assets/Audio/Drunken sailor.wav")
        self._ambient_music = pygame.mixer.Sound("Assets/Audio/ambient Loop.wav")
        self._cannon_fire_sound = pygame.mixer.Sound("Assets/Audio/Cannon Fire.wav")
        self._drink_sound = pygame.mixer.Sound("Assets/Audio/Drink.wav")
        self._main_music.set_volume(volume)
        self._ambient_music.set_volume(volume)
        self._cannon_fire_sound.set_volume(volume)
        self._drink_sound.set_volume(volume*1.5)
        self.volume = volume

    def play(self, loops=0):
        self.sound.play(loops=loops)

    def stop(self):
        self.sound.stop()
    
    def set_volume(self, volume):
        self.sound.set_volume(volume)
    
    def Fire(self):
        self._cannon_fire_sound.play()
    
    def PlayMusic(self):
        self._main_music.play(loops=-1)
        self._ambient_music.play(loops=-1)
    
    def StopMusic(self):
        self._main_music.stop()
        self._ambient_music.stop()

    def Drink(self):
        self._drink_sound.play()

    def set_master_volume(self, volume):
        volume = max(0.0, min(1.0, volume))  # clamp 0–1

        self._main_music.set_volume(volume)
        self._ambient_music.set_volume(volume)
        self._cannon_fire_sound.set_volume(volume)
        self._drink_sound.set_volume(volume * 1.5)

        self.volume = volume
