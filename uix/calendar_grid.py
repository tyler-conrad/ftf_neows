from typing import Callable, Any
from datetime import date
import calendar

from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from shared import EARLIEST_DATE, TODAY


class DayButton(Button):
    def __init__(self, year: int, month: int, day: int, on_selection: Callable[[date], None],
                 **kwargs):
        super().__init__(**kwargs)
        self.year = year
        self.month = month
        self.day = day
        self.on_selection = on_selection
        self.text = str(day)

    def on_press(self):
        self.on_selection(date(self.year, self.month, self.day))
        self.parent.parent.parent.parent.dismiss()


class YearMonthTitleButton(Button):
    def __init__(self, year: int, month: int, **kwargs):
        super().__init__(**kwargs)
        self.text = f'{months[month]} - {year}'

    def on_press(self):
        self.parent.parent.parent.mode = 'month'


class DayGrid(Widget):
    def __init__(self, start: date, end: date, year: int, month: int,
                 on_selection: Callable[[date], None], **kwargs):
        super().__init__(**kwargs)
        days_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                        'Saturday']
        labels = [Label(text=dow) for dow in days_of_week]
        horz_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        for label in labels:
            horz_layout.add_widget(label)
        self.vert_layout = BoxLayout(orientation='vertical')
        self.vert_layout.add_widget(YearMonthTitleButton(year, month, size_hint_y=0.1))
        self.vert_layout.add_widget(horz_layout)
        grid_layout = GridLayout(cols=7, size_hint_y=0.8)
        days = [DayButton(year, dt.month, dt.day, on_selection) for dt in
                calendar.Calendar(firstweekday=6).itermonthdates(year, month)]
        for day in days:
            if day.month != month or not (start <= date(day.year, day.month, day.day) <= end):
                day.disabled = True
            grid_layout.add_widget(day)
        self.vert_layout.add_widget(grid_layout)
        self.add_widget(self.vert_layout)

    def on_size(self, _instance: Any, size):
        self.vert_layout.size = size

    def on_pos(self, _instance, pos):
        self.vert_layout.pos = pos


months = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May',
          6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October',
          11: 'November', 12: 'December', }


class MonthButton(Button):
    def __init__(self, month: int, **kwargs):
        super().__init__(**kwargs)
        self.month = month
        self.text = months[self.month]

    def on_press(self):
        modal = self.parent.parent.parent.parent
        modal.month = self.month
        modal.mode = 'day'


class YearTitleButton(Button):
    def __init__(self, year: int, **kwargs):
        super().__init__(**kwargs)
        self.text = str(year)

    def on_press(self):
        self.parent.parent.parent.mode = 'year'


class MonthGrid(Widget):
    def __init__(self, year: int, start: date, end: date, **kwargs):
        super().__init__(**kwargs)
        month_range = range(1, 13)
        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(YearTitleButton(year, size_hint_y=0.1))
        buttons = [MonthButton(month) for month in month_range]
        grid = GridLayout(cols=4, size_hint_y=0.9)
        for button in buttons:
            if start.year == year and start.month > button.month or end.year == year and end.month < button.month:
                button.disabled = True
            grid.add_widget(button)
        self.layout.add_widget(grid)
        self.add_widget(self.layout)

    def on_size(self, _instance: Any, size: list[float]):
        self.layout.size = size

    def on_pos(self, _instance: Any, pos: list[float]):
        self.layout.pos = pos


class YearButton(Button):
    def __init__(self, year: int, **kwargs):
        super().__init__(**kwargs)
        self.year = year
        self.text = str(year)

    def on_press(self):
        modal = self.parent.parent
        modal.year = self.year
        modal.mode = 'month'


class Calendar(ModalView):
    mode = StringProperty(None)

    def __init__(self, on_selection: Callable[[date], None], **kwargs):
        super().__init__(**kwargs)
        self.id = 'calendar'
        self.year = None
        self.on_selection = on_selection
        self.start = EARLIEST_DATE
        self.end = TODAY
        self.active_child = Widget()
        self.mode = 'year'

    def on_mode(self, _instance, mode: str):
        if mode == 'year':
            self.remove_widget(self.active_child)
            year_grid = GridLayout(cols=6)
            for year in range(self.start.year, self.end.year + 1):
                year_grid.add_widget(YearButton(year))
            self.active_child = year_grid
            self.add_widget(self.active_child)
        elif mode == 'month':
            self.remove_widget(self.active_child)
            self.active_child = MonthGrid(year=self.year, start=self.start, end=self.end)
            self.add_widget(self.active_child)
        elif mode == 'day':
            self.remove_widget(self.active_child)
            self.active_child = DayGrid(self.start, self.end, self.year, self.month,
                                        self.on_selection)
            self.add_widget(self.active_child)


class CalendarButton(Button):
    pass
