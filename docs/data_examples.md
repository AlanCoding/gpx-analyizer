# Example Outputs

### Speed Histograms

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