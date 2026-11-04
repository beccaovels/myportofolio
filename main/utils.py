import re

_DRIVE_FILE_ID = re.compile(r"/d/([a-zA-Z0-9_-]+)")


def normalize_drive_image_url(url):
    """Turn a Google Drive 'view' link into a direct thumbnail image link.

    Shared by SkillForm and SkillSerializer so the HTML form and the API
    store logo URLs the same way. Other URLs are returned unchanged.
    """
    if url and "drive.google.com/file/d/" in url:
        match = _DRIVE_FILE_ID.search(url)
        if match:
            return f"https://drive.google.com/thumbnail?id={match.group(1)}&sz=w1000"
    return url
