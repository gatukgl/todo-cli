from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json


questions = [
    {
        'type': 'input',
        'name': 'task',
        'message': f"What's your task?",
    },
    {
        'type': 'input',
        'name': 'due_date',
        'message': 'When it need to be done?',
    }
]

answers = prompt(questions)
print('🔮 Your task today is: ', answers['task'])
