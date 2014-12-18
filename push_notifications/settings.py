""" Get settings, dynamically if constance is available. """

from django.conf import settings

try:
    from constance import config

except ImportError:
    config = None

else:
    from speaklater import make_lazy_string

PUSH_NOTIFICATIONS_SETTINGS = getattr(settings,
                                      "PUSH_NOTIFICATIONS_SETTINGS",
                                      {})


def get_apns_host(debug=None):
    """ Get APNS host. """

    if debug is None:
        debug = config.APNS_DEBUG

    if debug:
        return 'gateway.sandbox.push.apple.com'
    else:
        return 'gateway.push.apple.com'


def get_apns_feedback_host(debug=False):
    """ Get APNS feedback host. """

    if debug is None:
        debug = config.APNS_DEBUG

    if debug:
        return 'feedback.sandbox.push.apple.com'
    else:
        return 'feedback.push.apple.com'


def get_apns_certificate():
    """ Get APNS certificate file, dynamically based on ``config.APNS_DEBUG``.

    Please define ``APNS_CERTIFICATE_DEBUG`` and ``APNS_CERTIFICATE_PRODUCTION``
    in constance configuration. You can optionnaly put ``{BASE_ROOT}`` in their
    constance values; it will be replaced dynamically by ``settings.BASE_ROOT``,
    which you can define to anything.
    """

    if config.APNS_DEBUG:
        return config.APNS_CERTIFICATE_DEBUG.format(
            BASE_ROOT=settings.BASE_ROOT)

    else:
        return config.APNS_CERTIFICATE_PRODUCTION.format(
            BASE_ROOT=settings.BASE_ROOT)


# GCM
PUSH_NOTIFICATIONS_SETTINGS.setdefault(
    "GCM_POST_URL", "https://android.googleapis.com/gcm/send")
PUSH_NOTIFICATIONS_SETTINGS.setdefault("GCM_MAX_RECIPIENTS", 1000)


# APNS
PUSH_NOTIFICATIONS_SETTINGS.setdefault("APNS_PORT", 2195)
PUSH_NOTIFICATIONS_SETTINGS.setdefault("APNS_FEEDBACK_PORT", 2196)
PUSH_NOTIFICATIONS_SETTINGS.setdefault("APNS_ERROR_TIMEOUT", None)
PUSH_NOTIFICATIONS_SETTINGS.setdefault("APNS_MAX_NOTIFICATION_SIZE", 2048)

if config is None:
    PUSH_NOTIFICATIONS_SETTINGS.setdefault(
        "APNS_HOST", get_apns_host(settings.DEBUG))
    PUSH_NOTIFICATIONS_SETTINGS.setdefault(
        "APNS_FEEDBACK_HOST", get_apns_feedback_host(settings.DEBUG))

else:
    PUSH_NOTIFICATIONS_SETTINGS.setdefault(
        "APNS_HOST", make_lazy_string(get_apns_host))
    PUSH_NOTIFICATIONS_SETTINGS.setdefault(
        "APNS_FEEDBACK_HOST", make_lazy_string(get_apns_feedback_host))
    PUSH_NOTIFICATIONS_SETTINGS.setdefault(
        "APNS_CERTIFICATE", make_lazy_string(get_apns_certificate))
