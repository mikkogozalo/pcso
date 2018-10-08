from django.db import models


class Game(models.Model):
    class Meta:
        db_table = 'game'

    name = models.CharField(max_length=255)
    pcso_game_id = models.PositiveSmallIntegerField(db_index=True)
    digits = models.PositiveSmallIntegerField(default=6)
    max_digit = models.PositiveSmallIntegerField(default=58)


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
