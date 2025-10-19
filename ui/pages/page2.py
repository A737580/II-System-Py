from nicegui import ui
from typing import List

from ui.components.list_box import ListBox
from models.exercise2.fuzzy_statement import FuzzyStatement
from models.exercise2.fuzzy_set import FuzzySet


class Page2:
    def __init__(self):
        self.statements: List[FuzzyStatement] = []
        self.fuzzy_sets: list[FuzzySet] = []
        self.setup_tabs()
    
    def setup_tabs(self):
        # Создаем табы
        with ui.tabs().classes('w-full') as tabs:
            task_2_1_tab = ui.tab('Задание 2.1')
            task_2_2_tab = ui.tab('Задание 2.2')
        
        # Содержимое табов
        with ui.tab_panels(tabs, value=task_2_1_tab).classes('w-full'):
            with ui.tab_panel(task_2_1_tab):
                self.setup_task_2_1()
            
            with ui.tab_panel(task_2_2_tab):
                self.setup_task_2_2()
    
    def setup_task_2_1(self):
        """Первое поле - ваш существующий интерфейс"""
        with ui.row().classes("w-full justify-center"):
            with ui.column().classes(
                "border-2 border-blue-200 w-[900px] mx-auto h-full px-6 pb-6 gap-10 bg-gray-50"
            ):
                # --- верхняя панель: список высказываний + панель добавления ---
                with ui.row().classes("w-full gap-0"):

                    # Левая колонка: список высказываний
                    with ui.column().classes("w-1/3 gap-0"):
                        ui.label("Список высказываний").classes("text-h6")
                        with ui.row().classes("w-[250px] gap-0"):
                            self.statement_box = ListBox(height="220px")
                    with ui.column().classes("w-2/3 gap-0"):
                        ui.label("Добавить высказывание").classes("text-h6")
                        with ui.row().classes("w-full gap-0"):
                            # Правая колонка: панель добавления
                            with ui.column().classes("w-1/2"):
                                self.text_input = ui.input("Текст высказывания")
                                self.category_input = ui.input("Категория")
                                self.number_input = ui.number(label="Числовая часть")

                            with ui.column().classes("mt-5 w-1/2"):
                                self.truth_input = ui.number(
                                    "Степень истинности (0-1)",
                                    value=1.0,
                                    min=0,
                                    max=1,
                                    step=0.1,
                                    format="%.2f",
                                ).style("width:150px")
                                ui.button("Добавить", on_click=self.add_statement)
                                ui.button(
                                    "Удалить",
                                    on_click=self.remove_statement,
                                )

                with ui.row().classes("w-full gap-0"):
                    # --- нижняя панель: результат ---
                    with ui.column().classes("w-1/3 gap-0"):
                        ui.label("Результат").classes("text-h6")
                        with ui.row().classes("w-[250px] gap-0"):
                            self.result_box = ListBox(height="270px")
                    with ui.column().classes("w-2/3 gap-0"):
                        ui.label("Операции над высказываниями").classes("text-h6")
                        with ui.row().classes("w-full gap-0"):
                            # --- средняя панель: операции ---
                            with ui.column().classes("w-1/2"):

                                self.operation = ui.radio(
                                    ["Отрицание", "Конъюнкция", "Дизъюнкция"],
                                    value="Отрицание",
                                )

                                # выбор операндов
                                with ui.row():
                                    self.left_operand = ui.select(
                                        self.statements, label="Высказывание A"
                                    )
                                    self.right_operand = ui.select(
                                        self.statements, label="Высказывание B"
                                    )

                            with ui.column().classes("w-1/2"):
                                # варианты норм (для конъююнкции/дизъюнкции)
                                self.norm = ui.radio(
                                    [
                                        "Минмакс",
                                        "Алгебраическая сумма",
                                        "Граничная сумма",
                                        "Драстическая сумма",
                                    ],
                                    value="Минмакс",
                                )
                                ui.button(
                                    "Выполнить операцию",
                                    on_click=self.perform_operation,
                                )
                                ui.button(
                                    "Очистить все поля",
                                    on_click=self.clear_all,
                                    color="red",
                                )
    
   
    def setup_task_2_2(self):
        """Интерфейс для работы с классом FuzzySet"""
        with ui.row().classes("w-full justify-center"):
            with ui.column().classes(
                "border-2 border-blue-200 w-[950px] mx-auto h-full px-6 pb-6 gap-10 bg-gray-50"
            ):

                # --- Верхняя панель: создание и добавление элементов ---
                with ui.row().classes("w-full"):
                    # левая часть — список множеств
                    with ui.column().classes("w-1/3"):
                        ui.label("Список нечетких множеств").classes("text-h6")
                        self.fuzzy_box = ListBox(height="230px")

                    # правая часть — добавление множества и элементов
                    with ui.column().classes("w-2/3"):
                        ui.label("Создать или дополнить множество").classes("text-h6")

                        with ui.row().classes("gap-4"):
                            self.fuzzy_name = ui.input("Имя множества").style("width:200px")
                            self.param_input = ui.number("Параметр", step=0.1)
                            self.truth_input = ui.number(
                                "Степень принадлежности (0-1)",
                                min=0, max=1, step=0.1, value=1.0
                            ).style("width:200px")

                        with ui.row().classes("gap-2 mt-2"):
                            ui.button("Создать/Добавить", on_click=self.add_fuzzy)
                            ui.button("Удалить параметр", on_click=self.remove_param)
                            ui.button("Очистить все", on_click=self.clear_all_sets, color="red")

                # --- Средняя панель: операции ---
                with ui.row().classes("w-full mt-4"):
                    with ui.column().classes("w-1/3"):
                        ui.label("Результаты операций").classes("text-h6")
                        self.result_box = ListBox(height="270px")

                    with ui.column().classes("w-2/3"):
                        ui.label("Операции над нечеткими множествами").classes("text-h6")
                        with ui.row():
                            self.operation = ui.radio(
                                ["Отрицание", "Конъюнкция", "Дизъюнкция"],
                                value="Отрицание"
                            )

                        with ui.row().classes("gap-4 mt-2"):
                            self.left_set = ui.select([], label="Множество A")
                            self.right_set = ui.select([], label="Множество B")

                        with ui.row().classes("gap-4 mt-4"):
                            self.norm_type = ui.radio(
                                ["Минмакс", "Алгебраическая сумма", "Граничная сумма", "Драстическая сумма"],
                                value="Минмакс"
                            )

                        with ui.row().classes("gap-4 mt-4"):
                            ui.button("Выполнить операцию", on_click=self.perform_fuzzy_operation)
                            ui.button("Очистить результат", on_click=lambda: self.result_box.clear())

    def clear_all(self):
        self.statements:list[FuzzyStatement] = []
        self.statement_box.clear()
        self.result_box.clear()
        self.update_selector_operands()
        self.text_input.value = ""
        self.category_input.value = ""
        self.truth_input.value = 1.00
        self.number_input.value = None
        self.operation.value = "Отрицание"
        self.norm.value = "Минмакс"

    def update_selector_operands(self):
        stmt_tmp = [x.to_string() for x in self.statements]
        self.left_operand.set_options(stmt_tmp)
        self.right_operand.set_options(stmt_tmp)

    def remove_statement(self):
        if self.statement_box.get_selected_index() != -1 and self.statements.pop(
            self.statement_box.get_selected_index()
        ):
            self.statement_box.remove_selected()
            self.update_selector_operands()


    def add_statement(self):
        text = self.text_input.value
        cat = self.category_input.value
        number = self.number_input.value
        truth = self.truth_input.value

        if (
            text is not None
            and cat is not None
            and number is not None
            and truth is not None
        ):
            stmt = FuzzyStatement(text, cat, number, truth)
            self.statements.append(stmt)
            self.statement_box.add_item(stmt.to_string())
            self.update_selector_operands()

    def perform_operation(self):
        op = self.operation.value
        norm = str(self.norm.value).lower()
        left = self.left_operand.value
        right = self.right_operand.value

        if op == "Отрицание":
            if left is not None:
                stmt_tmp = [x.to_string() for x in self.statements]
                index = stmt_tmp.index(left)
                stmt_cls = self.statements[index]
                stmt_negative = stmt_cls.negative()

                self.statements.append(stmt_negative)
                self.statement_box.add_item(stmt_negative.to_string())
                self.result_box.add_item(stmt_negative.to_string())
                self.update_selector_operands()
        else:
            if op == "Конъюнкция":
                if left is not None and right is not None:
                    stmt_tmp = [x.to_string() for x in self.statements]
                    lf_index = stmt_tmp.index(left)
                    rg_index = stmt_tmp.index(right)
                    stmt_conj:FuzzyStatement = None
                    if norm == "алгебраическая сумма":
                        stmt_conj = self.statements[lf_index].conjunction(self.statements[rg_index],norm)
                    elif norm == "граничная сумма":
                        stmt_conj = self.statements[lf_index].conjunction(self.statements[rg_index],norm)
                    elif norm == "драстическая сумма":
                        stmt_conj = self.statements[lf_index].conjunction(self.statements[rg_index],norm)
                    elif norm == "минмакс":
                        stmt_conj = self.statements[lf_index].conjunction(self.statements[rg_index],norm)

                    self.statements.append(stmt_conj)
                    self.statement_box.add_item(stmt_conj.to_string())
                    self.result_box.add_item(stmt_conj.to_string())
                    self.update_selector_operands()


            elif op == "Дизъюнкция":
                if left is not None and right is not None:
                    stmt_tmp = [x.to_string() for x in self.statements]
                    lf_index = stmt_tmp.index(left)
                    rg_index = stmt_tmp.index(right)
                    stmt_disj:FuzzyStatement = None
                    if norm == "алгебраическая сумма":
                        stmt_disj = self.statements[lf_index].disjunction(self.statements[rg_index],norm)
                    elif norm == "граничная сумма":
                        stmt_disj = self.statements[lf_index].disjunction(self.statements[rg_index],norm)
                    elif norm == "драстическая сумма":
                        stmt_disj = self.statements[lf_index].disjunction(self.statements[rg_index],norm)
                    elif norm == "минмакс":
                        stmt_disj = self.statements[lf_index].disjunction(self.statements[rg_index],norm)

                    self.statements.append(stmt_disj)
                    self.statement_box.add_item(stmt_disj.to_string())
                    self.result_box.add_item(stmt_disj.to_string())
                    self.update_selector_operands()
            else:
                result = "Ошибка операции"

 # === НОВЫЙ ТАБ ===

    def add_fuzzy(self):
        name = self.fuzzy_name.value
        param = self.param_input.value
        truth = self.truth_input.value

        if not name or param is None or truth is None:
            ui.notify("Заполните все поля!", color="red")
            return

        # Проверяем, есть ли множество с таким именем
        existing = next((fs for fs in self.fuzzy_sets if fs.get_name() == name), None)
        if existing is None:
            existing = FuzzySet(name)
            self.fuzzy_sets.append(existing)
            ui.notify(f"Создано множество: {name}")

        if existing.add(param, truth):
            ui.notify(f"Добавлен параметр {param} со степенью {truth} в {name}")
        else:
            ui.notify("Такой параметр уже существует!", color="orange")

        self.update_fuzzy_list()

    def remove_param(self):
        name = self.fuzzy_name.value
        param = self.param_input.value
        if not name or param is None:
            ui.notify("Введите имя множества и параметр!", color="red")
            return

        existing = next((fs for fs in self.fuzzy_sets if fs.get_name() == name), None)
        if existing and existing.remove(param):
            ui.notify(f"Параметр {param} удалён из {name}")
        else:
            ui.notify("Не найдено!", color="orange")
        self.update_fuzzy_list()

    def clear_all_sets(self):
        self.fuzzy_sets.clear()
        self.fuzzy_box.clear()
        self.result_box.clear()
        self.left_set.set_options([])
        self.right_set.set_options([])
        ui.notify("Все множества очищены", color="red")

    def update_fuzzy_list(self):
        """Обновить список множеств и селекты"""
        self.fuzzy_box.clear()
        for fs in self.fuzzy_sets:
            items = ", ".join([f"{p}:{t}" for p, t in fs.to_dict().items()])
            self.fuzzy_box.add_item(f"{fs.get_name()} → {{{items}}}")

        names = [fs.get_name() for fs in self.fuzzy_sets]
        self.left_set.set_options(names)
        self.right_set.set_options(names)

    def perform_fuzzy_operation(self):
        op = self.operation.value
        norm = self.norm_type.value
        left_name = self.left_set.value
        right_name = self.right_set.value

        if not left_name:
            ui.notify("Выберите хотя бы одно множество!", color="red")
            return

        left = next((fs for fs in self.fuzzy_sets if fs.get_name() == left_name), None)
        right = next((fs for fs in self.fuzzy_sets if fs.get_name() == right_name), None)

        if op == "Отрицание":
            result = left.negate()
        elif op == "Конъюнкция":
            if not right:
                ui.notify("Выберите второе множество!", color="orange")
                return
            result = left.conjunction(right, norm.lower())
        elif op == "Дизъюнкция":
            if not right:
                ui.notify("Выберите второе множество!", color="orange")
                return
            result = left.disjunction(right, norm.lower())
        else:
            ui.notify("Неизвестная операция", color="red")
            return

        # Добавляем результат в список
        self.fuzzy_sets.append(result)
        ui.notify(f"Создано новое множество: {result.get_name()}")
        self.update_fuzzy_list()
        self.result_box.add_item(f"{result.get_name()} → {result.to_dict()}")
