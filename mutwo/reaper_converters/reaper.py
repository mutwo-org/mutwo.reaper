import typing


from mutwo import core_converters
from mutwo import core_events
from mutwo import core_parameters
from mutwo import reaper_converters

__all__ = (
    "EventToReaperMarkerString",
    "SimpleEventToMarkerName",
    "SimpleEventToMarkerColor",
)


class SimpleEventToMarkerName(core_converters.SimpleEventToAttribute):
    """Convert :class:`~mutwo.core_events.SimpleEvent` to a name of a marker.

    By default `mutwo` will fetch from an event the
    :const:`~mutwo.reaper_converters.configurations.DEFAULT_MARKER_NAME_ATTRIBUTE_NAME`.
    If no attribute with `attribute_name` can be found the converter will simply return
    ``None``.
    """

    def __init__(
        self,
        attribute_name: typing.Optional[str] = None,
        exception_value=None,
    ):
        if attribute_name is None:
            attribute_name = (
                reaper_converters.configurations.DEFAULT_MARKER_NAME_ATTRIBUTE_NAME
            )
        super().__init__(attribute_name, exception_value)


class SimpleEventToMarkerColor(core_converters.SimpleEventToAttribute):
    """Convert :class:`~mutwo.core_events.SimpleEvent` to the color of a marker.

    By default `mutwo` will fetch from an event the
    :const:`~mutwo.reaper_converters.configurations.DEFAULT_MARKER_COLOR_ATTRIBUTE_NAME`.
    If no attribute with `attribute_name` can be found the converter will simply return
    ``None``.
    """

    def __init__(
        self,
        attribute_name: typing.Optional[str] = None,
        exception_value=None,
    ):
        if attribute_name is None:
            attribute_name = (
                reaper_converters.configurations.DEFAULT_MARKER_COLOR_ATTRIBUTE_NAME
            )
        super().__init__(attribute_name, exception_value)


class EventToReaperMarkerString(core_converters.abc.EventConverter):
    """Make Reaper Marker entries.

    :param simple_event_to_marker_name: A function which converts a
        :class:`~mutwo.core_events.SimpleEvent` to the marker
        name. If the function returns ``None`` `mutwo` will ignore`
        the current event. By default `simple_event_to_marker_name` is set
        to :class:`SimpleEventToMarkerName`.
    :type simple_event_to_marker_name: typing.Callable[[core_events.SimpleEvent], str]
    :param simple_event_to_marker_color: A function which converts a
        :class:`~mutwo.core_events.SimpleEvent` to the marker
        color. If the function returns ``None`` `mutwo` will ignore`
        the current event. By default `simple_event_to_marker_name` is set
        to :class:`SimpleEventToMarkerColor`.
    :type simple_event_to_marker_color: typing.Callable[[core_events.SimpleEvent], str]

    The resulting string can be copied into the respective reaper
    project file one line before the '<PROJBAY' tag.

    **Example:**

    >>> from mutwo import reaper_converters
    >>> from mutwo import core_events
    >>> marker_converter = reaper_converters.EventToReaperMarkerString()
    >>> events = core_events.SequentialEvent([core_events.SimpleEvent(2), core_events.SimpleEvent(3)])
    >>> events[0].name = 'beginning'
    >>> events[0].color = r'0 16797088 1 B {A4376701-5AA5-246B-900B-28ABC969123A}'
    >>> events[1].name = 'center'
    >>> events[1].color = r'0 18849803 1 B {E4DD7D23-98F4-CA97-8587-F4259A9498F7}'
    >>> marker_converter.convert(events)
    'MARKER 0 0 beginning 0 16797088 1 B {A4376701-5AA5-246B-900B-28ABC969123A}\nMARKER 1 2 center 0 18849803 1 B {E4DD7D23-98F4-CA97-8587-F4259A9498F7}'
    """

    def __init__(
        self,
        simple_event_to_marker_name: typing.Callable[
            [core_events.SimpleEvent], str
        ] = SimpleEventToMarkerName(),  # type: ignore
        simple_event_to_marker_color: typing.Callable[
            [core_events.SimpleEvent], str
        ] = SimpleEventToMarkerColor(),  # type: ignore
    ):
        self._simple_event_to_marker_name = simple_event_to_marker_name
        self._simple_event_to_marker_color = simple_event_to_marker_color

    def _convert_simple_event(
        self,
        simple_event: core_events.SimpleEvent,
        absolute_entry_delay: core_parameters.abc.Duration,
    ) -> tuple[str, ...]:
        marker_name = self._simple_event_to_marker_name(simple_event)
        marker_color = self._simple_event_to_marker_color(simple_event)

        # If any of the functions return ``None`` `mutwo` will ignore`
        # the current event.
        if marker_name is None or marker_color is None:
            return tuple([])

        return (
            "{} {} {}".format(
                absolute_entry_delay.duration_in_floats, marker_name, marker_color
            ),
        )

    def convert(self, event_to_convert: core_events.abc.Event) -> str:
        """Convert event to reaper markers (as plain string).

        :param event_to_convert: The event which shall be
            converted to reaper marker entries.
        :type event_to_convert: events.abc.Event
        :return: The reaper marker entries as plain strings.
            Copy them to your reaper project file one line
            before the '<PROJBAY' tag and the next time when
            you open the project they will appear.
        :return type: str
        """

        reaper_marker_tuple = tuple(
            "MARKER {} {}".format(marker_index, marker_data)
            for marker_index, marker_data in enumerate(
                self._convert_event(event_to_convert, core_parameters.DirectDuration(0))
            )
        )
        return "\n".join(reaper_marker_tuple)
