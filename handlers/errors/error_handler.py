import logging
from aiogram.exceptions import (
    TelegramMigrateToChat, UnsupportedKeywordArgument, AiogramError,
    CallbackAnswerException, ClientDecodeError, DetailedAiogramError, RestartingTelegram,
    SceneException, TelegramAPIError, TelegramBadRequest, TelegramConflictError, TelegramEntityTooLarge,
    TelegramForbiddenError, TelegramNetworkError, TelegramNotFound, TelegramRetryAfter, TelegramServerError, TelegramUnauthorizedError
)
from aiogram.types import Update
from loader import dp


@dp.errors()
async def errors_handler(update: Update, exception: Exception):
    """
    Обработчик исключений. Ловит все исключения внутри задач.
    :param update:
    :param exception:
    :return: логгирование в stdout
    """
    if isinstance(exception, TelegramMigrateToChat):
        logging.exception("Exception raised when chat has been migrated to a supergroup.")
        return True

    if isinstance(exception, TelegramUnauthorizedError):
        logging.exception("Exception raised when bot token is invalid.")
        return True
    
    if isinstance(exception, UnsupportedKeywordArgument):
        logging.exception('Exception raised when a keyword argument is passed as filter.')
        return True

    if isinstance(exception, AiogramError):
        logging.exception('Base exception for all aiogram errors.')
        return True

    if isinstance(exception, CallbackAnswerException):
        logging.exception('Exception for callback answer.')
        return True

    if isinstance(exception, ClientDecodeError):
        logging.exception('Exception raised when client can’t decode response. (Malformed response, etc.)')
        return True

    if isinstance(exception, DetailedAiogramError):
        logging.exception('Base exception for all aiogram errors with detailed message.')
        return True

    if isinstance(exception, TelegramAPIError):
        logging.exception('Base exception for all Telegram API errors.')
        return True

    if isinstance(exception, RestartingTelegram):
        logging.exception("""Exception raised when Telegram server is restarting.

It seems like this error is not used by Telegram anymore, but it’s still here for backward compatibility.

Currently, you should expect that Telegram can raise RetryAfter (with timeout 5 seconds)
error instead of this one.

""")
        return True

    if isinstance(exception, SceneException):
        logging.exception('Exception for scenes.')
        return True
    
    if isinstance(exception, TelegramBadRequest):
        logging.exception("Exception raised when request is malformed.")
        return True

    if isinstance(exception, TelegramConflictError):
        logging.exception('Exception raised when bot token is already used by another application in polling mode.')
        return True

    if isinstance(exception, TelegramEntityTooLarge):
        logging.exception('Exception raised when you are trying to send a file that is too large.')
        return True

    if isinstance(exception, TelegramForbiddenError):
        logging.exception('Exception raised when bot is kicked from chat or etc.')
        return True

    if isinstance(exception, TelegramNetworkError):
        logging.exception('Base exception for all Telegram network errors.')
        return True
    
    if isinstance(exception, TelegramNotFound):
        logging.exception("Exception raised when chat, message, user, etc. not found.")
        return True

    if isinstance(exception, TelegramRetryAfter):
        logging.exception('Exception raised when flood control exceeds.')
        return True

    if isinstance(exception, TelegramServerError):
        logging.exception('Exception raised when Telegram server returns 5xx error.')
        return True
    
    logging.exception(f'Update: {update} \n{exception}')
