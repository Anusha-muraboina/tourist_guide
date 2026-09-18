from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import Tour
from .utils.newsletter import send_newsletter

from blog.models import Blog


# ============================================================
# HELPER
# ============================================================

def get_site_url():
    """
    Get the website URL from Django settings.
    Never use localhost/127.0.0.1 in production emails.
    """
    return getattr(
        settings,
        "SITE_URL",
        "https://getourguide.in"
    ).rstrip("/")


# ============================================================
# NEW TOUR NEWSLETTER
# ============================================================

@receiver(post_save, sender=Tour)
def new_tour_created(sender, instance, created, **kwargs):

    # Send newsletter only when a NEW tour is created
    if not created:
        return

    # --------------------------------------------------------
    # Tour name
    # --------------------------------------------------------

    tour_name = (
        getattr(instance, "name", None)
        or getattr(instance, "title", None)
        or "New Tour"
    )

    # --------------------------------------------------------
    # Tour slug
    # --------------------------------------------------------

    slug = getattr(instance, "slug", None)

    # --------------------------------------------------------
    # Website URL
    # --------------------------------------------------------

    site_url = get_site_url()

    if slug:
        tour_url = f"{site_url}/tours/{slug}/"
    else:
        tour_url = f"{site_url}/tours/"

    # --------------------------------------------------------
    # Unsubscribe URL
    # --------------------------------------------------------

    unsubscribe_url = (
        f"{site_url}/api/newsletter/unsubscribe/"
    )

    # --------------------------------------------------------
    # Subject
    # --------------------------------------------------------

    subject = (
        f"New Tour Added to GetOurGuide - {tour_name}"
    )

    # --------------------------------------------------------
    # Plain text email
    # --------------------------------------------------------

    text_content = f"""
Hello,

A new tour has been added to GetOurGuide.in.

Tour:
{tour_name}

Explore the tour:
{tour_url}

You are receiving this email because you subscribed
to the GetOurGuide.in newsletter.

To unsubscribe:
{unsubscribe_url}
"""

    # --------------------------------------------------------
    # HTML email
    # --------------------------------------------------------

    html_content = f"""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{tour_name}</title>
</head>

<body style="
    margin:0;
    padding:0;
    background:#f4f7fb;
    font-family:Arial, Helvetica, sans-serif;
">

    <div style="
        max-width:600px;
        margin:30px auto;
        background:#ffffff;
        border-radius:12px;
        overflow:hidden;
        border:1px solid #e5e7eb;
    ">

        <!-- HEADER -->

        <div style="
            background:#071B3B;
            padding:28px;
            text-align:center;
            color:#ffffff;
        ">

            <h1 style="
                margin:0;
                font-size:26px;
                font-weight:700;
            ">
                GetOurGuide.in
            </h1>

            <p style="
                margin:8px 0 0;
                color:#67e8f9;
                font-size:14px;
            ">
                New Tour Available
            </p>

        </div>


        <!-- CONTENT -->

        <div style="
            padding:30px;
        ">

            <p style="
                margin:0 0 15px;
                color:#333333;
                font-size:15px;
            ">
                Hello,
            </p>

            <h2 style="
                margin:0 0 18px;
                color:#071B3B;
                font-size:23px;
            ">
                {tour_name}
            </h2>

            <p style="
                margin:0;
                color:#555555;
                line-height:1.7;
                font-size:15px;
            ">
                A new tour has been added to
                GetOurGuide.in.
                Explore the destination and start
                planning your next adventure.
            </p>


            <!-- BUTTON -->

            <div style="
                text-align:center;
                margin:30px 0;
            ">

                <a
                    href="{tour_url}"
                    target="_blank"
                    style="
                        display:inline-block;
                        background:#06b6d4;
                        color:#ffffff;
                        text-decoration:none;
                        padding:14px 28px;
                        border-radius:7px;
                        font-weight:bold;
                        font-size:15px;
                    "
                >
                    Explore This Tour
                </a>

            </div>


            <p style="
                margin:0;
                color:#777777;
                font-size:13px;
                line-height:1.6;
            ">
                You are receiving this email because you
                subscribed to the GetOurGuide.in newsletter.
            </p>

        </div>


        <!-- FOOTER -->

        <div style="
            background:#071B3B;
            color:#aaaaaa;
            text-align:center;
            padding:20px;
            font-size:12px;
        ">

            <p style="margin:0 0 10px;">
                GetOurGuide.in
            </p>

            <p style="margin:0;">
                © 2026 GetOurGuide.in
            </p>

            <p style="
                margin:12px 0 0;
            ">
                <a
                    href="{unsubscribe_url}"
                    target="_blank"
                    style="
                        color:#67e8f9;
                        text-decoration:underline;
                    "
                >
                    Unsubscribe
                </a>
            </p>

        </div>

    </div>

</body>
</html>
"""

    # --------------------------------------------------------
    # SEND NEWSLETTER
    # --------------------------------------------------------

    send_newsletter(
        subject=subject,
        html_content=html_content,
        text_content=text_content,
    )


# ============================================================
# NEW / PUBLISHED BLOG NEWSLETTER
# ============================================================

