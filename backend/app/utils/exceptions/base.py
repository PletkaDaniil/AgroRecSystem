class AppError(Exception):
    """
        Базовое исключение приложения — от него будем наследовать остальное
    """
    status_code = 500
    error_code = "internal_error"
    message = "Internal server error"

    def __init__(self, message: str | None = None, details: dict | None = None):
        self.message = message or self.message
        self.details = details or {}
        super().__init__(self.message)


class BadRequestError(AppError):
    status_code = 400
    error_code = "bad_request"
    message = "Bad request"


class UnauthorizedError(AppError):
    status_code = 401
    error_code = "unauthorized"
    message = "Authentication required"


class PaymentRequiredError(AppError):
    status_code = 402
    error_code = "payment_required"
    message = "Payment required"


class ForbiddenError(AppError):
    status_code = 403
    error_code = "forbidden"
    message = "Access denied"


class NotFoundError(AppError):
    status_code = 404
    error_code = "not_found"
    message = "Resource not found"


class ConflictError(AppError):
    status_code = 409
    error_code = "conflict"
    message = "Resource already exists"


class ValidationError(AppError):
    status_code = 422
    error_code = "validation_error"
    message = "Validation failed"


class InternalServerError(AppError):
    status_code = 500
    error_code = "internal_error"
    message = "Internal server error"


class ExternalServiceError(AppError):
    """
        Например, недоступен Sentinel
    """
    status_code = 502
    error_code = "external_service_error"
    message = "External service unavailable"


class ServiceUnavailableError(AppError):
    status_code = 503
    error_code = "service_unavailable"
    message = "Service temporarily unavailable"
