import speech_recognition as sr 
import pyttsx3 # Text to Speech librarie
import datetime
import wikipedia # Wikipedia Integration
import webbrowser # To open Urls
import os 
import time
import ctypes
import json

class VoiceActivatedChatbot:
    def __init__(self):
        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.setup_voice()
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        
        # Configuration
        self.recognizer.pause_threshold = 1
        self.recognizer.energy_threshold = 300
        
        # User data
        self.notes_file = "notes.json"
        self.load_notes()
        
    def setup_voice(self):
        """Configure the text-to-speech engine"""
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)  # Female voice
        self.engine.setProperty('rate', 180)  # Speech rate
        self.engine.setProperty('volume', 2)  # Volume level
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"Assistant: {text}")
        self.engine.say(text)
        self.engine.runAndWait()
    
    def wish_me(self):
        """Greet user based on time of day"""
        hour = int(datetime.datetime.now().hour)
        
        if hour >= 0 and hour < 12:
            greeting = "Good Morning!"
        elif hour >= 12 and hour < 18:
            greeting = "Good Afternoon!"
        else:
            greeting = "Good Evening!"
        
        self.speak(f"{greeting} I am your voice assistant. How can I help you today?")
    
    def take_command(self):
        """Listen for voice input and convert to text"""
        try:
            with self.microphone as source:
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            print("Recognizing...")
            query = self.recognizer.recognize_google(audio, language='en-in')
            print(f"User: {query}")
            return query.lower()
            
        # except sr.WaitTimeoutError:
        #     self.speak("I didn't hear anything. Please try again.")
        #     return "none"
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't understand that. Could you please repeat?")
            return "none"
        except sr.RequestError as e:
            self.speak("Sorry, there was an error with the speech recognition service.")
            return "none"
        except Exception as e:
            print(f"Error: {e}")
            return "none"
    
    def get_time(self):
        """Get current time"""
        str_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.speak(f"The time is {str_time}")
    
    def get_date(self):
        """Get current date"""
        today = datetime.datetime.now()
        date_str = today.strftime("%B %d, %Y")
        day_str = today.strftime("%A")
        self.speak(f"Today is {day_str}, {date_str}")
    
    def search_wikipedia(self, query):
        """Search Wikipedia and speak summary"""
        try:
            self.speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "").strip()
            results = wikipedia.summary(query, sentences=2)
            self.speak("According to Wikipedia")
            self.speak(results)
        except wikipedia.exceptions.DisambiguationError as e:
            self.speak(f"Multiple results found. Being more specific about {e.options[0]}")
            try:
                results = wikipedia.summary(e.options[0], sentences=2)
                self.speak(results)
            except:
                self.speak("Sorry, I couldn't find specific information.")
        except wikipedia.exceptions.PageError:
            self.speak("Sorry, I couldn't find any information on that topic.")
        except Exception as e:
            self.speak("Sorry, there was an error searching Wikipedia.")
    
    def open_website(self, site_name):
        """Open various websites"""
        websites = {
            'google': 'https://www.google.com',
            'youtube': 'https://www.youtube.com',
            'facebook': 'https://www.facebook.com',
            'twitter': 'https://www.twitter.com',
            'instagram': 'https://www.instagram.com',
            'linkedin': 'https://www.linkedin.com',
            'github': 'https://www.github.com',
            'stackoverflow': 'https://stackoverflow.com'
        }
        
        for site, url in websites.items():
            if site in site_name:
                self.speak(f"Opening {site}")
                webbrowser.open(url)
                return True
        return False
    
    def system_shutdown(self):
        """Shutdown the computer"""
        self.speak("Shutting down the computer in 10 seconds. Say cancel to abort.")
        time.sleep(5)
        # os.system("shutdown /s /t 10")  
        self.speak("Shutdown cancelled for safety. Uncomment the code to enable.")
    
    def system_restart(self):
        """Restart the computer"""
        self.speak("Restarting the computer in 10 seconds. Say cancel to abort.")
        time.sleep(5)
        # os.system("shutdown /r /t 10")  
        self.speak("Restart cancelled for safety. Uncomment the code to enable.")
    
    def lock_computer(self):
        """Lock the computer"""
        self.speak("Locking the computer")
        #ctypes.windll.user32.LockWorkStation()
        
    def load_notes(self):
        """Load notes from file"""
        try:
            if os.path.exists(self.notes_file):
                with open(self.notes_file, 'r') as f:
                    self.notes = json.load(f)
            else:
                self.notes = []
        except:
            self.notes = []
    
    def save_notes(self):
        """Save notes to file"""
        try:
            with open(self.notes_file, 'w') as f:
                json.dump(self.notes, f, indent=2)
        except Exception as e:
            print(f"Error saving notes: {e}")
    
    def add_note(self, note_text):
        """Add a note"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        note = {
            "text": note_text,
            "timestamp": timestamp
        }
        self.notes.append(note)
        self.save_notes()
        self.speak("Note added successfully")
    
    def read_notes(self):
        """Read all notes"""
        if not self.notes:
            self.speak("You have no notes")
            return
        
        self.speak(f"You have {len(self.notes)} notes:")
        for i, note in enumerate(self.notes, 1):
            self.speak(f"Note {i}: {note['text']}")
    
    def clear_notes(self):
        """Clear all notes"""
        self.notes = []
        self.save_notes()
        self.speak("All notes cleared")
    
    def tell_joke(self):
        """Tell a random joke"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a fake noodle? An impasta!",
            "Why did the math book look so sad? Because it had too many problems!"
        ]
        import random
        joke = random.choice(jokes)
        self.speak(joke)
    
    def process_command(self, query):
        """Process voice commands"""
        query = query.lower()
        
        # Greetings
        if any(word in query for word in ['hello', 'hi', 'hey']):
            self.speak("Hello! How can I help you?")
        
        # Time and date
        elif 'time' in query:
            self.get_time()
        
        elif 'date' in query:
            self.get_date()
        
        # Wikipedia search
        elif 'wikipedia' in query:
            self.search_wikipedia(query)
        
        # Open websites
        elif 'open' in query:
            if self.open_website(query):
                pass  # Website opened successfully
            else:
                self.speak("Sorry, I don't know how to open that website")
        
        # Notes functionality
        elif 'take note' in query or 'add note' in query:
            self.speak("What would you like me to note down?")
            note_text = self.take_command()
            if note_text != "none":
                self.add_note(note_text)
        
        elif 'read notes' in query or 'show notes' in query:
            self.read_notes()
        
        elif 'clear notes' in query:
            self.clear_notes()
        
        # System commands
        # elif 'shutdown' in query:
        #     self.system_shutdown()
        
        # elif 'restart' in query:
        #     self.system_restart()
        
        # elif 'lock' in query:
        #     self.lock_computer()
        
        # Entertainment
        elif 'joke' in query:
            self.tell_joke()
        
        # Search Google
        elif 'search' in query:
            search_term = query.replace('search', '').strip()
            if search_term:
                self.speak(f"Searching for {search_term}")
                webbrowser.open(f"https://www.google.com/search?q={search_term}")
            else:
                self.speak("What would you like me to search for?")
        
        # Exit commands
        elif any(word in query for word in ['exit', 'quit', 'goodbye', 'bye']):
            self.speak("Goodbye! Have a great day!")
            return False
        
        # Default response
        elif query != "none":
            self.speak("Sorry, I didn't understand that command. Please try again.")
        
        return True
    
    def run(self):
        """Main execution loop"""
        self.wish_me()
        
        while True:
            try:
                query = self.take_command()
                if not self.process_command(query):
                    break
                    
            except KeyboardInterrupt:
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"Error in main loop: {e}")
                self.speak("Sorry, there was an error. Please try again.")

if __name__ == "__main__":
    chatbot = VoiceActivatedChatbot()
    chatbot.run()