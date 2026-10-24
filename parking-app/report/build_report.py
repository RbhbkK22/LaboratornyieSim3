"""Собирает пояснительную записку к курсовой работе в .docx (python-docx)."""
import re
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

HERE = Path(__file__).parent
IMG = HERE / "img"
SRC = HERE.parent / "src" / "main" / "java" / "ru" / "urfu" / "parking"
OUT = HERE.parent.parent / "Пояснительная записка Помазов К.Д..docx"

FONT = "Times New Roman"
CODE_FONT = "Courier New"
SIZE = Pt(12)

doc = Document()
fig_no = 0
tab_no = 0


# ---------- стили ----------

def set_font(style_or_run, name=FONT, size=SIZE, bold=None):
    f = style_or_run.font
    f.name = name
    f.size = size
    if bold is not None:
        f.bold = bold
    f.color.rgb = RGBColor(0, 0, 0)
    el = style_or_run.element if hasattr(style_or_run, "element") else style_or_run._element
    rpr = el.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), name)
    for attr in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
        rfonts.attrib.pop(qn(attr), None)


normal = doc.styles["Normal"]
set_font(normal)
pf = normal.paragraph_format
pf.line_spacing = 1.5
pf.first_line_indent = Cm(1.25)
pf.space_before = Pt(0)
pf.space_after = Pt(0)
pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

for lvl in (1, 2):
    st = doc.styles[f"Heading {lvl}"]
    # главные заголовки 14 пт, подразделы как основной текст - 12 пт
    set_font(st, size=Pt(14) if lvl == 1 else SIZE, bold=True)
    st.font.italic = False
    hp = st.paragraph_format
    hp.line_spacing = 1.5
    hp.space_before = Pt(0)
    hp.space_after = Pt(12)
    hp.keep_with_next = True
    hp.first_line_indent = Cm(1.25)
    hp.alignment = WD_ALIGN_PARAGRAPH.LEFT

sec = doc.sections[0]
sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
sec.left_margin, sec.right_margin = Cm(3), Cm(1.5)
sec.top_margin, sec.bottom_margin = Cm(2), Cm(2)
sec.different_first_page_header_footer = True


def add_field(paragraph, instr, placeholder=""):
    """Вставляет поле Word (PAGE, TOC и т.п.)."""
    run = paragraph.add_run()
    b = OxmlElement("w:fldChar")
    b.set(qn("w:fldCharType"), "begin")
    b.set(qn("w:dirty"), "true")
    run._r.append(b)
    run = paragraph.add_run()
    it = OxmlElement("w:instrText")
    it.set(qn("xml:space"), "preserve")
    it.text = instr
    run._r.append(it)
    run = paragraph.add_run()
    s = OxmlElement("w:fldChar")
    s.set(qn("w:fldCharType"), "separate")
    run._r.append(s)
    paragraph.add_run(placeholder)
    run = paragraph.add_run()
    e = OxmlElement("w:fldChar")
    e.set(qn("w:fldCharType"), "end")
    run._r.append(e)


# номер страницы внизу по центру (на титуле нет)
fp = sec.footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
fp.paragraph_format.first_line_indent = Cm(0)
add_field(fp, "PAGE", "2")


# ---------- хелперы контента ----------

def p(text, align=None, indent=True, bold=False, size=None, space_after=None, keep=False):
    para = doc.add_paragraph()
    if align is not None:
        para.alignment = align
    if not indent:
        para.paragraph_format.first_line_indent = Cm(0)
    if space_after is not None:
        para.paragraph_format.space_after = Pt(space_after)
    if keep:
        para.paragraph_format.keep_with_next = True
    # **жирный** внутри текста
    for i, part in enumerate(re.split(r"\*\*(.+?)\*\*", text)):
        if part:
            r = para.add_run(part)
            r.bold = bold or (i % 2 == 1)
            if size:
                r.font.size = size
    return para


def bullets(items):
    for it in items:
        para = p("– " + it)
        para.paragraph_format.first_line_indent = Cm(1.25)


def page_break():
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def h1(text, structural=False):
    para = doc.add_heading(text, level=1)
    para.paragraph_format.page_break_before = True
    if structural:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        para.paragraph_format.first_line_indent = Cm(0)
    return para


def h2(text):
    para = doc.add_heading(text, level=2)
    para.paragraph_format.space_before = Pt(12)
    return para


def figure(name, caption, width_cm=16.0):
    global fig_no
    fig_no += 1
    para = doc.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.paragraph_format.first_line_indent = Cm(0)
    para.paragraph_format.keep_with_next = True
    para.paragraph_format.line_spacing = 1.0
    para.paragraph_format.space_before = Pt(6)
    para.add_run().add_picture(str(IMG / name), width=Cm(width_cm))
    cap = p(f"Рисунок {fig_no} – {caption}", align=WD_ALIGN_PARAGRAPH.CENTER, indent=False, space_after=6)
    return fig_no


