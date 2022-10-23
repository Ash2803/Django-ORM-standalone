import os

import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from datacenter.models import Passcard, Visit  # noqa: E402


def get_duration(visit):
    current_time = django.utils.timezone.localtime().replace(microsecond=0, second=0)
    entered_time = visit.entered_at.replace(tzinfo=timezone.utc).astimezone(tz=None)
    delta = str(current_time - entered_time)
    return delta[:-3]


def get_visitor_name(visitor):
    return visitor.passcard


non_closed_visits = []
visits = Visit.objects.all().filter(leaved_at=None)
for visit in visits:
    slovar = {
        'who_entered': get_visitor_name(visit),
        'entered_at': visit.entered_at,
        'duration': get_duration(visit),
    }
    non_closed_visits.append(slovar)


def is_visit_long(visit, minutes=60):
    suspicious_visits = []
    for suspicious_visit in visit:
        if suspicious_visit.leaved_at is None:
            continue
        entered_time = suspicious_visit.entered_at.replace(tzinfo=timezone.utc).astimezone(tz=None)
        leave_time = suspicious_visit.leaved_at.replace(tzinfo=timezone.utc).astimezone(tz=None)
        suspicious_time = (leave_time - entered_time).total_seconds() // 60
        if suspicious_time > minutes:
            suspicious_visits.append(suspicious_visit)
    return suspicious_visits


if __name__ == '__main__':
    visitors_name = Passcard.objects.all().filter(is_active=True)
    for i in visitors_name:
        person_visits = Visit.objects.filter(passcard=i)
        print(is_visit_long(person_visits))

