import plotly.express as px
import pandas as pd
import requests
import datetime
from bs4 import BeautifulSoup

filter_date = {'filter-thursday': '2021-07-29',
               'filter-friday': '2021-07-30',
               'filter-saturday': '2021-07-31',
               'filter-sunday': '2021-08-01'}


def get_page(url):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    return soup


def handler_soup(soup):
    df = pd.DataFrame()
    schedule_items = soup.select('div.schedule__item ')

    for item in schedule_items:
        intersection = " ".join(item['class'] & filter_date.keys())
        artist = item.select('div.schedule__item-title')[0].text
        stage = item.select('div.schedule__item-stage')[0].text
        times = item.select('div.schedule__item-date')[0].text.split('-')
        time_start = fix_time_shift(str(filter_date[intersection]) + ' ' + str(times[0]))
        time_finish = fix_time_shift(str(filter_date[intersection]) + ' ' + str(times[1]))

        df = df.append({
            'Artist': artist,
            'Start': time_start,
            'Finish': time_finish,
            'Scenes': stage},
            ignore_index=True)
    return df


def fix_time_shift(datetime_str):
    dt = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
    if dt.hour < 6:
        dt += datetime.timedelta(days=1)
    return dt


def generate_dataframe():
    df = pd.DataFrame([
        dict(Artist="Job A", Start='2009-01-01 9:00', Finish='2009-01-01 12:00', Scenes="Сцена А"),
        dict(Artist="Job B", Start='2009-01-01 12:10', Finish='2009-01-01 13:00', Scenes="Сцена А"),
        dict(Artist="Job C", Start='2009-01-01 12:00', Finish='2009-01-01 12:10', Scenes="Сцена Б")
    ])
    return df


def show_lineup(df):
    fig = px.timeline(df,
                      x_start="Start",
                      x_end="Finish",
                      y="Scenes",
                      text="Artist",
                      height=720,
                      facet_row_spacing=0.0)
    # fig.update_yaxes(autorange="reversed")
    fig.update_traces(textangle=-90,
                      textposition="inside")
    fig.update_yaxes(tickangle=-90)
    fig.update_xaxes(type='date',
                     dtick=600000,
                     tickangle=-90,
                     ticklabelposition='inside',
                     ticklabelmode='period',
                     tickformat='%H:%M')
    fig.show()


if __name__ == '__main__':
    soup = get_page('https://nashestvie.ru/lineup/')
    df = handler_soup(soup)
    show_lineup(df)