import pygame as pg
import random
import math

pg.init()

# ディスプレイの設定
SCREEN_WIDTH = pg.display.Info().current_w
SCREEN_HEIGHT = pg.display.Info().current_h
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.FULLSCREEN)
BACKGROUND_IMAGE = pg.transform.scale(pg.image.load('fig/background.png'), (SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
pg.display.set_caption("しゅぅてぃんぐげぇむ")

# 色の定義
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# ゲームエリア
GAME_AREA_SIZE = min(SCREEN_WIDTH, SCREEN_HEIGHT) * 0.6
GAME_AREA_X = (SCREEN_WIDTH - GAME_AREA_SIZE) / 2
GAME_AREA_Y = (SCREEN_HEIGHT - GAME_AREA_SIZE) / 2


class Player:
    """
    Playerの操作するキャラのクラス
    """
    def __init__(self):
        self.width = 50
        self.height = 50
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT // 2 - self.height // 2
        self.speed = 5
        self.hp = 100 # プレイヤーHPの追加（初期化）
        self.sp = 0 # プレイヤーSP(スキルポイント)の追加（初期化）

    def move(self, dx:int, dy:int):
        """
        自機を速度ベクトルself.x,self.yに基づき,
        new_x,new_yとして移動させる
        プレイヤーの行動範囲を制御する
        """
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        if (GAME_AREA_X < new_x < GAME_AREA_X + GAME_AREA_SIZE - self.width and
            GAME_AREA_Y < new_y < GAME_AREA_Y + GAME_AREA_SIZE - self.height):
            self.x = new_x
            self.y = new_y

    def draw(self, screen: pg.Surface):
        """
        引数 screen：画面surface
        """
        player_image = pg.image.load('fig/player.png').convert_alpha()  # プレイヤーの画像を読み込む
        screen.blit(player_image, (self.x, self.y))  # プレイヤーの画像を描画


class Enemy:
    """
    敵キャラを表示するクラス
    """
    def __init__(self):
        self.width = 60
        self.height = 60
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = 50
        self.speed = random.uniform(2, 5)
        self.hp = 100 # 敵HPの追加（初期化）
        self.direction = random.choice([-1, 1])
        self.change_direction_counter = 0 # 敵の移動判定のカウンターの初期化
        self.change_direction_threshold = random.randint(60, 180) # 敵の停止時間をランダム値で設定
        self.enemy_image = pg.image.load('fig/enemy.png').convert_alpha()  # 画像の読み込み
        self.enemy_image = pg.transform.scale(self.enemy_image, (self.width, self.height))  # サイズ変更

    def move(self):
        """
        敵キャラを速度ベクトルself.x,self.directionに基づき移動させる
        """
        self.x += self.speed * self.direction
        if self.x <= 0 or self.x >= SCREEN_WIDTH - self.width:
            self.direction *= -1

        self.change_direction_counter += 1 # 敵の移動判定のカウンターの更新
        if self.change_direction_counter >= self.change_direction_threshold: # 敵の停止時間超えたら敵を移動させる
            self.direction = random.choice([-1, 1]) # 敵の動くy軸+-の方向をランダムに設定
            self.speed = random.uniform(2, 5) # 敵の移動量をランダムに設定
            self.change_direction_counter = 0 # 敵の移動判定のカウンターのリセット
            self.change_direction_threshold = random.randint(60, 180) # 敵の停止時間をランダム値で設定

    def draw(self, screen: pg.Surface):
        """
        引数 screen：画面surface
        """
        screen.blit(self.enemy_image, (self.x, self.y))


class Bullet:
    """
    敵味方が攻撃を行う弾を表すクラス。

    変数:
        x : 弾の現在のx座標
        y : 弾の現在のy座標
        dx : x方向の移動速度
        dy : y方向の移動速度

    メソッド:
        move(): 弾を移動させる
        draw(screen): 弾を画面上に描画する
    """
    def __init__(self, x:float, y:float, target_x:float, target_y:float, bullet_type: str):
        """
        Bulletオブジェクトを初期化する。

        引数:
            x : 弾の初期x座標
            y : 弾の初期y座標
            target_x : プレイヤーのx座標
            target_y : プレイヤーのy座標
        """
        self.width = 10
        self.height = 10
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.dx = 0
        self.dy = 0
        self.bullet_image = None
        self.type = bullet_type  # 弾の種類を記録

        # 弾の種類に応じて画像をロード
        if bullet_type == 'player':
            self.bullet_image = pg.image.load('fig/player_bullet.png').convert_alpha()
        elif bullet_type == 'enemy':
            self.bullet_image = pg.image.load('fig/enemy_bullet.png').convert_alpha()

        self.bullet_image = pg.transform.scale(self.bullet_image, (self.width, self.height))  # サイズ変更
        angle = math.atan2(target_y - y, target_x - x)
        speed = 5
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed

    def move(self):
        """弾を現在の速度に基づいて移動させる。"""
        self.x += self.dx
        self.y += self.dy

    def draw(self, screen: pg.Surface):
        """
        弾を画面上に描画する。

        引数:
            screen (pygame.Surface): 描画対象の画面
        """
        screen.blit(self.bullet_image, (int(self.x), int(self.y)))

def main():
    global screen
    frame_image = pg.image.load('fig/frame.png').convert_alpha()
    frame_image = pg.transform.scale(frame_image, (GAME_AREA_SIZE+80, GAME_AREA_SIZE+140))
    font = pg.font.Font(None, 24)
    background = BACKGROUND_IMAGE
    player = Player()
    enemy = Enemy() # enemy関数の呼び出し
    player_bullets = [] #プレイヤーと敵の弾を保持するリスト
    enemy_bullets = []
    clock = pg.time.Clock()

    running = True
    while running:

        screen.blit(background, (0, 0))
        screen.blit(frame_image, (GAME_AREA_X-40, GAME_AREA_Y-70))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
                elif event.key == pg.K_SPACE:  # スペースキーで弾の発射
                    player_bullets.append(Bullet(player.x + player.width // 2, player.y,
                                                player.x + player.width // 2, 0, 'player'))

        keys = pg.key.get_pressed()
        player.move(keys[pg.K_RIGHT] - keys[pg.K_LEFT], keys[pg.K_DOWN] - keys[pg.K_UP])

        enemy.move()

        if random.random() < 0.02: # 弾の発生
            # 画面の四辺からランダムに弾を発射
            side = random.choice(['top', 'bottom', 'left', 'right'])
            if side == 'top':
                x = random.randint(0, SCREEN_WIDTH)
                y = 0
            elif side == 'bottom':
                x = random.randint(0, SCREEN_WIDTH)
                y = SCREEN_HEIGHT
            elif side == 'left':
                x = 0
                y = random.randint(0, SCREEN_HEIGHT)
            else:  # right
                x = SCREEN_WIDTH
                y = random.randint(0, SCREEN_HEIGHT)

            target_x = GAME_AREA_X + GAME_AREA_SIZE // 2
            target_y = GAME_AREA_Y + GAME_AREA_SIZE // 2
            enemy_bullets.append(Bullet(x, y, target_x, target_y, 'enemy'))

        # プレイヤーの弾の移動と当たり判定
        for bullet in player_bullets[:]: # 弾の動きと衝突
            bullet.move()
            if bullet.y < 0:
                player_bullets.remove(bullet)
            elif (enemy.x < bullet.x < enemy.x + enemy.width and
                  enemy.y < bullet.y < enemy.y + enemy.height):
                enemy.hp -= 10 # 敵HPの更新
                player.sp += 5 # プレイヤーSPの更新
                player_bullets.remove(bullet)

        # 敵の弾の移動と当たり判定
        for bullet in enemy_bullets[:]:
            bullet.move()
            if (bullet.x < 0 or bullet.x > SCREEN_WIDTH or
                bullet.y < 0 or bullet.y > SCREEN_HEIGHT):
                enemy_bullets.remove(bullet)
            elif (player.x < bullet.x < player.x + player.width and
                  player.y < bullet.y < player.y + player.height):
                player.hp -= 1 # プレイヤーHPの更新
                enemy_bullets.remove(bullet)

        if player.hp <= 0 or enemy.hp <= 0: # ゲームの終了判定
            running = False # ゲームを終了させる

        #screen.fill((0, 0, 0))
        # プレイヤーの行動範囲を視覚的に表示する
        # pg.draw.rect(screen, WHITE, (GAME_AREA_X, GAME_AREA_Y, GAME_AREA_SIZE, GAME_AREA_SIZE), 2)
        player.draw(screen)
        # 敵キャラを表示
        enemy.draw(screen)
        for bullet in player_bullets + enemy_bullets: # 弾の描画
            bullet.draw(screen)

        # プレイヤーのHPバーとテキストを描画
        pg.draw.rect(screen, RED, (10, SCREEN_HEIGHT - 30, player.hp * 2, 20))  # プレイヤーHPのゲージを表示
        hp_text_surface = font.render(f"HP: {player.hp}", True, (255, 255, 255))  # テキストサーフェスを作成
        screen.blit(hp_text_surface, (10, SCREEN_HEIGHT - 50))  # テキストを描画

        # 敵のHPバーとテキストを描画
        pg.draw.rect(screen, GREEN, (10, 10, enemy.hp * 2, 20))  # 敵HPのゲージを表示
        enemy_hp_text_surface = font.render(f"Enemy HP: {enemy.hp}", True, (255, 255, 255))  # テキストサーフェスを作成
        screen.blit(enemy_hp_text_surface, (10, 40))  # テキストを描画

        # プレイヤーのSPバーとテキストを描画
        pg.draw.rect(screen, BLUE, (SCREEN_WIDTH - 210, SCREEN_HEIGHT - 30, player.sp * 2, 20))  # プレイヤーSPのゲージを表示
        sp_text_surface = font.render(f"SP: {player.sp}", True, (255, 255, 255))  # テキストサーフェスを作成
        screen.blit(sp_text_surface, (SCREEN_WIDTH - 210, SCREEN_HEIGHT - 50))  # テキストを描画

        pg.display.flip()
        clock.tick(60)

    pg.quit()


if __name__ == "__main__":
    main()