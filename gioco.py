import arcade
import random

# ---------------- COSTANTI ----------------
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Zombie Shooter"

PLAYER_SPEED = 5
BULLET_SPEED = 10
ZOMBIE_SPEED = 1   

SOUND_SHOT = "./gioco/Shot.wav"

LEVELS = 5


# ---------------- PLAYER ----------------
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("C:/Users/saulv/Downloads/python/gioco/personaggio.png", scale=0.5)
        self.change_x = 0
        self.change_y = 0

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # blocca dentro lo schermo
        self.center_x = max(0, min(self.center_x, SCREEN_WIDTH))
        self.center_y = max(0, min(self.center_y, SCREEN_HEIGHT))


# ---------------- ZOMBIE ----------------
class Zombie(arcade.Sprite):
    def __init__(self, level):
        super().__init__("C:/Users/saulv/Downloads/python/gioco/zombie.png", scale=0.5)
        self.speed = ZOMBIE_SPEED 
        self.life = 100

    def update(self, delta_time):
        self.center_x -= self.speed


# ---------------- PROIETTILE ----------------
class Bullet(arcade.Sprite):
    def __init__(self):
        super().__init__("C:/Users/saulv/Downloads/python/gioco/proiettile.png", scale=0.8)
        self.danno = 50

    def update(self, delta_time):
        self.center_x += BULLET_SPEED


# ---------------- GAME ----------------
class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.player = None
        self.player_list = None
        self.zombie_list = None
        self.bullet_list = None

        self.level = 1
        self.score = 0

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.zombie_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        self.player = Player()
        self.player.center_x = 100
        self.player.center_y = SCREEN_HEIGHT // 2
        self.player_list.append(self.player)

        self.spawn_zombies()

    def spawn_zombies(self):
        for i in range(4 * self.level):
            zombie = Zombie(self.level)
            zombie.center_x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 500)
            zombie.center_y = random.randint(50, SCREEN_HEIGHT - 50)
            self.zombie_list.append(zombie)

    # ---------------- DRAW ----------------
    def on_draw(self):
        self.clear()
        self.player_list.draw()
        self.zombie_list.draw()
        self.bullet_list.draw()

        arcade.draw_text(f"Livello: {self.level}", 10, 680, arcade.color.WHITE, 16)
        arcade.draw_text(f"Punti: {self.score}", 10, 700, arcade.color.WHITE, 16)

    # ---------------- UPDATE ----------------
    def on_update(self, delta_time):
        self.player_list.update()
        self.zombie_list.update()
        self.bullet_list.update()

        # collisioni proiettili
        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.zombie_list)

            for zombie in hit_list:
                zombie.life -= bullet.danno
                bullet.remove_from_sprite_lists()

                if zombie.life <= 0:
                    zombie.remove_from_sprite_lists()
                    self.score += 1

        # rimuovi proiettili fuori schermo
        for bullet in self.bullet_list:
            if bullet.center_x > SCREEN_WIDTH:
                bullet.remove_from_sprite_lists()

        # zombie che toccano player
        if arcade.check_for_collision_with_list(self.player, self.zombie_list):
            print("GAME OVER")
            arcade.close_window()

        # livello completato
        if len(self.zombie_list) == 0:
            self.level += 1

            if self.level > LEVELS:
                print("HAI VINTO!")
                arcade.close_window()
            else:
                self.spawn_zombies()

    # ---------------- INPUT ----------------
    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player.change_y = PLAYER_SPEED
        elif key == arcade.key.S:
            self.player.change_y = -PLAYER_SPEED
        elif key == arcade.key.A:
            self.player.change_x = -PLAYER_SPEED
        elif key == arcade.key.D:
            self.player.change_x = PLAYER_SPEED

        # sparo
        if key == arcade.key.SPACE:
            bullet = Bullet()
            bullet.center_x = self.player.center_x
            bullet.center_y = self.player.center_y
            self.bullet_list.append(bullet)
            arcade.Sound(SOUND_SHOT).play(volume = 25)

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.S):
            self.player.change_y = 0
        elif key in (arcade.key.A, arcade.key.D):
            self.player.change_x = 0


# ---------------- MAIN ----------------
def main():
    game = Game()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()