import sys
import random
from copy import deepcopy
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QMessageBox, QVBoxLayout, QComboBox, QLabel
from PyQt5.QtCore import QSize


class Morpion(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jeu de Morpion")
        self.setFixedSize(300, 350)
        self.initUI()

    def initUI(self):
        # Layout principal
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # Menu pour sélectionner le mode de jeu
        self.mode_label = QLabel("Mode de jeu :")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Joueur contre Joueur", "Joueur contre IA"])
        self.main_layout.addWidget(self.mode_label)
        self.main_layout.addWidget(self.mode_combo)

        # Menu pour sélectionner le niveau de l'IA
        self.level_label = QLabel("Niveau de difficulté (IA) :")
        self.level_combo = QComboBox()
        self.level_combo.addItems(["Simple", "Intermédiaire", "Expert"])
        self.main_layout.addWidget(self.level_label)
        self.main_layout.addWidget(self.level_combo)

        # Layout pour la grille
        self.layout = QGridLayout()
        self.main_layout.addLayout(self.layout)

        # Création de la grille de jeu
        self.grid = [[None for _ in range(3)] for _ in range(3)]

        self.current_player = "X"

        for i in range(3):
            for j in range(3):
                button = QPushButton("")
                button.setFixedSize(QSize(80, 80))
                button.clicked.connect(lambda _, x=i, y=j: self.make_move(x, y))
                self.layout.addWidget(button, i, j)
                self.grid[i][j] = button

    def make_move(self, x, y):
        # Vérifie si la case est vide
        if self.grid[x][y].text() == "":
            # Remplir la case avec le symbole du joueur actuel
            self.grid[x][y].setText(self.current_player)

            # Vérifie si le joueur actuel a gagné
            if self.check_winner():
                QMessageBox.information(self, "Victoire", f"Le joueur {self.current_player} a gagné !")
                self.reset_game()
                return

            # Vérifie s'il y a égalité
            if self.is_draw():
                QMessageBox.information(self, "Égalité", "Match nul !")
                self.reset_game()
                return

            # Change de joueur ou laisse l'IA jouer
            if self.mode_combo.currentText() == "Joueur contre IA":
                if self.current_player == "X":  # L'humain a joué
                    self.current_player = "O"
                    QApplication.processEvents()  # Assure l'affichage
                    self.ai_move()
            else:  # Mode Joueur contre Joueur
                self.current_player = "O" if self.current_player == "X" else "X"

    def ai_move(self):
        # Récupère le niveau de difficulté de l'IA
        level = self.level_combo.currentText()

        if level == "Simple":
            self.simple_ai()
        elif level == "Intermédiaire":
            self.intermediate_ai()
        elif level == "Expert":
            self.expert_ai()

        # Vérifie si l'IA a gagné
        if self.check_winner():
            QMessageBox.information(self, "Victoire", f"L'IA ({self.current_player}) a gagné !")
            self.reset_game()
            return

        # Vérifie s'il y a égalité
        if self.is_draw():
            QMessageBox.information(self, "Égalité", "Match nul !")
            self.reset_game()
            return

        # Revenir au joueur humain
        self.current_player = "X"

    def simple_ai(self):
        # IA simple : joue un coup aléatoire
        available_moves = [(i, j) for i in range(3) for j in range(3) if self.grid[i][j].text() == ""]
        if available_moves:
            x, y = random.choice(available_moves)
            self.grid[x][y].setText(self.current_player)

    def intermediate_ai(self):
        # IA intermédiaire : bloque ou gagne si possible
        for i in range(3):
            for j in range(3):
                if self.grid[i][j].text() == "":
                    # Simule un coup pour l'IA
                    self.grid[i][j].setText(self.current_player)
                    if self.check_winner():
                        return
                    self.grid[i][j].setText("")

                    # Simule un coup pour l'adversaire
                    self.grid[i][j].setText("X")
                    if self.check_winner():
                        self.grid[i][j].setText(self.current_player)
                        return
                    self.grid[i][j].setText("")

        # Si aucun coup décisif, joue aléatoirement
        self.simple_ai()

    def expert_ai(self):
        # IA Expert utilisant l'algorithme Minimax
        _, move = self.best_move(self.get_board(), self.current_player)
        if move:
            x, y = move
            self.grid[x][y].setText(self.current_player)

    def best_move(self, board, sign):
        opponent = "X" if sign == "O" else "O"
        best_score = -float("inf") if sign == self.current_player else float("inf")
        best_move = None

        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    # Simule un coup
                    board[i][j] = sign
                    if self.check_winner_board(board):
                        score = 1 if sign == self.current_player else -1
                    elif self.is_draw_board(board):
                        score = 0
                    else:
                        score, _ = self.best_move(board, opponent)
                    # Annule le coup
                    board[i][j] = ""

                    # Mise à jour du meilleur score
                    if sign == self.current_player:
                        if score > best_score:
                            best_score = score
                            best_move = (i, j)
                    else:
                        if score < best_score:
                            best_score = score
                            best_move = (i, j)

        return best_score, best_move

    def get_board(self):
        # Retourne l'état actuel de la grille sous forme de liste
        return [[self.grid[i][j].text() for j in range(3)] for i in range(3)]

    def check_winner(self):
        return self.check_winner_board(self.get_board())

    def is_draw(self):
        board = self.get_board()
        return self.is_draw_board(board) and not self.check_winner_board(board)


    def is_draw_board(self, board):
        """Retourne True si toutes les cases de la grille sont remplies."""
        return all(cell != "" for row in board for cell in row)

    def check_winner_board(self, board):
        """Retourne True si un gagnant est détecté sur la grille."""
        # Vérifie les lignes
        for row in board:
            if row[0] == row[1] == row[2] and row[0] != "":
                return True
        # Vérifie les colonnes
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] and board[0][col] != "":
                return True
        # Vérifie les diagonales
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "":
            return True
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "":
            return True
        return False


    def reset_game(self):
        # Réinitialise le jeu
        for row in self.grid:
            for button in row:
                button.setText("")
        self.current_player = "X"


# Point d'entrée du programme
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Morpion()
    window.show()
    sys.exit(app.exec_())
