import uuid
import streamlit as st
from cohere import Client, ChatConnector, ParseInfo
from cohere import ClassifyExample

from preview.internal import secrets

co = Client(secrets.COHERE_API_KEY)
KEYWORD = "opinion"

train_examples = [
    ClassifyExample(text="Taylor Swift's Era's Tour Receives Rave Reviews: Critics Applaud Spectacular Performances", label="Positive"),
    ClassifyExample(text="Taylor Swift's Era's Tour Takes Fans on an Unforgettable Journey Through Her Music", label="Positive"),
    ClassifyExample(text="Taylor Swift Delights Fans with Surprise Guests at Era's Tour Stops", label="Positive"),
    ClassifyExample(text="Fans Overflow with Emotion as Taylor Swift Performs Classics on Era's Tour", label="Positive"),
    ClassifyExample(text="Taylor Swift's Era's Tour Merchandise Line Breaks Records: Fans Can't Get Enough", label="Positive"),
    ClassifyExample(text="Taylor Swift's Era's Tour Sells Out Stadiums Across the Globe", label="Positive"),
    ClassifyExample(text="Taylor Swift Engages with Fans During Era's Tour Meet-and-Greets: Heartwarming Moments Captured", label="Positive"),
    ClassifyExample(text="Taylor Swift's Era's Tour Inspires Thousands with Messages of Love and Resilience", label="Positive"),
    ClassifyExample(text="Taylor Swift's Era's Tour Leaves a Lasting Impact on Fans: Memories to Cherish Forever", label="Positive"),
    ClassifyExample(text="Taylor Swift Wows Audiences with Jaw-Dropping Performances on Era's Tour", label="Positive"),
    ClassifyExample(text="Controversy Erupts as Taylor Swift's Era's Tour Ticket Prices Soar", label="Negative"),
    ClassifyExample(text="Taylor Swift Faces Criticism Over VIP Treatment on Era's Tour: Fans Express Discontent", label="Negative"),
    ClassifyExample(text="Disappointment Looms as Taylor Swift Cancels Era's Tour Dates Due to Unforeseen Circumstances", label="Negative"),
    ClassifyExample(text="Security Breach Raises Concerns at Taylor Swift's Era's Tour Venue: Safety Measures Under Scrutiny", label="Negative"),
    ClassifyExample(text="Taylor Swift's Era's Tour Plagued by Technical Glitches: Fans Express Frustration", label="Negative"),
    ClassifyExample(text="Taylor Swift's Era's Tour Faces Legal Challenges Over Copyright Infringement Claims", label="Negative"),
    ClassifyExample(text="Ticketing System Crashes Amid High Demand for Taylor Swift's Era's Tour: Chaos Ensues", label="Negative"),
    ClassifyExample(text="Taylor Swift's Era's Tour Merchandise Recalled Due to Quality Issues: Fans Disappointed", label="Negative"),
    ClassifyExample(text="Taylor Swift's Era's Tour Draws Criticism for Lack of Diversity in Lineup", label="Negative"),
    ClassifyExample(text="Fans Left Disheartened as Taylor Swift's Era's Tour Comes to an Abrupt End", label="Negative")
]

# fine tune model
# single_label_dataset = co.datasets.create(name="single-label-dataset",
#                                          data=open("/Users/lindama/produhacks-2024/preview/preview/pages/train.csv", "rb"),
#                                          type="single-label-classification-finetune-input",
#                                          csv_delimiter=","
#                                         #  parse_info=ParseInfo(delimiter=",")
#                                          ) # parse_info is optional
# print(single_label_dataset.await_validation())
# single_label_dataset = co.create_dataset(name="single-label-dataset",
#                                          data=open("/Users/lindama/produhacks-2024/preview/preview/pages/train.csv", "rb"),
#                                          dataset_type="single-label-classification-finetune-input",
#                                          parse_info=ParseInfo(delimiter=",")) # parse_info is optional
# print(single_label_dataset.await_validation())

# start the fine-tune job using this dataset
# finetune = co.create_finetuned_model(
#     name="single-label-ft", 
#     dataset=single_label_dataset,
#     model_type="CLASSIFY"
# )

# finetune.wait() # this will poll the server for status updates
# print(f"fine-tune ID: {finetune.id}, fine-tune status: {finetune.status}")

def get_sentiment_analysis(inputs, examples):
    response = co.classify(
        inputs=inputs,
        examples=examples
    )

    return response

st.title("Hi Tree Paine 👋")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = uuid.uuid4()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    text = ''
    sources = []
    with st.status("Researching...", state='running') as status:
        response = co.chat_stream(
            model="command-r",
            message=prompt,
            conversation_id=st.session_state.conversation_id,
            connectors=[ChatConnector(id='web-search')]
        )

        citations = []
        cited_documents = []
        cited_document_titles = {}
        for event in response:
            if event.event_type == 'citation-generation':
                citations.extend(event.citations)
            elif event.event_type == 'search-results':
                cited_documents = event.documents

            if citations:
                for document in cited_documents:
                    cited_document_titles[document['title']] = document['url']
                    
            if event.event_type == 'stream-end':
                text = event.response.text

                if cited_document_titles.keys():
                    sources.append('\n*Sources*\n')
                    for key, value in cited_document_titles.items():
                        sources.append(key + ': ' + value)

                    sources = '\n- '.join(sources)
                    st.markdown(sources)
        
        status.update(label='Done!', state='complete')

    # add check to see if prompt contains sentiment
    if KEYWORD in prompt: 
        # check blank
        parsed_txt = [x.strip() for x in text.split('.')]
        parsed_txt.pop()
        response = get_sentiment_analysis(parsed_txt, train_examples)
        positive_count, negative_count = 0, 0
        for res in response.classifications: 
            if res.prediction == "Positive":
                positive_count += 1
            else: 
                negative_count += 1
        # ft = co.get_custom_model_by_name('single-label-ft')
        # response = co.classify(
        #     inputs=text,
        #     model=ft.model_id,
        # )
        total = positive_count + negative_count
        pos_percentage = (positive_count / total) * 100
        formatted_pos_percentage = format(pos_percentage, '.2f')
        neg_percentage = 100 - pos_percentage
        formatted_neg_percentage = format(neg_percentage, '.2f')
        final = f'\n**The current public opinion is {formatted_pos_percentage}% positive and {formatted_neg_percentage}% negative based on the latest sentiment analysis.**\n'
        final += text
    elif sources:
        final = '\n'.join([text, sources])
    else: 
        final = text

    with st.chat_message("assistant"):
        st.markdown(final)

    st.session_state.messages.append({"role": "assistant", "content": final})
