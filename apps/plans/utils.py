from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import DailyPlan

def send_daily_plan_email(daily_plan):
    subject = f'Your Daily Plan for {daily_plan.date}'
    html_message = render_to_string('email/daily_plan.html', {
        'user': daily_plan.user,
        'date': daily_plan.date,
        'tasks': daily_plan.dailyplantask_set.all().order_by('start_time')
    })
    plain_message = strip_tags(html_message)
    from_email = 'your-email@example.com'
    to_email = daily_plan.user.email

    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)