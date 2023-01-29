# importing discord
import discord
from discord import app_commands
# importing .env 
from dotenv import load_dotenv
load_dotenv()
import os
# import required things for the ai
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy
import tflearn
import tensorflow
import random
import json
# end imports

# BOT SETUP
TOKEN = os.environ.get("TOKEN")
intents = discord.Intents.default()
intents.message_content = True

# SET UP THE AI
try:
    nltk.download('punkt')
except:
    pass

with open('intents.json') as file:
    data = json.load(file)

words = []
labels = []
docs_x = []
docs_y = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        wrds = nltk.word_tokenize(pattern)
        words.extend(wrds)
        docs_x.append(wrds)
        docs_y.append(intent["tag"])

    if intent["tag"] not in labels:
        labels.append(intent["tag"])

words = [stemmer.stem(w.lower()) for w in words if w != "?"]
words = sorted(list(set(words)))

labels = sorted(labels)

training = []
output = []

out_empty = [0 for _ in range(len(labels))]

for x, doc in enumerate(docs_x):
    bag = []

    wrds = [stemmer.stem(w.lower()) for w in doc]

    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)


training = numpy.array(training)
output = numpy.array(output)

tensorflow.compat.v1.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

model.fit(training, output, n_epoch=5500, batch_size=128, show_metric=True)
model.save("model.tflearn")

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return numpy.array(bag)

set_response = ""

def chat():
    inp = str(discord.Message.content)

    results = model.predict([bag_of_words(inp, words)])
    print('Results:', results)
    results_index = numpy.argmax(results)
    tag = labels[results_index]
    print('Tag:', tag)

    for tg in data["intents"]:
        if tg['tag'] == tag:
            responses = tg['responses']
    print('Responses:', responses)

    set_response = random.choice(responses)
    print('set_response:', set_response)
    return set_response



# RUN BOT
class myClient(discord.Client):
    async def on_ready(self):
        await tree.sync(guild=discord.Object(id=964294311715938308))
        print(f"Logged in as {self.user}.")

    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")
        if message.author == self.user:
            return
        response = chat()
        await message.channel.send(response)

client = myClient(intents=intents)
tree = app_commands.CommandTree(client)

# COMMANDS
@tree.command(name="ping", description="Pings the bot.", guild=discord.Object("964294311715938308"))
async def ping_command(interaction):
    await interaction.response.send_message("Pong!")

@tree.command(name="chat", description="Talk to the bot.", guild=discord.Object("964294311715938308"))
async def chat_command(interaction, message: str):
    await interaction.response.send_message("bruh")

# RUN WITH TOKEN
client.run(TOKEN)