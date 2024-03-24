import streamlit as st
import cohere

from cohere import Client, ChatConnector

# from preview.internal.secrets import COHERE_API_KEY

co = Client(COHERE_API_KEY)

st.title("PReview")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = co.chat_stream(
        model="command-r",
        message=prompt,
        connectors=[ChatConnector(id='web-search')]
    )

    print('\nChatbot:')

    citations = []
    cited_documents = []
    cited_document_titles = {}
    for event in response:
        if event.event_type == 'citation-generation':
            citations.extend(event.citations)
        elif event.event_type == 'search-results':
            cited_documents = event.documents

        if citations:

            # print("\nDOCUMENTS:")
            for document in cited_documents:
                cited_document_titles[document['title']] = document['url']

            # print(f"\n{'-'*100}\n")
                
        if event.event_type == 'stream-end':
            # content = event.response.text
            # if cited_document_titles.keys():
            #     content += '*Sources*'
            #     for key in cited_document_titles.keys():
            #         content = content + key + ": " + cited_document_titles[key]
            #         # st.markdown(key + ": " + cited_document_titles[key])
            with st.chat_message("assistant"):
                # st.markdown(content)
                st.markdown(event.response.text)
                if cited_document_titles.keys():
                    st.markdown("*Sources*")
                    for key in cited_document_titles.keys():
                        st.markdown(key + ": " + cited_document_titles[key])
                st.session_state.messages.append({"role": "assistant", "content": event.response.text})


