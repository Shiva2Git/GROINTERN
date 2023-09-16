import pygame as pg
import button

pg.init()

clock = pg.time.Clock()

W = 1150
H = 900
screen = pg.display.set_mode((W, H))

my_font = pg.font.SysFont('Arial', 20)
large_font = pg.font.SysFont('Arial', 40)


def draw_text(text, font, t_color, x_text, y_text):
    font_img = font.render(text, True, t_color)
    screen.blit(font_img, (x_text, y_text))


# define colors
BG = 0, 25, 51
cell_color = 0, 51, 102
dark_red1 = 102, 0, 0
dark_green1 = 0, 102, 0
dark_blue1 = 0, 76, 153
dark_red = 204, 0, 0
dark_green = 0, 153, 0
dark_blue2 = 0, 102, 204

# cell side size
a = 90

# loading images for x and o
x = pg.transform.scale(pg.image.load('x.png'), (a, a))
o = pg.transform.scale(pg.image.load('o.png'), (a, a))
x_win = pg.transform.scale(pg.image.load('x_red.png'), (a, a))
o_win = pg.transform.scale(pg.image.load('o_green.png'), (a, a))

# list of cell coordinates
cell_list = []
cell_x = 420
cell_y = 270
cell_gap = a + 5
cell_0 = (cell_x, cell_y)
cell_1 = (cell_x + cell_gap, cell_y)
cell_2 = (cell_x + 2 * cell_gap, cell_y)
cell_3 = (cell_x, cell_y + cell_gap)
cell_4 = (cell_x + cell_gap, cell_y + cell_gap)
cell_5 = (cell_x + 2 * cell_gap, cell_y + cell_gap)
cell_6 = (cell_x, cell_y + 2 * cell_gap)
cell_7 = (cell_x + cell_gap, cell_y + 2 * cell_gap)
cell_8 = (cell_x + 2 * cell_gap, cell_y + 2*cell_gap)

cell_list.extend((cell_0, cell_1, cell_2, cell_3, cell_4, cell_5, cell_6, cell_7, cell_8))


class Cell(pg.sprite.Sprite):
    def __init__(self, x0, y0):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((a, a))
        self.image.fill(cell_color)
        self.rect = self.image.get_rect()
        self.rect.x = x0
        self.rect.y = y0
        self.clicked = False
        self.status = None

    def draw(self):
        if self.clicked:
            if self.status == 1:
                self.image = x
            if self.status == 2:
                self.image = o
        screen.blit(self.image, self.rect)

    def lightning(self, pos):
        global turn
        if not self.clicked:
            if self.rect.x < pos[0] < self.rect.x + a and self.rect.y < pos[1] < self.rect.y + a:
                if turn == -1:
                    pg.draw.rect(screen, dark_red1, pg.Rect(self.rect.x, self.rect.y, a, a))
                elif turn == 1:
                    pg.draw.rect(screen, dark_green1, pg.Rect(self.rect.x, self.rect.y, a, a))

    def update(self, ev, pos):
        global turn, click_counter, win_list, winning
        # if someone clicks the mouse button
        if ev.type == pg.MOUSEBUTTONDOWN and not winning:
            # if mouse cursor is in the cell
            if self.rect.x < pos[0] < self.rect.x + a and self.rect.y < pos[1] < self.rect.y + a and not self.clicked:
                self.clicked = True
                click_counter += 1
                turn *= -1
                if turn == 1:
                    self.status = 1
                else:
                    self.status = 2

                ii = 0
                for c_coord in cell_list:
                    if self.rect.x == c_coord[0] and self.rect.y == c_coord[1]:
                        if self.status == 1:
                            values[ii] = 1
                        else:
                            values[ii] = 0
                    ii += 1

                win_list = [[(cell_0, values[0]), (cell_1, values[1]), (cell_2, values[2])],
                            [(cell_3, values[3]), (cell_4, values[4]), (cell_5, values[5])],
                            [(cell_6, values[6]), (cell_7, values[7]), (cell_8, values[8])],
                            [(cell_0, values[0]), (cell_3, values[3]), (cell_6, values[6])],
                            [(cell_1, values[1]), (cell_4, values[4]), (cell_7, values[7])],
                            [(cell_2, values[2]), (cell_5, values[5]), (cell_8, values[8])],
                            [(cell_0, values[0]), (cell_4, values[4]), (cell_8, values[8])],
                            [(cell_2, values[2]), (cell_4, values[4]), (cell_6, values[6])]
                            ]