@receiver(post_save, sender=Blog)
def new_blog_created(sender, instance, created, **kwargs):

    # --------------------------------------------------------
    # IMPORTANT:
    #
    # We need to detect:
    #
    # 1. New blog created as published
    # 2. Existing draft changed to published
    #
    # --------------------------------------------------------

    current_status = getattr(instance, "status", None)

    # If the model has a status field, only published blogs
    # should send newsletters.

    if hasattr(instance, "status"):

        if current_status != "published":
            return

    # --------------------------------------------------------
    # Prevent duplicate emails when an already-published
    # blog is edited.
    #
    # For a newly created blog:
    # created = True
    #
    # For an existing blog:
    # created = False
    #
    # We need to know the previous status.
    # --------------------------------------------------------

    if not created:

        try:
            old_instance = Blog.objects.get(pk=instance.pk)
            old_status = getattr(old_instance, "status", None)
        except Blog.DoesNotExist:
            old_status = None

        # NOTE:
        # post_save already saved the new value, so this simple
        # lookup cannot reliably detect the old status.
        #
        # Therefore, if your admin publishes blogs by editing
        # status, use the Blog admin/view to call the newsletter
        # after publication, or implement pre_save status tracking.
        #
        # For now, don't send on normal edits.
        return

    # --------------------------------------------------------
    # Blog title
    # --------------------------------------------------------

    blog_title = (
        getattr(instance, "title", None)
        or getattr(instance, "name", None)
        or "New Travel Blog"
    )

    # --------------------------------------------------------
    # Slug
    # --------------------------------------------------------

    slug = getattr(instance, "slug", None)

    # --------------------------------------------------------
    # Website URL
    # --------------------------------------------------------

    site_url = get_site_url()

    if slug:
        blog_url = f"{site_url}/blogs/{slug}/"
    else:
        blog_url = f"{site_url}/blogs/"

    # --------------------------------------------------------
    # Unsubscribe URL
    # --------------------------------------------------------

    unsubscribe_url = (
        f"{site_url}/api/newsletter/unsubscribe/"
    )

    # --------------------------------------------------------
    # Subject
    # --------------------------------------------------------

    subject = (
        f"New Travel Blog from GetOurGuide - {blog_title}"
    )

    # --------------------------------------------------------
    # Plain text
    # --------------------------------------------------------

    text_content = f"""
Hello,

A new travel blog has been published on GetOurGuide.in.

{blog_title}

Read the blog:
{blog_url}

You are receiving this email because you subscribed
to the GetOurGuide.in newsletter.

To unsubscribe:
{unsubscribe_url}
"""

    # --------------------------------------------------------
    # HTML
    # --------------------------------------------------------

    html_content = f"""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{blog_title}</title>
</head>

<body style="
    margin:0;
    padding:0;
    background:#f4f7fb;
    font-family:Arial, Helvetica, sans-serif;
">

    <div style="
        max-width:600px;
        margin:30px auto;
        background:#ffffff;
        border-radius:12px;
        overflow:hidden;
        border:1px solid #e5e7eb;
    ">

        <!-- HEADER -->

        <div style="
            background:#071B3B;
            padding:28px;
            text-align:center;
            color:#ffffff;
        ">

            <h1 style="
                margin:0;
                font-size:26px;
                font-weight:700;
            ">
                GetOurGuide.in
            </h1>

            <p style="
                margin:8px 0 0;
                color:#67e8f9;
                font-size:14px;
            ">
                New Travel Blog
            </p>

        </div>


        <!-- CONTENT -->

        <div style="
            padding:30px;
        ">

            <p style="
                margin:0 0 15px;
                color:#333333;
                font-size:15px;
            ">
                Hello,
            </p>

            <h2 style="
                margin:0 0 18px;
                color:#071B3B;
                font-size:23px;
            ">
                {blog_title}
            </h2>

            <p style="
                margin:0;
                color:#555555;
                line-height:1.7;
                font-size:15px;
            ">
                A new travel article is now available
                on GetOurGuide.in.
            </p>


            <!-- BUTTON -->

            <div style="
                text-align:center;
                margin:30px 0;
            ">

                <a
                    href="{blog_url}"
                    target="_blank"
                    style="
                        display:inline-block;
                        background:#06b6d4;
                        color:#ffffff;
                        text-decoration:none;
                        padding:14px 28px;
                        border-radius:7px;
                        font-weight:bold;
                        font-size:15px;
                    "
                >
                    Read Full Blog
                </a>

            </div>


            <p style="
                margin:0;
                color:#777777;
                font-size:13px;
                line-height:1.6;
            ">
                You are receiving this email because you
                subscribed to the GetOurGuide.in newsletter.
            </p>

        </div>


        <!-- FOOTER -->

        <div style="
            background:#071B3B;
            color:#aaaaaa;
            text-align:center;
            padding:20px;
            font-size:12px;
        ">

            <p style="margin:0 0 10px;">
                GetOurGuide.in
            </p>

            <p style="margin:0;">
                © 2026 GetOurGuide.in
            </p>

            <p style="
                margin:12px 0 0;
            ">
                <a
                    href="{unsubscribe_url}"
                    target="_blank"
                    style="
                        color:#67e8f9;
                        text-decoration:underline;
                    "
                >
                    Unsubscribe
                </a>
            </p>

        </div>

    </div>

</body>
</html>
"""

    # --------------------------------------------------------
    # SEND
    # --------------------------------------------------------

    send_newsletter(
        subject=subject,
        html_content=html_content,
        text_content=text_content,
    )