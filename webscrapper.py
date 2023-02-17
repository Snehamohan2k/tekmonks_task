import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    response = requests.get('https://time.com/')
    soup = BeautifulSoup(response.content, 'html.parser')
    latest_stories_section = soup.find('div', {'class': 'partial latest-stories'})
    stories = latest_stories_section.find_all('a')
    latest_stories = [{'title': story.text, 'link': story['href']} for story in stories]
    featured_voice_section = soup.find('div', {'class': 'partial featured-voices'})
    featured_voice_title = featured_voice_section.find('h2', {'class': 'section-heading featured-voices__heading'}).text
    featured_voice_author = featured_voice_section.find('span', {'class': 'featured-voices__list-item-author display-block'}).text
    featured_voice_excerpt = featured_voice_section.find('h3', {'class': 'featured-voices__list-item-headline display-block'}).text
    return render_template('index.html', latest_stories=latest_stories, 
                           featured_voice_title=featured_voice_title, 
                           featured_voice_author=featured_voice_author, 
                           featured_voice_excerpt=featured_voice_excerpt,
                           date=datetime.datetime.now().strftime("%B %d, %Y %I:%M %p"))

if __name__ == '__main__':
    app.run()
