import datetime
from dateutil.parser import parse

from scrapy import Spider, FormRequest, Request
from scrapy.http import Response
from scrapy.selector import SelectorList, Selector


class PCSOResultsSpider(Spider):
    name = 'results'

    MONITORED_GAMES = [
        'Ultra Lotto 6/58',
        'Grand Lotto 6/55',
        'Super Lotto 6/49',
        'Mega Lotto 6/45',
        'Lotto 6/42'
    ]

    def start_requests(self):
        yield Request('http://www.pcso.gov.ph/SearchLottoResult.aspx')

    def parse(self, response: Response):
        games: SelectorList = response.xpath('id("cphContainer_cpContent_ddlSelectGame")/option[not(@value="0")]')
        today = datetime.datetime.now().date()
        formatted_date = today.strftime('%B %d %Y').split(' ')
        for game in games:
            game: Selector = game
            game_name = game.xpath('text()').extract_first()
            game_id = game.xpath('@value').extract_first()
            if game_name not in self.MONITORED_GAMES:
                continue
            yield FormRequest.from_response(
                response,
                formid='mainform',
                formdata={
                    'ctl00$ctl00$cphContainer$cpContent$ddlStartMonth': 'January',
                    'ctl00$ctl00$cphContainer$cpContent$ddlStartDate': '1',
                    'ctl00$ctl00$cphContainer$cpContent$ddlStartYear': '2008',
                    'ctl00$ctl00$cphContainer$cpContent$ddlEndMonth': formatted_date[0],
                    'ctl00$ctl00$cphContainer$cpContent$ddlEndDate': str(int(formatted_date[1])),
                    'ctl00$ctl00$cphContainer$cpContent$ddlEndYear': formatted_date[2],
                    'ctl00$ctl00$cphContainer$cpContent$btnSearch': 'Search Lotto',
                    'ctl00$ctl00$cphContainer$cpContent$ddlSelectGame': game_id
                },
                callback=self.parse_results,
                meta={
                    'game_name': game_name,
                    'game_id': game_id
                }
            )

    def parse_results(self, response: Response):
        results_sel: SelectorList = response.xpath('id("cphContainer_cpContent_GridView1")/tr[not(position()=1)]')
        for result_sel in results_sel:
            result_sel: Selector = result_sel
            numbers = result_sel.xpath('td[2]/text()').extract_first().split('-')
            date = parse(result_sel.xpath('td[3]/text()').extract_first())
            jackpot = result_sel.xpath('td[4]/text()').extract_first().replace(',', '')
            winners = result_sel.xpath('td[5]/text()').extract_first()
            yield {
                'game_name': response.meta['game_name'],
                'game_id': response.meta['game_id'],
                'numbers': numbers,
                'date': date,
                'jackpot': jackpot,
                'winners': winners
            }