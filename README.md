# Ordered Demultiplexer in Python
Single pass approach to Demultiplexing/Demuxing

Break an iterator into multiple iterators based on a break filter.

Typical demuxers will place elements into different iterators,
such as splitting [0,1,2,3] into ([0,2], [1,3]) based on odd or
even elements. Ordered Demuxers focus on breaking iterators into 
contiguous blocks that are meant to be immediately worked upon, 
without having to iterate over the list more than once. 

This makes them appropriate to use with iterators where the contents
cannot be fully held in memory, such as retrieving data online.

### Example
With an input such as
```
[
  0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0
]
```


This can be broken into;
```
[
  [0, 0, 0, 0, 1], [0, 0, 0, 1], [0, 0, 0]
]
```

While leaving the items contained with the iterators, so the return is actually
```
[
  Iterator[Item=int], 
  Iterator[Item=int],
  Iterator[Item=int]
]
```

Although it requires the consumption of each iterator entirely to make this possible.

## Installation
```bash
python -m pip install ordered-demuxer
```

## Usage
```python
>>> from ordered_demuxer import FilterCondition, OrderedDemuxer
>>> x = [1, 2, 3, 4]
>>> y = FilterCondition(lambda x: x > 2)
>>> splt = OrderedDemuxer(data_source=iter(x), filter=y, split_after=False)
>>> x_iter = splt.__next__()
>>> print(list(x_iter))
  [1, 2]
```
