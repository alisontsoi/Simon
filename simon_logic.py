from random import randrange


class Simon():
    def __init__(self):
        self.color_dict = {1: 'green', 2: 'yellow', 3: 'red', 4: 'blue'}
        self.memory_list = []
        self.game_over = False 
        self.score = 0
        
    def get_score(self):
        return self.score
    
    def get_memory(self):
        color_list = []
        for i in self.memory_list:
            color_list.append(self.color_dict[i])
        return color_list
            
        
    def score_point(self):
        self.score += 1
        return self.score
    
    def reset(self):
        self.memory_list = []
        self.game_over = False
        self.score = 0
        
    def add_color(self):
        self.memory_list.append(randrange(1,5))
         
    def check_equality(self, user_input):
        for i in range(len(self.memory_list)):
            if self.color_dict[self.memory_list[i]] != user_input[i]:
                self.game_over = True
                return False
        return True 