# Run this script second, after server.py
# Change the configuration at the top right corner to client to run this script
# To have 2 client windows at the same time: Run > Edit Configurations make sure "allow parallel run" is checked

import pygame
from network import Network
import pickle

pygame.font.init()
pygame.init()

width = 700
height = 700

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("impact", 40)
        text = font.render(self.text, True, (255, 255, 255))
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                        self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redraw_window(win, game, player):
    win.fill((128, 128, 128))

    if not (game.connected()):
        font = pygame.font.SysFont("impact", 80)
        text = font.render("Waiting for a player...", True, (255, 0, 0), True)
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    else:
        font = pygame.font.SysFont("impact", 40)
        text = font.render("Your move:", True, (0, 255, 255))
        win.blit(text, (80, 200))

        text = font.render("Opponent's move:", True, (0, 255, 255))
        win.blit(text, (380, 200))

        move_player1 = game.get_player_move(0)
        move_player2 = game.get_player_move(1)
        if game.both_went():
            text1 = font.render(move_player1, True, (0, 0, 0))
            text2 = font.render(move_player2, True, (0, 0, 0))
        else:
            if game.player1_went and player == 0:
                text1 = font.render(move_player1, True, (0, 0, 0))
            elif game.player1_went:
                text1 = font.render("Locked in", True, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", True, (0, 0, 0))

            if game.player2_went and player == 1:
                text2 = font.render(move_player2, True, (0, 0, 0))
            elif game.player2_went:
                text2 = font.render("Locked in", True, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", True, (0, 0, 0))

        if player == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()


btns = [Button("Rock", 50, 500, (0, 0, 0)),
        Button("Scissors", 250, 500, (255, 0, 0)),
        Button("Paper", 450, 500, (0, 255, 0))]


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()  # Connect to the server
    player = int(n.get_player())
    print("You are player ", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get match")
            break

        # Check who won if both players left the match
        if game.both_went():
            redraw_window(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get match")
                break

            font = pygame.font.SysFont("impact", 60)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You won!", True, (255, 0, 0))
            elif game.winner() == -1:
                text = font.render("Tie!", True, (255, 0, 0))
            else:
                text = font.render("You lost!", True, (255, 0, 0))

            win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.player1_went:
                                n.send(btn.text)
                        else:
                            if not game.player2_went:
                                n.send(btn.text)

        redraw_window(win, game, player)


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("impact", 60)
        text = font.render("Click to play", 1, (255, 0, 0))
        win.blit(text, (100, 200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
    main()


while True:
    menu_screen()
