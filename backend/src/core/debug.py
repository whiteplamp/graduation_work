import logging
import traceback
from functools import wraps
from typing import Callable, Any
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def debug_error(func: Callable) -> Callable:
    """Декоратор для дебага ошибок в эндпоинтах"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            # Логируем входные параметры
            logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")

            result = await func(*args, **kwargs)

            # Логируем успешный результат
            logger.debug(f"{func.__name__} completed successfully")
            return result

        except Exception as e:
            # Получаем полный stack trace
            error_traceback = traceback.format_exc()

            # Логируем ошибку со всеми деталями
            logger.error(f"Error in {func.__name__}: {str(e)}")
            logger.error(f"Traceback:\n{error_traceback}")

            # Определяем request из аргументов
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break

            if request:
                logger.error(f"Request details: {request.method} {request.url}")
                logger.error(f"Headers: {dict(request.headers)}")

                # Для POST/PUT запросов логируем тело (осторожно с большими данными)
                if request.method in ["POST", "PUT", "PATCH"]:
                    try:
                        body = await request.body()
                        logger.error(f"Request body: {body[:500]}")  # Только первые 500 символов
                    except:
                        pass

            # Перевыбрасываем исключение
            raise

    return wrapper

# Использование:
# @app.post("/example")
# @debug_error
# async def example_endpoint():
#     pass