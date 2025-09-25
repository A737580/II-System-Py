from nicegui import ui
from ui.components.list_box import ListBox
from services.logical_conclusion_service import LogicalConclusionService
from models.facts import Facts
from models.rules import Rules

class Page1:
    def __init__(self):
        self.selected_logic = "Прямой логический вывод"
        self.facts = Facts()
        self.rules = Rules()
        with ui.column().classes("border-2 border-blue-200"):
            with ui.column().classes("w-full h-full px-6 pb-6 gap-10 bg-gray-50"):   

                # ======= Первая строка =======
                with ui.row().classes("w-full gap-16 items-start"):

                    # ---- Левая колонка: Факты ----
                    with ui.column().classes("gap-3"):
                        ui.label("Факты").classes("text-xl font-bold")

                        with ui.row().classes("items-start gap-6"):
                            # ListBox вместо TextArea
                            with ui.column().classes("gap-2 w-300"):
                                ui.label("Список фактов").classes("text-sm")
                                self.facts_box = ListBox(height="192px")

                            # Панель управления
                            with ui.column().classes("gap-2"):
                                ui.button("Удалить", on_click=self.remove_fact)
                                ui.button("Добавить", on_click=self.add_fact)
                                self.fact_input = ui.input("Введите факт").classes("w-40")

                    # ---- Правая колонка: Логический вывод ----
                    with ui.column().classes("gap-4 w-1/3"):
                        ui.label("Логический вывод").classes("text-xl font-bold")

                        self.radio_logic = ui.radio(
                            ["Прямой логический вывод", "Обратный логический вывод"],
                            value="Прямой логический вывод",
                        ).bind_value(self, "selected_logic")

                        with ui.row():
                            ui.button("Поиск", on_click=self.search_logic).classes("mt-2")
                            self.search_fact = ui.input("Поиск факта").classes("w-32")

                        self.answers_box = ui.textarea(
                            label="Ответы", placeholder="Результаты"
                        ).classes("w-96 h-48")

                # ======= Вторая строка =======
                with ui.row().classes("w-full gap-16  items-start"):

                    # ---- Левая колонка: Правила ----
                    with ui.column().classes("gap-3 w-full"):   
                        ui.label("Правила").classes("text-lg font-bold")

                        with ui.row().classes("items-start gap-6 w-full"):  
                            # ListBox вместо TextArea
                            with ui.column().classes("gap-2 w-1/2"):
                                ui.label("Список правил").classes("text-sm")
                                self.rules_box = ListBox(height="192px")

                            # Панель управления
                            with ui.column().classes("gap-2"):
                                ui.button("Удалить", on_click=self.remove_rule)
                                ui.button("Добавить", on_click=self.add_rule)
                                with ui.row().classes("items-center gap-2"):
                                    self.antec_input = ui.input("Антецеденты").classes("w-32")
                                    ui.label("-->")
                                    self.conseq_input = ui.input("Консеквент").classes("w-32")

                            # Кнопка в нижнем правом углу
                            with ui.column().classes("ml-auto"):
                                ui.button("Очистить все поля", on_click=self.clear_all, color="red")

    # ======= Логика кнопок =======
    def add_fact(self):
        if self.fact_input.value:
            fact = str(self.fact_input.value).strip().upper()[0]
            if(self.facts.add(fact)):
                self.facts_box.add_item(fact)
                self.fact_input.value = ""

    def remove_fact(self):
        if self.fact_input.value and self.facts.delete(self.fact_input.value):
            self.facts_box.remove_item(self.fact_input.value)
            self.fact_input.value = ""
        else:
            if self.facts_box.get_selected_index() != -1 and self.facts.delete(self.facts_box.get_selected_item()):
                self.facts_box.remove_selected()


    def add_rule(self):
        if self.conseq_input.value and self.antec_input.value:
            antecedents_str = self.antec_input.value.replace(" ", "").upper()
            consequent_str = self.conseq_input.value.replace(" ", "").upper()
            
            or_parts = [part for part in antecedents_str.split('|') if part]
            rules_list = []
            
            for part in or_parts:
                if not part:
                    continue
                and_parts = [p for p in part.split('&') if p]
                sorted_antecedents = ''.join(sorted(and_parts))
                rules_list.append(sorted_antecedents)
            
            consequent = consequent_str[0]   
            
            for antecedents in rules_list:
                if self.rules.add(consequent, antecedents):
                    rule_display = antecedents + "-->" + consequent
                    self.rules_box.add_item(rule_display)
                    self.conseq_input.value = ""
                    self.antec_input.value = ""

    def remove_rule(self):
        if self.conseq_input.value and self.antec_input.value and self.rules.delete_by_fact(self.conseq_input.value,self.antec_input.value):
            rule = f"{self.antec_input.value}-->{self.conseq_input.value}"
            self.rules_box.remove_item(rule)
            self.conseq_input.value = ""
            self.antec_input.value = ""
        else:
            if self.rules_box.get_selected_index() != -1:
                selected_item = self.rules_box.get_selected_item()
                items = selected_item.split("-->")
                if len(items) == 2:
                    antecedents = items[0].replace('&', '')
                    consequent = items[1][0] 
                    if self.rules.delete_by_fact(consequent, antecedents):
                        self.rules_box.remove_selected()

    def search_logic(self):
        if self.selected_logic == "Прямой логический вывод":
            
            result = LogicalConclusionService.straight_move(self.facts, self.rules)

            result_text = "\n".join(
            f"Элемент {i+1}: {', '.join(sorted(step))}" 
            for i, step in enumerate(result)
            )
            r = ""
            for i in result:
                r += f"{i} "

            self.answers_box.value = (
                f"Режим: {self.radio_logic.value}\n"
                f"Факты: {len(self.facts.get_all())} шт.\n"
                f"Правила: {sum(len(rules_set) for rules_set in self.rules.get_all().values())} шт.\n"
                f"Результат поиска:\n{result_text}\n"
                +r
            )
        else:
            target_fact = str(self.search_fact.value).strip().upper()[0]
            if not target_fact is None and target_fact != "":
                steps = LogicalConclusionService.reverse_move(self.facts, self.rules, target_fact)
                
                result_text = "\n".join(steps)

                self.answers_box.value = (
                    f"🔍 ОБРАТНЫЙ ЛОГИЧЕСКИЙ ВЫВОД\n"
                    f"Целевой факт: {target_fact}\n"
                    f"Исходные факты: {len(self.facts.get_all())} шт.\n"
                    f"Правила: {sum(len(rules_set) for rules_set in self.rules.get_all().values())} шт.\n\n"
                    f"Ход вывода:\n{result_text}"
                )
    def clear_all(self):
        self.facts_box.clear()
        self.rules_box.clear()
        self.answers_box.value = ""