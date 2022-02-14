import pygame
from pghl.generic_types import Pos, Size, ColorValue, Events


class Toggle:
    """
    Toggle widget used for Punctuation
    Slightly more flexible widget and can be used for other projects as well
    (A large amount of time was spent into designing the implementation and implementing this,
     it would be disappointing if I could not use this in other projects)
    """
    def __init__(self, size: Size):
        self.size = size

        # Make rounded Surface
        self.surf = pygame.Surface(size)
        self.surf.set_colorkey((0, 0, 0))

        # Color variables
        self.grey = 100
        self.color = (self.grey, self.grey, self.grey)
        self.hover_border_color = pygame.Color("yellow")
        self.hover_border_width = 2

        # Flags

        # Rectangles
        self.rect = pygame.Rect((0, 0), self.size)
        self.pos_rect = pygame.Rect((0, 0), self.size)
        self.radius = self.size[1] // 2
        self.whole_rect = pygame.Rect(
            (0, 0), (self.rect.width + 2 * self.radius, self.rect.height)
        )
        self.hover_border_rect = pygame.Rect(
            (0, 0),
            (
                self.size[0] + self.hover_border_width * 2,
                self.size[1] + self.hover_border_width * 2,
            ),
        )

        # Toggle circle thingy
        self.toggle_circle_radius = self.radius - 5
        self.toggle_circle_rect = pygame.Rect(
            (0, 0), (self.toggle_circle_radius, self.toggle_circle_radius)
        )
        self.toggle_x = 0

        # Information
        self.label = Label(
            self.rect.center,
            (40 * 2.5, 10 * 2.5),
            "punctuation: ",
            colour="black",
            border_colour="white",
        )
        self.animation_speed = 3

        # Flags
        self.switch = False
        self.transition = False
        self.hover = False
        self.initial_pos = True

        # Count variables
        self.dt = 0

    def update(self, mouse_pos: Pos, events: Events, dt: float) -> None:
        """
        Update the toggle widget

        :param mouse_pos: Position of the mouse
        :param events: Events going on in the current frame
        :param dt: Amount of time taken to complete last frame * FPS
        :return: None
        """
        self.dt = dt

        self.hover = self.whole_rect.collidepoint(mouse_pos)

        for event in events:
            if self.hover:
                self.label.rect.topleft = mouse_pos
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.switch = not self.switch

        # Animate toggle
        if self.switch:
            if self.toggle_circle_rect.x < self.pos_rect.midright[0]:
                self.toggle_x += self.animation_speed * self.dt
        else:
            if self.toggle_circle_rect.x > self.pos_rect.midleft[0]:
                self.toggle_x -= self.animation_speed * self.dt
        self.toggle_circle_rect.x = self.toggle_x

    def transition_fade(self) -> None:
        """
        Convert rgb(100, 100, 100) -> rgb(0, 255, 0)
        And vice versa
        Causes pleasant and subtle fade effect

        :return: None
        """
        r, g, b = self.color

        # r = 100, g = 100, b = 100
        if self.switch:
            if r > 0:
                r -= 1
            if g < 255:
                g += 1
            if b > 0:
                b -= 1
        # r = 0, g = 255, b = 0
        else:
            if r < 100:
                r += 1
            if g > 100:
                g -= 1
            if b < 100:
                b += 1

        self.color = (r, g, b)

    def draw(self, screen: pygame.Surface, pos: Pos, resize_frame: bool):
        self.surf.fill((0, 0, 0))
        self.transition_fade()
        # s_rect = screen.get_rect()

        # Positioning widgets
        self.pos_rect.topleft = pos
        self.whole_rect.center = self.pos_rect.center
        self.hover_border_rect.center = self.pos_rect.center

        if resize_frame:
            self.initial_pos = True

        if self.initial_pos:
            if self.switch:
                self.toggle_x = self.pos_rect.midright[0]
            else:
                self.toggle_x = self.pos_rect.midleft[0]
            self.toggle_circle_rect.x = self.toggle_x
            self.initial_pos = False
        self.toggle_circle_rect.y = self.pos_rect.midleft[1] - 2

        # Hover yellow borderline effect
        if self.hover:
            pygame.draw.circle(
                screen,
                self.hover_border_color,
                self.pos_rect.midleft,
                self.radius + self.hover_border_width,
            )
            pygame.draw.circle(
                screen,
                self.hover_border_color,
                self.pos_rect.midright,
                self.radius + self.hover_border_width,
            )

            pygame.draw.rect(screen, self.hover_border_color, self.hover_border_rect)

        pygame.draw.circle(
            screen,
            self.color,
            self.pos_rect.midleft,
            self.radius,
        )
        pygame.draw.circle(screen, self.color, self.pos_rect.midright, self.radius)

        pygame.draw.rect(self.surf, self.color, self.rect)
        screen.blit(self.surf, pos)

        # Draw toggle circle thingy
        pygame.draw.circle(
            screen,
            "white",
            center=self.toggle_circle_rect.center,
            radius=self.toggle_circle_radius,
        )

        # Widget information
        if self.hover:
            content = "on" if self.switch else "off"
            self.label.change_txt(f"punctuation: {content}")
            self.label.draw(screen)


