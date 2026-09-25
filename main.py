from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.animation import Animation
import math
import os

# ====== ПУТЬ К ФОТО ======
# Вариант А: фото лежит рядом со скриптом
IMAGE_PATH = 'bg.jpg'

# Вариант Б: полный путь (раскомментируй, если А не работает)
# IMAGE_PATH = '/storage/emulated/0/Download/bg.jpg'


class ObemButton(Button):
    """Кнопка с объёмом, прозрачным фоном и подсветкой."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)
        self.color = (0.95, 0.88, 0.6, 1)
        self.bold = True
        self.font_size = '18sp'
        self.bind(pos=self._redraw, size=self._redraw, state=self._redraw)

    def _redraw(self, *args):
        self.canvas.before.clear()
        self.canvas.after.clear()
        x, y = self.pos
        w, h = self.size
        r = dp(8)
        pressed = self.state == 'down'

        with self.canvas.before:
            Color(0, 0, 0, 0.55)
            RoundedRectangle(pos=(x + dp(2), y - dp(4)), size=(w, h), radius=[r])

        with self.canvas.before:
            Color(1, 1, 1, 0.10 if not pressed else 0.05)
            RoundedRectangle(pos=(x, y + dp(2)), size=(w, h), radius=[r])

        with self.canvas.before:
            Color(0.08, 0.08, 0.12, 0.55 if not pressed else 0.7)
            RoundedRectangle(pos=(x, y), size=(w, h), radius=[r])

        with self.canvas.after:
            Color(0.85, 0.72, 0.35, 0.85 if not pressed else 1)
            Line(rounded_rectangle=(x, y, w, h, r), width=1.2)

        with self.canvas.after:
            Color(1, 1, 1, 0.06)
            RoundedRectangle(pos=(x + dp(4), y + h - dp(8)),
                             size=(w - dp(8), dp(4)), radius=[dp(2)])


class VolumeTitle(Widget):
    """Объёмная анимированная надпись."""
    def __init__(self, text='SLOBODA OBLOK', **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(420), dp(70))

        self.shadow = Label(
            text=f'[b]{text}[/b]', markup=True,
            font_size='42sp', color=(0, 0, 0, 0.85),
            size=self.size, halign='center', valign='middle',
        )
        self.glow = Label(
            text=f'[b]{text}[/b]', markup=True,
            font_size='42sp', color=(1, 0.85, 0.35, 0.35),
            size=self.size, halign='center', valign='middle',
        )
        self.highlight = Label(
            text=f'[b]{text}[/b]', markup=True,
            font_size='42sp', color=(1, 0.97, 0.75, 0.75),
            size=self.size, halign='center', valign='middle',
        )
        self.main = Label(
            text=f'[b]{text}[/b]', markup=True,
            font_size='42sp', color=(0.92, 0.78, 0.32, 1),
            size=self.size, halign='center', valign='middle',
        )
        for lbl in (self.shadow, self.glow, self.highlight, self.main):
            self.add_widget(lbl)

        self.bind(pos=self._layout, size=self._layout)
        self._layout()

        self._t = 0.0
        self._base_y = 0
        self._float_amp = dp(6)
        self._glow_min = 0.20
        self._glow_max = 0.55
        Clock.schedule_interval(self._animate, 1 / 60.0)

    def _layout(self, *args):
        for lbl in (self.shadow, self.glow, self.highlight, self.main):
            lbl.size = self.size
            lbl.text_size = self.size
        self._base_y = self.y
        self.shadow.pos = (self.x + dp(3), self.y - dp(5))
        self.glow.pos = (self.x, self.y)
        self.highlight.pos = (self.x - dp(1.5), self.y + dp(2))
        self.main.pos = (self.x, self.y + dp(1))

    def _animate(self, dt):
        self._t += dt
        offset = math.sin(self._t * 1.6) * self._float_amp
        self.y = self._base_y + offset
        k = (math.sin(self._t * 2.2) + 1) / 2
        alpha = self._glow_min + (self._glow_max - self._glow_min) * k
        self.glow.color = (1, 0.85, 0.35, alpha)
        self.highlight.color = (1, 0.97, 0.75, 0.55 + 0.25 * k)
        self.shadow.pos = (self.x + dp(3), self.y - dp(5))
        self.glow.pos = (self.x, self.y)
        self.highlight.pos = (self.x - dp(1.5), self.y + dp(2))
        self.main.pos = (self.x, self.y + dp(1))


class SlobodaOblock(App):
    def build(self):
        Window.clearcolor = (0.05, 0.05, 0.08, 1)
        root = FloatLayout()

        # ===== ФОН: ФОТО =====
        if os.path.exists(IMAGE_PATH):
            root.add_widget(Image(
                source=IMAGE_PATH,
                allow_stretch=True,
                keep_ratio=False,
                size_hint=(1, 1),
                pos_hint={'x': 0, 'y': 0},
            ))
        else:
            # Если фото не найдено — простой тёмный фон
            with root.canvas.before:
                Color(0.06, 0.06, 0.10, 1)
                fallback = Rectangle(pos=(0, 0), size=Window.size)
            Window.bind(size=lambda *a: setattr(fallback, 'size', Window.size))

        # Затемняющий оверлей поверх фото (для читаемости текста)
        with root.canvas.after:
            Color(0, 0, 0, 0.45)
            overlay = Rectangle(pos=(0, 0), size=Window.size)
        Window.bind(size=lambda *a: setattr(overlay, 'size', Window.size))

        # ===== ОБЪЁМНАЯ АНИМИРОВАННАЯ НАДПИСЬ =====
        title = VolumeTitle(
            text='SLOBODA OBLOK',
            pos_hint={'center_x': 0.5, 'top': 0.94},
        )
        root.add_widget(title)
        title.opacity = 0
        Animation(opacity=1, d=1.2).start(title)

        # ===== КНОПКИ =====
        buttons = [
            ('НОВАЯ ИГРА', 0.60),
            ('СОХРАНЕНИЯ', 0.48),
            ('ИСТОРИЯ ПЕРСОНАЖЕЙ', 0.36),
            ('ПОДДЕРЖАТЬ АВТОРА', 0.24),
        ]
        for text, y in buttons:
            b = ObemButton(
                text=text,
                size_hint=(0.7, 0.09),
                pos_hint={'center_x': 0.5, 'center_y': y},
            )
            b.bind(on_press=lambda inst, t=text: print(f'Нажато: {t}'))
            root.add_widget(b)

        return root


SlobodaOblock().run()