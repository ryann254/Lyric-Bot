from collections import Counter
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from time import sleep

def answer(prompt):
    value = str(input(prompt))
    answer = value.title()

    return answer

title = answer('What\'s the title of the song: ')
singer = answer('Who\'s the singer of the song: ')
lyric_website = 'http://www.songlyrics.com/'
lyric_website_2 = 'https://www.lyrics.com/'

class Lyric_Bot():
    def __init__(self, singer, title):
        self.singer = singer
        self.title = title

        self.driver = webdriver.Chrome('Add the path to your where you have downloaded your chromedriver here')
        self.driver.get(lyric_website)
        # Save the window opener (current window, do not mistake with tab... not the same)
        main_window = self.driver.current_window_handle
        sleep(2)


        try:
            # Search for the search input and give it the title and singer of the song
            div_search_input = self.driver.find_element_by_id('header_search')
            form_search_input = div_search_input.find_element_by_name('searchForm')
            input_search_input = form_search_input.find_element_by_name('searchW')
            input_search_input.send_keys(singer, ' ', title)

            button = form_search_input.find_element_by_name('submit')
            button.click()
            sleep(2)

            # Click the first link in the search
            self.driver.find_element_by_xpath("//a[contains(node(), '{} Lyrics')]".format(title)).click()
            sleep(3)
            lyric_container = self.driver.find_element_by_id('songLyricsDiv').text
            # Store the lyrics in a variable
            self.lyric_container = lyric_container

        except NoSuchElementException:
            # Open a new window / tab by simulating a click on a link
            first_result = self.driver.find_element_by_tag_name('body')
            first_link = first_result.find_element_by_tag_name('a')
            # Open the link in a new tab by sending key strokes on the element
            # Use: Keys.CONTROL + Keys.SHIFT + Keys.RETURN to open tab on top of the stack
            first_link.send_keys(Keys.CONTROL + Keys.RETURN)
            # Switch tab to the new tab, which we will assume is the next one on the right
            first_result.send_keys(Keys.CONTROL + Keys.TAB)
            # Put focus on current window which will, in fact, put focus on the current visible tab
            self.driver.switch_to.window(main_window)
            self.driver.get(lyric_website_2)
            sleep(2)

            # Search for the search input and give it the title and singer of the song
            self.driver.find_element_by_id('search').send_keys(title)
            self.driver.find_element_by_id('page-word-search-button').click()
            sleep(2)

            # Click the first link in the best matches sector
            self.driver.find_element_by_class_name('best-matches')
            self.driver.find_element_by_xpath("//a[contains(node(), '{}')]".format(title)).click()
            sleep(2)
            lyric_container = self.driver.find_element_by_id('lyric-body-text').text
            # Store the lyrics in a variable
            self.lyric_container = lyric_container

    def get_lyrics(self):
        song = self.lyric_container
        apostrophe_words = [word for word in song.split() if "'" in word]
        normal_words = [word for word in song.split() if "'" not in word]
        # Filter all the words that have more than three letters in to the lyrics list
        lyrics = [lyric for lyric in normal_words if len(lyric) > 3]
        for lyric in apostrophe_words:
            if len(lyric) > 3:
                lyrics.append(lyric)

        lyrics_counter = Counter(lyrics)
        most_repeated_words = lyrics_counter.most_common(3)
        print(most_repeated_words)


ryan_bot = Lyric_Bot(singer, title)
ryan_bot.get_lyrics()