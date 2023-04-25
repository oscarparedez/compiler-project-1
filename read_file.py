def read_input():
    input_text = ''
    with open('input.txt', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            input_text += line
    return input_text