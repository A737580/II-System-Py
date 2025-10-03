from nicegui import ui
from typing import List

from ui.components.list_box import ListBox
from models.exercise2.fuzzy_statement import FuzzyStatement


class Page2:
    def __init__(self):
        self.statements: List[FuzzyStatement] = []
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
        """Второе поле - пока пустое, можно добавить заглушку"""
        with ui.row().classes("w-full justify-center"):
            with ui.column().classes(
                "border-2 border-green-200 w-[900px] mx-auto h-full px-6 pb-6 gap-10 bg-gray-50"
            ):
                ui.label("Задание 2.2").classes("text-h4 text-center")
                ui.label("Это поле пока пустое").classes("text-lg text-center text-gray-500")
                
                # Можно добавить заглушку или базовые элементы
                with ui.column().classes("items-center gap-4 mt-8"):
                    ui.icon("construction", size="xl").classes("text-gray-400")
                    ui.label("Интерфейс для задания 2.2 будет добавлен позже")
                    
                    # Пример будущих элементов
                    with ui.card().classes("w-80 mt-4"):
                        ui.label("Будущие элементы:").classes("font-bold")
                        ui.label("• Настройки нечеткой логики")
                        ui.label("• Графики функций принадлежности")
                        ui.label("• Таблицы истинности")

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
        stmt_tmp = [x.ToString() for x in self.statements]
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
            self.statement_box.add_item(stmt.ToString())
            self.update_selector_operands()

    def perform_operation(self):
        op = self.operation.value
        norm = str(self.norm.value).lower()
        left = self.left_operand.value
        right = self.right_operand.value

        if op == "Отрицание":
            if left is not None:
                stmt_tmp = [x.ToString() for x in self.statements]
                index = stmt_tmp.index(left)
                stmt_cls = self.statements[index]
                stmt_negative = stmt_cls.Negative()

                self.statements.append(stmt_negative)
                self.statement_box.add_item(stmt_negative.ToString())
                self.result_box.add_item(stmt_negative.ToString())
                self.update_selector_operands()
        else:
            if op == "Конъюнкция":
                if left is not None and right is not None:
                    stmt_tmp = [x.ToString() for x in self.statements]
                    lf_index = stmt_tmp.index(left)
                    rg_index = stmt_tmp.index(right)
                    stmt_conj:FuzzyStatement = None
                    if norm == "алгебраическая сумма":
                        stmt_conj = FuzzyStatement.Conjunction(self.statements[lf_index],self.statements[rg_index],norm)
                    elif norm == "граничная сумма":
                        stmt_conj = FuzzyStatement.Conjunction(self.statements[lf_index],self.statements[rg_index],norm)
                    elif norm == "драстическая сумма":
                        stmt_conj = FuzzyStatement.Conjunction(self.statements[lf_index],self.statements[rg_index],norm)
                    elif norm == "минмакс":
                        stmt_conj = FuzzyStatement.Conjunction(self.statements[lf_index],self.statements[rg_index],norm)

                    self.statements.append(stmt_conj)
                    self.statement_box.add_item(stmt_conj.ToString())
                    self.result_box.add_item(stmt_conj.ToString())
                    self.update_selector_operands()


            elif op == "Дизъюнкция":
                if left is not None and right is not None:
                    stmt_tmp = [x.ToString() for x in self.statements]
                    lf_index = stmt_tmp.index(left)
                    rg_index = stmt_tmp.index(right)
                    stmt_disj:FuzzyStatement = None
                    if norm == "алгебраическая сумма":
                        stmt_disj = FuzzyStatement.Disjunction(self.statements[lf_index],self.statements[rg_index],norm)
                    elif norm == "граничная сумма":
                        stmt_disj = FuzzyStatement.Disjunction(self.statements[lf_index],self.statements[rg_index],norm)
                    elif norm == "драстическая сумма":
                        stmt_disj = FuzzyStatement.Disjunction(self.statements[lf_index],self.statements[rg_index],norm)
                    elif norm == "минмакс":
                        stmt_disj = FuzzyStatement.Disjunction(self.statements[lf_index],self.statements[rg_index],norm)

                    self.statements.append(stmt_disj)
                    self.statement_box.add_item(stmt_disj.ToString())
                    self.result_box.add_item(stmt_disj.ToString())
                    self.update_selector_operands()
            else:
                result = "Ошибка операции"

