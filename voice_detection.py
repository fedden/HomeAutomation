import os
import uuid
import json
import apiai
import signal
import snowboydecoder
from light import Light
import speech_recognition as sr


"""
The beginning of Albus the house assistant. Exciting times.
"""


def prepend_resource_folder(file_name):
    current_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_path, 'resources', file_name)


def call_functionality(intent_name):
    print("detected: '{}'".format(intent_name))

    if intent_name == 'Decrement Brightness':
        light.decrease_brightness()

    elif intent_name == 'Decrement Hue':
        light.decrease_hue()

    elif intent_name == 'Decrement Saturation':
        light.decrease_saturation()

    elif intent_name == 'Decrement Warmth':
        light.decrease_warmth()

    elif intent_name == 'Increment Brightness':
        light.increase_brightness()

    elif intent_name == 'Increment Hue':
        light.increase_hue()

    elif intent_name == 'Increment Saturation':
        light.increase_saturation()

    elif intent_name == 'Increment Warmth':
        light.increase_warmth()

    elif intent_name == 'Light On':
        light.turn_on()

    elif intent_name == 'Lights Off':
        light.turn_off()

    elif intent_name == 'Random Colour':
        light.random_colour()

    else:
        print("No meaningful translation between intent and code action")


def audio_file_to_text(audio_file_path):
    recogniser = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio = recogniser.record(source)

    try:
        return recogniser.recognize_google(audio)

    except sr.UnknownValueError:
        print("Google speech recognition did not understand this audio file.")

    except sr.RequestError as e:
        print("Issues requesting the results from Google: {}".format(e))

    os.remove(audio_file_path)

    return ""


def text_to_intent(client_access_token, session_id, query_str):

    ai = apiai.ApiAI(client_access_token)

    request = ai.text_request()
    request.lang = 'en-GB'
    request.session_id = session_id
    request.query = query_str

    response = request.getresponse()
    response_data = response.read()
    response_str = response_data.decode('utf-8')

    return json.loads(response_str)


def audio_recorder_callback(audio_file_path):

    query_str = audio_file_to_text(audio_file_path)

    if query_str != "":

        intent = text_to_intent(client_access_token, session_id, query_str)

        intent_confidence = intent['result']['score']
        intent_name = intent['result']['metadata']['intentName']

        if intent_confidence > 0.5:
            call_functionality(intent_name)
            snowboydecoder.play_audio_file(success_sound)
            print()
            print()
            print("*" * 20)
            print('Predicted: {}'.format(intent_name))
            print("*" * 20)
            print()
            print()

        else:
            print("Not confident enough to understand intent.")
            snowboydecoder.play_audio_file(end_interaction_sound)

    else:
        print("No words recognised in audio file.")
        snowboydecoder.play_audio_file(end_interaction_sound)


def detected_callback():
    print('recording audio...')
    snowboydecoder.play_audio_file(start_interaction_sound)


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted


client_access_token = '4ea1cf05d14e4b40960d3cc95d18ad26'

interrupted = False
session_id = str(uuid.uuid4())
project_id = 'albus-d8845'
language_code = 'en-GB'

hotword_sensitivity = 0.26

models = [
    'albus_ella.pmdl',
    'albus_leon.pmdl'
]

light = Light()

sensitivities = [hotword_sensitivity for _ in models]
models = [prepend_resource_folder(m) for m in models]
detected_callbacks = [detected_callback for _ in models]

start_sound = prepend_resource_folder('start.wav')
success_sound = prepend_resource_folder('success.wav')
program_end_sound = prepend_resource_folder('program_end.wav')
end_interaction_sound = prepend_resource_folder('end_interaction.wav')
start_interaction_sound = prepend_resource_folder('start_interaction.wav')

# Capture SIGINT signal, e.g., Ctrl+C.
signal.signal(signal.SIGINT, signal_handler)
snowboydecoder.play_audio_file(start_sound)

detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivities)

print('Listening... Press Ctrl+C to exit')

# Main loop.
detector.start(detected_callback=detected_callbacks,
               audio_recorder_callback=audio_recorder_callback,
               interrupt_check=interrupt_callback,
               silent_count_threshold=3,
               recording_timeout=10,
               sleep_time=0.01)

detector.terminate()

snowboydecoder.play_audio_file(program_end_sound)
