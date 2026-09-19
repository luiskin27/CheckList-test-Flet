import json
import os
import flet as ft

data_file = "expenses.json"

def load_expenses():
    if os.path.exists(data_file):
        with open(data_file, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_expenses(expenses):
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(expenses, f, ensure_ascii=False, indent=4)


def main(page: ft.Page):
    page.title = "Expense Tracker"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    expenses = load_expenses()

    # Поля ввода
    amount_input = ft.TextField(
        label="Amount", 
        keyboard_type=ft.KeyboardType.NUMBER,
        width=180
    )
    
    category_dropdown = ft.Dropdown(
        label="Category",
        options=[
            ft.dropdown.Option("Food"),
            ft.dropdown.Option("Transport"),
            ft.dropdown.Option("Entertainment"),
            ft.dropdown.Option("Utilities"),
            ft.dropdown.Option("Other")
        ],
        width=180
    )

    error_text = ft.Text("", color="red")
    total_text = ft.Text("Total Expenses: 0.00 som", size=20, weight=ft.FontWeight.BOLD)
    expense_list = ft.ListView(expand=True, spacing=10)

    def update_ui():
        expense_list.controls.clear()
        total_sum = 0.0

        for expense in expenses:
            total_sum += expense["amount"]
            expense_list.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.ListTile(
                            leading=ft.Icon(ft.Icons.SHOPPING_BAG),
                            title=ft.Text(f"{expense['category']}"),
                            subtitle=ft.Text(f"{expense['amount']:.2f} som"),
                        ),
                        padding=10,
                    )
                )
            )
        
        total_text.value = f"Total Expenses: {total_sum:.2f} som"
        page.update()

    def add_expense_click(e):
        if not amount_input.value or not category_dropdown.value:
            error_text.value = "Please fill in all fields."
            page.update()
            return

        try:
            amount = float(amount_input.value)
            if amount <= 0:
                error_text.value = "Amount must be greater than zero."
                page.update()
                return
        except ValueError:
            error_text.value = "Invalid amount. Please enter a number."
            page.update()
            return

        error_text.value = ""

        # Добавляем новую запись
        new_expense = {
            "amount": amount,
            "category": category_dropdown.value
        }
        expenses.append(new_expense)
        
        # Сохраняем в JSON
        save_expenses(expenses)

        # Очищаем поля ввода
        amount_input.value = ""
        category_dropdown.value = None

        # Обновляем список на экране
        update_ui()

    add_btn = ft.Button("Save", on_click=add_expense_click)

    # Отрисовка основного интерфейса
    page.add(
        ft.Text("New Expense!", size=20, weight=ft.FontWeight.BOLD),
        ft.Row([amount_input, category_dropdown], alignment=ft.MainAxisAlignment.CENTER),
        error_text,
        ft.Row([add_btn], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(),
        total_text,
        expense_list
    )

    # Первоначальный вывод сохраненных данных
    update_ui()
    
ft.run(main, view=ft.AppView.WEB_BROWSER, host="127.0.0.1", port=8550)