def next_fig():
    return fig_no + 1


def table(caption, headers, rows, widths):
    global tab_no
    tab_no += 1
    p(f"Таблица {tab_no} – {caption}", align=WD_ALIGN_PARAGRAPH.LEFT, indent=False, keep=True)
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for row_idx, values in enumerate([headers] + rows):
        cells = t.rows[0].cells if row_idx == 0 else t.add_row().cells
        for i, v in enumerate(values):
            cells[i].width = Cm(widths[i])
            cp = cells[i].paragraphs[0]
            cp.paragraph_format.first_line_indent = Cm(0)
            cp.paragraph_format.line_spacing = 1.0
            cp.alignment = WD_ALIGN_PARAGRAPH.CENTER if row_idx == 0 else WD_ALIGN_PARAGRAPH.LEFT
            # не отрывать шапку и строки небольшой таблицы друг от друга
            if row_idx < len(rows) and len(rows) <= 8:
                cp.paragraph_format.keep_with_next = True
            r = cp.add_run(str(v))
            r.bold = row_idx == 0
    # повтор шапки на следующей странице
    trpr = t.rows[0]._tr.get_or_add_trPr()
    th = OxmlElement("w:tblHeader")
    th.set(qn("w:val"), "true")
    trpr.append(th)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return tab_no


def next_tab():
    return tab_no + 1


def code(text):
    for line in text.rstrip().split("\n"):
        para = doc.add_paragraph()
        pf_ = para.paragraph_format
        pf_.first_line_indent = Cm(0)
        pf_.line_spacing = 1.0
        pf_.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = para.add_run(line if line else " ")
        set_font(r, name=CODE_FONT, size=Pt(12))
    doc.add_paragraph().paragraph_format.line_spacing = 1.0


def src(rel):
    return (SRC / rel).read_text(encoding="utf-8")


def method(rel, signature_start):
    """Вырезает метод из исходника по началу сигнатуры (до парной закрывающей скобки)."""
    text = src(rel)
    i = text.index(signature_start)
    # захватываем аннотации и комментарий над методом
    line_start = text.rfind("\n", 0, i) + 1
    j = text.index("{", i)
    depth = 0
    for k in range(j, len(text)):
        if text[k] == "{":
            depth += 1
        elif text[k] == "}":
            depth -= 1
            if depth == 0:
                block = text[line_start:k + 1]
                lines = block.split("\n")
                # убираем общий отступ
                pad = min(len(l) - len(l.lstrip()) for l in lines if l.strip())
                return "\n".join(l[pad:] for l in lines)
    raise ValueError(signature_start)


# ================= ТИТУЛЬНЫЙ ЛИСТ =================

def tp(text, bold=False, space_after=0, align=WD_ALIGN_PARAGRAPH.CENTER):
    para = p(text, align=align, indent=False, bold=bold, space_after=space_after)
    para.paragraph_format.line_spacing = 1.15
    return para


tp("Министерство науки и высшего образования Российской Федерации")
tp("Федеральное государственное автономное образовательное учреждение")
tp("высшего образования «Уральский федеральный университет")
tp("имени первого Президента России Б.Н. Ельцина»")
tp("Институт радиоэлектроники и информационных технологий – РТФ")
tp("Центр ускоренного обучения", space_after=0)
for _ in range(7):
    tp("")
tp("КУРСОВАЯ РАБОТА", bold=True, space_after=6)
tp("по дисциплине «Технологии программирования»", space_after=6)
tp("на тему", space_after=6)
tp("«Разработка веб-приложения для учета автомобилей на парковке", bold=True)
tp("с использованием Spring Boot»", bold=True)
tp("Вариант 7")
for _ in range(6):
    tp("")
right = WD_ALIGN_PARAGRAPH.LEFT
for line in ("Студент: Помазов К. Д.", "Группа: РИЗ-250213у", "", "Преподаватель: Архипов Н. А.", "",
             "Оценка: ____________________", "Подпись: ___________________"):
    para = tp(line, align=right)
    para.paragraph_format.left_indent = Cm(9.5)
for _ in range(5):
    tp("")
tp("Екатеринбург 2026")

# ================= СОДЕРЖАНИЕ =================
h = p("СОДЕРЖАНИЕ", align=WD_ALIGN_PARAGRAPH.CENTER, indent=False, bold=True, size=Pt(14), space_after=12)
h.paragraph_format.page_break_before = True
toc = doc.add_paragraph()
toc.paragraph_format.first_line_indent = Cm(0)
add_field(toc, 'TOC \\o "1-2" \\h \\z \\u', "Оглавление обновится при открытии (правой кнопкой → «Обновить поле»).")

