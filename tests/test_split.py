from ordered_demuxer import OrderedDemuxer, FilterCondition

def test_split():
    x = [1, 2, 3, 4]
    y = lambda x: x > 2
    splt = OrderedDemuxer(data_source=iter(x), filter=FilterCondition(y), split_after=False)
    x_iter = splt.__next__()
    assert list(x_iter) == [1, 2]
    x_iter = splt.__next__()
    assert list(x_iter) == [3, 4]

def test_split_after():
    x = [1, 2, 3, 4]
    y = lambda x: x > 2
    splt = OrderedDemuxer(data_source=iter(x), filter=FilterCondition(y), split_after=True)
    x_iter = splt.__next__()
    assert list(x_iter) == [1, 2, 3]
    x_iter = splt.__next__()
    assert list(x_iter) == [4]

