This is a collection for notes about resources I had to look up while building
this.

## Python datetime, math, and regex

How to read datetime

http://stackoverflow.com/questions/19068269/how-to-convert-a-string-date-into-datetime-format-in-python

Test regular expressions online. I use this all the same, and this project
is no different.

http://pythex.org/

Project structuring suggestions.

http://learnpythonthehardway.org/book/ex46.html

#### Custom Iterables

Make a custom iterable list

http://stackoverflow.com/questions/19151/how-to-make-class-iterable

Iterate over just first 3

http://stackoverflow.com/questions/2702158/fast-iterating-over-first-n-items-of-an-iterable-not-a-list-in-python

## Models

#### GPX standards

Here are some details about the format in general:

http://www.topografix.com/gpx_manual.asp

#### Coordinate calculations

Brew up calculations for distances between points:

http://stackoverflow.com/questions/15736995/how-can-i-quickly-estimate-the-distance-between-two-latitude-longitude-points

## Iterables

When I first started this, I approached it with the tremendously unpythonic
method of creating an iterator that went through the file list by maintaining
an integer index inside of the iterable class.

After a lot of searching, this was the post that answered my questions
about how python iterables ultimately work.

http://www.shutupandship.com/2012/01/understanding-python-iterables-and.html

If you have a list, you can iterate in a "for x in a" block, or you can
manually do that work with code like the following:

```python
ia = iter(a)
while True:
	try:
		x = ia.__next__()
		# do stuff with x
	except StopIteration:
		break
```
