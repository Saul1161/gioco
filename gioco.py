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
LANE_Y = SCREEN_HEIGHT // 5

MAX_BULLETS = 2
SHOOT_COOLDOWN = 0.25


# ---------------- PLAYER ----------------
class Player(arcade.Sprite):
    def __init__(self):
        super().__init__(scale=3.5)

        self.textures_walk = [
            arcade.load_texture("walkk1.png"),
            arcade.load_texture("walkk2.png"),
            arcade.load_texture("walkk3.png"),
            arcade.load_texture("walkk4.png"),
            arcade.load_texture("walkk5.png"),
            arcade.load_texture("walkk6.png"),
            arcade.load_texture("walkk7.png"),
            arcade.load_texture("walkk8.png"),
        ]

        self.textures_shoot = [
            arcade.load_texture("Shoot1.png"),
            arcade.load_texture("Shoot2.png"),
            arcade.load_texture("Shoot3.png"),
        ]

        self.texture = self.textures_walk[0]

        self.cur_texture = 0
        self.anim_timer = 0

        self.change_x = 0
        self.is_shooting = False

    def update(self, delta_time):
        self.center_x += self.change_x
        self.center_y = LANE_Y
        self.center_x = max(0, min(self.center_x, SCREEN_WIDTH))

        self.anim_timer += delta_time

        if self.is_shooting:
            if self.anim_timer > 0.08:
                self.anim_timer = 0
                self.cur_texture += 1

                if self.cur_texture >= len(self.textures_shoot):
                    self.is_shooting = False
                    self.cur_texture = 0
                    self.texture = self.textures_walk[0]
                else:
                    self.texture = self.textures_shoot[self.cur_texture]
        else:
            if self.change_x != 0:
                if self.anim_timer > 0.1:
                    self.anim_timer = 0
                    self.cur_texture = (self.cur_texture + 1) % len(self.textures_walk)
                    self.texture = self.textures_walk[self.cur_texture]


# ---------------- ZOMBIE ----------------
class Zombie(arcade.Sprite):
    def __init__(self, level):
        super().__init__(scale=3.5)

        self.textures_walk = [
            arcade.load_texture("Walk1.png"),
            arcade.load_texture("Walk2.png"),
            arcade.load_texture("Walk3.png"),
            arcade.load_texture("Walk4.png"),
            arcade.load_texture("Walk5.png"),
            arcade.load_texture("Walk6.png"),
            arcade.load_texture("Walk7.png"),
            arcade.load_texture("Walk8.png"),
        ]

        self.textures_attack = [
            arcade.load_texture("Attack1.png"),
            arcade.load_texture("Attack2.png"),
            arcade.load_texture("Attack3.png"),
            arcade.load_texture("Attack4.png"),
        ]

        self.texture = self.textures_walk[0]

        self.cur_texture = 0
        self.anim_timer = 0

        self.speed = ZOMBIE_BASE_SPEED + (level * 0.5)
        self.life = 100 + (level * 20)
        self.center_y = LANE_Y

        self.is_attacking = False

    def update(self, delta_time):
        if not self.is_attacking:
            self.center_x -= self.speed

        self.anim_timer += delta_time

        if self.is_attacking:
            if self.anim_timer > 0.15:
                self.anim_timer = 0
                self.cur_texture = (self.cur_texture + 1) % len(self.textures_attack)
                self.texture = self.textures_attack[self.cur_texture]
        else:
            if self.anim_timer > 0.15:
                self.anim_timer = 0
                self.cur_texture = (self.cur_texture + 1) % len(self.textures_walk)
                self.texture = self.textures_walk[self.cur_texture]


# ---------------- PROIETTILE ----------------
class Bullet(arcade.Sprite):
    def __init__(self):
        super().__init__("proiettile.png", scale=0.2)
        self.danno = 50

    def update(self, delta_time):
        self.center_x += BULLET_SPEED
        self.center_y = LANE_Y


