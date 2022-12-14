from enum import Enum, unique


@unique
class HttpStatusCode(Enum):

    """Http Status Code Enum.

    Example usage:
        HttpStatusCode.OK.value  # 100
        HttpStatusCode.INTERNAL_SERVER_ERROR.value  # 500
    """

    # INFORMATIONAL RESPONSES (100–199)
    CONTINUE = 100
    SWITCHING_PROTOCOL = 101
    PROCESSING = 102
    EARLY_HINTS = 103

    # SUCCESSFUL RESPONSES (200–299)
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NON_AUTHORITATIVE_INFORMATION = 203
    NO_CONTENT = 204
    RESET_CONTENT = 205
    PARTIAL_CONTENT = 206
    MULTI_STATUS = 207
    ALREADY_REPORTED = 208
    IM_USED = 226

    # REDIRECTS (300–399)
    MULTIPLE_CHOICE = 300
    MOVED_PERMANENTLY = 301
    FOUND = 302
    SEE_OTHER = 303
    NOT_MODIFIED = 304
    USE_PROXY = 305
    UNUSED = 306
    TEMPORARY_REDIRECT = 307
    PERMANENT_REDIRECT = 308

    # CLIENT ERRORS (400–499)
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    PAYMENT_REQUIRED = 402
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    NOT_ACCEPTABLE = 406
    PROXY_AUTHENTICATION_REQUIRED = 407
    REQUEST_TIMEOUT = 408
    CONFLICT = 409
    GONE = 410
    LENGTH_REQUIRED = 411
    PRECONDITION_FAILED = 412
    PAYLOAD_TOO_LARGE = 413
    URI_TOO_LONG = 414
    UNSUPPORTED_MEDIA_TYPE = 415
    REQUESTED_RANGE_NOT_SATISFIABLE = 416
    EXPECTATION_FAILED = 417
    IM_A_TEAPOT = 418
    MISDIRECTED_REQUEST = 421
    UNPROCESSABLE_ENTITY = 422
    LOCKED = 423
    FAILED_DEPENDENCY = 424
    TOO_EARLY = 425
    UPGRADE_REQUIRED = 426
    PRECONDITION_REQUIRED = 428
    TOO_MANY_REQUESTS = 429
    REQUEST_HEADER_FIELDS_TOO_LARGE = 431
    UNAVAILABLE_FOR_LEGAL_REASONS = 451

    # SERVER ERRORS (500–599)
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504
    HTTP_VERSION_NOT_SUPPORTED = 505
    VARIANT_ALSO_NEGOTIATES = 506
    INSUFFICIENT_STORAGE = 507
    LOOP_DETECTED = 508
    NOT_EXTENDED = 510
    NETWORK_AUTHENTICATION_REQUIRED = 511


@unique
class Responses(Enum):
    NO_QUERY = (
        "You must have a query value in order to perform a search",
        HttpStatusCode.NOT_ACCEPTABLE.value,
    )
    NO_TOKEN = (
        "You must have a token in order to perform continuation search",
        HttpStatusCode.NOT_ACCEPTABLE.value,
    )
    NO_CHANNEL_ID = (
        "You must have a valid channel ID",
        HttpStatusCode.NOT_ACCEPTABLE.value,
    )
    NO_VIDEO_ID = (
        "You must have a valid video ID",
        HttpStatusCode.NOT_ACCEPTABLE.value,
    )
    NO_CHANNEL_NAME = (
        "You must have a valid channel Name in order to get the ID of the Youtube Channel",
        HttpStatusCode.NOT_ACCEPTABLE.value,
    )

    NO_USER_NAME = (
        "You must have a valid username in order to get the ID of the Tiktok User",
        HttpStatusCode.NOT_ACCEPTABLE.value,
    )
    WRONG_LIMIT_VALUE = (
        "The value of limit must be a between 1 and 60",
        HttpStatusCode.NOT_ACCEPTABLE.value,
    )

    WRONG_COUNTRY_VALUE = (
        "Please provide a valid country ISO code",
        HttpStatusCode.NOT_ACCEPTABLE.value,
    )
