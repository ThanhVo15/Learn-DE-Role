from ex1_post_aggregator.src.post_aggregator import PostAggregator
from ex1_post_aggregator.src.models import Post

def test_count_per_user_basic():
    posts = [
        Post(userId=1, id=1, title="a", body="b"),
        Post(userId=1, id=2, title="c", body="d"),
        Post(userId=2, id=3, title="e", body="f"),
    ]
    counter = PostAggregator.count_per_user(posts)
    assert counter == {1: 2, 2: 1}
    top1 = PostAggregator.top_n(counter, 1)
    assert top1 == [(1, 2)]
