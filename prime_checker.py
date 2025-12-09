import sys
import math
import os
import json
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit,
    QFrame, QGridLayout, QSpacerItem, QSizePolicy, QScrollArea,
    QGroupBox, QRadioButton, QButtonGroup, QMessageBox
)
from PyQt6.QtCore import Qt, QTranslator, QLocale, QLibraryInfo, pyqtSignal, QThread
from PyQt6.QtGui import QFont, QPalette, QColor, QLinearGradient, QBrush, QIcon, QPainter

class PrimeWorker(QThread):
    finished = pyqtSignal(bool, list)
    error = pyqtSignal(str)

    def __init__(self, number):
        super().__init__()
        self.number = number

    def run(self):
        if self.number <= 1:
            self.finished.emit(False, [])
            return
        if self.number <= 3:
            self.finished.emit(True, [])
            return

        divisors = []
        sqrt_n = int(math.sqrt(self.number)) + 1

        if self.number % 2 == 0:
            divisors.append(2)
            if self.number // 2 != 2:
                divisors.append(self.number // 2)
        elif self.number % 3 == 0:
            divisors.append(3)
            if self.number // 3 != 3:
                divisors.append(self.number // 3)

        for i in range(5, sqrt_n, 6):
            if self.number % i == 0:
                divisors.append(i)
                if self.number // i != i:
                    divisors.append(self.number // i)
            if self.number % (i + 2) == 0:
                divisors.append(i + 2)
                if self.number // (i + 2) != i + 2:
                    divisors.append(self.number // (i + 2))

        is_prime = len(divisors) == 0
        divisors.sort()
        self.finished.emit(is_prime, divisors)


class HistoryManager:
    def __init__(self):
        self.history_file = "prime_history.json"
        self.history = self.load_history()

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_history(self):
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def add_entry(self, number, is_prime, divisors, lang):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "number": number,
            "is_prime": is_prime,
            "divisors": divisors,
            "language": lang
        }
        self.history.insert(0, entry)
        self.history = self.history[:100]
        self.save_history()

    def get_history(self):
        return self.history

    def clear_history(self):
        self.history = []
        self.save_history()


class PrimeCheckerApp(QMainWindow):
    language_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.translators = {}
        self.current_lang = 'en'
        self.dark_mode = False
        self.theme = 'system'
        self.history_manager = HistoryManager()
        self.worker = None
        self.init_ui()
        self.load_translations()
        self.apply_language('en')
        self.apply_theme()

    def init_ui(self):
        self.setWindowTitle("Prime Number Checker")
        self.setMinimumSize(950, 750)
        self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, True)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(18)

        # Header
        header = self.create_header()
        main_layout.addWidget(header)

        # Controls
        controls = self.create_controls()
        main_layout.addWidget(controls)

        # Input
        input_section = self.create_input_section()
        main_layout.addWidget(input_section)

        # Result
        self.result_area = self.create_result_section()
        main_layout.addWidget(self.result_area)

        # History Panel
        history_panel = self.create_history_panel()
        main_layout.addWidget(history_panel)

        # Footer
        footer = self.create_footer()
        main_layout.addWidget(footer)

        self.setStyleSheet(self.get_base_styles())

    def create_header(self):
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setMinimumHeight(110)
        frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 #667eea, stop:1 #764ba2);
                border-radius: 18px;
                margin: 5px;
            }
        """)
        layout = QHBoxLayout(frame)

        title = QLabel("Prime Number Analyzer")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("title_label")
        font = QFont("Segoe UI", 26, QFont.Weight.Bold)
        title.setFont(font)
        title.setStyleSheet("color: white;")

        subtitle = QLabel("Check if a number is prime or find its divisors")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setObjectName("subtitle_label")
        subtitle_font = QFont("Segoe UI", 11)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet("color: #f0f0f0;")

        vbox = QVBoxLayout()
        vbox.addWidget(title)
        vbox.addWidget(subtitle)
        vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(vbox)
        return frame

    def create_controls(self):
        group = QGroupBox()
        group.setMinimumHeight(85)
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 14px;
                margin: 8px;
                padding: 12px;
                background-color: #f8f9fa;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 12px;
                color: #2c3e50;
            }
        """)
        layout = QHBoxLayout(group)

        lang_label = QLabel("Language:")
        lang_label.setStyleSheet("color: #2c3e50; font-weight: bold;")
        self.lang_combo = QComboBox()
        self.lang_combo.addItems([
            "English", "فارسی", "中文", "Русский"
        ])
        self.lang_combo.setCurrentIndex(0)
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        self.lang_combo.setStyleSheet(self.get_combo_style())

        theme_label = QLabel("Theme:")
        theme_label.setStyleSheet("color: #2c3e50; font-weight: bold;")
        self.theme_combo = QComboBox()
        self.theme_combo.addItems([
            "System Default", "Light", "Dark", "Blue", "Red"
        ])
        self.theme_combo.currentIndexChanged.connect(self.change_theme)
        self.theme_combo.setStyleSheet(self.get_combo_style())

        layout.addWidget(lang_label)
        layout.addWidget(self.lang_combo)
        layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        layout.addWidget(theme_label)
        layout.addWidget(self.theme_combo)

        return group

    def create_input_section(self):
        group = QGroupBox()
        group.setMinimumHeight(160)
        group.setStyleSheet("""
            QGroupBox {
                border: 2px solid #bdc3c7;
                border-radius: 14px;
                margin: 8px;
                padding: 12px;
                background-color: #f8f9fa;
            }
        """)
        layout = QVBoxLayout(group)

        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter a positive integer...")
        self.input_field.setMinimumHeight(55)
        self.input_field.setFont(QFont("Segoe UI", 13))
        self.input_field.setStyleSheet(self.get_input_style())

        check_btn = QPushButton("Check Number")
        check_btn.setMinimumHeight(55)
        check_btn.setMinimumWidth(190)
        check_btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        check_btn.clicked.connect(self.check_prime)
        check_btn.setStyleSheet(self.get_button_style())

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(check_btn)

        layout.addLayout(input_layout)
        return group

    def create_result_section(self):
        group = QGroupBox()
        group.setMinimumHeight(320)
        group.setStyleSheet("""
            QGroupBox {
                border: 2px solid #bdc3c7;
                border-radius: 14px;
                margin: 8px;
                padding: 12px;
                background-color: #f8f9fa;
            }
        """)
        layout = QVBoxLayout(group)

        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.result_display.setFont(QFont("Consolas", 12))
        self.result_display.setPlaceholderText("Results will appear here...")
        self.result_display.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 12px;
            }
        """)

        layout.addWidget(self.result_display)
        return group

    def create_history_panel(self):
        group = QGroupBox("History")
        group.setMinimumHeight(180)
        group.setStyleSheet("""
            QGroupBox {
                border: 2px solid #bdc3c7;
                border-radius: 14px;
                margin: 8px;
                padding: 12px;
                background-color: #f8f9fa;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 12px;
                color: #2c3e50;
            }
        """)
        layout = QVBoxLayout(group)

        self.history_list = QTextEdit()
        self.history_list.setReadOnly(True)
        self.history_list.setMaximumHeight(120)
        self.history_list.setStyleSheet("""
            QTextEdit {
                background-color: #f1f3f4;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 8px;
                font-size: 11px;
            }
        """)
        self.update_history_display()

        clear_btn = QPushButton("Clear History")
        clear_btn.setStyleSheet(self.get_button_style("#e74c3c"))
        clear_btn.clicked.connect(self.clear_history)

        hbox = QHBoxLayout()
        hbox.addWidget(self.history_list)
        hbox.addWidget(clear_btn, alignment=Qt.AlignmentFlag.AlignTop)

        layout.addLayout(hbox)
        return group

    def create_footer(self):
        frame = QFrame()
        frame.setMinimumHeight(55)
        frame.setStyleSheet("""
            QFrame {
                background-color: #ecf0f1;
                border-top: 1px solid #bdc3c7;
                border-radius: 0 0 14px 14px;
            }
        """)
        layout = QHBoxLayout(frame)

        status = QLabel("Ready")
        status.setObjectName("status_label")
        status.setStyleSheet("color: #27ae60; font-weight: bold;")

        version = QLabel("v2.1.0")
        version.setObjectName("version_label")
        version.setStyleSheet("color: #7f8c8d;")

        layout.addWidget(status)
        layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        layout.addWidget(version)

        return frame

    def load_translations(self):
        self.translators = {
            'en': self.create_translator('en', 'English'),
            'fa': self.create_translator('fa', 'فارسی'),
            'zh': self.create_translator('zh', '中文'),
            'ru': self.create_translator('ru', 'Русский')
        }

    def create_translator(self, lang_code, native_name):
        translator = QTranslator()
        return translator

    def apply_language(self, lang):
        self.current_lang = lang
        texts = self.get_translations(lang)

        self.setWindowTitle(texts['window_title'])
        self.findChild(QLabel, "title_label").setText(texts['main_title'])
        self.findChild(QLabel, "subtitle_label").setText(texts['subtitle'])

        # Update controls labels
        all_labels = self.findChildren(QLabel)
        for label in all_labels:
            if label.text().startswith("Language") or label.text().startswith("زبان") or label.text().startswith("语言") or label.text().startswith("Язык"):
                label.setText(texts['language_label'])
            elif label.text().startswith("Theme") or label.text().startswith("تم") or label.text().startswith("主题") or label.text().startswith("Тема"):
                label.setText(texts['theme_label'])

        # Update buttons
        for btn in self.findChildren(QPushButton):
            current_text = btn.text()
            if any(x in current_text for x in ["Check", "بررسی", "检查", "Проверить"]):
                btn.setText(texts['check_button'])
            elif any(x in current_text for x in ["Clear", "پاک", "清除", "Очистить"]):
                btn.setText(texts['clear_history'])

        self.input_field.setPlaceholderText(texts['input_placeholder'])
        self.findChild(QLabel, "status_label").setText(texts['ready_status'])

        # RTL for Persian
        if lang == 'fa':
            self.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
            self.input_field.setAlignment(Qt.AlignmentFlag.AlignRight)
        else:
            self.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
            self.input_field.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.language_changed.emit(lang)
        self.update_history_display()

    def get_translations(self, lang):
        translations = {
            'en': {
                'window_title': 'Prime Number Checker',
                'main_title': 'Prime Number Analyzer',
                'subtitle': 'Check if a number is prime or find its divisors',
                'language_label': 'Language:',
                'theme_label': 'Theme:',
                'check_button': 'Check Number',
                'input_placeholder': 'Enter a positive integer...',
                'ready_status': 'Ready',
                'is_prime': 'is PRIME!',
                'not_prime': 'is NOT prime.',
                'divisors': 'Divisible by:',
                'error_invalid': 'Please enter a valid positive integer.',
                'error_large': 'Number is too large to process efficiently.',
                'processing': 'Processing...',
                'clear_history': 'Clear History'
            },
            'fa': {
                'window_title': 'بررسی اعداد اول',
                'main_title': 'تحلیلگر اعداد اول',
                'subtitle': 'بررسی کنید که آیا عدد اول است یا مقسوم‌علیه‌های آن را بیابید',
                'language_label': 'زبان:',
                'theme_label': 'تم:',
                'check_button': 'بررسی عدد',
                'input_placeholder': 'یک عدد صحیح مثبت وارد کنید...',
                'ready_status': 'آماده',
                'is_prime': 'عدد اول است!',
                'not_prime': 'عدد اول نیست.',
                'divisors': 'قابل تقسیم بر:',
                'error_invalid': 'لطفاً یک عدد صحیح مثبت معتبر وارد کنید.',
                'error_large': 'عدد خیلی بزرگ است و پردازش آن زمان‌بر است.',
                'processing': 'در حال پردازش...',
                'clear_history': 'پاک کردن تاریخچه'
            },
            'zh': {
                'window_title': '质数检查器',
                'main_title': '质数分析器',
                'subtitle': '检查一个数字是否为质数或找到它的除数',
                'language_label': '语言：',
                'theme_label': '主题：',
                'check_button': '检查数字',
                'input_placeholder': '输入一个正整数...',
                'ready_status': '就绪',
                'is_prime': '是质数！',
                'not_prime': '不是质数。',
                'divisors': '可被整除：',
                'error_invalid': '请输入有效的正整数。',
                'error_large': '数字太大，处理效率低下。',
                'processing': '处理中...',
                'clear_history': '清除历史'
            },
            'ru': {
                'window_title': 'Проверка простых чисел',
                'main_title': 'Анализатор простых чисел',
                'subtitle': 'Проверьте, является ли число простым или найдите его делители',
                'language_label': 'Язык:',
                'theme_label': 'Тема:',
                'check_button': 'Проверить число',
                'input_placeholder': 'Введите положительное целое число...',
                'ready_status': 'Готово',
                'is_prime': 'является ПРОСТЫМ!',
                'not_prime': 'НЕ является простым.',
                'divisors': 'Делится на:',
                'error_invalid': 'Пожалуйста, введите корректное положительное целое число.',
                'error_large': 'Число слишком велико для эффективной обработки.',
                'processing': 'Обработка...',
                'clear_history': 'Очистить историю'
            }
        }
        return translations.get(lang, translations['en'])

    def change_language(self, index):
        languages = ['en', 'fa', 'zh', 'ru']
        if index < len(languages):
            self.apply_language(languages[index])

    def change_theme(self, index):
        themes = ['system', 'light', 'dark', 'blue', 'red']
        if index < len(themes):
            self.theme = themes[index]
            self.apply_theme()

    def apply_theme(self):
        style = self.get_theme_style(self.theme)
        self.setStyleSheet(self.get_base_styles() + style)
        self.update()

    def get_base_styles(self):
        return """
        QMainWindow {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                        stop:0 #f0f2f5, stop:1 #e0e5ea);
        }
        QLabel#title_label { color: white; }
        QLabel#subtitle_label { color: #f0f0f0; }
        QLabel#status_label { color: #27ae60; font-weight: bold; }
        QLabel#version_label { color: #7f8c8d; }
        """

    def get_combo_style(self):
        return """
        QComboBox {
            background-color: white;
            border: 2px solid #ced4da;
            border-radius: 10px;
            padding: 8px 12px;
            font-size: 13px;
        }
        QComboBox::drop-down {
            border: none;
            width: 30px;
        }
        """

    def get_input_style(self):
        return """
        QLineEdit {
            background-color: white;
            border: 2px solid #ced4da;
            border-radius: 12px;
            padding: 12px 16px;
            font-size: 14px;
        }
        QLineEdit:focus {
            border-color: #4a90e2;
            background-color: white;
        }
        """

    def get_button_style(self, color="#3498db"):
        return f"""
        QPushButton {{
            background-color: {color};
            color: white;
            border: none;
            border-radius: 12px;
            padding: 12px;
            font-weight: bold;
            font-size: 13px;
        }}
        QPushButton:hover {{
            background-color: {self.darken_color(color)};
        }}
        QPushButton:pressed {{
            background-color: {self.darken_color(color, 0.8)};
        }}
        """

    def darken_color(self, color, factor=0.8):
        if color.startswith("#"):
            color = color[1:]
        r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
        return f"#{int(r*factor):02x}{int(g*factor):02x}{int(b*factor):02x}"

    def get_theme_style(self, theme):
        if theme == 'dark':
            return """
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #2b2b2b, stop:1 #1e1e1e);
                color: #ecf0f1;
            }
            QWidget { color: #ecf0f1; }
            QGroupBox {
                border: 2px solid #444;
                color: #ecf0f1;
                background-color: #2c2c2c;
            }
            QLineEdit, QTextEdit, QComboBox {
                background-color: #353535;
                border: 2px solid #555;
                color: #ecf0f1;
                border-radius: 8px;
                padding: 8px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
            }
            """
        elif theme == 'light':
            return """
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #f8f9fa, stop:1 #e9ecef);
            }
            QLineEdit, QTextEdit, QComboBox {
                background-color: white;
                border: 2px solid #ced4da;
                color: #212529;
            }
            """
        elif theme == 'blue':
            return """
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #1e3a8a, stop:1 #1e40af);
                color: #dbeafe;
            }
            QGroupBox { border: 2px solid #60a5fa; color: #dbeafe; background-color: #172554; }
            QLineEdit, QTextEdit, QComboBox {
                background-color: #1e3a8a;
                border: 2px solid #60a5fa;
                color: #dbeafe;
            }
            """
        elif theme == 'red':
            return """
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #7f1d1d, stop:1 #991b1b);
                color: #fee2e2;
            }
            QGroupBox { border: 2px solid #f87171; color: #fee2e2; background-color: #450a0a; }
            QLineEdit, QTextEdit, QComboBox {
                background-color: #7f1d1d;
                border: 2px solid #f87171;
                color: #fee2e2;
            }
            """
        else:
            palette = QApplication.palette()
            return f"""
            QMainWindow {{
                background-color: {palette.window().color().name()};
                color: {palette.windowText().color().name()};
            }}
            """

    def check_prime(self):
        text = self.input_field.text().strip()
        if not text.isdigit():
            self.show_error("error_invalid")
            return

        num = int(text)
        if num <= 0:
            self.show_error("error_invalid")
            return
        if num == 1:
            self.show_result(1, False, [])
            return
        if num > 10**12:
            self.show_error("error_large")
            return

        self.result_display.setText(self.tr("processing"))
        QApplication.processEvents()

        self.worker = PrimeWorker(num)
        self.worker.finished.connect(lambda is_prime, divisors: self.show_result(num, is_prime, divisors))
        self.worker.start()

    def show_result(self, num, is_prime, divisors):
        lang = self.current_lang
        texts = self.get_translations(lang)

        self.result_display.clear()
        self.result_display.setFont(QFont("Consolas", 12))

        if is_prime:
            html = f"""
            <h2 style='color:#27ae60; text-align:center; font-family: Segoe UI;'>
                {num} {texts['is_prime']}
            </h2>
            <p style='text-align:center; font-size:14px; color:#2c3e50;'>
                No divisors other than 1 and itself.
            </p>
            """
        else:
            div_list = ", ".join(map(str, divisors)) if divisors else "None"
            html = f"""
            <h2 style='color:#e74c3c; text-align:center; font-family: Segoe UI;'>
                {num} {texts['not_prime']}
            </h2>
            <p style='text-align:center; font-size:14px; color:#2c3e50;'>
                <strong>{texts['divisors']}</strong> {div_list}
            </p>
            """

        html += """
        <hr style='border: 1px dashed #95a5a6; margin: 25px 0;'>
        <p style='color:#7f8c8d; font-size:11px; text-align:center;'>
            Powered by advanced primality testing • Instant results
        </p>
        """

        self.result_display.setHtml(html)

        # Save to history
        self.history_manager.add_entry(num, is_prime, divisors, lang)
        self.update_history_display()

    def show_error(self, error_key):
        texts = self.get_translations(self.current_lang)
        self.result_display.setHtml(f"""
        <h3 style='color:#e74c3c; text-align:center; font-family: Segoe UI;'>
            Warning: {texts[error_key]}
        </h3>
        """)

    def tr(self, text):
        texts = self.get_translations(self.current_lang)
        return texts.get(text, text)

    def update_history_display(self):
        history = self.history_manager.get_history()
        if not history:
            self.history_list.setText("No history yet.")
            return

        lines = []
        for entry in history[:10]:
            num = entry["number"]
            is_prime = "PRIME" if entry["is_prime"] else "COMPOSITE"
            time = entry["timestamp"][11:19]
            lines.append(f"[{time}] {num} → {is_prime}")

        self.history_list.setText("\n".join(lines))

    def clear_history(self):
        self.history_manager.clear_history()
        self.update_history_display()
        QMessageBox.information(self, "History", "History cleared!")


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("PrimeChecker Pro")
    app.setApplicationVersion("2.1.0")
    app.setOrganizationName("MathTools")
    app.setStyle("Fusion")

    window = PrimeCheckerApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()