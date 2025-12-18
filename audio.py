import pygame

class Audio:
    def __init__(self, volume=1.0):
        self._main_music = pygame.mixer.Sound("Assets/Audio/Drunken sailor.wav")
        self._ambient_music = pygame.mixer.Sound("Assets/Audio/ambient Loop.wav")
        self._cannon_fire_sound = pygame.mixer.Sound("Assets/Audio/Cannon Fire.wav")
        self._drink_sound = pygame.mixer.Sound("Assets/Audio/Drink.wav")
        self._death_sound = pygame.mixer.Sound("Assets/Audio/Death_Sound_Effect.wav")
        self._seagull_sound = pygame.mixer.Sound("Assets/Audio/Seagulls.wav")
        self._upgrade_sound = pygame.mixer.Sound("Assets/Audio/Upgrade_Sound_Effect.wav")

        self._main_music.set_volume(volume)
        self._ambient_music.set_volume(volume)
        self._cannon_fire_sound.set_volume(volume)
        self._drink_sound.set_volume(volume*1.5)
        self._death_sound.set_volume(volume)
        self._seagull_sound.set_volume(volume*8)
        self._upgrade_sound.set_volume(volume)
        self.muted = False
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
        self._seagull_sound.stop()
    
    def StopMusic(self):
        self._main_music.stop()
        self._ambient_music.stop()


    def Drink(self):
        self._drink_sound.play()

    def Death(self):
        self._death_sound.play()
        self._seagull_sound.play()
        self._main_music.stop()
    
    def Upgrade(self):
        self._upgrade_sound.play()

    def _apply_volume(self):
        vol = 0 if self.muted else self.volume
        self._main_music.set_volume(vol)
        self._ambient_music.set_volume(vol)
        self._cannon_fire_sound.set_volume(vol)
        self._drink_sound.set_volume(vol * 1.5)

    def set_master_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
        self._apply_volume()

    def toggle_mute(self):
        self.muted = not self.muted
        self._apply_volume()
