import speech_recognition as sr # type: ignore
import pyttsx3
import wikipedia
import re
import datetime

# Initialize the speech engine
engine = pyttsx3.init)
recognizer = sr.Recognizer(;

def speak(text):
    """Speak the given text using TTS."""
    engine.say(text)
    engine.runAndWait()

def listen_for_query():
    """Listen for user's voice input and return it as text."""
    with sr.Microphone() as source:
        print("\n🎤 Listening for your speech...")
        audio = recognizer.listen(source)

        try:
            query = recognizer.recognize_google(audio)
            print(f"🗣 You said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            print("❌ Sorry, I could not understand your speech.")
            return None
        except sr.RequestError:
            print("⚠ Error with the speech recognition service.")
            return None

def calculate_expression(expression):
    """Calculate simple math expressions using eval."""
    try:
        expression = re.sub(r'[^\d\+\-\*/\.\(\)]', '', expression)
        result = eval(expression)
        return f"The answer is {result}"
    except Exception:
        return "Sorry, I couldn't calculate that."

def get_wikipedia_summary(query):
    """Get a summary from Wikipedia."""
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found: {e.options[:3]}"
    except wikipedia.exceptions.PageError:
        return f"I couldn't find anything on Wikipedia for '{query}'."
    except Exception as e:
        return f"An error occurred while searching: {e}"

def process_query(query):
    """Process the user's query and return a response."""
    if any(op in query for op in ['+', '-', '*', '/', 'plus', 'minus', 'times', 'divided']):
        query = query.replace("plus", "+").replace("minus", "-").replace("times", "*").replace("divided", "/")
        return calculate_expression(query)

    elif "who is" in query or "what is" in query:
        person = query.replace("who is", "").replace("what is", "").strip()
        return get_wikipedia_summary(person)

    elif "time" in query:
        now = datetime.datetime.now()
        return f"The time is {now.strftime('%I:%M %p')}"

    elif "hello" in query or "hi" in query:
        return "Hello! How can I assist you today?"

    elif "bye" in query or "exit" in query or "quit" in query:
        speak("Goodbye!")
        print("👋 Exiting assistant.")
        exit()

    else:
        return "Sorry, I didn't understand that. Please try again."

def log_interaction(question, response):
    """Log question and response to a file."""
    with open("log.txt", "a") as f:
        f.write(f"User: {question}\nAssistant: {response}\n\n")

def main():
    """Main function to handle the assistant workflow."""
    while True:
        question = listen_for_query()
        if question:
            response = process_query(question)
            print(f"🧠 Response: {response}")
            speak(response)
            log_interaction(question, response)

if _name_ == "_main_":
    main()
