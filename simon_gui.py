import simon_logic
import tkinter


class SimonApp():
    def __init__(self):
        self.simon_state = simon_logic.Simon()
        
        self._root_window = tkinter.Tk()
        self._root_window.title('Simon')
        self._root_window.resizable(width= False, height = False)
        
        self._canvas = tkinter.Canvas(master = self._root_window, width = 500, height = 500, background = 'black')
        self._canvas.grid(row = 1 , column = 0 , sticky = tkinter.N + tkinter. E + tkinter.S + tkinter.W)
        self._root_window.columnconfigure(0, weight = 1)
        self._root_window.rowconfigure(1, weight = 1)
        
        self._welcome()
        self.play_button_clicked = False
        
        self._canvas.bind('<Button-1>', self._on_canvas_clicked)
        
        self.turn_pattern = True
        self.user_clicks = []
        
    def run(self):
        self._root_window.mainloop()
    
    def _on_canvas_clicked(self, event: tkinter.Event):
        if not self.play_button_clicked:
            self._canvas.delete(tkinter.ALL)
            self._start()
            self.play_button_clicked = True
            
        elif self.simon_state.game_over:
            self._canvas.delete(tkinter.ALL)
            self.simon_state = simon_logic.Simon()
            self.user_clicks = []
            self._start() 
            
        else:
            color_click = self._which_rectangle(event.x , event.y)
            self._handle_click(color_click)
            
    def _handle_click(self, color_click):
        
        if color_click == None:
            return 
        if not self.turn_pattern:
            self.user_clicks.append(color_click)
            self._flash_color(color_click, 0, 200)
            self._handle_game()
        
    def _handle_game(self):
        if len(self.user_clicks) == len(self.simon_state.get_memory()):
            if not self.simon_state.check_equality(self.user_clicks):
                self._game_over()
            else:
                self.simon_state.score_point()
                self._get_score()
                self.user_clicks = []
                self._current_pattern()
                   
    def _start(self):
        self._draw_rectangles()
        self.color_dict = {'green': self._green , 'yellow': self._yellow, 'red' : self._red, 'blue' : self._blue}
        self._get_score()
        self._current_pattern()
        
        
    def _draw_rectangles(self):
        self._canvas.update()
        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()
        
        self._green = self._canvas.create_rectangle(10,10, canvas_width/ 2 , canvas_height/2 - 10, fill = 'green')
        self._yellow = self._canvas.create_rectangle(canvas_width/2 +10 , 10, canvas_width -10 , canvas_height/2 - 10 , fill = 'yellow')
        self._red = self._canvas.create_rectangle(10, canvas_height/2 , canvas_width/2 , canvas_height -10, fill = 'red')
        self._blue = self._canvas.create_rectangle(canvas_width/2 +10 , canvas_height/2 , canvas_width - 10, canvas_height -10, fill = 'blue')
        
        
    def _get_score(self):
        score_text = 'Score: {}'.format(self.simon_state.get_score())
        self._score_label= tkinter.Label(master= self._root_window, text = score_text, font = 'verdana 10')
        self._score_label.grid( row = 2, column = 0, sticky = tkinter.E)
    
    def _welcome(self):
        self._canvas.create_text(250,100, text = 'SIMON', fill = 'white', font = 'verdana 40')
        self._canvas.create_text(250, 215 , text = 'Do as simon says by following the white \nfor as long as you can ',
                                  fill = 'white', font = 'verdana 15', justify= tkinter.CENTER)
        self._canvas.create_text(250,400, text = '.:PLAY:.', fill = 'white', font = 'verdana 50', activefill = 'red')
        self._canvas.update()
        
    def _current_pattern(self):
        self.turn_pattern = True
        self.simon_state.add_color()
        self._canvas.after(500, lambda: self._show_pattern())
        
    def _show_pattern(self):
        i = 500
        for color in self.simon_state.get_memory():
            self._flash_color(color, i, 500)
            i += 1000
            
        self._canvas.after(i-1000, lambda: self._pattern_done())  
         
    def _flash_color(self, color,  i, j):
        self._canvas.after(i, lambda: self._canvas.itemconfig(self.color_dict[color], fill= 'white'))
        self._canvas.after(i+j, lambda: self._canvas.itemconfig(self.color_dict[color], fill= color))
       
    
    def _which_rectangle(self, x , y):
        for i in [self._green, self._red, self._blue, self._yellow]:
            x0,y0, x1, y1 = self._canvas.coords(i)
            if x0 <= x <= x1 and y0 <= y <= y1:
                return self._canvas.itemcget(i, "fill")
            
    def _game_over(self):
        self._canvas.delete(tkinter.ALL)
        self._canvas.create_text(250,100, text = 'GAME OVER', fill = 'white', font = 'verdana 40')
        self._canvas.create_text(250, 215 , text = 'Score: {} \nClick to play again'.format(self.simon_state.get_score()),
                                 fill = 'white', font = 'verdana 15', justify = tkinter.CENTER)
        self._canvas.create_text(250,400, text = '.:PLAY AGAIN:.', fill = 'white', font = 'verdana 30', activefill = 'red')
        self._canvas.update()
    
    def _pattern_done(self):
        self.turn_pattern = False  
         
        
if __name__ == '__main__':
    SimonApp().run()