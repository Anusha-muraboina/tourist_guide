from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from user.models import NewsletterSubscription


def get_active_subscribers():

    return list(
        NewsletterSubscription.objects
        .filter(is_active=True)
        .values_list("email", flat=True)
    )


def send_newsletter(
    subject,
    html_content,
    text_content,
):

    subscribers = get_active_subscribers()

    print("========================================")
    print("NEWSLETTER SENDING")
    print("========================================")

    print(
        "FROM EMAIL:",
        settings.DEFAULT_FROM_EMAIL
    )

    print(
        "SMTP HOST:",
        settings.EMAIL_HOST
    )

    print(
        "SMTP PORT:",
        settings.EMAIL_PORT
    )

    print(
        "ACTIVE SUBSCRIBERS:",
        len(subscribers)
    )

    if not subscribers:

        print("No active subscribers found.")

        print("========================================")

        return 0

    sent_count = 0
    failed_count = 0

    site_url = getattr(
        settings,
        "SITE_URL",
        "https://getourguide.in"
    ).rstrip("/")

    unsubscribe_url = (
        f"{site_url}/api/newsletter/unsubscribe/"
    )

    for subscriber_email in subscribers:

        try:

            email = EmailMultiAlternatives(
                subject=subject,

                body=text_content,

                from_email=settings.DEFAULT_FROM_EMAIL,

                to=[subscriber_email],

                reply_to=[
                    settings.EMAIL_HOST_USER
                ],

                headers={
                    "X-Mailer": "GetOurGuide Newsletter",

                    "List-Unsubscribe":
                        f"<{unsubscribe_url}?email={subscriber_email}>",

                    "List-Unsubscribe-Post":
                        "List-Unsubscribe=One-Click",
                },
            )
            
            email.attach_alternative(
                html_content,
                "text/html"
            )

            result = email.send(
                fail_silently=False
            )

            print(
                f"SMTP RESULT for {subscriber_email}:",
                result
            )

            if result == 1:

                sent_count += 1

                print(
                    f"SUCCESS: {subscriber_email}"
                )

            else:

                failed_count += 1

                print(
                    f"FAILED: {subscriber_email}"
                )

        except Exception as error:

            failed_count += 1

            print(
                f"EMAIL FAILED: {subscriber_email}"
            )

            print(
                "ERROR TYPE:",
                type(error).__name__
            )

            print(
                "ERROR:",
                error
            )

    print("========================================")
    print("NEWSLETTER RESULT")
    print(
        "Successfully sent:",
        sent_count
    )
    print(
        "Failed:",
        failed_count
    )
    print("========================================")

    return sent_count

