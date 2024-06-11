import pygame
from network import Network

pygame.font.init()

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

    def draw(self):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255,255,255))
        win.blit(text, (self.x + (self.width//2 - text.get_width()//2), self.y + (self.height//2 - text.get_height()//2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if pygame.Rect(self.x, self.y, self.width, self.height).collidepoint(pos):
            return True
        else:
            return False

def draw_window(window, game, p):
    window.fill((128,128,128))

    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for other player...", True, (255,0,0))
        win.blit(text, (width//2 - text.get_width()//2, height//2 - text.get_height()//2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your Move", True, (0,255,255))
        win.blit(text, (80,200))

        text = font.render("Opponent Move", True, (0,255,255))
        win.blit(text, (380,200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.both_went():
            text1 = font.render(move1, 1, (0,0,0))
            text2 = font.render(move2, 1, (0,0,0))

        else:
            if game.p1_went and p == 0:
                text1 = font.render(move1, 1, (0,0,0))
            elif game.p1_went:
                text1 = font.render("Locked In", 1, (0,0,0))
            else:
                text1 = font.render("Waiting...", 1, (0,0,0))
            if game.p2_went and p == 1:
                text2 = font.render(move2, 1, (0,0,0))
            elif game.p2_went:
                text2 = font.render("Locked In", 1, (0,0,0))
            else:
                text2 = font.render("Waiting...", 1, (0,0,0))

        if p == 1:
            win.blit(text2, (100,350))
            win.blit(text1, (400,350))
        else:
            win.blit(text1, (100,350))
            win.blit(text2, (400,350))

        for button in buttons:
            button.draw()

    pygame.display.update()

buttons = [Button("Rock", 50,500,(0,255,0)), Button("Scissors",250,500, (255,0,0)), Button("Paper",450,500, (0,0,255))]

def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    p = int(n.get_p())
    print("You Are Player ", p)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.both_went():
            draw_window(win, game, p)
            pygame.time.delay(200)

            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("comicsans", 90)
            if (game.get_winner() == p):
                text = font.render("You Won!", True, (255,255,255))
            elif game.get_winner() == -1:
                text = font.render("Draw!", True, (255,255,255))
            else:
                text = font.render("You Lost!", True, (255,255,255))
            win.blit(text, (width//2 - text.get_width()//2, height//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.click(pos) and game.connected():
                        if (p == 0 and not game.p1_went) or not game.p2_went:
                            n.send(button.text)

        draw_window(win, game, p)


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (255,0,0))
        win.blit(text, (100,200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

# while True:
#     menu_screen()

main()