from django.db import models

class Score(models.Model):
    username = models.CharField(max_length=100)  # 유저 이름
    score = models.IntegerField()  # 점수
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간
    
    class Meta:
        ordering = ['-score']  # 점수 높은 순으로 자동 정렬
    
    def __str__(self):
        return f"{self.username}: {self.score}"