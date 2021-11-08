from ordered_demuxer import OrderedDemuxer, FilterCondition

def test_loop():
    x = [1, 2, 3, 4]
    y = lambda x: x > 2
    splt = OrderedDemuxer(data_source=iter(x), filter=FilterCondition(y), split_after=False)
    total = 0
    for stream in splt:
        print(stream)
        for y in stream:
            total += y
    assert total == sum(x)
