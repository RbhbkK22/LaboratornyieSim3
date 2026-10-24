"""Рисует диаграммы для отчета: структура БД, классы, схема Spring MVC."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(__file__).parent / "img"
OUT.mkdir(exist_ok=True)
plt.rcParams["font.family"] = "DejaVu Sans"


def table(ax, x, y, title, rows, w=3.2, head="#dbe7f5"):
    """Рисует таблицу/класс: заголовок + строки. (x, y) - левый верхний угол."""
    lh = 0.42
    h = lh * (len(rows) + 1)
    ax.add_patch(FancyBboxPatch((x, y - h), w, h, boxstyle="round,pad=0.02", fc="white", ec="#333", lw=1.2))
    ax.add_patch(FancyBboxPatch((x, y - lh), w, lh, boxstyle="round,pad=0.02", fc=head, ec="#333", lw=1.2))
    ax.text(x + w / 2, y - lh / 2, title, ha="center", va="center", fontsize=11, weight="bold")
    for i, r in enumerate(rows):
        ax.text(x + 0.12, y - lh * (i + 1.5), r, ha="left", va="center", fontsize=9.5, family="DejaVu Sans Mono")
    return (x, y - h, w, h)


def arrow(ax, p1, p2, text="", style="-|>", color="#333", ls="-"):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=14, color=color, lw=1.2, linestyle=ls))
    if text:
        ax.text((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2 + 0.15, text, ha="center", fontsize=9, color=color)


def er():
    fig, ax = plt.subplots(figsize=(11, 4.6))
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 5.2)
    ax.axis("off")
    table(ax, 0.3, 4.9, "users", ["PK id        BIGINT", "   username  VARCHAR UNIQUE", "   password  VARCHAR", "   role      VARCHAR"], w=3.6)
    table(ax, 4.6, 4.9, "automobiles", ["PK id            BIGINT", "   plate_number  VARCHAR", "   owner_name    VARCHAR", "   color         VARCHAR",
                                        "   parking_place INTEGER", "   arrival_date  DATE", "FK model_id      BIGINT", "   created_by    VARCHAR"], w=3.8)
    table(ax, 9.2, 4.9, "car_models", ["PK id            BIGINT", "   brand         VARCHAR", "   model_name    VARCHAR", "   release_year  INTEGER",
                                       "   price         DOUBLE", "   created_by    VARCHAR"], w=3.6)
    arrow(ax, (8.4, 2.05), (9.2, 4.25), "N : 1")
    arrow(ax, (4.6, 1.33), (2.1, 2.78), color="#777", ls="--")
    ax.text(0.4, 1.6, "created_by хранит\nusername автора записи", fontsize=9, color="#777")
    fig.savefig(OUT / "er.png", dpi=170, bbox_inches="tight")
    plt.close(fig)


def classes():
    fig, ax = plt.subplots(figsize=(12, 7.6))
    ax.set_xlim(0, 16)
    ax.set_ylim(-1.0, 10.4)
    ax.axis("off")
    c_ctrl, c_srv, c_rep, c_ent = "#fde2c8", "#d9f0d3", "#dbe7f5", "#ece0f5"
    # контроллеры
    table(ax, 0.2, 10.2, "AutomobileController", ["list(), newForm()", "editForm(), save()", "delete()"], w=3.6, head=c_ctrl)
    table(ax, 4.2, 10.2, "CarModelController", ["list(), newForm()", "editForm(), save()", "delete()"], w=3.6, head=c_ctrl)
    table(ax, 8.2, 10.2, "CalcController", ["form()", "calculate()"], w=3.6, head=c_ctrl)
    table(ax, 12.2, 10.2, "AdminController", ["users()", "changeRole()"], w=3.6, head=c_ctrl)
    # сервисы
    table(ax, 0.2, 7.6, "AutomobileService", ["findAllForCurrentUser()", "findById(), save()", "delete()"], w=3.6, head=c_srv)
    table(ax, 4.2, 7.6, "CarModelService", ["findAllForCurrentUser()", "findAll(), findById()", "save(), delete()"], w=3.6, head=c_srv)
    table(ax, 8.2, 7.6, "CalcService", ["countDays()", "parkingCost()", "carValue()"], w=3.6, head=c_srv)
    table(ax, 12.2, 7.6, "UserService", ["loadUserByUsername()", "register()", "changeRole()"], w=3.6, head=c_srv)
    # репозитории
    table(ax, 0.2, 5.1, "AutomobileRepository", ["findByCreatedBy()", "findByModelId()"], w=3.6, head=c_rep)
    table(ax, 4.2, 5.1, "CarModelRepository", ["findByCreatedBy()"], w=3.6, head=c_rep)
    table(ax, 12.2, 5.1, "UserRepository", ["findByUsername()", "existsByUsername()"], w=3.6, head=c_rep)
    ax.text(8.3, 4.6, "все репозитории наследуют\nJpaRepository<T, Long>", fontsize=9, style="italic")
    # сущности
    table(ax, 0.2, 2.9, "Automobile", ["id, plateNumber", "ownerName, color", "parkingPlace", "arrivalDate, createdBy", "model : CarModel"], w=3.6, head=c_ent)
    table(ax, 4.2, 2.9, "CarModel", ["id, brand, modelName", "releaseYear, price", "createdBy", "getFullName()"], w=3.6, head=c_ent)
    table(ax, 12.2, 2.9, "User", ["id, username", "password", "role : Role"], w=3.6, head=c_ent)
    table(ax, 8.2, 2.9, "«enum» Role", ["READ_ONLY", "USER", "ADMIN"], w=3.6, head=c_ent)
    for x in (2.0, 6.0, 10.0, 14.0):
        arrow(ax, (x, 8.45), (x, 7.65))
    for x in (2.0, 6.0, 14.0):
        arrow(ax, (x, 5.9), (x, 5.15))
        arrow(ax, (x, 3.85), (x, 2.95), ls="--", color="#666")
    arrow(ax, (3.8, 1.55), (4.2, 1.55), style="-|>")
    arrow(ax, (12.2, 1.9), (11.8, 1.9), style="-|>")
    ax.text(0.3, -0.05, "+ MainController (главная, о приложении), AuthController (вход, регистрация)",
            fontsize=8.5, style="italic", va="center")
    legend = [("controller", c_ctrl), ("service", c_srv), ("repository", c_rep), ("entity", c_ent)]
    for i, (lbl, col) in enumerate(legend):
        ax.add_patch(FancyBboxPatch((0.3 + i * 2.4, -0.85), 0.4, 0.3, boxstyle="round,pad=0.02", fc=col, ec="#333"))
        ax.text(0.8 + i * 2.4, -0.7, lbl, va="center", fontsize=9)
    fig.savefig(OUT / "classes.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


def mvc():
    fig, ax = plt.subplots(figsize=(11, 4.4))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 5.6)
    ax.axis("off")

    def box(x, y, w, h, text, fc):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05", fc=fc, ec="#333", lw=1.2))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=10)

    box(0.2, 2.3, 2.0, 1.0, "Браузер\n(клиент)", "#eeeeee")
    box(3.4, 2.3, 2.6, 1.0, "DispatcherServlet", "#fde2c8")
    box(3.4, 0.3, 2.6, 1.0, "HandlerMapping", "#dbe7f5")
    box(7.4, 4.3, 2.6, 1.0, "Controller\n(@Controller)", "#d9f0d3")
    box(11.0, 4.3, 2.6, 1.0, "Service /\nRepository / БД", "#ece0f5")
    box(7.4, 2.3, 2.6, 1.0, "ViewResolver", "#dbe7f5")
    box(7.4, 0.3, 2.6, 1.0, "View\n(Thymeleaf шаблон)", "#fff5c2")
    arrow(ax, (2.2, 3.0), (3.4, 3.0))
    ax.text(2.8, 3.55, "1. запрос", ha="center", fontsize=9)
    arrow(ax, (4.7, 2.3), (4.7, 1.3), "")
    ax.text(4.85, 1.6, "2. поиск\nобработчика", fontsize=9, ha="left")
    arrow(ax, (5.2, 3.3), (7.4, 4.9), "")
    ax.text(4.2, 4.3, "3. вызов метода", fontsize=9)
    arrow(ax, (10.0, 4.8), (11.0, 4.8), "4")
    arrow(ax, (8.0, 4.3), (6.0, 3.1), "", color="#666")
    ax.text(7.05, 3.45, "5. Model + имя view", fontsize=9, color="#666")
    arrow(ax, (6.0, 2.7), (7.4, 2.7), "6")
    arrow(ax, (6.0, 2.4), (7.4, 0.9))
    ax.text(6.95, 1.75, "7. рендер", fontsize=9)
    arrow(ax, (3.4, 2.5), (2.2, 2.5))
    ax.text(2.8, 1.95, "8. HTML-ответ", ha="center", fontsize=9)
    fig.savefig(OUT / "mvc.png", dpi=170, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    er()
    classes()
    mvc()
    print("ok")
