from game import Game 
import numpy as np
import time
import cv2

class case_score():
    ###Assumption Two player game only
    def __init__(self,gameplay):
        self.gameplay = gameplay
        self.count = 0
        self.points = np.zeros(4)

    def roll(self):
        (self.dice, self.move_pieces, self.player_pieces, enemy_pieces, self.player_is_a_winner, self.there_is_a_winner), self.player_i = self.gameplay.get_observation()

    def getPlayer(self):
        return self.player_i    

    def is_winner(self):
        if self.player_is_a_winner or self.there_is_a_winner:
            return True
    
    def update_positions(self):
        self.player = self.gameplay.get_pieces()[0][0]
        self.opponent = self.gameplay.get_pieces()[0][2]
        for i in range(len(self.opponent)):
            if self.opponent[i] < 27:
                self.opponent[i] += 26
            else:
                self.opponent[i] -= 26
        print(self.opponent,' opponent')
        print(self.player,' player')

    def in_enemy_radar(self):
        #w1
        enemy_radar_arr = [0]*4
        for i in range(4):
            for j in range(4):
                if 0 < self.player[i] - self.opponent[j]  <= 6:
                    if self.player[i] + self.dice < self.opponent[j] + 3:
                        enemy_radar_arr[i] = -100
                    else:
                        enemy_radar_arr[i] = 100
                else:
                        enemy_radar_arr[i] = 0
        return enemy_radar_arr

    def in_player_radar(self):
        #w2
        player_radar_arr = [0]*4
        for i in range(4):
            for j in range(4):
                if 0 < self.opponent[j] - self.player[i] <= 6:
                    if (self.player[i] + self.dice == self.opponent[j]): 
                        player_radar_arr[i] += 300
                        break
                    if (self.opponent[j] - self.player[i] + self.dice <= 6): 
                        player_radar_arr[i] += 50
                    if self.player[i] + self.dice > self.opponent[j]:
                        player_radar_arr[i] -= 100
        return player_radar_arr

    def calcPoints(self):
        self.points[self.player_i] += self.dice
        pass
        #Left to be completed

    def isZero(self,obj):
        if obj == 0:
            return True

    def safe_token(self):
        pass

    def token_at_start(self):
        #w5
        start_token_arr = [0]*4
        for i in range(4):
            if self.isZero(self.player[i]):
                start_token_arr[i] += self.count * 2
        return start_token_arr

    def token_in_home_lane(self):
        #w6
        home_lane_arr = [0]*4
        for i in range(4):
            if 51 < self.player[i] < 57:
                if self.player[i] +  self.dice == 57:
                        home_lane_arr[i] = 1000
                elif self.player[i] +  self.dice < 57:  
                    home_lane_arr[i] = 200
                else:
                    home_lane_arr[i] = -100
                    
        return home_lane_arr
                
    def return_score(self):
        w1 = 15
        w2 = 15
        w5 = 1
        w6 = 10
        w7 = 5
        total_score = [0]*4
        for i in range(4):
            total_score[i] = self.in_enemy_radar()[i] * w1 + self.in_player_radar()[i] * w2 + self.token_at_start()[i] * w5 + self.token_in_home_lane()[i] * w6 + self.player[i] * w7
            print('i:',total_score[i])
        return total_score

    def player_move(self):
        print("player dice: ",self.dice)
        self.count += 1
        mod_score = []
        score = self.return_score()
        print("total score", score)
        if not len(self.move_pieces):
            print("player not moving")
            self.gameplay.answer_observation(-1)
            return

        if len(self.move_pieces) == 4:
            print('4 pieces')
            self.player_chosen = score.index(max(score))
            self.gameplay.answer_observation(score.index(max(score)))
            print("chosen token = ", self.player_chosen)
            return

        for i in range(4):
            if i in self.move_pieces:
                mod_score.append((score[i],i))
        
        print("mod_score", mod_score)
        print('no 4 pieces')
        self.player_chosen = max(mod_score)[1]
        #print(score.index(max(mod_score)[1]))
        #print(self.move_pieces)
        self.gameplay.answer_observation(max(mod_score)[1])
        print("chosen token = ", self.player_chosen)

    def opponent_move(self):
        print("opponent dice: ",self.dice)
        if len(self.move_pieces):
            print("opponent moved")
            #print(self.move_pieces)
            #print(random.choice(np.array(self.move_pieces)))
            self.gameplay.answer_observation(np.random.choice(self.move_pieces))
        else:
            self.gameplay.answer_observation(-1)
            print("opponent not moving")

    def winner(self):
        return self.gameplay.get_winners_of_game()

    def display(self):
        enviroment_image_rgb = self.gameplay.render_environment() # RGB image of the enviroment
        enviroment_image_bgr = cv2.cvtColor(enviroment_image_rgb, cv2.COLOR_RGB2BGR)
        cv2.imshow("Enviroment", enviroment_image_bgr)
        cv2.waitKey(1)
    