# ---------------- GAME ----------------
class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.state = "MENU"

        self.player = None
        self.player_list = None
        self.zombie_list = None
        self.bullet_list = None

        self.level = 1
        self.score = 0
        self.hp = 3

        self.spawn_timer = 0

        self.can_shoot = True
        self.shoot_timer = 0

        self.background = None

    def setup(self):
        self.background = arcade.load_texture("sfondo.png")

        self.player_list = arcade.SpriteList()
        self.zombie_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        self.player = Player()
        self.player.center_x = 100
        self.player_list.append(self.player)

        self.level = 1
        self.score = 0
        self.hp = 3

        self.spawn_timer = 0

        self.spawn_wave()

    def spawn_wave(self):
        for i in range(4 * self.level):
            self.spawn_zombie()

    def spawn_zombie(self):
        zombie = Zombie(self.level)
        zombie.center_x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 300)
        self.zombie_list.append(zombie)

    # ---------------- DRAW ----------------
    def on_draw(self):
        self.clear()

        if self.state == "MENU":
            arcade.draw_text("ZOMBIE SHOOTER",
                             SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50,
                             arcade.color.WHITE, 40, anchor_x="center")

            arcade.draw_text("Premi ENTER per iniziare",
                             SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                             arcade.color.GRAY, 20, anchor_x="center")
            return

        if self.state == "GAME":
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

        elif self.state == "GAME_OVER":
            arcade.draw_text("GAME OVER",
                             SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50,
                             arcade.color.RED, 40, anchor_x="center")

            arcade.draw_text("Premi R per ricominciare",
                             SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                             arcade.color.WHITE, 20, anchor_x="center")

        elif self.state == "WIN":
            arcade.draw_text("HAI VINTO!",
                             SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50,
                             arcade.color.GREEN, 40, anchor_x="center")

            arcade.draw_text("Premi R per rigiocare",
                             SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                             arcade.color.WHITE, 20, anchor_x="center")

    # ---------------- UPDATE ----------------
    def on_update(self, delta_time):

        if self.state != "GAME":
            return

        self.player_list.update()
        self.zombie_list.update()
        self.bullet_list.update()

        if not self.can_shoot:
            self.shoot_timer += delta_time
            if self.shoot_timer >= SHOOT_COOLDOWN:
                self.can_shoot = True
                self.shoot_timer = 0

        self.spawn_timer += delta_time
        if self.spawn_timer > max(0.5, 2 - self.level * 0.2):
            self.spawn_timer = 0
            self.spawn_zombie()

        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.zombie_list)

            for zombie in hit_list:
                zombie.life -= bullet.danno
                bullet.remove_from_sprite_lists()

                if zombie.life <= 0:
                    zombie.remove_from_sprite_lists()
                    self.score += 1

        for bullet in self.bullet_list:
            if bullet.center_x > SCREEN_WIDTH:
                bullet.remove_from_sprite_lists()

        for zombie in self.zombie_list:
            if abs(zombie.center_x - self.player.center_x) < 50:
                zombie.is_attacking = True

                if random.random() < 0.02:
                    self.hp -= 1

                    if self.hp <= 0:
                        self.state = "GAME_OVER"
            else:
                zombie.is_attacking = False

        if self.score >= self.level * 10:
            self.level += 1

            if self.level > LEVELS:
                self.state = "WIN"

    # ---------------- INPUT ----------------
    def on_key_press(self, key, modifiers):

        if key == arcade.key.ENTER and self.state == "MENU":
            self.state = "GAME"
            self.setup()

        if key == arcade.key.R and self.state in ("GAME_OVER", "WIN"):
            self.state = "GAME"
            self.setup()

        if self.state != "GAME":
            return

        if key == arcade.key.A:
            self.player.change_x = -PLAYER_SPEED
        elif key == arcade.key.D:
            self.player.change_x = PLAYER_SPEED

        if key == arcade.key.SPACE:
            if len(self.bullet_list) < MAX_BULLETS and self.can_shoot:
                bullet = Bullet()
                bullet.center_x = self.player.center_x + self.player.width // 2 + 10
                bullet.center_y = LANE_Y
                self.bullet_list.append(bullet)

                arcade.Sound(SOUND_SHOT).play()

                self.player.is_shooting = True
                self.player.cur_texture = 0
                self.player.anim_timer = 0

                self.can_shoot = False

    def on_key_release(self, key, modifiers):
        if self.state != "GAME":
            return

        if key in (arcade.key.A, arcade.key.D):
            self.player.change_x = 0


# ---------------- MAIN ----------------
def main():
    game = Game()
    arcade.run()


if __name__ == "__main__":
    main()