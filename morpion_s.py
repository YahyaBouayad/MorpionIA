import copy
import random
import streamlit as st


class Joueur:

    def __init__(self, sign):
        self.sign = sign

    def play(self, game):
        return (0, 0)

class Humain(Joueur):
    def play(self, game):
       y = int(input("Entrer le numero de la ligne (1 a "+str(game.size)+") : "))
       x = int(input("Entrer le numero de la colonne (1 a "+str(game.size)+") : "))
       return (x-1, y-1)
   
    def play_streamlit(self, game):
        # Avec Streamlit, utilisez des widgets pour obtenir les entrées de l'utilisateur
        y = st.number_input("Entrer le numéro de la ligne (1 à {})".format(game.size), 1, game.size)
        x = st.number_input("Entrer le numéro de la colonne (1 à {})".format(game.size), 1, game.size)

        # Le bouton pour effectuer le mouvement
        if 'bouton_clique' not in st.session_state:
            st.session_state['bouton_clique'] = False

        if st.button('Jouer ce coup') or st.session_state['bouton_clique']:
            st.session_state['bouton_clique'] = True
            return (x-1, y-1)  # Retourner les coordonnées ajustées
        else:
            return None
    
class Robot(Joueur):
    
    def __init__(self, sign, depth=5):
        self.sign = sign
        self.depth = depth      


    def play(self, game):
        x, y, _ = self.minimax_ab(game)
        return (x, y)
    def play_streamlit(self, game):
        x, y, _ = self.minimax_ab(game)
        return (x, y)

    def minimax_ab(self, game, depth=None, alpha=float('-inf'), beta=float('inf'), maximizing_player=True):
        if depth is None:
            depth = self.depth

        if depth == 0 or game.full(game.table) or game.win(game.table) != "*":
            return None, None, self.evaluate(game)

        if maximizing_player:
            value = float('-inf')
            best_move = None
            for x in range(game.size):
                for y in range(game.size):
                    if game.table[x][y] == "*":
                        new_game = copy.deepcopy(game)
                        new_game.play(x, y, self.sign)
                        new_value = self.minimax_ab(new_game, depth-1, alpha, beta, False)[2]
                        if new_value > value:
                            value = new_value
                            best_move = (x, y)
                        alpha = max(alpha, value)
                        if alpha >= beta:
                            break
            return best_move[0], best_move[1], value
        else:
            value = float('inf')
            best_move = None
            for x in range(game.size):
                for y in range(game.size):
                    if game.table[x][y] == "*":
                        new_game = copy.deepcopy(game)
                        new_game.play(x, y, "O" if self.sign == "X" else "X")
                        new_value = self.minimax_ab(new_game, depth-1, alpha, beta, True)[2]
                        if new_value < value:
                            value = new_value
                            best_move = (x, y)
                        beta = min(beta, value)
                        if beta <= alpha:
                            break
            return best_move[0], best_move[1], value

    def evaluate(self, game):
        winner = game.win(game.table)
        if winner == self.sign:
            return 1
        elif winner is not None:
            return -1
        else:
            return 0

       