#def board(self, name):
#visualizer.draw_basic_board(draw_taile_number=False)
    def board(self):
        print("************BOARD DETAILS***********************")
        print("is in enemy's radar =",self.in_enemy_radar()) 
        print("is in player's radar =",self.in_player_radar())
        print("Token is at start =",self.token_at_start()) 
        print("Token is in homelane =",self.token_in_home_lane())
        #print("Token is in homelane =",self.token_in_home_lane())

    def getFlag(self):
        return self.gameplay.getFlagOrigin()

    #def save(self, name):
    #self.gameplay.save_video(name)
    def getKill_status(self):
                        
        pass    
gp = Game(ghost_players=[1, 3])
gameplay = case_score(gp)
gameplay.roll()
while gameplay.getFlag():
    print("")
    gameplay.update_positions()
    if gameplay.getPlayer() == 0:
        print("player")   
        gameplay.display()
        #gameplay.board()
        gameplay.player_move()
        gameplay.roll()
    time.sleep(2)

    if gameplay.getPlayer() == 2:
        print("Opponent")   
        gameplay.display()
        gameplay.opponent_move()
        gameplay.roll()
    time.sleep(2)
    print("--------------------NEW ",gameplay.count," TURN---------------------------")
#print(gameplay.winner())
cv2.destroyAllWindows()
"""
winner_matrix = [0] * 2
for i in range(100):
    gp = Game(ghost_players=[1, 3])
    gameplay = case_score(gp)
    gameplay.roll()
    while not gameplay.is_winner(): 
        #gameplay.display()
        print("")
        gameplay.update_positions()
        if gameplay.getPlayer() == 0:
            print("player")   
            #gameplay.board()
            gameplay.player_move()
            gameplay.roll()
        if gameplay.getPlayer() == 2:
            print("Opponent")   
            gameplay.opponent_move()
            gameplay.roll()
        print("--------------------NEW TURN---------------------------")
        #time.sleep(2)
    if gameplay.winner() == [0]:
        winner_matrix[0] += 1
    else:
        winner_matrix[1] += 1
"""
#gameplay.save("game_video.mp4")

"""
gameplay.save_video(f"game_video.mp4")
gp.get_observation() 
# dice, selfPosition, OpponentPosition, Gives player position
# [3 arrays for positions with respect to player]
# player_is_a_winner, there_is_a_winner
# Current_player > Which player's turn it is
gp.answer_observation()
#takes one parameter that is player to be moved.
"""

"""
RULES
Setupludo

Rules for Ludo apply to 2-4 players.
Each player chooses 4 pieces of the same color and places them in the space of the corresponding color.
You can play with general. dice or ludo dice. 
The Ludo cube has six sides, but eyes 3 and 5 have been replaced with globes and stars. If you hit a globe,
you must move a piece to the nearest globe space on the playing board also from your starting area. If you hit a star with the dice, you must move one piece forward to the nearest star field - and from there jump to the next one. If a piece is too close to the target to benefit from a globe or star, the move cannot be used on that piece. All other rolls give the right to move a piece the number of squares shown by the eyes.
Extra throws are awarded by hitting a globe or a six.
Common is a six-sided cube without star and globe. With it, you have to roll a six to move a checker out of the starting area, while all other throws give you the right to move a checker the number of squares the eyes show. Extra throw is given when a six is hit.
Start

The players take turns rolling the dice.
When 6s are hit, you have the right to move a piece onto the field.
If all pieces are the same in the starting field, you have three attempts to hit a 6.
The players take turns hitting clockwise.
The course of the game

A 6 gives the right to an extra roll.
The player moves the number of spaces corresponding to the eyes on the die. You follow the cleaning of the clock around the track.
If you land on a square where there is already a checker, the checker that arrived first must return to
the starting square. If, on the other hand, there are two pieces on the field, it is the last one that has to go back to the start.
You cannot fail to move a piece. That is you have to move a piece, even if that means you have to
go back to the start.
Fields

On the playing board there are several special areas and fields.

    The starting area is where the four pieces start. To take a piece out of the starting area, you have to hit a globe if you play with the ludo dice, or a six if you play with a regular dice. If you have all your pieces in the starting area, you get up to three moves with the dice before the turn is passed on.
    The target area is where the four pieces must be followed. Each player has his own goal area, and no other player may take his pieces into it. To reach the end of the target area, it must be hit precisely - otherwise you have to move your piece in the opposite direction.
    Globus fields protect the pieces from being knocked home. If an opponent's piece lands on a protected piece, it is itself knocked home. However, there is an exception for the colored globe fields. For example, only red pieces can be protected on the red globe field, regardless of the number of pieces you have on the field. If you have two pieces standing on the opponent's colored globe, they can both be knocked home.
    Star fields act as shortcuts that can bring the pieces to the target area faster. If a piece lands on a star, it must be moved forward to the next star. If it is the star in front of the goal area that lands on, the piece is moved directly into the goal.

The winner

.. is the first to get all 4 pieces to the finish line.
The goal is the center, and you have to go all the way around and in via your own color to get to the goal. Once
you have entered the colored fields, you cannot be beaten home.
Is played with general. die, the exact number of missing eyes must be hit in order to move to
the top. If you cannot move forward, you must remain standing until the next turn. 

"""
