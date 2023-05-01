import asyncio
from datetime import date, timedelta
from typing import Any, Optional

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.properties import NumericProperty
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

from shared import MAX_REQUESTS_PER_HOUR, EARLIEST_DATE, TODAY
from uix.calendar_grid import Calendar
import client


class LoadDateRangeButton(Button):
    pass


class DateChangeButton(Button):
    def on_done(self, task):
        widget_from_id('body').state = task.result()

    def on_selection(self, selection: date):
        widget_from_id('body').state = LoadingState()
        asyncio.ensure_future(client.neo_from_date(selection)).add_done_callback(
            self.on_done)

    def on_press(self):
        Calendar(self.on_selection).open()


class DateButton(DateChangeButton):
    pass


class RemainingRequestsLabel(Label):
    remaining = NumericProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = 'remaining_requests'
        self.remaining = MAX_REQUESTS_PER_HOUR

    def on_remaining(self, _instance: Any, remaining: int):
        self.text = f'Remaining Requests: {str(remaining)}'


class LoadingSpinner(Widget):
    pass


class NeoRow(BoxLayout):
    def __init__(self, data: dict, **kwargs):
        kwargs['orientation'] = 'horizontal'
        super().__init__(**kwargs)

        self.title_column = BoxLayout(size_hint_x=0.2, orientation='vertical')
        self.title_column.add_widget(Label(text=data['name'], font_size=30.0))
        self.title_column.add_widget(Label(text='Hazardous', color=(1.0, 0.0, 0.0, 1.0)) if data[
            'is_potentially_hazardous_asteroid'] else Label(text='Not Hazardous',
                                                            color=(0.0, 1.0, 0.0, 1.0)))
        self.title_column.add_widget(
            Label(text=f'Orbiting Body: {data["close_approach_data"][0]["orbiting_body"]}'))
        self.add_widget(self.title_column)

        self.size_column = BoxLayout(size_hint_x=0.2, orientation='vertical')
        self.size_column.add_widget(Label(text='Size:'))
        self.size_column.add_widget(
            Label(text=f'Min: {round(data["estimated_diameter"]["miles"]["min"], 4)} mi'))
        self.size_column.add_widget(
            Label(text=f'Max: {round(data["estimated_diameter"]["miles"]["max"], 4)} mi'))
        self.add_widget(self.size_column)

        self.close_approach_column = BoxLayout(size_hint_x=0.2, orientation='vertical')
        self.close_approach_column.add_widget(Label(text='Close Approach:'))
        self.close_approach_column.add_widget(Label(text=data['close_approach_data'][0]['date']))
        self.close_approach_column.add_widget(Widget())
        self.add_widget(self.close_approach_column)

        self.velocity_column = BoxLayout(size_hint_x=0.2, orientation='vertical')
        self.velocity_column.add_widget(Label(text='Velocity:'))
        self.velocity_column.add_widget(
            Label(
                text=f'{round(float(data["close_approach_data"][0]["relative_velocity"]["miles_per_hour"]), 0)} mi/hr'))
        self.velocity_column.add_widget(Widget())
        self.add_widget(self.velocity_column)

        self.miss_distance_column = BoxLayout(size_hint_x=0.2, orientation='vertical')
        self.miss_distance_column.add_widget(Label(text='Miss Distance:'))
        self.miss_distance_column.add_widget(Label(
            text=f'{round(float(data["close_approach_data"][0]["miss_distance"]["miles"]), 0)} mi'))
        self.miss_distance_column.add_widget(Widget())
        self.add_widget(self.miss_distance_column)


class PreviousButton(DateChangeButton):
    def __init__(self, day: date, **kwargs):
        kwargs['background_disabled_normal'] = 'assets/disabled.png'
        super().__init__(**kwargs)
        self.day = day
        if self.day < EARLIEST_DATE:
            self.disabled = True

    def on_press(self):
        self.on_selection(self.day)


class NextButton(DateChangeButton):
    def __init__(self, day: date, **kwargs):
        kwargs['background_disabled_normal'] = 'assets/disabled.png'
        super().__init__(**kwargs)
        self.day = day
        if self.day > TODAY:
            self.disabled = True

    def on_press(self):
        self.on_selection(self.day)


class HeaderDateDisplay(DateChangeButton):
    def __init__(self, day: date, **kwargs):
        super().__init__(**kwargs)
        self.text = day.strftime('%Y-%m-%d')


class Content(BoxLayout):
    def __init__(self, data: client.NeoData, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        widget_from_id('remaining_requests').remaining = data.remaining_requests
        self.header = BoxLayout(size_hint_y=0.1, orientation='horizontal')
        self.header.add_widget(PreviousButton(data.day - timedelta(days=1), size_hint_x=0.1))
        self.header.add_widget(HeaderDateDisplay(data.day))
        self.header.add_widget(NextButton(day=data.day + timedelta(days=1), size_hint_x=0.1))
        self.add_widget(self.header)
        self.scroll_content = BoxLayout(orientation='vertical', size_hint_y=None)
        self.scroll_content.bind(minimum_height=self.scroll_content.setter('height'))
        self.scroll_view = ScrollView(size_hint_y=0.9)
        for neo in data.data:
            self.scroll_content.add_widget(NeoRow(data=neo['data'], size_hint_y=None, height=384.0))
        self.scroll_view.add_widget(self.scroll_content)
        self.add_widget(self.scroll_view)


class LoadingState:
    pass


class Body(BoxLayout):
    state = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = 'body'
        self.active_widget = Widget()
        self.add_widget(self.active_widget)

    def on_state(self, _instance: Any, state: Any):
        if isinstance(state, LoadingState):
            self.remove_widget(self.active_widget)
            self.active_widget = LoadingSpinner()
            self.add_widget(self.active_widget)
        elif isinstance(state, client.NeoData):
            self.remove_widget(self.active_widget)
            self.active_widget = Content(state)
            self.add_widget(self.active_widget)
        else:
            raise Exception('Invalid state for Body()')


class NeoBrowserApp(App):
    pass


def widget_from_id(ident: str) -> Optional[Widget]:
    stack = [browser.root]
    while stack:
        widget = stack.pop()
        if hasattr(widget, 'id') and widget.id == ident:
            return widget
        stack.extend(widget.children)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    browser = NeoBrowserApp()
    loop.run_until_complete(browser.async_run())
    loop.close()
