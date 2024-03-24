import uuid
import streamlit as st
from cohere import Client, ChatConnector

from preview.internal import secrets

co = Client(secrets.COHERE_API_KEY)

st.title("PReview")


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

    final = '\n'.join([text, sources])
    with st.chat_message("assistant"):
        st.markdown(final)

    st.session_state.messages.append({"role": "assistant", "content": final})
