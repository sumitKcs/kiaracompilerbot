from telegram.ext import Updater, CommandHandler
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import requests
import json as js
import os


TOKEN = '5172471011:AAH8BgyFKj7DHhrifhLAyX7Lo-UDUAJh164'

PORT = int(os.environ.get('PORT', '8443'))

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        """Hey! I am Kiara, a Code Compiler Bot.\n 
Supported languages: C, CPP, JAVA, Python
Commands:
/compile : without stdin(input)
/compilein : with stdin(input) 
/help : for help""")

def gethelp(update: Update, context: CallbackContext):
    update.message.reply_text("""Supported languages: C, CPP, JAVA, Python\n 
Commands:
/compile : to compile
and Send your code in this format:

YOUR_CODE

//@language

for example:

print("hello world!!!")

//@python

/compilein : to compile with stdin(input) 
and Send your code in this format:

YOUR_CODE

//@language

/*@
input1
input2
*/

for example:

a= input("Enter first value")
b=input("Enter second value")
c=a+b
print(c)

//@python

/*@
20
30
*/

/help : for help""")

def compilein(update: Update, context: CallbackContext):
    update.message.reply_text("""Send your code in this format:

YOUR_CODE

//@language

/*@
input1
input2
*/

for example:

a= input("Enter first value")
b=input("Enter second value")
c=a+b
print(c)

//@python

/*@
20
30
*/

""")

def compile(update: Update, context: CallbackContext):
    update.message.reply_text("""Send your code in this format:

YOUR_CODE

//@language

for example:

print("hello world!!!")

//@python

""")

def get_url(result):
    codeInput= ""
    lang = ""
    input=""
    indxa=''
    if("//@" in result):
        indxa = result.index("//@")
        lang = result[indxa:indxa+5]
        lang = lang.lower()
        if("py" in lang):
          lang = "py"
        elif("c" in lang):
          if("cp" not in lang or "c+" not in lang):
            lang = "c"
          else: lang = "cpp"
        elif("ja" in lang):
          lang = "java"
        elif("py" in lang):
          lang = "py"
    else: return """Enter lang by appneding //@Lang to the code
e.g.
//@java"""
      
    if("/*@" in result):
        indx = result.index("/*@")
        input = result[indx:]
        input = input.replace("/*@","")
        input = input.replace("*/","")
    if(indxa!=""):
      dummy = result[indxa:]
      codeInput = result.replace(dummy, "") 
    data= {
    'code' : codeInput,
    'language' : lang,
    'input' : input
    }
    headers= { 
    'Content-Type': 'application/json'
    }
    try:
        url = "https://codexweb.netlify.app/.netlify/functions/enforceCode"
        response = requests.request("POST", url, headers=headers, json=data)
        response = js.loads(response.text)
        output = response["output"]
        return output
    except Exception as e:
        print(e)

def result(update: Update, context: CallbackContext):
    data = get_url(update.message.text)
    if "//@Lang" not in data:
        update.message.reply_text("Compiled Result: 👇\n"+data)
    else: update.message.reply_text(data)

   #https://api.telegram.org/bot5254089086:AAG6O7913WDe_j7dm7jFUCW42PGXj6Gvmcc/getMe


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start',start))
    dp.add_handler(CommandHandler('help',gethelp))
    dp.add_handler(CommandHandler('compile',compile))
    dp.add_handler(CommandHandler('compilein',compilein))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, result))
    # updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN,
                          webhook_url="https://kiaraurlshortbot.herokuapp.com/"+TOKEN)

    updater.idle()

if __name__ == '__main__':
    main()
