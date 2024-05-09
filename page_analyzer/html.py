from bs4 import BeautifulSoup


def parse_page(content):
    parsed_data = {}
    soup = BeautifulSoup(content, 'html.parser')
    h1_tag = soup.find('h1')
    parsed_data['h1'] = h1_tag.get_text().strip() if h1_tag else ''
    title_tag = soup.find('title')
    parsed_data['title'] = title_tag.get_text().strip() if title_tag else ''
    description_tag = soup.find('meta', attrs={'name': 'description'})
    if description_tag:
        parsed_data['description'] = description_tag.get('content', '').strip()
    else:
        parsed_data['description'] = ''
    return parsed_data