# ================= ОПРЕДЕЛЕНИЯ =================
h1("ОПРЕДЕЛЕНИЯ", structural=True)
p("В настоящей пояснительной записке применяют следующие термины с соответствующими определениями:")
for term, d in [
    ("Фреймворк", "программная платформа, которая задает структуру приложения и берет на себя типовые задачи (обработку запросов, работу с базой данных, безопасность)."),
    ("Веб-приложение", "клиент-серверное приложение, с которым пользователь работает через браузер."),
    ("Сущность (Entity)", "Java-класс, объекты которого сохраняются в таблицу базы данных."),
    ("Репозиторий", "интерфейс доступа к данным одной сущности: поиск, сохранение, удаление записей."),
    ("Контроллер", "класс, который принимает HTTP-запросы пользователя и возвращает страницу или данные."),
    ("Аутентификация", "проверка того, что пользователь является тем, за кого себя выдает (ввод логина и пароля)."),
    ("Авторизация", "проверка прав пользователя на выполнение конкретного действия."),
    ("Роль", "набор прав пользователя в системе (READ_ONLY, USER, ADMIN)."),
    ("Бин (Bean)", "объект, созданием и жизненным циклом которого управляет контейнер Spring."),
]:
    p(f"**{term}** – {d}")

# ================= СОКРАЩЕНИЯ =================
h1("ОБОЗНАЧЕНИЯ И СОКРАЩЕНИЯ", structural=True)
for a, d in [
    ("БД", "база данных"), ("СУБД", "система управления базами данных"),
    ("API", "Application Programming Interface, программный интерфейс приложения"),
    ("CRUD", "Create, Read, Update, Delete – создание, чтение, изменение и удаление записей"),
    ("HTTP", "HyperText Transfer Protocol, протокол передачи гипертекста"),
    ("JDBC", "Java Database Connectivity, стандартный API Java для работы с БД"),
    ("JPA", "Jakarta Persistence API, спецификация объектно-реляционного отображения в Java"),
    ("JVM", "Java Virtual Machine, виртуальная машина Java"),
    ("MVC", "Model-View-Controller, архитектурный шаблон «модель – представление – контроллер»"),
    ("ORM", "Object-Relational Mapping, объектно-реляционное отображение"),
    ("SQL", "Structured Query Language, язык структурированных запросов"),
    ("UI", "User Interface, пользовательский интерфейс"),
]:
    p(f"**{a}** – {d}.")

# ================= ВВЕДЕНИЕ =================
h1("ВВЕДЕНИЕ", structural=True)
p("Сейчас большая часть корпоративных информационных систем делается в виде веб-приложений. Пользователю не нужно "
  "ничего устанавливать – достаточно браузера, а все данные хранятся централизованно на сервере. Для языка Java "
  "самым популярным инструментом для таких задач является фреймворк Spring и его надстройка Spring Boot.")
p("Учет автомобилей на парковке – типичная задача небольшой организации: нужно знать, какие машины стоят на "
  "парковке, на каком месте, сколько времени и сколько должен заплатить владелец. Если вести такой учет в тетради "
  "или в Excel, то данные легко потерять, а разграничить доступ между сотрудниками почти невозможно.")
p("**Цель работы** – разработать веб-приложение для учета автомобилей на парковке и справочника моделей "
  "автомобилей с их стоимостью с использованием Spring Boot.")
p("Для достижения цели нужно решить следующие **задачи**:")
bullets([
    "изучить существующие Java-фреймворки и выбрать технологии для разработки;",
    "спроектировать структуру базы данных и классов приложения;",
    "реализовать веб-формы входа, регистрации, списков, ввода данных, расчета, управления ролями и «О приложении»;",
    "реализовать разграничение доступа по ролям READ_ONLY, USER и ADMIN;",
    "подключить Spring Boot Actuator для мониторинга приложения;",
    "проверить работу приложения и оформить пояснительную записку.",
])
p("Объект исследования – процесс учета автомобилей на парковке. Предмет исследования – разработка веб-приложений "
  "на платформе Spring Boot.")

# ================= 1 ТЕХНОЛОГИИ =================
h1("1 Описание используемых технологий")
h2("1.1 Существующие фреймворки Java")
p("Для разработки серверных приложений на Java существует несколько фреймворков. Кратко рассмотрим самые известные.")
p("**Spring Framework / Spring Boot** – самый распространенный фреймворк в корпоративной разработке. Основан на "
  "внедрении зависимостей, имеет модули почти под любую задачу: веб, безопасность, работа с БД, очереди сообщений. "
  "Spring Boot упрощает настройку за счет автоконфигурации и встроенного сервера.")
p("**Jakarta EE** (раньше Java EE) – набор стандартов (Servlet, JPA, CDI, JAX-RS и др.), которые реализуют "
  "серверы приложений, например WildFly или GlassFish. Подходит для крупных систем, но настройка сложнее.")
p("**Quarkus** – современный фреймворк от Red Hat, ориентированный на облака и Kubernetes. Быстро запускается и "
  "умеет компилироваться в нативный код через GraalVM.")
