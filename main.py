import flet as ft
from db import main_db

def main(page: ft.Page):
    page.title = 'Buy List'
    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column(spacing=10)

    filter_type = 'all'


    def load_tasks():
        task_list.controls.clear()
        for task_id, task_text, completed in main_db.get_task(filter_type):
            task_list.controls.append(create_task_row(task_id=task_id, task_text=task_text, completed = completed))
        page.update()

    def create_task_row(task_id, task_text, completed):
        task_field = ft.TextField(value=task_text, expand=True, read_only=True)

        checkbox_task  = ft.Checkbox(value=bool(completed), on_change=lambda e: toggle_task(task_id, e.control.value))

        row_task = ft.Row()
        

        def enable_edit(_):
            task_field.read_only = False
            task_field.update()

        edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=enable_edit)

        def save_task(_):
            main_db.update_task(task_id=task_id, new_task=task_field.value)
            task_field.read_only = True
            task_field.update()
            page.update()

        save_button = ft.IconButton(icon=ft.Icons.SAVE, on_click=save_task)

        def delete_task(_):
            main_db.delete_task(task_id=task_id)
            task_list.controls.remove(row_task)
            task_field.update()
            page.update()

        delete_button = ft.IconButton(ft.Icons.DELETE, ft.Colors.RED, on_click=delete_task)

        row_task.controls = [checkbox_task, task_field, edit_button, save_button, delete_button]
        return row_task
    
    def toggle_task(task_id, is_completed):
        main_db.update_task(task_id=task_id, completed=int(is_completed))
        load_tasks()
    
    def add_task(_):
        if task_input.value:
            task = task_input.value
            task_id = main_db.add_task(task)
            task_list.controls.append(create_task_row(task_id=task_id, task_text=task, completed=None))
            task_input.value = None
            page.update()

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_tasks()

    filter_button = ft.Row([
        ft.ElevatedButton('all tasks', icon=ft.Icons.ALL_INBOX, on_click=lambda e:set_filter('all')),
        ft.ElevatedButton('dont buyed', icon=ft.Icons.STOP_OUTLINED, on_click=lambda e:set_filter('uncompleted'), color=ft.Colors.ORANGE_700),
        ft.ElevatedButton('buyed', icon=ft.Icons.CHECK_BOX, on_click= lambda e: set_filter('completed'), color=ft.Colors.GREEN_700)
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    task_input = ft.TextField(label='text the task', expand=True, on_submit=add_task)
    task_button = ft.IconButton(ft.Icons.SEND, on_click=add_task)


    







    page.add(ft.Row([task_input, task_button]), task_list, filter_button)
    load_tasks()
if __name__ == '__main__':
    main_db.init_db()
    ft.app(target=main) 