class LoadingBar:
    def __init__(self, value, fg_color, bg_color, rect: pygame.Rect, _border_img: pygame.Surface, max_value=100):
        self.value = value
        self.sfg_color = fg_color
        self.sbg_color = bg_color
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.rect = rect
        self.rect.center = self.rect.topleft
        self.val_rect = pygame.Rect(
            rect.topleft,
            (self.value, self.rect.height)
        )
        self.loaded = False
        self.border_img = _border_img

        self.border_img = pygame.transform.scale(self.border_img, rect.size)
        self.max_value = max_value

    def draw(self, screen: pygame.Surface, camera, moving: bool = False):
        if moving:
            self.val_rect = pygame.Rect(
                self.rect.topleft,
                (self.value, self.rect.height)
            )
        pygame.draw.rect(screen, self.bg_color, pygame.Rect((self.rect.x - camera[0], self.rect.y - camera[1]),
                                                            self.rect.size))

        self.loaded = self.value >= self.rect.width

        pygame.draw.rect(screen, self.fg_color, pygame.Rect((self.val_rect.x - camera[0], self.val_rect.y - camera[1]),
                                                            (int(self.value), self.rect.height)))

        screen.blit(self.border_img, (self.rect.x - camera[0], self.rect.y - camera[1]))


class Label:
    """
    Label widget used to display information about other widgets
    """
    def __init__(
        self,
        position: Pos,
        size: Size | tuple[float, float],
        content: str,
        colour: ColorValue = None,
        border_colour: ColorValue = None,
        txt_colour: ColorValue = (255, 255, 255),
        shape: str = "rectangle",
    ):
        """
        Initialize the Label Widget.

        :param position: Top-left position of the label
        :param size: Size of the label (width, height)
        :param content:
        :param colour:
        :param border_colour:
        :param txt_colour:
        :param shape:
        """
        self.position = position
        self.size = size
        self.rect = pygame.Rect(self.position, self.size)
        self.surface = pygame.Surface(self.size)
        # self.surface.set_colorkey((0, 0, 0))
        self.content = content

        self.colour = colour or None
        self.border_colour = border_colour or None
        self.txt_colour = txt_colour
        self.shape = shape
        self.t = pygame.font.SysFont("bahnschrift", size=self.rect.width // 14).render(
            content, True, self.txt_colour
        )

    def change_txt(self, txt):
        """
        Changes the label content

        :param txt: Text to be changed into
        :return:
        """
        self.t = pygame.font.SysFont("arial", size=self.rect.size[0] // 8).render(
            txt, True, self.txt_colour
        )

    def change_pos(self, pos):
        """
        Changes the position of the label

        :param pos:
        :return:
        """

        self.position = pos
        self.rect = pygame.Rect(pos, self.size)

    def draw(self, screen: pygame.Surface):
        """
        Draws the label

        :param screen: Screen to blit on
        :return:
        """
        if self.colour:
            if self.shape == "rectangle":
                pygame.draw.rect(
                    self.surface,
                    self.colour,
                    self.surface.get_rect(),
                    border_radius=1,
                    width=5,
                )
        if self.border_colour:
            pygame.draw.rect(
                self.surface,
                self.border_colour,
                self.surface.get_rect(),
                border_radius=4,
                width=1,
            )

        screen.blit(self.surface, self.rect)
        screen.blit(self.t, self.t.get_rect(center=self.rect.center))