class Jeu:

    # Initialisation du tableau de jeu
    def __init__(self, size, player1, player2):
        self.size = size
        self.table = [["*" for x in range(size)] for y in range(size)]
        self.player1 = player1
        self.player2 = player2
        
    def show_streamlit(self):
        display_str = ""
        line = "  "
        for x in range(self.size):
            line += str(x+1) + " "
        display_str += line + "\n"
    
        for y in range(self.size):
            line = str(y+1) + " "
            for x in range(self.size):
                line += self.table[x][y] + " "
            display_str += line + "\n"
    
        game_display.text(display_str)
        
    def show(self):
        print("")
        line = "  "
        for x in range(self.size):
            line += str(x+1)+" "
        print(line)
        for y in range(self.size):
            line = str(y+1)+" "
            for x in range(self.size):
                line += self.table[x][y]+" "
            print(line)
        print("")

    def full(self, table):
        for x in range(self.size):
            for y in range(self.size):
                if table[x][y] == "*":
                    return False
        return True
    
    def line(self, table, y):
        player = table[0][y]
        changed = False
        for x in range(self.size):
            if table[x][y] != player:
                changed = True
        if changed:
            return "*"
        return player
    
    def col(self, table, x):
        player = table[x][0]
        changed = False
        for y in range(self.size):
            if table[x][y] != player:
                changed = True
        if changed:
            return "*"
        return player
    
    def dia(self, table, d):
        i = (0 if d == 0 else self.size-1)
        player = table[i][0]
        changed = False
        for x in range(self.size):
            i = (x if d == 0 else self.size-1-x)
            if table[i][x] != player:
                changed = True
        if changed:
            return "*"
        return player
    
    def play(self, x, y, player):
       if x >= 0 and x < self.size and y >= 0 and y < self.size and self.table[x][y] == "*":
           self.table[x][y] = player
           return True
       return False
   
    def win(self, table):
        for i in range(self.size):
            line = self.line(table, i)
            if line != "*":
                return line
            col = self.col(table, i)
            if col != "*":
                return col
        for i in range(2):
            dia = self.dia(table, i)
            if dia != "*":
                return dia
        return "*"
    # ...

    def start(self):
        if 'game_state' not in st.session_state:
            st.session_state['game_state'] = {
                'table': [["*" for _ in range(self.size)] for _ in range(self.size)],
                'current_player': 0,
                'game_over': False
            }

        self.table = st.session_state['game_state']['table']
        current_player_index = st.session_state['game_state']['current_player']
        game_over = st.session_state['game_state']['game_over']

        

        if game_over:
            # Logique pour afficher le résultat final
            # ...
            return

        player = [self.player1, self.player2][current_player_index]
        st.write("Tour de {}".format(player.sign))
        if isinstance(player, Robot):
            move = player.play(self)
            if move is not None:
                (x, y) = move
                if self.play(x, y, player.sign):
                    # Mettre à jour l'état du jeu après le mouvement de l'IA
                    st.session_state['game_state']['table'] = self.table
                    st.session_state['game_state']['current_player'] = 1 - current_player_index
                    # Vérifier si le jeu est terminé
                    if self.win(self.table) != "*" or self.full(self.table):
                        st.session_state['game_state']['game_over'] = True
        else:
            move = player.play_streamlit(self)
            if move is not None:
                (x, y) = move
                if self.play(x, y, player.sign):
                    # Mettre à jour l'état du jeu
                    st.session_state['game_state']['table'] = self.table
                    st.session_state['game_state']['current_player'] = 1 - current_player_index
    
                    if self.win(self.table) != "*" or self.full(self.table):
                        st.session_state['game_state']['game_over'] = True
        self.show_streamlit()

# ...


                    



st.title("Jeu de Morpion")
mode_jeu = st.radio("Choisissez le mode de jeu", ('J1 vs J2', 'J1 vs IA', 'IA vs IA'))


# Créer une fonction pour initialiser le jeu selon le mode
def initialiser_jeu(mode):
    size = 3
    if mode == 'J1 vs J2':
        return Jeu(size, Humain("X"), Humain("O"))
    elif mode == 'J1 vs IA':
        return Jeu(size, Humain("X"), Robot("O"))
    else:  # IA vs IA
        return Jeu(size, Robot("X"), Robot("O"))

# Bouton pour démarrer le jeu
if st.button('Démarrer le jeu'):
    game = initialiser_jeu(mode_jeu)
    st.session_state['game'] = game
    st.session_state['game_started'] = True

game_display = st.empty()
# Logique du jeu
if st.session_state.get('game_started', False):
    game = st.session_state['game']
    game.start()
if st.button("Actualiser ( si probleme )"):
    print(1+1)


