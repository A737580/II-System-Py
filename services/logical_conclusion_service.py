from models.facts import Facts
from models.rules import Rules
from typing import Set, List


class LogicalConclusionService:
    @staticmethod
    def straight_move(general_facts: Facts, general_rules: Rules) -> Set[str]:
        primary_facts = general_facts.get_all()
        rules_copy = general_rules.get_copy()
        is_complete_rule = True

        while is_complete_rule:
            is_complete_rule = False
            iteration_copy = rules_copy.get_all()
            
            for possible_fact in iteration_copy.keys():
                for rule in iteration_copy[possible_fact]:
                    is_feasible_rule = True
                    
                    for antecedent in rule:
                        if antecedent not in primary_facts:
                            is_feasible_rule = False
                            break
                    
                    if is_feasible_rule:
                        primary_facts.add(possible_fact)
                        rules_copy.delete_by_fact(possible_fact, rule)
                        is_complete_rule = True
        
        return set(primary_facts)

    @staticmethod
    def reverse_move(general_facts: Facts, general_rules: Rules, target: str) -> List[str]:
        """Обратный логический вывод с продолжением пока выводятся новые факты."""
        steps = []
        proven_facts = general_facts.get_all().copy()
        steps.append(f"🔍 Начинаем обратный вывод для факта: {target}")
        steps.append(f"Исходные факты: {', '.join(sorted(proven_facts))}")
        
        # Флаг для продолжения цикла
        new_fact_derived = True
        iteration = 1
        
        while new_fact_derived:
            new_fact_derived = False
            steps.append(f"\n🔄 Итерация {iteration}:")
            iteration += 1
            
            # Собираем все цели для проверки на этой итерации
            # Это все факты, которые могут быть выведены из текущих правил
            all_potential_goals = set()
            rules_dict = general_rules.get_all()
            
            # Добавляем все следствия из правил как потенциальные цели
            for consequent in rules_dict.keys():
                if consequent not in proven_facts:
                    all_potential_goals.add(consequent)
            
            # Также добавляем антецеденты из всех правил
            for antecedents_set in rules_dict.values():
                for antecedents in antecedents_set:
                    for antecedent in antecedents:
                        if antecedent not in proven_facts:
                            all_potential_goals.add(antecedent)
            
            # Добавляем исходную цель если она еще не доказана
            if target not in proven_facts:
                all_potential_goals.add(target)
            
            goals_to_check = list(all_potential_goals)
            steps.append(f"Цели для проверки: {', '.join(sorted(goals_to_check))}")
            
            # Проверяем все цели на этой итерации
            for current_goal in goals_to_check:
                if current_goal in proven_facts:
                    continue
                    
                steps.append(f"  📌 Проверяем: {current_goal}")
                
                if current_goal in rules_dict:
                    for i, antecedents in enumerate(rules_dict[current_goal], 1):
                        steps.append(f"    Правило {i}: {antecedents} → {current_goal}")
                        
                        # Проверяем все ли антецеденты доказаны
                        all_proven = True
                        for antecedent in antecedents:
                            if antecedent not in proven_facts:
                                all_proven = False
                                steps.append(f"      ❌ Не доказан: {antecedent}")
                                break
                        
                        if all_proven:
                            proven_facts.add(current_goal)
                            new_fact_derived = True
                            steps.append(f"    ✅ Правило применено! Новый факт: {current_goal}")
                            break
                        else:
                            steps.append(f"    ❌ Правило не применимо")
                else:
                    steps.append(f"    ❌ Нет правил для вывода {current_goal}")
            
            steps.append(f"Факты после итерации: {', '.join(sorted(proven_facts))}")
            
            # Защита от бесконечного цикла
            if iteration > 100:
                steps.append("⚠️  Прервано: превышено максимальное число итераций")
                break
        
        # Финальный результат
        steps.append("\n" + "="*50)
        if target in proven_facts:
            steps.append(f"🎯 ЦЕЛЬ ДОСТИГНУТА! Факт '{target}' ВЫВОДИМ")
        else:
            steps.append(f"💥 ЦЕЛЬ НЕ ДОСТИГНУТА! Факт '{target}' НЕ ВЫВОДИМ")
        
        steps.append(f"📈 Всего доказано фактов: {len(proven_facts)}")
        steps.append(f"📋 Доказанные факты: {', '.join(sorted(proven_facts))}")
        
        return steps

