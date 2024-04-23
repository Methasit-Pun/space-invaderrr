import pygame
import sys
from button import Button
import subprocess
from alllevel import EasyLevel,NormalLevel,HardLevel

pygame.init()

SCREEN = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Menu")

# Load background image
BG = pygame.image.load("assets/BG.jpg")

# Load music
pygame.mixer.music.load("assets/Alien.mp3")
pygame.mixer.music.play(-1)  # -1 will loop the music indefinitely

# Define function to get font
def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)
# Define play function
# Define play function
def show_loading_screen():
    SCREEN.fill((0, 0, 0))  # Fill the screen with black or any other color
    font = get_font(50)
    text = font.render("Loading...", True, (255, 255, 255))
    text_rect = text.get_rect(center=(1920 // 2, 1080 // 2))
    SCREEN.blit(text, text_rect)
    pygame.display.update()
    pygame.time.delay(2000)  # Simulate loading time, adjust as necessary

def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(pygame.image.load("assets/BG1.jpg"), (0, 0))

        EASY_IMAGE = pygame.image.load("assets/EASY.png")
        EASY_BUTTON = Button(image=EASY_IMAGE, pos=(400, 650))

        HARD_IMAGE = pygame.image.load("assets/HARD.png")
        HARD_BUTTON = Button(image=HARD_IMAGE, pos=(1500, 650))

        NORMAL_IMAGE = pygame.image.load("assets/NORMAL.png")
        NORMAL_BUTTON = Button(image=NORMAL_IMAGE, pos=(950, 600))

        EASY_BUTTON.update(SCREEN)
        HARD_BUTTON.update(SCREEN)
        NORMAL_BUTTON.update(SCREEN)

        PLAY_BACK = Button(image=None, pos=(1700, 1000), text_input="BACK", font=get_font(40), base_color="White", hovering_color="Green")
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                if EASY_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    show_loading_screen()
                    EasyLevel().run()
                if NORMAL_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    show_loading_screen()
                    NormalLevel().run()
                if HARD_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    show_loading_screen()
                    HardLevel().run()

        pygame.display.update()




# Define options function
# Define options function
def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        # Load background image
        lead = pygame.image.load("assets/Leaderboaro.jpg")
        SCREEN.blit(lead, (0, 0))


        OPTIONS_BACK = Button(image=None, pos=(1700, 1000),
                            text_input="BACK", font=get_font(40), base_color="White", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


# Define main menu function
def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_WIDTH, MENU_HEIGHT = 1920, 1080  # Updated resolution to 1920x1080

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        START_GAME_IMAGE = pygame.image.load("assets/START GAME.png")
        START_GAME_BUTTON = Button(pos=(MENU_WIDTH // 2, MENU_HEIGHT // 2.2),
                                   image=START_GAME_IMAGE)  # Using image for the play buttonw

        LEADERBOARD_IMAGE = pygame.image.load("assets/LEADERBOARD.png")
        LEADERBOARD_BUTTON = Button(pos=(MENU_WIDTH // 2, MENU_HEIGHT // 1.8),
                                    image=LEADERBOARD_IMAGE)  # Using image for the leaderboard button

        QUIT_IMAGE = pygame.image.load("assets/Quit.png")
        QUIT_BUTTON = Button(pos=(MENU_WIDTH // 2, MENU_HEIGHT // 1.5),
                             image=QUIT_IMAGE)  # Using image for the quit button

        START_GAME_BUTTON.update(SCREEN)
        LEADERBOARD_BUTTON.update(SCREEN)
        QUIT_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if START_GAME_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if LEADERBOARD_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()  # Assuming this is for the leaderboard
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def main_func():
    main_menu()
if __name__ == "__main__":
    main_menu()
