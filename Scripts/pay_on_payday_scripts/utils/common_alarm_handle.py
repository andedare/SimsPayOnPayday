"""
The Sims 4 Community Library is licensed under the Creative Commons Attribution 4.0 International public license (CC BY 4.0).
https://creativecommons.org/licenses/by/4.0/
https://creativecommons.org/licenses/by/4.0/legalcode

Copyright (c) COLONOLNUTTY
"""
from alarms import AlarmHandle
from date_and_time import DateAndTime, TimeSpan
from scheduling import Timeline
from sims4.commands import Command, CommandType, CheatOutput
from sims4communitylib.utils.common_time_utils import CommonTimeUtils
from typing import Any, Callable


class CommonAlarmHandle(AlarmHandle):
    """A custom alarm handle that keeps track of when it is slated to trigger for the first time."""
    def __init__(
        self,
        owner: Any,
        on_alarm_triggered_callback: Callable[['CommonAlarmHandle'], None],
        timeline: Timeline,
        when: DateAndTime,
        should_repeat: bool=False,
        time_until_repeat: TimeSpan=None,
        accurate_repeat: bool=True,
        persist_across_zone_loads: bool=False
    ):
        self.started_at_date_and_time = when
        super().__init__(
            owner,
            on_alarm_triggered_callback,
            timeline,
            when,
            repeating=should_repeat,
            repeat_interval=time_until_repeat,
            accurate_repeat=accurate_repeat,
            cross_zone=persist_across_zone_loads
        )


@Command('pop.print_current_time', command_type=CommandType.Live)
def _ss_print_current_time(_connection: int=None):
    output = CheatOutput(_connection)
    output('Current time')
    output('Hour {} Minute {}'.format(CommonTimeUtils.get_current_date_and_time().hour(), CommonTimeUtils.get_current_date_and_time().minute()))
    output('Abs Hour {} Abs Minute {}'.format(CommonTimeUtils.get_current_date_and_time().absolute_hours(), CommonTimeUtils.get_current_date_and_time().absolute_minutes()))
