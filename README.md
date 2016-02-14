# gpx-analyizer
Project to gobble up some personal Garmin navigator data.

For research about some related resources, see [the notes page](docs/Notes.md).
For some pretty graphs, I hope to have an iPython notebook soon.
Will also look into a compilation of sample outputs as well.

## Instructions

Plug in your Garmin unit to your computer and copy over the files in the
gpx archive folder into the archive folder of this project. These should
follow a filename pattern like:

 - 1.gpx
 - 2.gpx
 - 3.gpx

You must put them in the archive folder with this naming. Then you can run the
analyzer with `python analyze.py`. Or, you can import the python module, and
then use it kind of like this:

```python
from alancodinggpx.objects import Archive

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


## Discoveries

## Packaged speed values

The Garmin units appear to record speed only in specific increments. These
increments seem to be 1.37 or 1.38, depending on how the rounding works out.
Here are a few of the first set of speeds that the unit uses:

    1.37, 2.75, 4.12, 5.49, 6.86, 8.24, 9.61, 10.98, 12.35, 13.73, 15.1, 16.47

In terms of units, there are almost certainly in terms of meters per second.

## Example outputs

Here is my own speed histogram, using bins defined by the native storage
method of speeds in the Garmin unit. These are converted to mph units below.

		upper_bound      frequency
		3.0646  ######################
		6.1516  ################################
		9.2162  ###############################################
		12.2808 ###########################################################################
		15.3454 ###################################################################
		18.4324 ####################################################
		21.497  ##########################################
		24.5616 ####################################
		27.6262 ##################################
		30.7132 #####################################
		33.7778 ####################################
		36.8424 #######################################
		39.907  ######################################
		42.994  ##################################
		46.0586 ###########################
		49.1232 #######################
		52.1878 #####################
		55.2748 #####################
		58.3394 ######################
		61.404  ######################
		64.4686 ###########################
		67.5556 #########################
		70.6202 #################
		73.6848 ########
		76.7494 ##
		79.8364
		82.901
		95.1818
		101.311
		104.398
		122.808
		150.4342

Why does the upper scale go up to 150 mph? Because it had data for that speed.
No, I assure you I never drove this fast. It's a numerical error that sometimes
pops up. This is out of >250,000 speed points, so it's not unreasonable that
it produced a dozen outliers due to equipment malfunction. I'm interested
to find out more about this small number of points. It seems likely that
those points were closer to the detection limits, so we would expect service
cutoff or other sporadic behavior around those points.
