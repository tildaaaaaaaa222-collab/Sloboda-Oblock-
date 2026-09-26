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

# ====== ПУТИ К ФАЙЛАМ ======
IMAGE_PATH = 'bg.jpg'
MUSIC_PATH = 'music.mp3'
VLAD_PHOTO = 'vlad.png'
CLICK_PATH = 'click.mp3'

try:
    from kivy.core.audio import SoundLoader
    AUDIO_OK = True
except Exception as e:
    print('Аудио недоступно:', e)
    AUDIO_OK = False

CLICK_SOUND = None
if AUDIO_OK and os.path.exists(CLICK_PATH):
    try:
        CLICK_SOUND = SoundLoader.load(CLICK_PATH)
        if CLICK_SOUND:
            CLICK_SOUND.volume = 0.6
            print('Звук клика загружен:', CLICK_PATH)
        else:
            print('Звук клика: формат не поддерживается')
    except Exception as e:
        print('Ошибка загрузки звука клика:', e)
else:
    if AUDIO_OK:
        print('Звук клика не найден:', CLICK_PATH)


# ====== ДАННЫЕ О СЛОЖНОСТЯХ ======
DIFFICULTIES = [
    {
        'name': 'ЛЁГКИЙ',
        'desc': 'Люди ведут себя не агрессивно.',
        'chance': 'Шанс выжить: 80%',
        'color': (0.4, 0.9, 0.4, 1),
    },
    {
        'name': 'СРЕДНИЙ',
        'desc': 'Люди могут вести себя агрессивно, но всё равно безопасные.',
        'chance': 'Шанс выжить: 65%',
        'color': (0.95, 0.85, 0.3, 1),
    },
    {
        'name': 'ТЯЖЁЛЫЙ',
        'desc': 'Люди докапываются, часто встречаются пьяные. '
                'При них лучше не говорить ничего лишнего.',
        'chance': 'Шанс выжить: 50%',
        'color': (0.95, 0.55, 0.2, 1),
    },
    {
        'name': 'НЕВОЗМОЖНЫЙ',
        'desc': 'Люди докапываются за любой косой взгляд, '
                'могут избить толпой.',
        'chance': 'Шанс выжить: 30%',
        'color': (0.9, 0.25, 0.25, 1),
    },
]


