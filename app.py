from flask import Flask, request, render_template, jsonify
#from langchain.llms import OpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
#from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
#from langchain.document_loaders import TextLoader
from langchain_community.document_loaders import DirectoryLoader
# Make embeddings, store in vector database, create retriever.
from langchain_openai import OpenAIEmbeddings
#from langchain_openai import ChatOpenAI
#import openai
import os


# Load documents from folders
os.system('unzip -o symptoms.zip')
os.system('unzip -o healthy_living.zip')
os.system('unzip -o disease_control.zip')
os.system('unzip -o mayoclinic.zip')
os.system('unzip -o amc_seoul.zip')
loader = DirectoryLoader('.', glob="*.txt", loader_cls=TextLoader)
documents = loader.load()

# Launch the app.
app = Flask(__name__)

# In-memory storage for chat history
chat_history = []

@app.route('/')
def index():
    return render_template('index.html', chat_history=chat_history)

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['message']
    bot_response = f'you entered {user_message}'
    
    # Store user message and bot response in chat history
    chat_history.append({'user': user_message, 'bot': bot_response})
    
    return jsonify({'user': user_message, 'bot': bot_response})

@app.route('/clear_history', methods=['POST'])
def clear_history():
    chat_history.clear()
    return jsonify({'status': 'Chat history cleared'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
