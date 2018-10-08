# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class PcsoSpiderPipeline(object):
    def open_spider(self, _):
        import os
        os.environ['DJANGO_SETTINGS_MODULE'] = 'pcso.settings'
        import django
        django.setup()

    def process_item(self, item, _):
        from core.models import Game, Draw, DrawBall
        game = Game.objects.get_or_create(pcso_game_id=item['game_id'], defaults={'name': item['game_name']})[0]
        draw = Draw.objects.filter(game=game, date=item['date']).first()
        if draw:
            return item
        draw = Draw(game=game, date=item['date'], jackpot=item['jackpot'], winners=item['winners'])
        draw.save()
        for order, ball in enumerate(item['numbers'], start=1):
            DrawBall(draw=draw, ball=ball, order=order).save()
        return item