class ObemButton(Button):
    """Кнопка с объёмом, прозрачным фоном, подсветкой и звуком клика."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)
        self.color = (0.95, 0.88, 0.6, 1)
        self.bold = True
        self.font_size = '18sp'
        self.bind(pos=self._redraw, size=self._redraw, state=self._redraw)
        self.bind(on_press=self._play_click)

    def _play_click(self, *args):
        if CLICK_SOUND:
            try:
                CLICK_SOUND.stop()
                CLICK_SOUND.play()
            except Exception as e:
                print('Ошибка воспроизведения клика:', e)

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
    """Белая надпись с обводкой и лёгким покачиванием."""
    def __init__(self, text='SLOBODA OBLOK', **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(420), dp(70))

        self.o_tl = Label(text=f'[b]{text}[/b]', markup=True, font_size='42sp',
                          color=(0, 0, 0, 1), size=self.size,
                          halign='center', valign='middle')
        self.o_tr = Label(text=f'[b]{text}[/b]', markup=True, font_size='42sp',
                          color=(0, 0, 0, 1), size=self.size,
                          halign='center', valign='middle')
        self.o_bl = Label(text=f'[b]{text}[/b]', markup=True, font_size='42sp',
                          color=(0, 0, 0, 1), size=self.size,
                          halign='center', valign='middle')
        self.o_br = Label(text=f'[b]{text}[/b]', markup=True, font_size='42sp',
                          color=(0, 0, 0, 1), size=self.size,
                          halign='center', valign='middle')

        self.glow = Label(text=f'[b]{text}[/b]', markup=True, font_size='42sp',
                          color=(1, 1, 1, 0.30), size=self.size,
                          halign='center', valign='middle')
        self.main = Label(text=f'[b]{text}[/b]', markup=True, font_size='42sp',
                          color=(1, 1, 1, 1), size=self.size,
                          halign='center', valign='middle')

        for lbl in (self.o_tl, self.o_tr, self.o_bl, self.o_br,
                    self.glow, self.main):
            self.add_widget(lbl)

        self.bind(pos=self._layout, size=self._layout)

        self._t = 0.0
        self._base_y = 0
        self._amp = dp(3)
        self._outline = dp(2)
        self._ready = False

        Clock.schedule_interval(self._animate, 1 / 60.0)

    def _place(self):
        d = self._outline
        self.o_tl.pos = (self.x - d, self.y + d)
        self.o_tr.pos = (self.x + d, self.y + d)
        self.o_bl.pos = (self.x - d, self.y - d)
        self.o_br.pos = (self.x + d, self.y - d)
        self.glow.pos = (self.x, self.y)
        self.main.pos = (self.x, self.y)

    def _layout(self, *args):
        for lbl in (self.o_tl, self.o_tr, self.o_bl, self.o_br,
                    self.glow, self.main):
            lbl.size = self.size
            lbl.text_size = self.size
        self._base_y = self.y
        self._place()
        self._ready = True

    def _animate(self, dt):
        if not self._ready:
            return
        self._t += dt
        offset = math.sin(self._t * 0.9) * self._amp
        self.y = self._base_y + offset
        k = (math.sin(self._t * 1.4) + 1) / 2
        self.glow.color = (1, 1, 1, 0.18 + 0.22 * k)
        self._place()


class CharacterCard(Widget):
    """Карточка персонажа."""
    def __init__(self, name='ВЛАД',
                 description='Это Влад, прикольный челик, '
                             'не ровный пацанчик, часто гуляет на чумака',
                 photo_path=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(460), dp(190))

        self._name = name
        self._description = description
        self._photo_path = photo_path

        self.name_lbl = Label(
            text=f'[b]{name}[/b]', markup=True,
            font_size='26sp', color=(1, 0.85, 0.35, 1),
            halign='left', valign='top',
            size_hint=(None, None),
        )
        self.add_widget(self.name_lbl)

        self.desc_lbl = Label(
            text=description,
            font_size='15sp', color=(0.92, 0.92, 0.95, 1),
            halign='left', valign='top',
            size_hint=(None, None),
        )
        self.add_widget(self.desc_lbl)

        self.photo_frame = Widget(size_hint=(None, None))
        self.add_widget(self.photo_frame)

        self.photo_img = None
        if photo_path and os.path.exists(photo_path):
            try:
                self.photo_img = Image(
                    source=photo_path,
                    allow_stretch=True,
                    keep_ratio=True,
                    size_hint=(None, None),
                )
                self.add_widget(self.photo_img)
            except Exception as e:
                print('Ошибка загрузки фото персонажа:', e)

        self._placeholder_lbl = Label(
            text='[i]фото[/i]', markup=True,
            font_size='13sp', color=(1, 1, 1, 0.35),
            halign='center', valign='middle',
            size_hint=(None, None),
        )
        if self.photo_img is None:
            self.add_widget(self._placeholder_lbl)

        self.bind(pos=self._layout_and_redraw, size=self._layout_and_redraw)

    def _layout(self, *args):
        pad = dp(14)
        x, y = self.pos
        w, h = self.size

        photo_size = dp(120)
        photo_x = x + w - photo_size - pad
        photo_y = y + h - photo_size - pad

        text_w = w - photo_size - pad * 3

        self.name_lbl.size = (text_w, dp(34))
        self.name_lbl.text_size = self.name_lbl.size
        self.name_lbl.pos = (x + pad, y + h - dp(40))

        self.desc_lbl.size = (text_w, h - dp(60))
        self.desc_lbl.text_size = self.desc_lbl.size
        self.desc_lbl.pos = (x + pad, y + dp(14))

        self.photo_frame.size = (photo_size, photo_size)
        self.photo_frame.pos = (photo_x, photo_y)

        if self.photo_img is not None:
            self.photo_img.size = (photo_size - dp(4), photo_size - dp(4))
            self.photo_img.pos = (photo_x + dp(2), photo_y + dp(2))
        else:
            self._placeholder_lbl.size = (photo_size, photo_size)
            self._placeholder_lbl.text_size = self._placeholder_lbl.size
            self._placeholder_lbl.pos = (photo_x, photo_y)

    def _redraw_frame(self):
        self.photo_frame.canvas.before.clear()
        self.photo_frame.canvas.after.clear()
        x, y = self.photo_frame.pos
        w, h = self.photo_frame.size
        r = dp(10)

        with self.photo_frame.canvas.before:
            Color(0, 0, 0, 0.55)
            RoundedRectangle(pos=(x, y), size=(w, h), radius=[r])

        with self.photo_frame.canvas.after:
            Color(0.85, 0.72, 0.35, 0.9)
            Line(rounded_rectangle=(x, y, w, h, r), width=1.4)

    def _layout_and_redraw(self, *args):
        self._layout(*args)
        self._redraw_frame() 

class DifficultySelector(Widget):
    """
    Селектор сложности со стрелками влево/вправо.
    Отображает название (с обводкой), описание и шанс выжить над кнопкой ВЫБРАТЬ.
    """
    def __init__(self, on_confirm=None, on_back=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(560), dp(500))

        self._index = 0
        self._on_confirm = on_confirm
        self._on_back = on_back

        # ===== Фон окна (тёмная рамка) =====
        self.bg_frame = Widget(size_hint=(None, None))
        self.add_widget(self.bg_frame)

        # ===== Заголовок =====
        self.title_lbl = Label(
            text='[b]ВЫБОР СЛОЖНОСТИ[/b]', markup=True,
            font_size='28sp', color=(1, 0.85, 0.35, 1),
            halign='center', valign='middle',
            size_hint=(None, None),
        )
        self.add_widget(self.title_lbl)

        # ===== Стрелка влево =====
        self.left_btn = ObemButton(text='<', font_size='28sp')
        self.left_btn.bind(on_press=self._prev)
        self.add_widget(self.left_btn)

        # ===== Стрелка вправо =====
        self.right_btn = ObemButton(text='>', font_size='28sp')
        self.right_btn.bind(on_press=self._next)
        self.add_widget(self.right_btn)

        # ===== Название сложности с обводкой =====
        self.n_tl = Label(markup=True, font_size='34sp', color=(0, 0, 0, 1),
                          halign='center', valign='middle', size_hint=(None, None))
        self.n_tr = Label(markup=True, font_size='34sp', color=(0, 0, 0, 1),
                          halign='center', valign='middle', size_hint=(None, None))
        self.n_bl = Label(markup=True, font_size='34sp', color=(0, 0, 0, 1),
                          halign='center', valign='middle', size_hint=(None, None))
        self.n_br = Label(markup=True, font_size='34sp', color=(0, 0, 0, 1),
                          halign='center', valign='middle', size_hint=(None, None))
        self.n_glow = Label(markup=True, font_size='34sp', color=(1, 1, 1, 0.3),
                            halign='center', valign='middle', size_hint=(None, None))
        self.name_lbl = Label(markup=True, font_size='34sp',
                              color=(0.4, 0.9, 0.4, 1),
                              halign='center', valign='middle', size_hint=(None, None))

        for lbl in (self.n_tl, self.n_tr, self.n_bl, self.n_br,
                    self.n_glow, self.name_lbl):
            self.add_widget(lbl)

        self._outline = dp(2)

        # ===== Описание =====
        self.desc_lbl = Label(
            text='', font_size='16sp',
            color=(0.92, 0.92, 0.95, 1),
            halign='center', valign='middle',
            size_hint=(None, None),
        )
        self.add_widget(self.desc_lbl)

        # ===== Шанс выжить =====
        self.chance_lbl = Label(
            text='', markup=True,
            font_size='20sp', color=(1, 0.85, 0.35, 1),
            halign='center', valign='middle',
            size_hint=(None, None),
        )
        self.add_widget(self.chance_lbl)

        # ===== Кнопка "ВЫБРАТЬ" =====
        self.confirm_btn = ObemButton(text='ВЫБРАТЬ')
        self.confirm_btn.bind(on_press=self._confirm)
        self.add_widget(self.confirm_btn)

        # ===== Кнопка "НАЗАД" =====
        self.back_btn = ObemButton(text='НАЗАД')
        self.back_btn.bind(on_press=self._back)
        self.add_widget(self.back_btn)

        # ===== Точки-индикаторы =====
        self._dots = []
        for _ in DIFFICULTIES:
            d = Widget(size_hint=(None, None))
            self.add_widget(d)
            self._dots.append(d)

        self.bind(pos=self._layout, size=self._layout)
        self._update()

    def _place_name_outline(self):
        d = self._outline
        bx, by = self.name_lbl.pos
        w, h = self.name_lbl.size
        self.n_tl.pos = (bx - d, by + d)
        self.n_tr.pos = (bx + d, by + d)
        self.n_bl.pos = (bx - d, by - d)
        self.n_br.pos = (bx + d, by - d)
        self.n_glow.pos = (bx, by)

    def _redraw_bg(self):
        self.bg_frame.canvas.before.clear()
        self.bg_frame.canvas.after.clear()
        x, y = self.pos
        w, h = self.size
        r = dp(14)

        with self.bg_frame.canvas.before:
            Color(0, 0, 0, 0.55)
            RoundedRectangle(pos=(x + dp(4), y - dp(6)),
                             size=(w, h), radius=[r])

        with self.bg_frame.canvas.before:
            Color(0.06, 0.06, 0.10, 0.97)
            RoundedRectangle(pos=(x, y), size=(w, h), radius=[r])

        with self.bg_frame.canvas.after:
            Color(0.85, 0.72, 0.35, 0.9)
            Line(rounded_rectangle=(x, y, w, h, r), width=1.4)

    def _layout(self, *args):
        x, y = self.pos
        w, h = self.size
        pad = dp(16)

        self.bg_frame.size = (w, h)
        self.bg_frame.pos = (x, y)
        self._redraw_bg()

        # Заголовок — верх
        self.title_lbl.size = (w, dp(40))
        self.title_lbl.text_size = self.title_lbl.size
        self.title_lbl.pos = (x, y + h - dp(50))

        # Стрелки по бокам
        arrow_w = dp(60)
        arrow_h = dp(60)
        name_h = dp(50)
        name_y = y + h - dp(130)
        self.left_btn.size = (arrow_w, arrow_h)
        self.left_btn.pos = (x + pad, name_y - dp(5))
        self.right_btn.size = (arrow_w, arrow_h)
        self.right_btn.pos = (x + w - arrow_w - pad, name_y - dp(5))

        # Название
        name_w = w - arrow_w * 2 - pad * 4
        name_x = x + arrow_w + pad * 2
        for lbl in (self.n_tl, self.n_tr, self.n_bl, self.n_br,
                    self.n_glow, self.name_lbl):
            lbl.size = (name_w, name_h)
            lbl.text_size = lbl.size
        self.name_lbl.pos = (name_x, name_y)
        self._place_name_outline()

        # Описание — под названием
        self.desc_lbl.size = (w - pad * 4, dp(70))
        self.desc_lbl.text_size = self.desc_lbl.size
        self.desc_lbl.pos = (x + pad * 2, y + h - dp(230))

        # Шанс выжить — под описанием
        self.chance_lbl.size = (w - pad * 4, dp(34))
        self.chance_lbl.text_size = self.chance_lbl.size
        self.chance_lbl.pos = (x + pad * 2, y + h - dp(305))

        # Точки-индикаторы — под шансом
        n = len(self._dots)
        dot_size = dp(12)
        total_w = n * dot_size * 2
        start_x = x + (w - total_w) / 2
        dot_y = y + h - dp(350)
        for i, d in enumerate(self._dots):
            d.size = (dot_size, dot_size)
            d.pos = (start_x + i * dot_size * 2, dot_y)

        # Кнопки — внизу
        btn_w = w - pad * 4
        btn_h = dp(50)
        self.confirm_btn.size = (btn_w, btn_h)
        self.confirm_btn.pos = (x + pad * 2, y + dp(80))
        self.back_btn.size = (btn_w, btn_h)
        self.back_btn.pos = (x + pad * 2, y + dp(18))

    def _redraw_dots(self):
        for i, d in enumerate(self._dots):
            d.canvas.before.clear()
            d.canvas.after.clear()
            x, y = d.pos
            s = d.size[0]
            active = (i == self._index)
            with d.canvas.before:
                Color(1, 0.85, 0.35, 1 if active else 0.3)
                RoundedRectangle(pos=(x, y), size=(s, s), radius=[s / 2])
            with d.canvas.after:
                if active:
                    Color(1, 1, 1, 0.4)
                    Line(rounded_rectangle=(x, y, s, s, s / 2), width=1)

    def _update(self):
        data = DIFFICULTIES[self._index]
        text = f"[b]{data['name']}[/b]"

        for lbl in (self.n_tl, self.n_tr, self.n_bl, self.n_br,
                    self.n_glow, self.name_lbl):
            lbl.text = text

        self.name_lbl.color = data['color']
        r, g, b, _ = data['color']
        self.n_glow.color = (r, g, b, 0.35)

        self.desc_lbl.text = data['desc']
        self.chance_lbl.text = f"[b]{data['chance']}[/b]"

        self._place_name_outline()
        self._redraw_dots()

    def _prev(self, *args):
        self._index = (self._index - 1) % len(DIFFICULTIES)
        self._update()

    def _next(self, *args):
        self._index = (self._index + 1) % len(DIFFICULTIES)
        self._update()

    def _confirm(self, *args):
        data = DIFFICULTIES[self._index]
        print(f"Выбрана сложность: {data['name']} — {data['chance']}")
        if self._on_confirm:
            self._on_confirm(data)

    def _back(self, *args):
        if self._on_back:
            self._on_back() 

class SlobodaOblock(App):
    music = None
    music_on = True
    volume = 0.5

    def start_music(self):
        if not AUDIO_OK:
            print('Аудио-модуль недоступен')
            return
        if not os.path.exists(MUSIC_PATH):
            print('Музыка не найдена:', MUSIC_PATH)
            return
        try:
            self.music = SoundLoader.load(MUSIC_PATH)
            if self.music:
                self.music.loop = True
                self.music.volume = self.volume
                self.music.play()
                print('Музыка играет:', MUSIC_PATH)
            else:
                print('SoundLoader вернул None (формат не поддерживается)')
        except Exception as e:
            print('Ошибка загрузки музыки:', e)
            self.music = None

    def toggle_music(self, *args):
        self.music_on = not self.music_on
        if self.music:
            try:
                if self.music_on:
                    self.music.play()
                else:
                    self.music.stop()
            except Exception as e:
                print('Ошибка переключения музыки:', e)
        if hasattr(self, 'music_btn') and self.music_btn:
            self.music_btn.text = 'МУЗЫКА: ВКЛ' if self.music_on else 'МУЗЫКА: ВЫКЛ'

    def on_start(self):
        self.start_music()

    def on_pause(self):
        try:
            if self.music:
                self.music.stop()
        except Exception:
            pass
        return True

    def on_resume(self):
        try:
            if self.music and self.music_on:
                self.music.play()
        except Exception:
            pass

    # ===== Настройки =====
    def open_settings(self, *args):
        if hasattr(self, 'settings_screen') and self.settings_screen:
            return

        screen = FloatLayout()
        with screen.canvas.before:
            Color(0, 0, 0, 0.88)
            bg = Rectangle(pos=(0, 0), size=Window.size)

        title = Label(
            text='[b]НАСТРОЙКИ[/b]', markup=True,
            font_size='32sp', color=(1, 0.85, 0.35, 1),
            size_hint=(1, None), height=dp(60),
            pos_hint={'center_x': 0.5, 'top': 0.92},
        )
        screen.add_widget(title)

        self.music_btn = ObemButton(
            text='МУЗЫКА: ВКЛ' if self.music_on else 'МУЗЫКА: ВЫКЛ',
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.55},
        )
        self.music_btn.bind(on_press=self.toggle_music)
        screen.add_widget(self.music_btn)

        back_btn = ObemButton(
            text='НАЗАД',
            size_hint=(0.6, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35},
        )
        back_btn.bind(on_press=self.close_settings)
        screen.add_widget(back_btn)

        self.settings_screen = screen
        self.root.add_widget(screen)

    def close_settings(self, *args):
        if hasattr(self, 'settings_screen') and self.settings_screen:
            if self.settings_screen.parent:
                self.settings_screen.parent.remove_widget(self.settings_screen)
            self.settings_screen = None
            self.music_btn = None

    # ===== История персонажей =====
    def open_characters(self, *args):
        if hasattr(self, 'characters_screen') and self.characters_screen:
            return

        screen = FloatLayout()
        with screen.canvas.before:
            Color(0, 0, 0, 0.9)
            bg = Rectangle(pos=(0, 0), size=Window.size)

        title = Label(
            text='[b]ИСТОРИЯ ПЕРСОНАЖЕЙ[/b]', markup=True,
            font_size='28sp', color=(1, 0.85, 0.35, 1),
            size_hint=(1, None), height=dp(50),
            pos_hint={'center_x': 0.5, 'top': 0.94},
        )
        screen.add_widget(title)

        vlad = CharacterCard(
            name='ВЛАД',
            description='Это Влад, прикольный челик, не ровный пацанчик, '
                        'часто гуляет на чумака',
            photo_path=VLAD_PHOTO,
            pos_hint={'center_x': 0.5, 'center_y': 0.55},
        )
        Clock.schedule_once(lambda dt: vlad._layout_and_redraw(), 0)
        screen.add_widget(vlad)

        back_btn = ObemButton(
            text='НАЗАД',
            size_hint=(0.5, 0.09),
            pos_hint={'center_x': 0.5, 'center_y': 0.15},
        )
        back_btn.bind(on_press=self.close_characters)
        screen.add_widget(back_btn)

        self.characters_screen = screen
        self.root.add_widget(screen)

    def close_characters(self, *args):
        if hasattr(self, 'characters_screen') and self.characters_screen:
            if self.characters_screen.parent:
                self.characters_screen.parent.remove_widget(self.characters_screen)
            self.characters_screen = None

    # ===== Новая игра / выбор сложности =====
    def open_new_game(self, *args):
        if hasattr(self, 'difficulty_screen') and self.difficulty_screen:
            return

        # Скрываем все элементы главного меню, чтобы не просвечивали
        self._menu_widgets = []
        for child in list(self.root.children):
            child.opacity = 0
            self._menu_widgets.append(child)

        screen = FloatLayout()
        with screen.canvas.before:
            Color(0, 0, 0, 0.92)
            bg = Rectangle(pos=(0, 0), size=Window.size)
        Window.bind(size=lambda *a: setattr(bg, 'size', Window.size))

        selector = DifficultySelector(
            on_confirm=self.on_difficulty_confirmed,
            on_back=self.close_new_game,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
        )
        screen.add_widget(selector)

        self.difficulty_screen = screen
        self.difficulty_selector = selector
        self.root.add_widget(screen)

    def close_new_game(self, *args):
        if hasattr(self, 'difficulty_screen') and self.difficulty_screen:
            if self.difficulty_screen.parent:
                self.difficulty_screen.parent.remove_widget(self.difficulty_screen)
            self.difficulty_screen = None
            self.difficulty_selector = None

        # Возвращаем видимость элементов главного меню
        if hasattr(self, '_menu_widgets'):
            for child in self._menu_widgets:
                child.opacity = 1
            self._menu_widgets = []

    def on_difficulty_confirmed(self, data):
        print(f"Старт игры на сложности: {data['name']} ({data['chance']})")
        # Здесь можно запустить саму игру с выбранной сложностью
        self.close_new_game()

    # ===== UI =====
    def build(self):
        Window.clearcolor = (0.05, 0.05, 0.08, 1)
        root = FloatLayout()

        if os.path.exists(IMAGE_PATH):
            try:
                root.add_widget(Image(
                    source=IMAGE_PATH,
                    allow_stretch=True,
                    keep_ratio=False,
                    size_hint=(1, 1),
                    pos_hint={'x': 0, 'y': 0},
                ))
            except Exception as e:
                print('Ошибка загрузки фото:', e)

        with root.canvas.after:
            Color(0, 0, 0, 0.45)
            overlay = Rectangle(pos=(0, 0), size=Window.size)
        Window.bind(size=lambda *a: setattr(overlay, 'size', Window.size))

        title = VolumeTitle(
            text='SLOBODA OBLOK',
            pos_hint={'center_x': 0.5, 'top': 0.94},
        )
        root.add_widget(title)
        title.opacity = 0
        Animation(opacity=1, d=1.2).start(title)

        # ===== Кнопки меню =====
        new_game_btn = ObemButton(
            text='НОВАЯ ИГРА',
            size_hint=(0.7, 0.09),
            pos_hint={'center_x': 0.5, 'center_y': 0.60},
        )
        new_game_btn.bind(on_press=self.open_new_game)
        root.add_widget(new_game_btn)

        saves_btn = ObemButton(
            text='СОХРАНЕНИЯ',
            size_hint=(0.7, 0.09),
            pos_hint={'center_x': 0.5, 'center_y': 0.48},
        )
        saves_btn.bind(on_press=lambda inst: print('Нажато: СОХРАНЕНИЯ'))
        root.add_widget(saves_btn)

        chars_btn = ObemButton(
            text='ИСТОРИЯ ПЕРСОНАЖЕЙ',
            size_hint=(0.7, 0.09),
            pos_hint={'center_x': 0.5, 'center_y': 0.36},
        )
        chars_btn.bind(on_press=self.open_characters)
        root.add_widget(chars_btn)

        support_btn = ObemButton(
            text='ПОДДЕРЖАТЬ АВТОРА',
            size_hint=(0.7, 0.09),
            pos_hint={'center_x': 0.5, 'center_y': 0.24},
        )
        support_btn.bind(on_press=lambda inst: print('Нажато: ПОДДЕРЖАТЬ АВТОРА'))
        root.add_widget(support_btn)

        settings_btn = ObemButton(
            text='НАСТРОЙКИ',
            size_hint=(0.45, 0.07),
            pos_hint={'center_x': 0.5, 'center_y': 0.11},
        )
        settings_btn.bind(on_press=self.open_settings)
        root.add_widget(settings_btn)

        return root


SlobodaOblock().run()
