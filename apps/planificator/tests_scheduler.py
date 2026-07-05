from datetime import datetime

from django.test import SimpleTestCase

from .scheduler import CourseScheduler
from .services import choose_start_date, generate_schedule_from_upload


class CourseSchedulerConstraintTests(SimpleTestCase):
    def test_short_course_must_stay_in_same_work_week_and_month(self):
        scheduler = CourseScheduler(2026, [])
        self.assertFalse(scheduler.can_schedule_course(datetime(2026, 1, 30), 2))
        self.assertFalse(scheduler.can_schedule_course(datetime(2026, 3, 30), 3))

    def test_long_course_can_cross_week_boundary(self):
        self.assertTrue(CourseScheduler(2026, []).can_schedule_course(datetime(2026, 1, 28), 6))

    def test_holiday_blocks_short_and_long_courses(self):
        short = CourseScheduler(2026, ["06.01.2026"])
        long = CourseScheduler(2026, ["30.01.2026"])
        self.assertFalse(short.can_schedule_course(datetime(2026, 1, 5), 2))
        self.assertFalse(long.can_schedule_course(datetime(2026, 1, 28), 6))

    def test_format_date_range_skips_weekend(self):
        self.assertEqual(
            CourseScheduler(2026, []).format_date_range(datetime(2026, 1, 8), 3),
            "08-12.01.2026",
        )

    def test_available_dates_are_cached_by_month_and_duration(self):
        scheduler = CourseScheduler(2026, [])
        first = scheduler.get_available_start_days(1, 3)
        second = scheduler.get_available_start_days(1, 3)
        scheduler.get_available_start_days(1, 2)
        self.assertIs(first, second)
        self.assertEqual(scheduler.available_date_calculations, 2)


class ScheduleGenerationTests(SimpleTestCase):
    def test_every_course_receives_every_selected_month(self):
        content = (
            "Title,Durata Curs,Permalink\n"
            "Același titlu,2 zile,https://example.com/unu\n"
            "Același titlu,2 zile,https://example.com/doi\n"
        ).encode()
        result = generate_schedule_from_upload(
            file_bytes=content,
            file_extension=".csv",
            year=2026,
            months=[1, 2],
            randomness=5,
            holidays=[],
            random_seed=42,
        )
        self.assertEqual(len(result.schedule), 4)
        self.assertEqual({row["source_row"] for row in result.schedule}, {2, 3})
        self.assertEqual(result.calendar_calculations, 2)

    def test_long_course_uses_earliest_allowed_date(self):
        available = [datetime(2026, 1, 20), datetime(2026, 1, 5), datetime(2026, 1, 12)]
        selected = choose_start_date(
            available_dates=available,
            scheduled_dates=set(),
            randomness=10,
            duration=6,
        )
        self.assertEqual(selected, datetime(2026, 1, 5))