p("**Micronaut** – похож на Quarkus, внедрение зависимостей выполняется на этапе компиляции, поэтому приложения "
  "потребляют мало памяти. Хорошо подходит для микросервисов.")
p("**Jakarta Server Faces (JSF)** – компонентный фреймворк для построения UI на сервере. Сейчас используется в "
  "основном в старых проектах.")
p("**Vaadin** – фреймворк, в котором интерфейс пишется полностью на Java, без HTML и JavaScript.")
p(f"Сравнение фреймворков приведено в таблице {next_tab()}.")
table("Сравнение Java-фреймворков",
      ["Фреймворк", "Сфера применения", "Открытый код", "Порог входа"],
      [["Spring Boot", "Корпоративные веб-приложения, микросервисы", "Да (Apache 2.0)", "Средний"],
       ["Jakarta EE", "Крупные корпоративные системы", "Да (EPL 2.0)", "Высокий"],
       ["Quarkus", "Облачные и нативные микросервисы", "Да (Apache 2.0)", "Средний"],
       ["Micronaut", "Микросервисы, serverless", "Да (Apache 2.0)", "Средний"],
       ["JSF", "Серверный UI, старые проекты", "Да", "Высокий"],
       ["Vaadin", "Бизнес-интерфейсы на чистой Java", "Да (ядро), есть платные компоненты", "Низкий"]],
      [3.0, 6.0, 4.0, 3.0])
p("Для курсовой работы выбран Spring Boot, так как он лучше всего документирован, по нему больше всего примеров и "
  "он чаще всего встречается в вакансиях (см. раздел 2.4).")

h2("1.2 Spring Boot")
p("Spring Boot – это проект на базе Spring Framework, задача которого – максимально упростить создание и запуск "
  "приложения. Основные возможности:")
bullets([
    "**стартеры** – готовые наборы зависимостей (spring-boot-starter-web, -data-jpa, -security и т.д.), не нужно "
    "подбирать версии библиотек вручную;",
    "**автоконфигурация** – Spring Boot сам настраивает бины по найденным в проекте библиотекам, например, увидев "
    "драйвер H2, сам создает подключение к БД;",
    "**встроенный сервер** Tomcat – приложение запускается как обычная Java-программа, без отдельного сервера приложений;",
    "**Actuator** – готовые эндпоинты для мониторинга (/actuator/health, /actuator/metrics и др.);",
    "настройка через один файл application.properties.",
])
p("В проекте используется Spring Boot 3.5. Точка входа – класс ParkingApplication с аннотацией "
  "@SpringBootApplication, которая включает автоконфигурацию и сканирование компонентов в пакете ru.urfu.parking.")

h2("1.3 База данных H2")
p("H2 – реляционная СУБД, написанная на Java. Ее можно запускать прямо внутри приложения (embedded-режим), "
  "хранить данные в памяти или в файле. Для учебного проекта это удобно: не нужно устанавливать отдельный "
  "сервер БД. В приложении данные хранятся в файле ./data/parking, поэтому не пропадают после перезапуска. "
  "Также у H2 есть веб-консоль, через которую можно посмотреть таблицы.")
p(f"Сравнение H2 с другими популярными СУБД приведено в таблице {next_tab()}.")
table("Сравнение СУБД",
      ["Критерий", "H2", "PostgreSQL", "MySQL"],
      [["Тип", "Встраиваемая / серверная", "Серверная", "Серверная"],
       ["Установка", "Не нужна (библиотека jar)", "Отдельный сервер", "Отдельный сервер"],
       ["Хранение", "В памяти или в файле", "На диске", "На диске"],
       ["Лицензия", "MPL 2.0 / EPL 1.0", "PostgreSQL License", "GPL / коммерческая"],
       ["Производительность на больших объемах", "Низкая", "Высокая", "Высокая"],
       ["Где применяется", "Тесты, прототипы, учебные проекты", "Промышленные системы", "Веб-проекты, CMS"]],
      [4.5, 4.0, 4.0, 4.0])
p("В Java и Spring есть несколько способов работы с БД:")
bullets([
    "**JDBC** – низкоуровневый API: открываем соединение, пишем SQL, вручную разбираем ResultSet;",
    "**JdbcTemplate** (Spring JDBC) – обертка над JDBC, убирает шаблонный код, но SQL пишется вручную;",
    "**JPA / Hibernate** – ORM: работаем с объектами, а SQL генерируется автоматически;",
    "**Spring Data JPA** – надстройка над JPA: достаточно объявить интерфейс репозитория, а реализация создается "
    "автоматически, запросы строятся по имени метода (findByCreatedBy);",
    "**MyBatis, jOOQ** – сторонние библиотеки, где SQL остается под контролем разработчика.",
])
p("В проекте используется Spring Data JPA, так как он требует меньше всего кода.")

