from ordered_demuxer import OrderedDemuxer, FilterCondition

def test_filter_name():
    x = [1, 2, 3, 4]
    y = lambda x: x > 2
    splt = OrderedDemuxer(data_source=iter(x), filter=FilterCondition(y, 'MoreThanTwo'), split_after=True)
    x_iter = splt.__next__()
    assert list(x_iter) == [1, 2, 3]
    x_iter = splt.__next__()
    assert splt.condition_met.name == "MoreThanTwo" 

