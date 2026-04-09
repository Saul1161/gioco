import arcade
import random

# ---------------- COSTANTI ----------------
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Zombie Shooter"

PLAYER_SPEED = 5
BULLET_SPEED = 10
ZOMBIE_BASE_SPEED = 1   

SOUND_SHOT = "Shot.wav"

LEVELS = 5
LANE_Y = SCREEN_HEIGHT // 2

MAX_BULLETS = 2
SHOOT_COOLDOWN = 0.25  # cooldown minimo tra un colpo e l'altro


# ---------------- PLAYER ----------------
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("personaggio.png", scale=0.5)
        self.change_x = 0

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y = LANE_Y
        self.center_x = max(0, min(self.center_x, SCREEN_WIDTH))


# ---------------- ZOMBIE ----------------
class Zombie(arcade.Sprite):
    def __init__(self, level):
        super().__init__("zombie.png", scale=0.5)
        self.speed = ZOMBIE_BASE_SPEED + (level * 0.5)
        self.life = 100 + (level * 20)
        self.center_y = LANE_Y

    def update(self, delta_time):
        self.center_x -= self.speed


# ---------------- PROIETTILE ----------------
class Bullet(arcade.Sprite):
    def __init__(self):
        super().__init__("proiettile.png", scale=0.8)
        self.danno = 50

    def update(self, delta_time):
        self.center_x += BULLET_SPEED
        self.center_y = LANE_Y


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
        self.hp = 3

        self.spawn_timer = 0

        # cooldown sparo
        self.can_shoot = True
        self.shoot_timer = 0

        self.background = None

    def setup(self):
        # carica sfondo
        self.background = arcade.load_texture("sfondo.png")

        self.player_list = arcade.SpriteList()
        self.zombie_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        self.player = Player()
        self.player.center_x = 100
        self.player.center_y = LANE_Y
        self.player_list.append(self.player)

        self.spawn_wave()

    def spawn_wave(self):
        for i in range(4 * self.level):
            self.spawn_zombie()

    def spawn_zombie(self):
        zombie = Zombie(self.level)
        zombie.center_x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 300)
        zombie.center_y = LANE_Y
        self.zombie_list.append(zombie)

    # ---------------- DRAW ----------------
    def on_draw(self):
        self.clear()
        # disegna sfondo
        arcade.draw_texture_rect(
            self.background,
            arcade.XYWH(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        self.player_list.draw()
        self.zombie_list.draw()
        self.bullet_list.draw()

        arcade.draw_text(f"Livello: {self.level}", 10, 680, arcade.color.WHITE, 16)
        arcade.draw_text(f"Punti: {self.score}", 10, 700, arcade.color.WHITE, 16)
        arcade.draw_text(f"HP: {self.hp}", 10, 660, arcade.color.RED, 16)

    # ---------------- UPDATE ----------------
    def on_update(self, delta_time):
        self.player_list.update()
        self.zombie_list.update()
        self.bullet_list.update()

        # gestisco cooldown sparo
        if not self.can_shoot:
            self.shoot_timer += delta_time
            if self.shoot_timer >= SHOOT_COOLDOWN:
                self.can_shoot = True
                self.shoot_timer = 0

        # spawn continuo zombie
        self.spawn_timer += delta_time
        if self.spawn_timer > max(0.5, 2 - self.level * 0.2):
            self.spawn_timer = 0
            self.spawn_zombie()

        # collisioni proiettili
        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.zombie_list)

            for zombie in hit_list:
                zombie.life -= bullet.danno
                bullet.remove_from_sprite_lists()

                if zombie.life <= 0:
                    zombie.remove_from_sprite_lists()
                    self.score += 1

        # rimuovo proiettili fuori schermo
        for bullet in self.bullet_list:
            if bullet.center_x > SCREEN_WIDTH:
                bullet.remove_from_sprite_lists()

        # collisione player-zombie
        hit_list = arcade.check_for_collision_with_list(self.player, self.zombie_list)
        for zombie in hit_list:
            zombie.remove_from_sprite_lists()
            self.hp -= 1
            print("HP:", self.hp)

            if self.hp <= 0:
                print("GAME OVER")
                arcade.close_window()

        # aumento livello
        if self.score >= self.level * 10:
            self.level += 1
            print("Livello:", self.level)

            if self.level > LEVELS:
                print("HAI VINTO!")
                arcade.close_window()

    # ---------------- INPUT ----------------
    def on_key_press(self, key, modifiers):
        if key == arcade.key.A:
            self.player.change_x = -PLAYER_SPEED
        elif key == arcade.key.D:
            self.player.change_x = PLAYER_SPEED

        # sparo moderato: cooldown + limite
        if key == arcade.key.SPACE:
            if len(self.bullet_list) < MAX_BULLETS and self.can_shoot:
                bullet = Bullet()
                bullet.center_x = self.player.center_x + self.player.width // 2 + 10
                bullet.center_y = LANE_Y
                self.bullet_list.append(bullet)
                arcade.Sound(SOUND_SHOT).play()
                self.can_shoot = False

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.A, arcade.key.D):
            self.player.change_x = 0


# ---------------- MAIN ----------------
def main():
    game = Game()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()