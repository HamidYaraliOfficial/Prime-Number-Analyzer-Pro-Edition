# Prime Number Analyzer – Pro Edition

## English

### Overview
**Prime Number Analyzer – Pro Edition** is a powerful, modern desktop application for testing **primality** and finding **divisors** of large numbers. Built with **Python** and **PyQt6**, it features **multi-threaded computation**, **real-time feedback**, **persistent history**, **multilingual support**, and **dynamic theming** — delivering a professional-grade experience for students, educators, and math enthusiasts.

### Key Features
- **Fast Primality Testing**: Efficient algorithm checks numbers up to **10¹²**.
- **Divisor Listing**: Instantly shows all divisors if not prime.
- **Multi-Threaded Processing**: Non-blocking UI with `QThread`.
- **Persistent History**: Saves last 100 checks in `prime_history.json`.
- **Multilingual Interface**: Full support for **English**, **فارسی (RTL)**, **中文**, and **Русский**.
- **5 Professional Themes**:
  - System Default
  - Light
  - Dark
  - Blue
  - Red
- **RTL Layout Support**: Automatic right-to-left for Persian.
- **Modern UI Design**:
  - Gradient headers
  - Rounded corners
  - Smooth animations
  - Professional typography

### Requirements
- Python 3.8+
- PyQt6

### Installation
1. Ensure Python is installed.
2. Install dependency:
   ```bash
   pip install PyQt6
   ```
3. Run the app:
   ```bash
   python prime_checker.py
   ```

### Usage
- **Enter Number**: Type any positive integer.
- **Click Check**: Get instant prime status and divisors.
- **View History**: See last 10 checks with timestamps.
- **Clear History**: Reset saved records.
- **Change Language/Theme**: Use dropdowns in controls panel.

### Screenshots
- Gradient header with bold title and subtitle  
- Clean input section with large button  
- Rich HTML result display with color-coded output  
- Persian RTL interface with full translation  
- Dark theme with high-contrast text and borders  
- History panel showing time-stamped entries  

### Technical Highlights
- **Optimized Prime Check**: Wheel factorization (6k±1) for speed.
- **QThread Worker**: Prevents UI freezing on large numbers.
- **JSON History**: Persistent, human-readable storage.
- **Dynamic Translations**: Real-time UI updates.
- **Cross-Platform**: Works on Windows, macOS, and Linux.

### Contributing
Fork and improve: add factorization tree, export to CSV, prime density graph, or Miller-Rabin test. Pull requests welcome!

### License
MIT License – Free for personal, educational, and commercial use.

---

## فارسی

### بررسی اجمالی
**تحلیلگر اعداد اول – نسخه حرفه‌ای** یک برنامه دسکتاپ قدرتمند و مدرن برای آزمایش **اول بودن** و یافتن **مقسوم‌علیه‌ها** اعداد بزرگ است. با **پایتون** و **PyQt6** ساخته شده و دارای **محاسبات چندنخی**، **بازخورد لحظه‌ای**، **تاریخچه پایدار**، **پشتیبانی چندزبانه** و **تم‌های پویا** است — تجربه‌ای حرفه‌ای برای دانش‌آموزان، معلمان و علاقه‌مندان به ریاضی ارائه می‌دهد.

### ویژگی‌های کلیدی
- **آزمایش اول بودن سریع**: الگوریتم بهینه تا **۱۰ به توان ۱۲**.
- **نمایش مقسوم‌علیه‌ها**: فوراً همه مقسوم‌علیه‌ها را نشان می‌دهد.
- **پردازش چندنخی**: رابط کاربری بدون انسداد با `QThread`.
- **تاریخچه پایدار**: ذخیره ۱۰۰ چک آخر در `prime_history.json`.
- **رابط چندزبانه**: پشتیبانی کامل از **انگلیسی**، **فارسی (راست‌چین)**، **چینی** و **روسی**.
- **۵ تم حرفه‌ای**:
  - پیش‌فرض سیستم
  - روشن
  - تاریک
  - آبی
  - قرمز
- **پشتیبانی راست‌چین**: جهت‌گیری خودکار برای فارسی.
- **طراحی مدرن**:
  - هدر گرادیانتی
  - گوشه‌های گرد
  - انیمیشن‌های نرم
  - تایپوگرافی حرفه‌ای

### پیش‌نیازها
- پایتون ۳.۸ یا بالاتر
- PyQt6

