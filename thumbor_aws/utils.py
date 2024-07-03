from thumbor.utils import logger


def normalize_path(context, prefix: str, path: str) -> str:
    """Convert a URL received from Thumbor to a key in a S3 bucket."""
    # Thumbor calls load/store functions with a URL that is  URL-encoded and
    # that always starts with a slash. S3Client doesn't expect URL-encoding
    # and S3 keys don't usually start with a slash. Decode and remove slash.
    new_path = context.config.AWS_NORMALIZER(path)

    if prefix:
        # Avoid double slash if prefix ends with a slash.
        prefix = prefix.rstrip("/")
        new_path = f"{prefix}/{new_path}"

    logger.debug("[NORMALIZER] '%s' -> '%s'", path, new_path)

    return new_path
