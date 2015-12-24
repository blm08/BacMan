import pygame
import constantes
from pygame.locals import *

class Container:
    MARGIN = 10
    """
    Classe créant un conteneur de boutons pour que ceux-ci soient centrés horizontalement et verticalement
    """

    def __init__(self, page, loop, margin_top=0, margin_bottom=0):
        self.page = page
        self.loop = loop

        self.margin_top = margin_top
        self.margin_bottom = margin_bottom

        self.l_widgets = []

    def add_widget(self, widget):
        self.l_widgets.append(widget)

        return widget

    def set_margin(self, top, bottom):
        self.margin_top = top
        self.margin_bottom = bottom

    def calculate_coords(self):
        # Hauteur de la pile d'éléments

        total_height = 0
        for widget in self.l_widgets:
            total_height += widget.get_height() + 2 * Container.MARGIN

        # Coordonné y du coin supérieur gauche du premier widget
        coord_y = (self.page.window.get_height() - self.margin_top - self.margin_bottom - total_height) / 2 + self.margin_top

        for widget in self.l_widgets:
            # Coordonné x du coin supérieur gauche du widget
            coord_x = (self.page.window.get_width() - widget.get_width()) / 2
            widget.set_coords(coord_x, coord_y + Container.MARGIN)
            coord_y += widget.get_height() + 2 * Container.MARGIN

    def render(self):
        for widget in self.l_widgets:
            widget.render()


class Button:
    """
    Classe d'instenciation des boutons
    """
    def __init__(self, page, loop, label, callback, directory=constantes.PATH_PIC_BUTTON):
        """
        __init__() --> None.
        """

        self.coords = (0, 0)

        self.label = label
        self.page = page    # variable 'background' de la classe 'MainMenu'
        self.action = callback # fonction à exécuter lors du clic sur le bouton
        self.loop = loop

        # Chargement de la texture du bouton
        self.surface = pygame.image.load(directory).convert_alpha()

        # Chargement de la police + taille de la police
        self.font = pygame.font.Font(constantes.MENUFONT_DIR, constantes.TEXTFONT_SIZE)
        self.label_surface = self.font.render(self.label, 0, constantes.RGB_WHITE)

        self.text_surface = self.label_surface

        # Ajout du bouton dans la boucle pour que celle-ci détecte les clics sur le bouton
        self.loop.add_widget(self)

    def render(self):

        # Positionnement du bouton dans la fenêtre
        self.page.window.blit(self.surface, self.coords)

        # Raccourcis
        b = self.surface
        t = self.text_surface

        #Affichage du texte en fonction de sa taille et celle du bouton, afin qu'il soit centré quelque soit sa taille
        self.page.window.blit(self.text_surface, (
            (self.coords[0] + b.get_width() / 2) - t.get_width() / 2,
            (self.coords[1] + b.get_height() / 2) - t.get_height() / 2
        ))

    def get_height(self):
        return self.surface.get_height()

    def get_width(self):
        return self.surface.get_width()

    def set_coords(self, x, y):
        self.coords = (x, y)

    def check_coords(self, coords):
        if self.coords[0] < coords[0] < self.coords[0] + self.surface.get_width():
            if self.coords[1] < coords[1] < self.coords[1] + self.surface.get_height():
                return True

        return False

    def disable(self):
        pass

    def enable(self):
        pass

class TextInput(Button):
    def __init__(self, page, loop, label, callback, max_length=20):
        Button.__init__(self, page, loop, label, callback)

        # Lors d'un cliq sur le champ, ce dernier obtient le focus
        self.action = self.set_focus
        self.content = ""
        self.max_length = max_length

        self.content_surface = self.font.render(self.content, 0, constantes.RGB_WHITE)

    def set_focus(self):
        self.loop.focus_on(self)

        self.focus = True

        self.text_surface = self.content_surface

    def remove_focus(self):
        self.focus = False

        if len(self.content) == 0:
            self.text_surface = self.label_surface

    def keydown(self, event):
        if chr(event.key) in constantes.KEYS and len(self.content) < self.max_length:
            self.content = self.content + chr(event.key)

        elif event.key == 8:
            if self.content:
                self.content = self.content[:-1]

        elif event.key == 13:
            self.page.submit()

        self.content_surface = self.font.render(self.content, 0, constantes.RGB_WHITE)

        self.text_surface = self.content_surface

class PasswordInput(TextInput):
    pass


class TextDisplay:
    """
    Classe d'instenciation d'une zone de texte. 
    """

    def __init__(self, page, loop, text):

        """
        __init__() --> None.
        """
        self.coords = (0, 0)

        self.page = page
        self.loop = loop
        self.text = text

        # Chargement de la police + taille de la police
        self.font = pygame.font.Font(constantes.TEXTFONT_DIR, constantes.TEXTFONT_SIZE)

        self.lines_surfaces = []

        # Construction des surfaces pygame pour chaque ligne
        for line in text.split("\n"):
            line_surface = self.font.render(line, 0, constantes.RGB_WHITE)
            self.lines_surfaces.append(line_surface)

        # Ajout du texte dans la boucle
        self.loop.add_widget(self)


    def render(self):

        line_y = self.coords[1]

        for line in self.lines_surfaces:
            line_x = self.coords[0] + (self.get_width() - line.get_width()) / 2

            print(line_x, line_y)
            self.page.window.blit(line, (line_x, line_y))

            line_y += line.get_height()


    def get_height(self):
        """
        Retourne la hauteur de la zone de texte
        """

        height = 0

        for surface in self.lines_surfaces:
            height += surface.get_height()

        return height

    def get_width(self):
        max_width = 0

        for surface in self.lines_surfaces:
            if surface.get_width() > max_width:
                max_width = surface.get_width()

        return max_width

    def set_coords(self, x, y):
        self.coords = (x, y)

    def check_coords(self, event):
        return False

