import unittest
from PyQt5.QtWidgets import QApplication
from morpion import Morpion  # Assurez-vous que le fichier du jeu est nommé "morpion.py"

class TestMorpion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialise l'application PyQt5 pour les tests."""
        cls.app = QApplication([])

    def setUp(self):
        """Initialise une nouvelle instance du jeu avant chaque test."""
        self.game = Morpion()

    def test_initialisation(self):
        """Vérifie que la grille est vide au début de la partie."""
        for i in range(3):
            for j in range(3):
                self.assertEqual(self.game.grid[i][j].text(), "", "La grille n'est pas vide au démarrage.")

    def test_tour_joueur(self):
        """Vérifie que le joueur peut placer son symbole dans une case vide."""
        self.game.make_move(0, 0)  # Le joueur place un X en haut à gauche
        self.assertEqual(self.game.grid[0][0].text(), "X", "Le symbole n'a pas été correctement placé.")

    def test_validation_coup(self):
        """Empêche qu'un joueur joue dans une case déjà occupée."""
        self.game.make_move(0, 0)  # Place un X
        self.game.make_move(0, 0)  # Tente de jouer à nouveau au même endroit
        self.assertEqual(self.game.grid[0][0].text(), "X", "Le coup invalide a été accepté.")

    def test_gestion_egalites(self):
        """Identifie une égalité lorsque toutes les cases sont pleines sans gagnant."""
        # Simule une égalité sur la grille
        moves = [
            (0, 0), (0, 1), (0, 2),
            (1, 0), (1, 1), (1, 2),
            (2, 0), (2, 1), (2, 2)
        ]
        for x, y in moves:
            self.game.current_player = "X"
            self.game.make_move(x, y)

        # Vérifie qu'il n'y a pas de gagnant
        self.assertFalse(self.game.check_winner(), "Le jeu a détecté un gagnant par erreur dans une égalité.")



    def test_ia_simple(self):
        """Vérifie que l'IA joue dans une case valide."""
        self.game.mode_combo.setCurrentText("Joueur contre IA")
        self.game.level_combo.setCurrentText("Simple")
        self.game.current_player = "O"  # Simule le tour de l'IA

        # Appelle l'IA pour jouer
        self.game.ai_move()
        valid_move = any(self.game.grid[i][j].text() == "O" for i in range(3) for j in range(3))
        self.assertTrue(valid_move, "L'IA n'a pas joué dans une case valide.")

    def test_fin_partie(self):
        """Vérifie que le jeu se termine correctement lorsqu'un joueur gagne."""
        # Simule une victoire pour X
        moves = [("X", 0, 0), ("X", 0, 1), ("X", 0, 2)]
        for player, x, y in moves:
            self.game.current_player = player
            self.game.make_move(x, y)

        self.assertTrue(all(self.game.grid[i][j].text() == "" for i in range(3) for j in range(3)),
                        "Le jeu ne s'est pas réinitialisé après la victoire.")

if __name__ == "__main__":
    unittest.main()