turn = None
click_counter = None
winning = None
values = None
win_coord = None
cell_group = pg.sprite.Group()
play_again_button = None
win_list = None


def set_initial_parameters():
    global turn, click_counter, winning, values, win_coord, cell_group, play_again_button, win_list
    turn = -1
    click_counter = 0
    winning = False
    values = [2, 2, 2, 2, 2, 2, 2, 2, 2]
    play_again_button=button.Button(450, 700)
    # list of winner's cell coordinates
    win_coord = []

    for cell in cell_group:
        cell.kill()
    for i in range(9):
        cell = Cell(cell_list[i][0], cell_list[i][1])
        cell_group.add(cell)

    win_list = [[(cell_0, values[0]), (cell_1, values[1]), (cell_2, values[2])],
                [(cell_3, values[3]), (cell_4, values[4]), (cell_5, values[5])],
                [(cell_6, values[6]), (cell_7, values[7]), (cell_8, values[8])],
                [(cell_0, values[0]), (cell_3, values[3]), (cell_6, values[6])],
                [(cell_1, values[1]), (cell_4, values[4]), (cell_7, values[7])],
                [(cell_2, values[2]), (cell_5, values[5]), (cell_8, values[8])],
                [(cell_0, values[0]), (cell_4, values[4]), (cell_8, values[8])],
                [(cell_2, values[2]), (cell_4, values[4]), (cell_6, values[6])]
                ]

set_initial_parameters()

run = True

while run:

    clock.tick(60)

    screen.fill(BG)

    mouse_pos = pg.mouse.get_pos()

    for c in cell_group:
        c.draw()
        c.lightning(mouse_pos)

    if click_counter >= 5:
        for j in range(8):
            for i in range(2):
                if win_list[j][0][1] == i and win_list[j][1][1] == i and win_list[j][2][1] == i:
                    winning = True
                    win_coord.extend((win_list[j][0][0], win_list[j][1][0], win_list[j][2][0]))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if play_again_button.clicked(event, mouse_pos):
            set_initial_parameters()
        cell_group.update(event, mouse_pos)

    if not winning and click_counter < 9:
        draw_text('Welcome to the Tic-Tac-Toe game.', my_font, dark_blue1, 383, 20)
        draw_text('To put an item, clck on the cell.', my_font, dark_blue1, 400, 60)

        if turn == -1 and click_counter < 9:
            draw_text('PLAYER 1', my_font, dark_red, 415, 160)
            draw_text('IT IS YOUR TURN!', my_font, dark_blue2, 523, 160)
        elif turn == 1 and click_counter < 9:
            draw_text('PLAYER 2', my_font, dark_green, 415, 160)
            draw_text('IT IS YOUR TURN!', my_font, dark_blue2, 523, 160)

    else:
        if turn == 1 and click_counter < 9 and winning:
            draw_text('X WON', large_font, (255, 0, 0), 480, 100)
            for i in range(3):
                screen.blit(x_win, win_coord[i])
        if turn == -1 and click_counter < 9 and winning:
            draw_text('O WON', large_font, (0, 255, 0), 480, 100)
            for i in range(3):
                screen.blit(o_win, win_coord[i])
        if click_counter == 9 and not winning:
            draw_text("It's a tie", my_font, dark_blue2, 520, 140)
        play_again_button.draw(screen)


    pg.display.flip()