h2("1.4 Spring MVC")
p("Spring MVC – модуль Spring для веб-приложений, построенный по шаблону Model-View-Controller. Модель – это данные, "
  "представление (View) – HTML-шаблон, контроллер – класс, который обрабатывает запрос и решает, какие данные и "
  f"какую страницу вернуть. Схема обработки запроса показана на рисунке {next_fig()}.")
figure("mvc.png", "Схема обработки запроса в Spring MVC", 15.5)
p("Все запросы сначала попадают в DispatcherServlet. Он через HandlerMapping находит метод контроллера, который "
  "подходит под URL (например, @GetMapping(\"/automobiles\")). Контроллер обращается к сервисам, кладет данные в "
  "объект Model и возвращает имя шаблона. ViewResolver находит шаблон Thymeleaf, тот формирует HTML, и ответ "
  "уходит в браузер.")

h2("1.5 Lombok")
p("Lombok – библиотека, которая на этапе компиляции генерирует шаблонный код по аннотациям: @Getter, @Setter, "
  "@NoArgsConstructor, @Data, @Builder и др. В проекте Lombok используется в классах-сущностях.")
p("Плюсы использования Lombok:")
bullets(["классы становятся короче и читаются легче;",
         "не нужно вручную обновлять геттеры и сеттеры при добавлении полей;",
         "меньше шанс ошибиться в шаблонном коде."])
p("Минусы:")
bullets(["нужен плагин в IDE, иначе среда разработки показывает ошибки;",
         "сгенерированного кода не видно, это мешает отладке;",
         "Lombok зависит от внутренностей компилятора, поэтому на новых версиях JDK может не работать. "
         "В проекте это случилось: версия из Spring Boot не собиралась на JDK 27, пришлось поднять версию Lombok "
         "до 1.18.48;",
         "аннотация @Data на JPA-сущностях может давать проблемы с equals/hashCode, поэтому в проекте "
         "использованы только @Getter и @Setter."])

h2("1.6 JPA")
p("JPA (Jakarta Persistence API) – это спецификация, то есть набор интерфейсов и аннотаций (@Entity, @Id, "
  "@ManyToOne и т.д.) для объектно-реляционного отображения. Сама по себе JPA ничего не делает, нужна реализация.")
p("Основные реализации JPA:")
bullets(["**Hibernate** – самая популярная реализация, используется в Spring Boot по умолчанию (используется и в проекте);",
         "**EclipseLink** – эталонная реализация JPA от Eclipse Foundation;",
         "**OpenJPA** – реализация от Apache, сейчас развивается слабо."])
p("Плюсы JPA: не нужно писать SQL для простых операций, код не зависит от конкретной СУБД, есть кэширование и "
  "ленивая загрузка связей. Минусы: сложнее понять, какие запросы реально выполняются, есть известная проблема "
  "N+1 запросов, для сложных отчетов все равно приходится писать JPQL или SQL.")

# ================= 2 ОПИСАНИЕ ЗАДАЧИ =================
h1("2 Описание задачи")
h2("2.1 Постановка задачи")
p("Необходимо разработать веб-приложение с базой данных, в которой есть таблица пользователей и таблицы по варианту 7: "
  "список автомобилей на парковке (Automobile) и список моделей автомобилей с их стоимостью.")
p("Пользователь открывает приложение, вводит логин и пароль и попадает на главную страницу. Из нее можно перейти "
  "к спискам автомобилей и моделей, где каждую запись можно изменить, удалить, а также добавить новую.")
p("В приложении должны быть роли:")
bullets(["**READ_ONLY** – только просмотр, выдается всем новым пользователям при регистрации;",
         "**USER** – видит и редактирует только записи, которые создал сам;",
         "**ADMIN** – полный доступ ко всем данным и форма назначения ролей."])
p("Также нужно подключить Spring Boot Actuator. Требуемые веб-формы: вход, списки и формы ввода для двух таблиц, "
  "главная страница, «О приложении», форма расчета характеристик и форма добавления ролей. В качестве расчета "
  "реализован расчет стоимости стоянки автомобиля и его примерной текущей стоимости с учетом износа.")

h2("2.2 Описание структуры базы данных")
p(f"База данных состоит из трех таблиц (рисунок {next_fig()}). Таблицы создаются автоматически Hibernate по "
  "классам-сущностям (spring.jpa.hibernate.ddl-auto=update).")
