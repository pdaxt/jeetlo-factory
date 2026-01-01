"""
Exceptions for JeetLo Factory.

These exceptions ensure the pipeline cannot proceed if validation fails.
"""


class JeetLoFactoryError(Exception):
    """Base exception for all JeetLo Factory errors."""
    pass


class ManifestError(JeetLoFactoryError):
    """Raised when manifest is missing, corrupted, or invalid."""
    pass


class ChainBrokenError(JeetLoFactoryError):
    """Raised when the cryptographic chain is broken.

    This means someone tried to bypass a step or modify files manually.
    """
    pass


class ValidationError(JeetLoFactoryError):
    """Raised when content validation fails.

    Examples: pronunciation errors, wrong text language, timing sync issues.
    """
    pass


class CINotPassedError(JeetLoFactoryError):
    """Raised when trying to post but CI has not passed.

    This is the KEY enforcement mechanism. The post() function checks
    GitHub CI status via API before allowing any post. This check
    CANNOT be bypassed because it queries GitHub's servers directly.
    """
    pass


class StepNotCompletedError(JeetLoFactoryError):
    """Raised when trying to run a step before its prerequisites."""
    pass


class ExternalServiceError(JeetLoFactoryError):
    """Raised when an external service (TTS, GitHub API) fails."""
    pass
