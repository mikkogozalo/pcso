from itertools import chain
from collections import Counter

from django.db import models


class Game(models.Model):
    class Meta:
        db_table = 'game'

    name = models.CharField(max_length=255)
    pcso_game_id = models.PositiveSmallIntegerField(db_index=True)
    digits = models.PositiveSmallIntegerField(default=6)
    max_digit = models.PositiveSmallIntegerField(default=58)

    def find_draws(self, numbers: str):
        numbers = [int(_) for _ in numbers.split('-')]
        draws_with_numbers = []
        for n in numbers:
            draws_with_numbers.append(Draw.objects.filter(balls__ball=n).distinct().values_list('id',
                                                                                                           flat=True))
        draws_with_numbers = chain(*draws_with_numbers)
        ball_counters = Counter(draws_with_numbers)
        winning = {k: v for k, v in ball_counters.items() if v >= 5}
        return winning


class Draw(models.Model):
    class Meta:
        db_table = 'draw'

    game = models.ForeignKey('Game', on_delete=models.CASCADE, db_index=True)
    date = models.DateField(db_index=True)
    jackpot = models.DecimalField(max_digits=13, decimal_places=2)
    winners = models.IntegerField()


class DrawBall(models.Model):
    class Meta:
        db_table = 'draw_ball'

    draw = models.ForeignKey('Draw', on_delete=models.CASCADE, related_name='balls')
    ball = models.PositiveSmallIntegerField()
    order = models.PositiveSmallIntegerField()
