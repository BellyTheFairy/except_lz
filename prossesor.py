import os
import pandas as pd

class Processor:

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.expected_structure = {
            'Участники гражданского оборота': str,
            'Тип операции': str,
            'Сумма операции': float,
            'Вид расчета': str,
            'Место оплаты': str,
            'Терминал оплаты': str,
            'Дата оплаты': str,
            'Время оплаты': str,
            'Результат операции': str,
            'Cash-back': str,
            'Сумма cash-back': float,
        }

    def process(self):
        try:
            self._check_file_exists()
            df = self._read_file()
            self._check_empty(df)
            self._check_structure(df)
            print("Чтение датафрейма завершено успешно.")
            return df
        except FileNotFoundError as e:
            print(f"Возникла следующая ошибка: {e}")
        except pd.errors.EmptyDataError:
            print("Возникла следующая ошибка: Датафрейм пуст")
        except ValueError as e:
            print(f"Структура датафрейма НЕ соответствует ожидаемой:\n{e}")
        except Exception as e:
            print(f"Возникла непредвиденная ошибка: {e}")

    def _check_file_exists(self):
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(
                f"[Errno 2] No such file or directory: '{self.filepath}'"
            )

    def _read_file(self):
        return pd.read_csv(self.filepath, encoding='utf-8-sig')

    def _check_empty(self, df: pd.DataFrame):
        if df.empty:
            raise pd.errors.EmptyDataError

    def _check_structure(self, df: pd.DataFrame):
        self._check_columns(df)
        self._check_dtypes(df)

    def _check_columns(self, df: pd.DataFrame):
        expected = list(self.expected_structure)
        actual = list(df.columns)
        if expected != actual:
            raise ValueError(
                "  - Названия столбцов не совпадают.\n"
                f"    Ожидаемые: {expected}\n"
                f"    Фактические: {actual}"
            )

    def _check_dtypes(self, df: pd.DataFrame):
        allowed = {
            str: {'object'},
            float: {'float64', 'int64'},
        }
        errors = []
        for col, expected_type in self.expected_structure.items():
            actual_type = str(df[col].dtype)
            if actual_type not in allowed[expected_type]:
                errors.append(
                    f"  - В столбце '{col}' тип данных не соответствует ожидаемому.\n"
                    f"    Ожидается: {expected_type.__name__}, Фактически: {actual_type}"
                )
        if errors:
            raise ValueError("\n".join(errors))
