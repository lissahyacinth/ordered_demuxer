# Ordered Demultiplexer in Python
Single pass approach to Demultiplexing/Demuxing

Break an iterator into multiple iterators based on a set of filters.

Typical demuxers will place elements into different iterators,
such as splitting [0,1,2,3] into ([0,2], [1,3]) based on odd or
even elements. Ordered Demuxers focus on breaking iterators into 
contiguous blocks that are meant to be immediately worked upon, 
without having to iterate over the list more than once. 

This makes them appropriate to use with iterators where the contents
cannot be fully held in memory, such as retrieving data online.

### Example
With any iterable input such as
```python
x = iter([ (_, 0), (_, 1), (MessageEnd, 2), (_, 3), (_, 4), (MessageEnd, 5) ])
```


This can be broken into;
```python
Iterator [
  Iterator [(_, 0), (_, 1), (MessageEnd, 2)], 
  Iterator [(_, 3), (_, 4), (MessageEnd, 5)]
]
```

Without passing over each element of data multiple times. This allows for methods like;

```python
for data_stream in demuxed_stream:
  for element in data_stream:
    function(element)
```

Or more interestingly;

```python
def foo(x: Iterator[T]):
  ...
  
for data_stream in demuxed_stream:
  foo(data_stream)
```

`foo` will consume part of the original iterator, up until the next break point, but still behave identically to passing it an iterator of just the data required.

Due to the way the filters are available within the Demuxer, it's also possible to send these partial iterators to functions according to the relevant filter, i.e.

```python
conditions = [
  FilterCondition(lambda x: x[0] == 'MessageEnd', 'SuccessfulMessageStream'),
  FilterCondition(lambda x: x[0] == 'MessageFailed', 'FailedMessageStream')
]

for data_stream in demuxed_stream:
  if demuxed_stream.condition_met is not None:
    match demuxed_stream.condition_met.name:
      case 'SuccessfulMessageStream':
        foo(data_stream)
      case 'FailedMessageStream':
        foo2(data_stream)
  else:
    foo3(data_stream)
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
>>> y = FilterCondition(lambda x: x == 2)
>>> splt = OrderedDemuxer(data_source=iter(x), filter=y, split_after=True)
>>> x_iter = splt.__next__()
>>> print(list(x_iter))
  [1, 2]
```
