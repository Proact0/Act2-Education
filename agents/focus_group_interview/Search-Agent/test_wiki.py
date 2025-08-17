import wikipediaapi

wiki_api = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent='EducationResourceSearcher/1.0'
)

page = wiki_api.page("LangChain")

if page.exists():
    print(f"Page title: {page.title}")
    print(f"Page URL: {page.fullurl}")
    print(f"Page summary: {page.summary[:500]}...")
else:
    print("Page does not exist.")