from cohere import Client, ChatConnector

key = ''
co = Client(key)
response = co.chat_stream(
    message="Recent news about Taylor Swift",
    connectors=[ChatConnector(id='web-search')]
)

print('\nChatbot:')

citations = []
cited_documents = []
for event in response:
    if event.event_type == 'text-generation':
        print(event.text, end='')
    elif event.event_type == 'citation-generation':
        citations.extend(event.citations)
    elif event.event_type == 'search-results':
        cited_documents = event.documents

if citations:
    print('\n\nCITATIONS:')
    for citation in citations:
        print(citation)
    
    print("\nDOCUMENTS:")
    for document in cited_documents:
        print({'id': document['id'],
            'snippet': document['snippet'][:50] + '...',
            'title': document['title'],
            'url': document['url']})

    print(f"\n{'-'*100}\n")