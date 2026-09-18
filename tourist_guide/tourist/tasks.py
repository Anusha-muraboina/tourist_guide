from celery import shared_task

from user.models import NewsletterSubscription
from .utils.newsletter import send_newsletter


@shared_task
def send_new_tour_newsletter(
    tour_name,
    tour_url,
):

    subject = (
        f"🌍 New Tour Added – {tour_name}"
    )

    description = f"""
A new tour has just been added to GetOurGuide.in!

Explore:

{tour_name}

Discover new destinations, exciting experiences,
and plan your next journey with us.
"""

    html_content = f"""
    <!DOCTYPE html>

    <html>

    <head>
        <meta charset="UTF-8">
        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">
    </head>

    <body style="
        margin:0;
        padding:0;
        background:#f3f6fa;
        font-family:Arial,sans-serif;
    ">

        <div style="
            max-width:600px;
            margin:40px auto;
            background:white;
            border-radius:18px;
            overflow:hidden;
        ">

            <div style="
                background:#0f2747;
                padding:35px;
                text-align:center;
            ">

                <h1 style="
                    color:white;
                    margin:0;
                ">
                    GetOurGuide.in
                </h1>

                <p style="
                    color:#dbeafe;
                    margin-top:8px;
                ">
                    Discover • Explore • Experience
                </p>

            </div>

            <div style="
                padding:40px;
                text-align:center;
            ">

                <div style="
                    font-size:50px;
                ">
                    🌍
                </div>

                <h2 style="
                    color:#172b4d;
                ">
                    New Tour Added!
                </h2>

                <h3 style="
                    color:#168de2;
                ">
                    {tour_name}
                </h3>

                <p style="
                    color:#667085;
                    line-height:1.7;
                ">
                    A new tour has just been added
                    to GetOurGuide.in.
                    Discover exciting experiences
                    and plan your next journey.
                </p>

                <a
                    href="{tour_url}"
                    style="
                        display:inline-block;
                        padding:14px 30px;
                        background:#168de2;
                        color:white;
                        text-decoration:none;
                        border-radius:8px;
                        font-weight:bold;
                    "
                >
                    Explore This Tour
                </a>

            </div>

            <div style="
                padding:25px;
                background:#f8fafc;
                text-align:center;
            ">

                <p style="
                    font-size:12px;
                    color:#98a2b3;
                ">
                    You received this email because
                    you subscribed to GetOurGuide.in.
                </p>

            </div>

        </div>

    </body>

    </html>
    """

    return send_newsletter(
        subject=subject,
        html_content=html_content,
        text_content=description,
    )
    
    
    
    
    
    
    
@shared_task
def send_new_blog_newsletter(
    blog_title,
    blog_url,
):

    subject = (
        f"📝 New Travel Blog – {blog_title}"
    )

    text_content = f"""
New Travel Blog Published!

{blog_title}

We've published a new travel blog
on GetOurGuide.in.

Read the latest travel tips,
destination information and travel inspiration.

Visit:
{blog_url}
"""

    html_content = f"""
    <!DOCTYPE html>

    <html>

    <head>
        <meta charset="UTF-8">
        <meta name="viewport"
              content="width=device-width, initial-scale=1.0">
    </head>

    <body style="
        margin:0;
        padding:0;
        background:#f3f6fa;
        font-family:Arial,sans-serif;
    ">

        <div style="
            max-width:600px;
            margin:40px auto;
            background:white;
            border-radius:18px;
            overflow:hidden;
        ">

            <div style="
                background:#0f2747;
                padding:35px;
                text-align:center;
            ">

                <h1 style="
                    color:white;
                    margin:0;
                ">
                    GetOurGuide.in
                </h1>

                <p style="
                    color:#dbeafe;
                ">
                    Discover • Explore • Experience
                </p>

            </div>

            <div style="
                padding:40px;
                text-align:center;
            ">

                <div style="
                    font-size:50px;
                ">
                    📝
                </div>

                <h2 style="
                    color:#172b4d;
                ">
                    New Travel Blog!
                </h2>

                <h3 style="
                    color:#168de2;
                ">
                    {blog_title}
                </h3>

                <p style="
                    color:#667085;
                    line-height:1.7;
                ">
                    We've published a new travel blog
                    on GetOurGuide.in.
                    Read the latest travel tips,
                    destination information and
                    travel inspiration.
                </p>

                <a
                    href="{blog_url}"
                    style="
                        display:inline-block;
                        padding:14px 30px;
                        background:#168de2;
                        color:white;
                        text-decoration:none;
                        border-radius:8px;
                        font-weight:bold;
                    "
                >
                    Read Blog
                </a>

            </div>

            <div style="
                padding:25px;
                background:#f8fafc;
                text-align:center;
            ">

                <p style="
                    font-size:12px;
                    color:#98a2b3;
                ">
                    You received this email because
                    you subscribed to GetOurGuide.in.
                </p>

            </div>

        </div>

    </body>

    </html>
    """

    return send_newsletter(
        subject=subject,
        html_content=html_content,
        text_content=text_content,
    )