### نصب
۱. پایتون را نصب کنید.
۲. وابستگی را نصب کنید:
   ```bash
   pip install PyQt6
   ```
۳. برنامه را اجرا کنید:
   ```bash
   python prime_checker.py
   ```

### نحوه استفاده
- **وارد کردن عدد**: هر عدد صحیح مثبت را تایپ کنید.
- **کلیک بررسی**: وضعیت اول بودن و مقسوم‌علیه‌ها را فوراً ببینید.
- **مشاهده تاریخچه**: ۱۰ چک آخر با زمان‌بندی.
- **پاک کردن تاریخچه**: حذف سوابق ذخیره‌شده.
- **تغییر زبان/تم**: از منوهای کشویی در پنل کنترل استفاده کنید.

### تصاویر
- هدر گرادیانتی با عنوان و زیرعنوان برجسته  
- بخش ورودی تمیز با دکمه بزرگ  
- نمایش نتیجه HTML غنی با خروجی رنگی  
- رابط فارسی راست‌چین با ترجمه کامل  
- تم تاریک با متن و حاشیه پرکنتراست  
- پنل تاریخچه با ورودی‌های زمان‌دار  

### نکات فنی
- **چک اول بهینه**: فاکتورگیری چرخ (۶k±۱) برای سرعت.
- **کارگر QThread**: جلوگیری از فریز رابط در اعداد بزرگ.
- **تاریخچه JSON**: ذخیره پایدار و خوانا.
- **ترجمه پویا**: به‌روزرسانی لحظه‌ای رابط.
- **چندپلتفرمی**: اجرا روی ویندوز، مک و لینوکس.

### مشارکت
فورک کنید و بهبود دهید: درخت فاکتورگیری، خروجی CSV، نمودار تراکم اول، یا آزمون میلر-رابین. Pull requestها خوش‌آمد!

### مجوز
مجوز MIT – آزاد برای استفاده شخصی، آموزشی و تجاری.

---

## 中文

### 概述
**质数分析器 – 专业版** 是一款功能强大、现代化桌面应用程序，用于测试大数的**质数性**并查找**除数**。使用 **Python** 和 **PyQt6** 构建，具备**多线程计算**、**实时反馈**、**持久历史记录**、**多语言支持**和**动态主题**，为学生、教师和数学爱好者提供专业级体验。

### 主要功能
- **快速质数检测**：高效算法支持高达 **10¹²** 的数字。
- **除数列表**：非质数时立即显示所有除数。
- **多线程处理**：使用 `QThread` 保持界面流畅。
- **持久历史**：保存最近 100 次检查至 `prime_history.json`。
- **多语言界面**：完全支持 **英语**、**波斯语（RTL）**、**中文** 和 **俄语**。
- **5 种专业主题**：
  - 系统默认
  - 明亮
  - 暗黑
  - 蓝色
  - 红色
- **RTL 布局支持**：波斯语自动右到左。
- **现代设计**：
  - 渐变标题栏
  - 圆角边框
  - 流畅动画
  - 专业排版

### 要求
- Python 3.8+
- PyQt6

### 安装
1. 确保已安装 Python。
2. 安装依赖：
   ```bash
   pip install PyQt6
   ```
3. 运行程序：
   ```bash
   python prime_checker.py
   ```

### 使用方法
- **输入数字**：键入任意正整数。
- **点击检查**：立即获得质数状态和除数。
- **查看历史**：显示最近 10 次带时间戳的记录。
- **清除历史**：重置保存记录。
- **切换语言/主题**：使用控制面板下拉菜单。

### 截图
- 渐变标题栏，醒目标题与副标题  
- 简洁输入区，超大按钮  
- 富HTML结果显示，彩色输出  
- 波斯语 RTL 界面，完整翻译  
- 暗黑主题，高对比度文本与边框  
- 历史面板，显示带时间戳的条目  

### 技术亮点
- **优化质数检查**：轮式因子分解（6k±1）提速。
- **QThread 工作线程**：大数处理不卡界面。
- **JSON 历史记录**：持久化、人性化存储。
- **动态翻译**：实时更新界面语言。
- **跨平台**：支持 Windows、macOS 和 Linux。

### 贡献
Fork 并改进：添加因子分解树、CSV 导出、质数密度图或 Miller-Rabin 测试。欢迎 Pull Request！

### 许可证
MIT 许可证 – 免费用于个人、教育和商业用途。