from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
from random import choice

Window.size = (300, 600)

SHAPES = {'I':[[1,1,1,1]],'O':[[1,1],[1,1]],'T':[[0,1,0],[1,1,1]],'S':[[0,1,1],[1,1,0]],'Z':[[1,1,0],[0,1,1]],'L':[[1,0,0],[1,1,1]],'J':[[0,0,1],[1,1,1]]}
COLORS = {'I':(0,1,1),'O':(1,1,0),'T':(1,0,1),'S':(0,1,0),'Z':(1,0,0),'L':(1,0.5,0),'J':(0,0,1)}

class Tetromino:
    def __init__(self, shape_name):
        self.shape_name = shape_name
        self.shape = [row[:] for row in SHAPES[shape_name]]
        self.color = COLORS[shape_name]
        self.x = 5 - len(self.shape[0]) // 2
        self.y = 0
    def get_rotated(self):
        rows, cols = len(self.shape), len(self.shape[0])
        return [[self.shape[rows-1-j][i] for j in range(rows)] for i in range(cols)]

class TetrisGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.grid_size_x = 12
        self.grid_size_y = 22
        self.cell_size = 25
        self.grid = [[None for _ in range(self.grid_size_x)] for _ in range(self.grid_size_y)]
        self.score = 0
        self.game_over = False
        self.current_piece = None
        self.next_piece = None
        self.fall_speed = 0.5
        self.fall_event = None
        self.score_label = Label(text="Score: 0", pos=(10,550), size_hint=(None,None))
        self.add_widget(self.score_label)
        btn_layout = BoxLayout(size_hint=(None,None), size=(300,80), pos=(0,20), spacing=10)
        btn_left = Button(text="←", size_hint=(None,None), size=(70,60))
        btn_left.bind(on_press=self.move_left)
        btn_right = Button(text="→", size_hint=(None,None), size=(70,60))
        btn_right.bind(on_press=self.move_right)
        btn_down = Button(text="↓", size_hint=(None,None), size=(70,60))
        btn_down.bind(on_press=self.move_down)
        btn_rotate = Button(text="↻", size_hint=(None,None), size=(70,60))
        btn_rotate.bind(on_press=self.rotate_piece)
        btn_layout.add_widget(btn_left)
        btn_layout.add_widget(btn_right)
        btn_layout.add_widget(btn_down)
        btn_layout.add_widget(btn_rotate)
        self.add_widget(btn_layout)
        self.spawn_new_piece()
        self.start_fall_timer()
        self.draw_grid()
    def spawn_new_piece(self):
        if not self.next_piece:
            self.next_piece = Tetromino(choice(list(SHAPES.keys())))
        self.current_piece = self.next_piece
        self.next_piece = Tetromino(choice(list(SHAPES.keys())))
        if self.check_collision(self.current_piece.shape, self.current_piece.x, self.current_piece.y):
            self.game_over = True
            if self.fall_event:
                self.fall_event.cancel()
            self.show_game_over()
    def check_collision(self, shape, x, y):
        for i,row in enumerate(shape):
            for j,cell in enumerate(row):
                if cell:
                    gx,gy = x+j, y+i
                    if gx<0 or gx>=self.grid_size_x or gy>=self.grid_size_y or (gy>=0 and self.grid[gy][gx] is not None):
                        return True
        return False
    def merge_piece(self):
        for i,row in enumerate(self.current_piece.shape):
            for j,cell in enumerate(row):
                if cell:
                    gx,gy = self.current_piece.x+j, self.current_piece.y+i
                    if 0<=gy<self.grid_size_y and 0<=gx<self.grid_size_x:
                        self.grid[gy][gx] = self.current_piece.color
        self.check_lines()
        self.spawn_new_piece()
        self.draw_grid()
    def check_lines(self):
        lines = 0
        for y in range(self.grid_size_y-1,-1,-1):
            if all(self.grid[y][x] is not None for x in range(self.grid_size_x)):
                del self.grid[y]
                self.grid.insert(0, [None for _ in range(self.grid_size_x)])
                lines += 1
        if lines:
            self.score += [100,300,500,800][min(lines,4)-1]
            self.score_label.text = f"Score: {self.score}"
    def move_left(self, instance=None):
        if not self.game_over and self.current_piece:
            self.current_piece.x -= 1
            if self.check_collision(self.current_piece.shape, self.current_piece.x, self.current_piece.y):
                self.current_piece.x += 1
            else:
                self.draw_grid()
    def move_right(self, instance=None):
        if not self.game_over and self.current_piece:
            self.current_piece.x += 1
            if self.check_collision(self.current_piece.shape, self.current_piece.x, self.current_piece.y):
                self.current_piece.x -= 1
            else:
                self.draw_grid()
    def move_down(self, instance=None):
        if not self.game_over and self.current_piece:
            self.current_piece.y += 1
            if self.check_collision(self.current_piece.shape, self.current_piece.x, self.current_piece.y):
                self.current_piece.y -= 1
                self.merge_piece()
            self.draw_grid()
    def rotate_piece(self, instance=None):
        if not self.game_over and self.current_piece:
            rotated = self.current_piece.get_rotated()
            if not self.check_collision(rotated, self.current_piece.x, self.current_piece.y):
                self.current_piece.shape = rotated
                self.draw_grid()
    def start_fall_timer(self):
        if self.fall_event:
            self.fall_event.cancel()
        self.fall_event = Clock.schedule_interval(self.drop_piece, self.fall_speed)
    def drop_piece(self, dt):
        if not self.game_over and self.current_piece:
            self.current_piece.y += 1
            if self.check_collision(self.current_piece.shape, self.current_piece.x, self.current_piece.y):
                self.current_piece.y -= 1
                self.merge_piece()
            self.draw_grid()
    def draw_grid(self):
        self.canvas.clear()
        cs = self.cell_size
        with self.canvas:
            for y in range(self.grid_size_y):
                for x in range(self.grid_size_x):
                    color = self.grid[y][x]
                    if color:
                        Color(color[0], color[1], color[2])
                        Rectangle(pos=(x*cs+50, (self.grid_size_y-y-1)*cs+80), size=(cs-1, cs-1))
                    else:
                        Color(0.3,0.3,0.3)
                        Rectangle(pos=(x*cs+50, (self.grid_size_y-y-1)*cs+80), size=(cs-1, cs-1))
            if self.current_piece and not self.game_over:
                Color(self.current_piece.color[0], self.current_piece.color[1], self.current_piece.color[2])
                for i,row in enumerate(self.current_piece.shape):
                    for j,cell in enumerate(row):
                        if cell:
                            x = (self.current_piece.x + j) * cs + 50
                            y = (self.grid_size_y - (self.current_piece.y + i) - 1) * cs + 80
                            Rectangle(pos=(x,y), size=(cs-1, cs-1))
    def show_game_over(self):
        self.game_over_label = Label(text=f"GAME OVER\nScore: {self.score}\nTap to restart", pos=(0,250), size_hint=(None,None), font_size=20)
        self.add_widget(self.game_over_label)
        self.bind(on_touch_down=self.restart_game)
    def restart_game(self, instance, touch):
        self.unbind(on_touch_down=self.restart_game)
        self.remove_widget(self.game_over_label)
        self.grid = [[None for _ in range(self.grid_size_x)] for _ in range(self.grid_size_y)]
        self.score = 0
        self.game_over = False
        self.score_label.text = "Score: 0"
        self.spawn_new_piece()
        self.start_fall_timer()
        self.draw_grid()

class TetrisApp(App):
    def build(self):
        return TetrisGame()

if __name__ == '__main__':
    TetrisApp().run()
