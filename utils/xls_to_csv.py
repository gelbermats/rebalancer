#!/usr/bin/env python3
import sys
import pandas as pd
import argparse
from pathlib import Path
from typing import Optional


def convert_xls_to_csv(
    input_file: str, 
    output_file: Optional[str] = None,
    sheet_name: str = 'Account_Statement_auto_EXC',
    encoding: str = 'utf-8-sig'
) -> str:
    """Конвертирует XLS файл в CSV формат."""
    
    input_path = Path(input_file)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Файл {input_file} не найден")
    
    if output_file is None:
        output_file = str(input_path.with_suffix('.csv'))
    
    try:
        print(f"Читаем XLS файл: {input_file}")
        df = pd.read_excel(input_file, sheet_name=sheet_name)
        
        print(f"Найдено {len(df)} строк и {len(df.columns)} колонок")
        
        print(f"Сохраняем в CSV файл: {output_file}")
        df.to_csv(output_file, index=False, encoding=encoding)
        
        print(f"✅ Конвертация завершена успешно!")
        print(f"   Входной файл: {input_file}")
        print(f"   Выходной файл: {output_file}")
        print(f"   Размер данных: {len(df)} строк x {len(df.columns)} колонок")
        
        return str(output_file)
        
    except Exception as e:
        raise ValueError(f"Ошибка при обработке файла {input_file}: {str(e)}")


def analyze_xls_structure(input_file: str, sheet_name: str = 'Account_Statement_auto_EXC'):
    """Анализирует структуру XLS файла и выводит информацию о данных."""
    
    try:
        print(f"\n=== АНАЛИЗ СТРУКТУРЫ ФАЙЛА {input_file} ===")
        
        df = pd.read_excel(input_file, sheet_name=sheet_name)
        
        print(f"Размер данных: {len(df)} строк x {len(df.columns)} колонок")
        print(f"Лист: {sheet_name}")
        
        print(f"\nЗаголовки колонок:")
        for i, col in enumerate(df.columns):
            print(f"  {i}: {col}")
        
        print(f"\nПервые 5 строк данных:")
        print(df.head().to_string())
        
        # Показываем только колонки с пустыми значениями
        print(f"\nИнформация о пустых значениях:")
        null_counts = df.isnull().sum()
        for col, count in null_counts.items():
            if count > 0:
                print(f"  {col}: {count} пустых значений")
        
        print(f"\nТипы данных:")
        for col, dtype in df.dtypes.items():
            print(f"  {col}: {dtype}")
            
    except Exception as e:
        print(f"❌ Ошибка при анализе файла: {str(e)}")


def main():
    """Основная функция для работы из командной строки."""
    
    parser = argparse.ArgumentParser(
        description="Конвертация XLS файлов брокерских отчетов в CSV формат",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python xls_to_csv.py statement_sign.xls
  python xls_to_csv.py statement_sign.xls output.csv
  python xls_to_csv.py statement_sign.xls --analyze
  python xls_to_csv.py statement_sign.xls --sheet "Other_Sheet"
        """
    )
    
    parser.add_argument(
        'input_file',
        help='Путь к входному XLS файлу'
    )
    
    parser.add_argument(
        'output_file',
        nargs='?',
        help='Путь к выходному CSV файлу (опционально)'
    )
    
    parser.add_argument(
        '--sheet',
        default='Account_Statement_auto_EXC',
        help='Имя листа для чтения (по умолчанию: Account_Statement_auto_EXC)'
    )
    
    parser.add_argument(
        '--encoding',
        default='utf-8-sig',
        help='Кодировка для CSV файла (по умолчанию: utf-8-sig)'
    )
    
    parser.add_argument(
        '--analyze',
        action='store_true',
        help='Анализировать структуру XLS файла без конвертации'
    )
    
    args = parser.parse_args()
    
    try:
        if args.analyze:
            # Только анализ структуры
            analyze_xls_structure(args.input_file, args.sheet)
        else:
            # Конвертация в CSV
            output_file = convert_xls_to_csv(
                args.input_file,
                args.output_file,
                args.sheet,
                args.encoding
            )
            
            # Также показываем краткий анализ
            print(f"\n=== КРАТКИЙ АНАЛИЗ КОНВЕРТИРОВАННЫХ ДАННЫХ ===")
            df = pd.read_csv(output_file, encoding=args.encoding)
            print(f"CSV файл содержит: {len(df)} строк x {len(df.columns)} колонок")
            
    except (FileNotFoundError, ValueError) as e:
        print(f"❌ Ошибка: {str(e)}")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n⚠️  Операция прервана пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()