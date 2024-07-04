from flask import Flask, render_template, request

app = Flask(__name__)

def vigenere(message, key, direction=1, alphabet='abcdefghijklmnopqrstuvwxyz'):
    key_index = 0
    final_message = ''
    alphabet_length = len(alphabet)
    
    for char in message:
        if char.lower() not in alphabet:
            final_message += char
        else:
            key_char = key[key_index % len(key)].lower()
            key_index += 1

            offset = alphabet.index(key_char) 
            if char.islower():
                index = alphabet.index(char)
                new_index = (index + offset * direction) % alphabet_length
                final_message += alphabet[new_index]
            else:
                index = alphabet.index(char.lower())
                new_index = (index + offset * direction) % alphabet_length
                final_message += alphabet[new_index].upper()
    
    return final_message

def encrypt(message, key, alphabet='abcdefghijklmnopqrstuvwxyz'):
    return vigenere(message, key, 1, alphabet)
    
def decrypt(message, key, alphabet='abcdefghijklmnopqrstuvwxyz'):
    return vigenere(message, key, -1, alphabet)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    if request.method == 'POST':
        text = request.form['text']
        custom_key = request.form['key']
        operation = request.form['operation']
        
        if any(char.lower() not in 'abcdefghijklmnopqrstuvwxyz' for char in custom_key):
            result = "Invalid key. Please ensure all characters in the key are letters from the alphabet."
        else:
            if operation == 'encrypt':
                result = encrypt(text, custom_key)
            else:
                result = decrypt(text, custom_key)
    
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
