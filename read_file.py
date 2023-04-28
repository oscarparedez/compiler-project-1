def read_input():
    input_text = ''
    with open('input.txt', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = '\n' + line
            line = line.replace(' ', 'ß')
            line = line.replace('\n', 'ß')
            line = line.replace('   ', '§')
            line = line.replace('*', 'Ж')
            line = line.replace('(', 'Л')
            line = line.replace(')', 'Ф')
            line = line.replace('.', 'Ц')
            input_text += line
    return input_text