# Description: Coping mechanisms game to teach
# coping strategies.
# Author: Jordan A. Caraballo-Vega
# Created: 08/07/2025

import pygame as pg

# ---------- Settings ----------
WIDTH, HEIGHT = 640, 360
FPS = 60
PLAYER_SPEED = 280
ENEMY_SPAWN_EVERY = 0.7  # seconds


# --- Start Menu (clickable + Enter/Space) ---
def show_start_menu(screen):

    clock = pg.time.Clock()
    title_font = pg.font.Font(None, 48)
    text_font = pg.font.Font(None, 28)

    # Centered "Start" button
    btn_rect = pg.Rect(0, 0, 220, 60)
    btn_rect.center = (WIDTH // 2, HEIGHT // 2 + 40)

    while True:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                return False  # user closed the window
            if e.type == pg.KEYDOWN and e.key in (pg.K_RETURN, pg.K_SPACE):
                return True   # keyboard start
            if e.type == pg.MOUSEBUTTONDOWN and e.button == 1 and btn_rect.collidepoint(e.pos):
                return True   # mouse start

        # Hover effect
        hovered = btn_rect.collidepoint(pg.mouse.get_pos())
        border_col = (255, 209, 102) if hovered else (255, 255, 255)

        # --- Draw menu ---
        screen.fill((20, 20, 28))
        title = title_font.render("Dodge the Blocks", True, "white")
        tip = text_font.render("Click Start or press Enter • ESC quits", True, (190, 190, 190))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
        screen.blit(tip, tip.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

        # Button
        pg.draw.rect(screen, (7, 59, 76), btn_rect, border_radius=12)
        pg.draw.rect(screen, border_col, btn_rect, width=3, border_radius=12)
        label = title_font.render("Start", True, border_col)
        screen.blit(label, label.get_rect(center=btn_rect.center))

        pg.display.flip()
        clock.tick(60)


def main():

    # here is where the game will be defined
    print("Start my game")

    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Dodge the Blocks (pygame-ce)")

    if not show_start_menu(screen):
        pg.quit()
        return

    return

# Run the game if this script is the main program
if __name__ == "__main__":
    main()
