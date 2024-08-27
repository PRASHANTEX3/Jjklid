
import telebot
import nltk
from nltk.chat.util import Chat, reflections

# Download NLTK resources if needed
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)

# Replace with your actual Telegram Bot Token
TOKEN = "7431071779:AAGQ1fUfee2lRpW5M548JCUsehu08Cp53i4"

bot = telebot.TeleBot(TOKEN)

# Initial pairs for the chatbot
pairs = [
    [
        r"my name is (.*)",
        ["Hello %1, how can I help you today?",]
    ],
    [
        r"what is your name ?",
        ["My name is EXTREME, and I'm here to assist you.",]
    ],
    [
        r"how are you ?",
        ["I am doing well, thanks for asking!", "I'm EXTREME, your chatbot, and I'm here to help!", "I'm functioning smoothly!"]
    ],
    [
        r"quit",
        ["Bye! Take care.", "It was nice talking to you.", "Goodbye!"]
    ],
]

# Create a chat object
chat = Chat(pairs, reflections)

# Keep track of the learning state and storage for programming code and math
learning_state = {}
programming_code_storage = {}
math_storage = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I'm EXTREME, your advanced learning Telegram Chatbot. Ask me anything!")

@bot.message_handler(commands=['learn'])
def start_learning(message):
    learning_state[message.chat.id] = {'expect_input': True}
    bot.reply_to(message, "How about I learn something new? Please tell me a phrase.")

@bot.message_handler(func=lambda message: learning_state.get(message.chat.id, {}).get('expect_input'))
def learn_new_phrase(message):
    learning_state[message.chat.id]['new_phrase'] = message.text
    learning_state[message.chat.id]['expect_input'] = False
    learning_state[message.chat.id]['expect_response'] = True
    bot.reply_to(message, "Got it! Now, please explain in brief what my response should be.")

@bot.message_handler(func=lambda message: learning_state.get(message.chat.id, {}).get('expect_response'))
def learn_new_response(message):
    new_phrase = learning_state[message.chat.id]['new_phrase']
    new_response = message.text

    # Add the new pair to the chatbot's knowledge
    pairs.append([new_phrase, [new_response]])
    chat._pairs = pairs

    # Reset learning state
    del learning_state[message.chat.id]

    bot.reply_to(message, "Learned! I will remember this.")

@bot.message_handler(commands=['learncode'])
def start_learn_code(message):
    learning_state[message.chat.id] = {'expect_code': True}
    bot.reply_to(message, "Please provide the programming code snippet you want me to learn.")

@bot.message_handler(func=lambda message: learning_state.get(message.chat.id, {}).get('expect_code'))
def learn_code(message):
    code_snippet = message.text
    learning_state[message.chat.id]['code_snippet'] = code_snippet
    learning_state[message.chat.id]['expect_code'] = False
    learning_state[message.chat.id]['expect_description'] = True
    bot.reply_to(message, "Got it! Now, please provide a brief description of what this code does.")

@bot.message_handler(func=lambda message: learning_state.get(message.chat.id, {}).get('expect_description'))
def learn_code_description(message):
    description = message.text
    code_snippet = learning_state[message.chat.id]['code_snippet']

    # Store the code and description
    programming_code_storage[description] = code_snippet

    # Reset learning state if it exists
    if message.chat.id in learning_state:
        del learning_state[message.chat.id]

    bot.reply_to(message, "Learned! I will remember this code snippet.")

@bot.message_handler(commands=['learnmath'])
def start_learn_math(message):
    learning_state[message.chat.id] = {'expect_math_question': True}
    bot.reply_to(message, "Please provide a math question (e.g., 'What is 2 + 2?') that you want me to learn.")

@bot.message_handler(func=lambda message: learning_state.get(message.chat.id, {}).get('expect_math_question'))
def learn_math_question(message):
    math_question = message.text
    learning_state[message.chat.id]['math_question'] = math_question
    learning_state[message.chat.id]['expect_math_question'] = False
    learning_state[message.chat.id]['expect_math_answer'] = True
    bot.reply_to(message, "Got it! Now, please provide the answer to this math question.")

@bot.message_handler(func=lambda message: learning_state.get(message.chat.id, {}).get('expect_math_answer'))
def learn_math_answer(message):
    math_answer = message.text
    math_question = learning_state[message.chat.id]['math_question']

    # Store the math question and answer
    math_storage[math_question] = math_answer

    # Reset learning state
    del learning_state[message.chat.id]

    bot.reply_to(message, "Learned! I will remember this math question and answer.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_message = message.text.lower()

    # Check for programming code requests
    for description, code in programming_code_storage.items():
        if description.lower() in user_message:
            bot.send_message(message.chat.id, code)
            return

    # Check for math question requests
    if user_message in math_storage:
        bot.send_message(message.chat.id, math_storage[user_message])
    else:
        # Use the chat object to generate a response
        response = chat.respond(user_message)
        if response:
            bot.reply_to(message, response)
        else:
            bot.reply_to(message, "I don't understand. You can teach me using the /learn command.")

# Start polling
bot.infinity_polling()     bot.reply_to(message, response)
        else:
            bot.reply_to(message, "I don't understand. You can teach me using the /learn command.")

bot.polling()ponse:
            bot.reply_to(message, response)
        else:
            bot.reply_to(message, "I don't understand. You can teach me using the /learn command.")

bot.polling()