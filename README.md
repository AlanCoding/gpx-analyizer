# GPX Stats Project

This is my project to gobble up some personal Garmin navigator data.
Its point is to be a data grinder for anyone who owns a navigation unit 
and drives around with it regularly. The kinds of questions it hopes to 
eventually answer are things like:

 - Where places did you visit most?
 - What speeds do you typically drive at?
 - What are the highest elevations you drive to?
 - What's the hardest you've ever braked?

### Site Map

For research about some related resources, see [the notes page](docs/Notes.md).
For some pretty graphs see [the data analysis examples](docs/data_examples.md).

## Instructions

Did you know that your GPS unit is probably storing a record of everywhere 
you go? Creeped out? Turn those lemons into lemonade today.

### "In Real Life" Instructions

Plug in your Garmin unit to your computer and copy over the files in the
gpx archive folder into the archive folder of this project. These should
follow a filename pattern like:

 - 1.gpx
 - 2.gpx
 - 3.gpx
 
The unit will store these sequentially as you drive, but it will delete 
old ones as it accumulates new data. Thus, I can't predict what numbers
you will see.

### Python Instructions

You must put them in the archive folder with this naming. Then you can run the
analyzer with `python analyze.py`. Or, you can import the python module, and
then use it kind of like this:

```python
from gpxstats.objects import Archive

archive = Archive('archive/')

for pt in archive:
    print(pt.speed)
```

## Questions

How can we take our extremely obvious intuition and apply it to a large set
of data like this? Some boundaries are easy to draw. I'm pretty sure my car
never went 1,000 miles per hour, so if we see that, it's safe to say that we
can mark some points as invalid. But our intuition is much more detailed than
this.


## Discoveries about Archive Character

Understanding exactly what type of thing a GPS unit stores is a trial and 
error process.

### Packaged speed values

The Garmin units appear to record speed only in specific increments. These
increments seem to be 1.37 or 1.38, depending on how the rounding works out.
Here are a few of the first set of speeds that the unit uses:

    1.37, 2.75, 4.12, 5.49, 6.86, 8.24, 9.61, 10.98, 12.35, 13.73, 15.1, 16.47

In terms of units, there are almost certainly in terms of meters per second.

### Data Imperfections

As of version 0.1, we can get a list of the top attributes for various fields.
Many of these just demonstrate where the data is bad. I will explain this 
point-by-point.

#### Elevation

I found about 9 clusters of highly negative elevation values. Again, no, 
I did not drive into Death Vally or something real like that. These are data 
artifacts that will eventually need to get ironed out somehow.

## Roadmap

Future features:

 - Data cleaning process that will drop a point if there is something 
   suspicious about it
 - Segment-based objects that will store information about driving between 
   stops
 - Trip and destination based objects

The final point is the spiffy ultimate goal, but the intermediate steps 
remain a little more murky. Should we store all segments in an array for 
the entire archive? That's not entirely clear.