figure("er.png", "Структура базы данных", 16)
p(f"Описание полей таблиц приведено в таблице {next_tab()}.")
table("Описание полей таблиц БД",
      ["Таблица", "Поле", "Тип", "Описание"],
      [["users", "id", "BIGINT", "Первичный ключ"],
       ["", "username", "VARCHAR", "Логин (уникальный)"],
       ["", "password", "VARCHAR", "Хеш пароля (BCrypt)"],
       ["", "role", "VARCHAR", "Роль: READ_ONLY, USER, ADMIN"],
       ["car_models", "id", "BIGINT", "Первичный ключ"],
       ["", "brand / model_name", "VARCHAR", "Марка и модель"],
       ["", "release_year", "INTEGER", "Год выпуска"],
       ["", "price", "DOUBLE", "Стоимость нового автомобиля, руб."],
       ["", "created_by", "VARCHAR", "Логин создателя записи"],
       ["automobiles", "id", "BIGINT", "Первичный ключ"],
       ["", "plate_number", "VARCHAR", "Государственный номер"],
       ["", "owner_name", "VARCHAR", "ФИО владельца"],
       ["", "color", "VARCHAR", "Цвет"],
       ["", "parking_place", "INTEGER", "Номер парковочного места"],
       ["", "arrival_date", "DATE", "Дата заезда на парковку"],
       ["", "model_id", "BIGINT", "Внешний ключ на car_models.id"],
       ["", "created_by", "VARCHAR", "Логин создателя записи"]],
      [3.0, 3.8, 2.4, 7.3])
p("Связь между automobiles и car_models – «многие к одному»: одной модели может соответствовать несколько "
  "автомобилей. Поле created_by хранит логин пользователя, который создал запись, по нему фильтруются записи "
  "для роли USER.")

h2("2.3 Описание классов")
p(f"Диаграмма классов приложения показана на рисунке {next_fig()}. Классы разделены на слои: контроллеры, сервисы, "
  "репозитории и сущности.")
figure("classes.png", "Диаграмма классов приложения", 16.5)
bullets([
    "**Сущности** (Automobile, CarModel, User, перечисление Role) описывают таблицы БД.",
    "**Репозитории** (AutomobileRepository, CarModelRepository, UserRepository) наследуют JpaRepository и дают "
    "доступ к данным. Дополнительные методы (findByCreatedBy, findByUsername) Spring Data строит по имени метода.",
    "**Сервисы** содержат логику: AutomobileService и CarModelService фильтруют записи по роли и проверяют, что "
    "USER не трогает чужие записи; CalcService выполняет расчет; UserService отвечает за регистрацию, смену ролей "
    "и загрузку пользователя для Spring Security.",
    "**Контроллеры** принимают запросы от форм и возвращают Thymeleaf-шаблоны.",
    "**Конфигурация**: SecurityConfig настраивает доступ к URL, DataInitializer заполняет БД тестовыми данными "
    "при первом запуске.",
])

h2("2.4 Востребованность фреймворка Spring Boot")
p("Чтобы оценить востребованность Spring Boot, был выполнен поиск вакансий на сайте hh.ru по названию фреймворка "
  f"и по аналогам из других языков. Результаты на 24.10.2026 приведены в таблице {next_tab()}.")
table("Количество вакансий на hh.ru (поиск по названию, 24.10.2026)",
      ["Фреймворк (язык)", "Россия", "Москва", "Екатеринбург"],
      [["Spring Boot (Java)", "253", "158", "2"],
       ["Django (Python)", "184", "84", "4"],
       ["Laravel (PHP)", "120", "77", "6"],
       ["ASP.NET Core (C#)", "107", "61", "2"],
       ["Quarkus (Java)", "13", "3", "0"]],
      [5.5, 3.5, 3.5, 3.5])
p("По данным поиска Spring Boot опережает аналоги на других языках по России в целом и по Москве. Среди "
  "Java-фреймворков он лидирует с большим отрывом (Quarkus почти не встречается). В Екатеринбурге вакансий "
  "по всем фреймворкам мало, поэтому разница там не показательна. Стоит учитывать, что многие вакансии "
  "Java-разработчика не содержат слов «Spring Boot» в названии, хотя знание Spring в них требуется, поэтому "
  "реальная доля Spring еще выше. Изучение Spring Boot полезно для трудоустройства.")

# ================= 3 РАЗРАБОТКА =================
h1("3 Разработка веб-приложения")
h2("3.1 Описание структуры проекта")
p("Проект собирается с помощью Maven (используется Maven Wrapper, поэтому Maven не нужно устанавливать отдельно). "
  "Структура пакетов:")
bullets([
    "**ru.urfu.parking** – главный класс ParkingApplication;",
    "**config** – настройки безопасности (SecurityConfig) и начальные данные (DataInitializer);",
    "**entity** – JPA-сущности и перечисление ролей;",
    "**repository** – интерфейсы Spring Data JPA;",
    "**service** – бизнес-логика и вспомогательный класс SecurityUtils для получения текущего пользователя;",
    "**controller** – Spring MVC контроллеры;",
    "**resources/templates** – HTML-шаблоны Thymeleaf (общий фрагмент fragments/header.html с меню и папки "
    "automobiles, models, admin);",
    "**resources/static/css** – стили; **application.properties** – настройки БД, Actuator и Thymeleaf.",
])

