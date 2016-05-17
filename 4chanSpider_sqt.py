import re
import requests
from bs4 import BeautifulSoup

#class comment:


def find_client_number(board_source_code):

    number_pattern = re.compile('''"\},"(\d{8})":\{"date":\d+,"file":"\S*\.\w*","r":\d+,"i":\d+,"lr":\{"id":\d+,'''
                                '''"date":\d*,"author":"\S+"\},"semantic_url":"sqt-''')
    the_number = re.search(number_pattern, board_source_code)
    return the_number.group(1)


def find_semantic_url(board_source_code):

    name_pattern = re.compile('''"semantic_url":"(sqt-[a-z|\-]*)''')
    thread_name = re.search(name_pattern, board_source_code)
    return thread_name.group(1)


def split_source_code(only_post_messages):

    text_to_cut = re.split('</blockquote>',only_post_messages)
    del text_to_cut[-1]
    return text_to_cut


def record_all_comments(urls):

    for i, url in enumerate(urls, 1):
        comments_file = open('4chan_sqt_comments_%r' % i, 'w')
        source_code = requests.get(url).content
        soup = BeautifulSoup(source_code, 'html.parser')
        only_post_messages = str(soup.find_all('blockquote', class_="postMessage"))
        list_of_messages = split_source_code(only_post_messages)

        for j, text in enumerate(list_of_messages, 1):
            soup = BeautifulSoup(text, 'html.parser')
            tag = soup.blockquote
            comments_file.write('Post Number : %d' % j + '\n')
            comments_file.write('ID Number : ' + tag['id'] + '\n\n')
            all_comments =  tag.get_text()
            all_comments = re.sub(r'>>\d{8}', r'', all_comments)
            comments_file.write(all_comments + '\n\n\n')


def main():

    text_file = open('4chan_urls', 'w')
    technology_board_url = "http://boards.4chan.org/g/catalog"
    board_source_code = requests.get(technology_board_url).content

#   Assembles the URL
    url_of_thread = "http://boards.4chan.org/g/thread/"
    url_of_thread += str(find_client_number(board_source_code))
    url_of_thread += "/"
    url_of_thread += str(find_semantic_url(board_source_code))

    list_of_urls = [url_of_thread, ]
    text_file.write(url_of_thread + '\n')

    for url in list_of_urls:
        if url_of_thread != url:
            list_of_urls += (str(url_of_thread),)
            text_file.write(url_of_thread + '\n')

    text_file.close()
    record_all_comments(list_of_urls)


if __name__ == "__main__":
    main()


