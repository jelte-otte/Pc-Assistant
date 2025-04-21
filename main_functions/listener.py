import speech_recognition as sr

class Listener:
    def __init__(self, keywords, callback, device_index=14):
        self.keywords = [k.lower() for k in keywords]
        self.callback = callback
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def start(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            print("Listening...")

        while True:
            with self.microphone as source:
                audio = self.recognizer.listen(source)

            try:
                text = self.recognizer.recognize_google(audio).lower()
                print("You said:", text)
                for keyword in self.keywords:
                    if keyword in text:
                        self.callback(keyword, text)
            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError as e:
                print(f"API error: {e}")