h2("3.2 Описание решения поставленной задачи")
p("Приложение «Парковка» позволяет вести учет автомобилей и справочник моделей. При первом запуске "
  "DataInitializer создает трех тестовых пользователей (admin, user, guest) и несколько записей.")
p("Безопасность построена на Spring Security. Пароли хранятся в виде хеша BCrypt. Права проверяются на двух "
  "уровнях: в SecurityConfig закрыты URL для добавления, изменения и удаления (доступны только USER и ADMIN), "
  "а в сервисах проверяется владелец записи – если пользователь с ролью USER попытается открыть чужую запись "
  "по прямой ссылке, будет выброшено AccessDeniedException и показана страница «Доступ запрещен». В шаблонах "
  "кнопки, недоступные роли, скрыты с помощью sec:authorize.")
p("Форма расчета считает стоимость стоянки: количество суток (включая день заезда) умножается на тариф, при "
  "стоянке от 30 суток дается скидка 15%. Дополнительно считается примерная текущая стоимость автомобиля: цена "
  "модели уменьшается на 10% за каждый год с года выпуска, но не ниже 20% от исходной цены.")

h2("3.3 Описание реализации веб-приложения")
p("Ниже приведены основные фрагменты кода. Сущность автомобиля связана с моделью через @ManyToOne, валидация "
  "полей сделана аннотациями Bean Validation:")
auto_src = src("entity/Automobile.java")
code(auto_src[auto_src.index("    @NotBlank(message = \"Укажите госномер\")"):auto_src.index("    private String color;")].rstrip()
     .replace("\n    ", "\n").lstrip())
p("Фильтрация записей по роли выполняется в сервисе:")
code(method("service/AutomobileService.java", "public List<Automobile> findAllForCurrentUser()"))
p("Контроллер сохранения автомобиля проверяет ошибки валидации и, если они есть, возвращает форму обратно "
  "с сообщениями об ошибках:")
code(method("controller/AutomobileController.java", "public String save("))
p("Расчет стоимости стоянки и стоимости автомобиля вынесен в отдельный сервис CalcService (листинг 2 приложения 1).")
p("Регистрация нового пользователя всегда выдает роль READ_ONLY (метод register в UserService). "
  "Actuator подключен зависимостью spring-boot-starter-actuator. В application.properties открыты эндпоинты "
  "health, info, metrics и loggers; /actuator/health и /actuator/info доступны всем, остальные – только ADMIN. "
  f"Ответ эндпоинта /actuator/health показан на рисунке {next_fig()}. "
  "Полный код классов SecurityConfig и CalcService приведен в приложении 1, остальной код – в репозитории.")
figure("12_actuator.png", "Ответ эндпоинта /actuator/health", 5.5)

h2("3.4 Результат работы веб-приложения")
p(f"Страница входа показана на рисунке {next_fig()}, страница регистрации – на рисунке {next_fig() + 1}.")
figure("01_login.png", "Форма входа в приложение", 11)
figure("02_register.png", "Форма регистрации", 11)
p(f"После входа открывается главная страница (рисунок {next_fig()}) с меню и количеством записей.")
figure("03_index_admin.png", "Главная страница (роль ADMIN)", 14.5)
p(f"Список автомобилей для администратора показан на рисунке {next_fig()}. ADMIN видит все записи и столбец "
  "«Создал».")
figure("04_autos_admin.png", "Список автомобилей (роль ADMIN)", 15)
p(f"Форма добавления автомобиля показана на рисунке {next_fig()}. Если отправить форму пустой, выводятся "
  f"сообщения об ошибках (рисунок {next_fig() + 1}).")
figure("05_auto_form.png", "Форма добавления автомобиля", 12.5)
figure("06_auto_validation.png", "Ошибки валидации в форме автомобиля", 12.5)
p(f"Список моделей и форма редактирования модели показаны на рисунках {next_fig()} и {next_fig() + 1}.")
figure("07_models_admin.png", "Список моделей автомобилей", 15)
figure("08_model_form.png", "Форма редактирования модели", 13)
p(f"Результат расчета стоимости для автомобиля, который стоит на парковке 41 день, показан на рисунке "
  f"{next_fig()}: 41 × 300 = 12 300 руб., со скидкой 15% – 10 455 руб.")
figure("09_calc.png", "Форма расчета стоимости", 13)
p(f"Форма назначения ролей доступна только администратору (рисунок {next_fig()}).")
figure("10_admin_roles.png", "Форма управления ролями", 15)
p(f"Пользователь с ролью USER видит только свою запись (рисунок {next_fig()}), а пользователь с ролью "
  f"READ_ONLY видит все записи, но без кнопок добавления, изменения и удаления (рисунок {next_fig() + 1}).")
figure("13_autos_user.png", "Список автомобилей для роли USER", 15)
figure("14_autos_guest.png", "Список автомобилей для роли READ_ONLY", 15)
p(f"При попытке READ_ONLY открыть форму добавления по прямой ссылке показывается страница «Доступ запрещен» "
  f"(рисунок {next_fig()}).")
