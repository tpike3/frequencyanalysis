# frequencyanalysis
code for event frequency analysis 

Code conducts frequency of event data for five biltateral relationships using the Integrated Confliect Early Warning System (ICEWs) data

ICEWs data was downladed ~ 17 March 2017

To run user will need to:

1. Download ICEWS data from Harvard Dataverse 
https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/28075

2. Unzip ICEWS data and save to local file folder (should be in same file as attached code)

3. Change line 31 in the code ("for file in glob.glob("dataverse_files/*"):") to 
"for file in glob.glob("YOURFILEOFUNZIPPEDICEWSDATA/*"): (replace caps with your file folder of ICEWS data
and make sure ICEWs folder in the same file as the code) 

