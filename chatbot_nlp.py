import streamlit as st
import nltk
nltk.download('punkt')  # download the necessary tokenizer data
from nltk.tokenize import word_tokenize
from datetime import datetime

# Define a function to check if a message contains a certain word
def check_for_word(message, word):
    tokens = word_tokenize(message.lower())
    return word.lower() in tokens

# Define a function to get the date from a message
def get_date(message):
    tokens = word_tokenize(message.lower())
    for i in range(len(tokens)):
        try:
            date = datetime.strptime(tokens[i], '%Y-%m-%d').date()
            return date
        except ValueError:
            pass  # not a date
    return None  # no date found

# Define a dictionary of sports events, their dates, and locations
events = {
    'Ramadan Sports Tournaments': {'date': datetime(2023, 3, 27).date(), 'location': 'Al Ain and Al Dhafra, Abu Dhabi'},
    '2026 Masters Games Series': {'date': datetime(2026, 3, 23).date(), 'location': 'Abu Dhabi, UAE'},
    'Burjeel Games': {'date': datetime(2023, 3, 24).date(), 'location': 'Al Hudairiyat Island, Abu Dhabi'},
}

# Define a dictionary of responses to different messages
responses = {
    'hello': 'Hello! How can I help you?',
    'goodbye': 'Goodbye!',
    'thanks': 'You\'re welcome!',
    'events': f'The upcoming events are: {", ".join(events.keys())}.',
    'event_info': lambda event: f'The date and location of {event} are {events[event]["date"].strftime("%Y-%m-%d")} at {events[event]["location"]}.',
    'unknown': 'Sorry, I didn\'t understand that. Please contact us at help@adsc.gov.ae or call +971 2 4088999 for more information.'
}

# Define the Streamlit app
def sports_event_chatbot_app():
    st.title("ADSC's Sports Event Chatbot")
    st.write('Enter your message below and the chatbot will respond.')
    message = st.text_input('You:')
    
    # Check for keywords in the user's message
    if check_for_word(message, 'hello'):
        st.write('Bot: ' + responses['hello'])
    elif check_for_word(message, 'goodbye'):
        st.write('Bot: ' + responses['goodbye'])
    elif check_for_word(message, 'thanks'):
        st.write('Bot: ' + responses['thanks'])
    elif check_for_word(message, 'events'):
        st.write('Bot: ' + responses['events'])
    elif any(event in message for event in events):
        event = next((event for event in events if event in message), None)
        if event is not None:
            st.write('Bot: ' + responses['event_info'](event))
        else:
            st.write('Bot: ' + responses['unknown'])
    elif get_date(message) is not None:
        date = get_date(message)
        upcoming_events = [event for event, event_info in events.items() if event_info['date'] >= date]
        if len(upcoming_events) > 0:
            event_info_strs = [f'{event} ({events[event]["location"]}) on {events[event]["date"].strftime("%Y-%m-%d")}' for event in upcoming_events]
            st.write('Bot: The upcoming events after ' + date.strftime('%Y-%m-%d') + ' are: ' + ', '.join(event_info_strs))
        else:
            st.write('Bot: There are no upcoming events after ' + date.strftime('%Y-%m-%d') + '.')
    else:
        st.write('Bot: ' + responses['unknown'])

# Run the Streamlit app
if __name__ == '__main__':
    sports_event_chatbot_app()

       
