import json

import click
from PyInquirer import prompt


@click.group()
def cli():
    pass


def get_todos_from_file():
    with open('todos.json', 'r') as todos_file:
        try:
            result = json.load(todos_file)
        except:
            result = []
        return result


def write_todo_to_file(todos):
    with open('todos.json', 'w') as todos_file:
        json.dump(todos, todos_file)


def transform_todo_to_question_checkbox(todos):
    result = []
    for each in todos:
        result.append({
            'name': each['task'],
            'checked': each['is_done']
        })

    return result


def clear_todos_state(todos):
    result = []
    for each in todos:
        result.append({
            'task': each['task'],
            'due_date': each['due_date'],
            'is_done': False
        })
    return result


def update_todos_with_done_list(done_list):
    todos = get_todos_from_file()
    todos = clear_todos_state(todos)
    for each in done_list:
        for item in todos:
            if item['task'] == each:
                item['is_done'] = True
                print('update', each)
    return todos


@cli.command()
def list():
    todos = get_todos_from_file()

    if len(todos) == 0:
        print('no todo')
    else:
        question_choices = {
            'type': 'checkbox',
            'name': 'done_list',
            'message': 'Todo List',
            'choices': transform_todo_to_question_checkbox(todos)
        }
        print('These are all your to do for today')

        answers = prompt(question_choices)
        updated_todos = update_todos_with_done_list(answers['done_list'])
        write_todo_to_file(updated_todos)

        for each in updated_todos:
            if each['is_done']:
                print(f'✅ {each["task"]}. It will be due at {each["due_date"]}')
            else:
                print(f'⭕️ {each["task"]}. It will be due at {each["due_date"]}')

        print('You\'ve updated todo list!')


@cli.command()
def add():
    questions = [
        {
            'type': 'input',
            'name': 'task',
            'message': 'What is my task?",
        },
        {
            'type': 'input',
            'name': 'due_date',
            'message': 'When it should be done?',
        }
    ]

    answers = prompt(questions)
    answers['is_done'] = False

    todos = get_todos_from_file()
    todos.append(answers)
    write_todo_to_file(todos)

    print(f'🔮 You added {answers["task"]} and it need to be done {answers["due_date"]}')


if __name__ == '__main__':
    cli()
