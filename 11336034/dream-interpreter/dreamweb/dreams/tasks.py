# dreams/tasks.py
import jieba
from collections import Counter
from django.utils import timezone
from dreams.models import DreamPost, DreamTrend

def update_dream_trends():
    """更新夢境趨勢數據 (建議通過定時任務每天運行)"""
    today = timezone.now().date()
    # 抓過去 7 天的夢境
    time_threshold = timezone.now() - timezone.timedelta(days=7)
    recent_dreams = DreamPost.objects.filter(created_at__gte=time_threshold)

    all_words = []
    for dream in recent_dreams:
        words = jieba.cut(dream.content)
        all_words.extend(list(words))

    # 停用詞過濾
    stopwords = ['的', '是', '了', '在', '和', '我']
    filtered_words = [w for w in all_words if w not in stopwords and len(w) > 1]

    # 統計詞頻
    word_counts = Counter(filtered_words)
    top_keywords = dict(word_counts.most_common(20))

    # 存入 JSONField
    trend, created = DreamTrend.objects.get_or_create(
        date=today,
        defaults={'trend_data': top_keywords}
    )

    if not created:
        trend.trend_data = top_keywords
        trend.save()
