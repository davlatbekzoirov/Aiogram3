import logging  # Импортируем модуль logging для логирования ошибок
import traceback  # Импортируем модуль traceback для получения трассировки стека
import requests  # Импортируем модуль requests для выполнения HTTP-запросов
import re  # Импортируем модуль re для работы с регулярными выражениями
import ast  # Импортируем модуль ast для работы с абстрактным синтаксическим деревом

# Класс для хранения ответов API Rextester
class Rex:
    def __init__(self, errors=None, result=None, stats=None, success=None):
        self.errors = errors
        self.result = result
        self.stats = stats
        self.success = success

# Класс, содержащий методы, связанные с интерпретацией и выполнением кода
class Interpreter(object):

    def detect_input(self, code_text: str):
        """
        Определяет, содержит ли код вызов функции input, и возвращает его позицию.
        """
        pattern = "input\s*\("  # Шаблон регулярного выражения для поиска вызовов функции input
        quote, double_quote, hashtag = "'", '"', '#'  # Переменные для кавычек и комментариев
        for line_number, line in enumerate(code_text.splitlines()):  # Перебираем каждую строку кода
            quote_open = False
            double_quote_open = False
            clean_line_string = ''
            for char in line:  # Перебираем каждый символ в строке
                if char == quote:
                    quote_open = not quote_open and not double_quote_open
                elif char == double_quote:
                    double_quote_open = not double_quote_open and not quote_open
                elif char == hashtag:
                    if not quote_open and not double_quote_open:
                        break
                else:
                    if not quote_open and not double_quote_open:
                        clean_line_string += char
            search_result = re.search(pattern, clean_line_string)  # Ищем вызовы функции input
            if search_result:
                return True, line_number + 1, search_result.start()
        return False, 0, 0

    def advanced_input_detection(self, code_string: str) -> bool:
        """
        Использует абстрактное синтаксическое дерево для обнаружения вызовов функции input в коде.
        """
        try:
            parsed_code = ast.parse(code_string)  # Преобразуем строку кода в абстрактное синтаксическое дерево
            for node in ast.walk(parsed_code):  # Перебираем каждый узел в AST
                if isinstance(node, ast.Call) and hasattr(node.func, 'id'):
                    if node.func.id == 'input':  # Проверяем вызовы функции input
                        return True
        except:
            pass
        return False

    def detect_code(self, text):
        """
        Определяет, представляет ли данный текст исполняемый код.
        """
        first_line = text.splitlines()[0]  # Извлекаем первую строку текста
        prefixes = [('#py2', 5), ('#py3', 24), ('#py', 24)]  # Общие префиксы для указания версии Python
        for prefix, language_code in prefixes:
            if first_line.startswith(prefix):  # Проверяем, начинается ли первая строка с распознанного префикса
                return True, language_code
        return False, -1

    def run(self, lang: int, code: str, input_data: str = "") -> Rex:
        """
        Выполняет данный код с использованием API Rextester и возвращает ответ.
        """
        try:
            url = "https://emkc.org/api/v2/piston/execute"  # Адрес API для выполнения кода
            payload = {"language": "python3", "files": [code], "stdin": input_data, "version": "3"}  # Полезная нагрузка для запроса
            request = requests.post(url, data=payload)  # Отправляем POST-запрос
            json_obj = request.json()  # Преобразуем JSON-ответ
            response = json_obj.get('run')  # Извлекаем ключ 'run' из ответа
            errors = response['stderr']  # Извлекаем ошибки из ответа
            result = response['output']  # Извлекаем вывод из ответа
            stats = ""  # В настоящее время не используется
            success = not errors  # Определяем успешность выполнения на основе наличия ошибок
            rex = Rex(errors, result, stats, success)  # Создаем экземпляр класса Rex с данными ответа
            return rex
        except:
            logging.error(traceback.format_exc())  # Логируем любые исключения, возникшие во время выполнения
            errors = "Некая ошибка..."  # Обобщенное сообщение об ошибке
            result = ""  # Пустой результат
            stats = ""  # В настоящее время не используется
            success = not errors  # Определяем успешность выполнения на основе наличия ошибок
            return Rex(result=result, errors=errors, stats=stats, success=success)

    def format_response(self, response) -> str:
        """
        Форматирует ответ от API Rextester в строку.
        """
        gt = (">", "&gt;")  # HTML-экранирование символа "больше"
        lt = ("<", "&lt;")  # HTML-экранирование символа "меньше"
        amp = ("&", "&amp;")  # HTML-экранирование символа "и"
        if response.errors:
            return "<b>Ошибка</b>\n<code>{errors}</code>".format(errors=response.errors.replace(amp[0], amp[1]).replace(gt[0], gt[1]).replace(lt[0], lt[1]))  # Форматирование сообщения об ошибке
        elif len(response.result) > 3000:
            return "Результат слишком велик, допустимый размер - {limit} символов".format(limit=3000)  # Обработка больших выводов
        return "<b>Результат</b>\n<code>{result}</code>".format(result=response.result.replace(amp[0], amp[1]).replace(gt[0], gt[1]).replace(lt[0], lt[1]))  # Форматирование сообщения с результатом