figure("15_access_denied.png", "Страница «Доступ запрещен»", 14)
p(f"Форма «О приложении» показана на рисунке {next_fig()}.")
figure("11_about.png", "Форма «О приложении»", 15)

# ================= ЗАКЛЮЧЕНИЕ =================
h1("ЗАКЛЮЧЕНИЕ", structural=True)
p("В ходе курсовой работы было разработано веб-приложение «Парковка» для учета автомобилей на парковке и "
  "справочника моделей автомобилей с их стоимостью.")
p("Были рассмотрены Java-фреймворки, СУБД и способы доступа к данным, выбраны Spring Boot, Spring MVC, "
  "Spring Security, Spring Data JPA (Hibernate), H2, Thymeleaf и Lombok. Спроектированы структура БД и классы "
  "приложения.")
p("В приложении реализованы все требуемые формы: вход и регистрация, списки и формы ввода для автомобилей и "
  "моделей, главная страница, «О приложении», расчет стоимости стоянки и текущей стоимости автомобиля, форма "
  "назначения ролей. Реализовано разграничение доступа по ролям READ_ONLY, USER и ADMIN, подключен Actuator.")
p("Приложение можно доработать: проверять, что парковочное место не занято, добавить поиск и сортировку в "
  "списках, перейти с H2 на PostgreSQL и написать больше автотестов.")

# ================= ИСТОЧНИКИ =================
h1("СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ", structural=True)
for i, s in enumerate([
    "Spring Boot Reference Documentation [Электронный ресурс]. – URL: https://docs.spring.io/spring-boot/ (дата обращения: 24.10.2026).",
    "Spring Framework Documentation. Web MVC [Электронный ресурс]. – URL: https://docs.spring.io/spring-framework/reference/web/webmvc.html (дата обращения: 24.10.2026).",
    "Spring Security Reference [Электронный ресурс]. – URL: https://docs.spring.io/spring-security/reference/ (дата обращения: 24.10.2026).",
    "Spring Data JPA Reference Documentation [Электронный ресурс]. – URL: https://docs.spring.io/spring-data/jpa/reference/ (дата обращения: 24.10.2026).",
    "Hibernate ORM User Guide [Электронный ресурс]. – URL: https://hibernate.org/orm/documentation/ (дата обращения: 24.10.2026).",
    "H2 Database Engine [Электронный ресурс]. – URL: https://www.h2database.com/ (дата обращения: 24.10.2026).",
    "Project Lombok [Электронный ресурс]. – URL: https://projectlombok.org/ (дата обращения: 24.10.2026).",
    "Thymeleaf Documentation [Электронный ресурс]. – URL: https://www.thymeleaf.org/documentation.html (дата обращения: 24.10.2026).",
    "Bootstrap 5 Documentation [Электронный ресурс]. – URL: https://getbootstrap.com/docs/5.3/ (дата обращения: 24.10.2026).",
    "Jakarta Persistence Specification [Электронный ресурс]. – URL: https://jakarta.ee/specifications/persistence/ (дата обращения: 24.10.2026).",
    "Уоллс К. Spring в действии. 6-е изд. – М.: ДМК Пресс, 2022. – 544 с.",
    "Курсовое проектирование: учебно-методическое пособие. – Екатеринбург: УрФУ, 2023.",
], 1):
    p(f"{i}. {s}")

# ================= ПРИЛОЖЕНИЯ =================
h1("ПРИЛОЖЕНИЕ 1", structural=True)
p("Фрагменты кода приложения", align=WD_ALIGN_PARAGRAPH.CENTER, indent=False, bold=True)
p("Ссылка на репозиторий: https://github.com/RbhbkK22/LaboratornyieSim3/tree/main")
p("Листинг 1 – SecurityConfig.java", indent=False, bold=True)
code(src("config/SecurityConfig.java"))
p("Листинг 2 – CalcService.java", indent=False, bold=True)
code(src("service/CalcService.java"))

h1("ПРИЛОЖЕНИЕ 2", structural=True)
p("Заключение онлайн-проверки на антиплагиат", align=WD_ALIGN_PARAGRAPH.CENTER, indent=False, bold=True)
p("[Сюда вставляется скриншот или справка о проверке работы на антиплагиат.]",
  align=WD_ALIGN_PARAGRAPH.CENTER, indent=False)

# поля обновятся при открытии в Word
settings = doc.settings.element
upd = OxmlElement("w:updateFields")
upd.set(qn("w:val"), "true")
settings.append(upd)

doc.core_properties.author = "Помазов К. Д."
doc.core_properties.title = "Пояснительная записка к курсовой работе"
doc.save(OUT)
print(f"saved {OUT}  figures={fig_no} tables={tab_no}")
