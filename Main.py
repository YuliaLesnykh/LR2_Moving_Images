import sys
import pygame

WIDTH = 900
HEIGHT = 600
FPS = 60

BALL_RADIUS = 24
INITIAL_HEIGHT = 320
GRAVITY = 900.0

RESTITUTION = 0.9

MIN_REBOUND_HEIGHT = 12.0

BACKGROUND = (255, 240, 245)
GROUND_COLOR = (90, 170, 90)
BALL_COLOR = (255, 182, 193)
TEXT_COLOR = (35, 45, 60)
ACCENT_COLOR = (0,0,0)


class BouncingBall:

    def __init__(self):
        self.floor_y = HEIGHT - 80
        self.x = WIDTH // 2
        self.radius = BALL_RADIUS
        self.reset()

    def reset(self):
        self.y = (
            self.floor_y
            - self.radius
            - INITIAL_HEIGHT
        )

        self.vy = 0.0
        self.finished = False
        self.bounces = 0

        self.current_height = INITIAL_HEIGHT

    def update(self, dt):

        if self.finished:
            return

        self.vy += GRAVITY * dt
        self.y += self.vy * dt

        if self.y + self.radius >= self.floor_y:

            self.y = self.floor_y - self.radius

            next_height = (
                RESTITUTION ** 2
                * self.current_height
            )

            self.bounces += 1

            if (
                next_height < MIN_REBOUND_HEIGHT
                or RESTITUTION == 0
            ):
                self.vy = 0.0
                self.finished = True

            else:
                self.vy = -RESTITUTION * abs(self.vy)

                self.current_height = next_height

    def draw(self, screen):

        pygame.draw.line(
            screen,
            GROUND_COLOR,
            (50, self.floor_y),
            (WIDTH - 50, self.floor_y),
            4
        )

        pygame.draw.circle(
            screen,
            BALL_COLOR,
            (self.x, int(self.y)),
            self.radius
        )

        pygame.draw.circle(
            screen,
            (255, 225, 255),
            (self.x - 8, int(self.y) - 8),
            6
        )


def draw_text(screen, font, text, position, color=TEXT_COLOR):
    image = font.render(text, True, color)
    screen.blit(image, position)


def main():

    pygame.init()

    screen = pygame.display.set_mode(
        (WIDTH, HEIGHT)
    )

    pygame.display.set_caption(
        "Упругий шарик"
    )

    clock = pygame.time.Clock()

    font = pygame.font.SysFont("arial", 22)
    small_font = pygame.font.SysFont("arial", 17)

    ball = BouncingBall()

    paused = False

    while True:

        dt = min(
            clock.tick(FPS) / 1000.0,
            0.03
        )

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                elif event.key == pygame.K_SPACE:
                    paused = not paused

                elif event.key == pygame.K_r:
                    ball.reset()
                    paused = False

        if not paused:
            ball.update(dt)

        screen.fill(BACKGROUND)

        ball.draw(screen)

        draw_text(
            screen,
            font,
            "Лабораторная работа №2",
            (28, 22)
        )

        draw_text(
            screen,
            small_font,
            f"g = {GRAVITY}    k = {RESTITUTION}",
            (30, 62)
        )

        draw_text(
            screen,
            small_font,
            f"Отскоков: {ball.bounces}",
            (30, 88)
        )

        draw_text(
            screen,
            small_font,
            "SPACE — пауза | R — заново | ESC — выход",
            (30, HEIGHT - 42)
        )

        if paused:
            draw_text(
                screen,
                font,
                "Пауза",
                (WIDTH // 2 - 42, 120),
                ACCENT_COLOR
            )

        if ball.finished:
            draw_text(
                screen,
                font,
                "Движение завершено",
                (WIDTH // 2 - 120, 130),
                ACCENT_COLOR
            )

        pygame.display.flip()


if __name__ == "__main__":
    main()