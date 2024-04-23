import pygame, sys
import subprocess
import sys

from button import Button


import main
pygame.init()

SCREEN = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/GAMEOVER.jpg")
score = "123,000"

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460),
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_game_over()

        pygame.display.update()

def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_game_over()

        pygame.display.update()

def main_game_over(score):

    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Adjusted position of the quit button
        QUIT_BUTTON = Button(pos=(1700, 1000), text_input="QUIT", font=get_font(60), base_color="White", hovering_color="White")
        AGAIN_BUTTON = Button(pos=(1000, 900), text_input="Play Again", font=get_font(35), base_color="White", hovering_color="White")
        # Load additional images
        HIGH_SCORES_IMAGE = pygame.image.load("assets/HIGH SCORES.png")
        SCORE_IMAGE = pygame.image.load("assets/SCORE_.png")
        END_INFO_IMAGE = pygame.image.load("assets/End_info.png")
        YOUR_RANK_IMAGE = pygame.image.load("assets/your rank_.png")

        for button in [QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        for button in [AGAIN_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        # Render additional images
        SCREEN.blit(HIGH_SCORES_IMAGE, (785, 390))
        SCREEN.blit(SCORE_IMAGE, (520, 270))
        SCREEN.blit(END_INFO_IMAGE, (565, 730))
        SCREEN.blit(YOUR_RANK_IMAGE, (830, 640))





        #Score
        font = pygame.font.Font("assets/font.ttf", 80)
        text = font.render(str(score*1000), True, (255, 255, 255))
        SCREEN.blit(text, (900, 257))

        #score_text = self.score_font.render("Score: " + str(self.score), True, (255, 255, 255))
        #high_score_text = self.score_font.render("High Score: " + str(self.high_score), True, (255, 255, 255))
        #SCREEN.blit(score, (600, 270))
        #self.screen.blit(high_score_text, (self.SCREEN_WIDTH - high_score_text.get_width() - 10, 10))


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                if AGAIN_BUTTON.checkForInput(MENU_MOUSE_POS):
                    #print("Hello world")
                    main.main_func()
                    #subprocess.run(['python',"main.py"])
                    #sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    main.main_func()
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    from hard_level import start_hard_level
                    start_hard_level(SCREEN=1)

 


        pygame.display.update()


    # Replace main_func() with handle_escape_action() in the key event handler

def game_is_over(score):
    main_game_over(score)

if __name__ == "__main__":
    main_game_over(score)
