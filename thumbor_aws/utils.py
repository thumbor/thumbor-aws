from urllib.parse import unquote


def normalize_path(prefix: str, path: str) -> str:
    """Convert a URL received from Thumbor to a key in a S3 bucket."""
    # Thumbor calls load/store functions with a URL that is  URL-encoded and
    # that always starts with a slash. S3Client doesn't expect URL-encoding
    # and S3 keys don't usually start with a slash. Decode and remove slash.
    path = unquote(path).lstrip("/")
    if prefix:
        # Avoid double slash if prefix ends with a slash.
        prefix = prefix.rstrip("/")
        return f"{prefix}/{path}"
    return path
