# FINANCIAL_GIGA_BOT

rep: https://github.com/Yadrick/financial_bot
project: https://github.com/users/Yadrick/projects/2

## О Телеграм-боте

Этот Телеграм-бот создан для учета финансовых транзакций (доходы/расходы)

Бот создавался в команде из 3-х человек.
Работа в команде происходила по методике Kanban, проводились ревью кода.

Общение с Телеграм API реализовано напрямую без сторонних библиотек.
Разработана машина состояний клиента. Применялись SOLID принципы.

### Возможности:
- Учет доходов и расходов
- Просмотр категорий доходов/расходов
- Удаление категорий доходов/расходов
- Отображение данных за текущий день
- Отображение данных за текущий месяц

### Компонентное взаимодействие / Архитектура
![Component Communication](assets/component_communication.png)

### Машина состояний сервиса записи доходов или расходов
![State Machine](assets/state_machine.png)

### Примеры работы бота

Пример записи расхода:

![Example Expense Record](assets/expense_record_example.png)

Пример некорректного ввода:

![Example Of Incorrect Input](assets/example_of_incorrect_input.png)

Пример удаления записи:

![Example Of Record Deletion](assets/example_of_record_deletion.png)


