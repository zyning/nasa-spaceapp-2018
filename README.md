## “Vigil”: Detecting Fire and Notifying People within 10 s

## Problem

Wildfire incidents across the world remain as one of the leading causes of death that threatens human safety.

To address this problem, we developed `Vigil`, a predictive analytics system for forecasting and prioritizing Fire Inspections in the forests. The system provides insightful suggestions to help fire departments have a better plan on their fire fighting strategies. Last but not least, it helps indoor and outdoor fire prevention and alarm systems to better identify their customers.

There are serval points we are seriosely considering during the development of our project.

(1)  Ecosystem: A wildfire is a fire in an area of combustible vegetation that occurs in rural areas. Depending on the type of vegetation where it occurs, a wildfire can also be classified more specifically as a brush fire, bush fire, desert fire, forest fire, grass fire, hill fire, peat fire, vegetation fire, and veld fire. Wildfire’s occurrence throughout the history of terrestrial life invites conjecture that fire must have had pronounced evolutionary effects on most ecosystems' flora and fauna. Wildfires are common in climates that are sufficiently moist to allow the growth of vegetation but feature extended dry, hot periods. Such places include the vegetated areas of Australia and Southeast Asia, the veld in southern Africa, the fynbos in the Western Cape of South Africa, the forested areas of the United States and Canada, and the Mediterranean Basin.

(2) Demographic and economic characteristics: as wildfire are mostly happened in the rural forest with poor public amenities where people are more likely to go for their vacations, it increased the difficulties for rescuing people and directing escape route on time.   

(3) Weather conditions: we hypothesized that the various weather features, in particular temperature and precipitation, would be a good proxy on the use of heater, AC. Other weather features like snow, wind, rain would commonly reflect some human behavioral attitudes towards staying at home. 

Our capacity to understand and evaluate our methods is bound by availability of contextual relevant data in different forests. To overcome the challenge of accessing to local and real data, our study test the theoretical models using the public data from NASA and posts from social media platforms. In this project, we conducted a series of experiments to demonstrate how we collected, filtered and merged different sources of data from open data portals to develop our predictive dashboard.  

# What does it do?

By improving connectivity between individuals, social medias, NASA's database, drones and other aircrafts, and firefighters, the wildfires can be detected within 10 s.

# How to Detect Wildfires and Notify People around Fires within 10 s

- 10 s before the Fire: Infer the Possibility of Wildfires by Climate Data 

   Home-made Code: https://github.com/zyning/nasa-spaceapp-2018/tree/master/FirePrediction
   
   Predicting Daily Fire Occurence: https://github.com/zyning/nasa-spaceapp-2018/blob/master/Prediction%20of%20Daily%20Fire%20Occurrence%20.pdf
   
   Third Party Code: https://github.com/zyning/nasa-spaceapp-2018/tree/master/Spaceapps/NASA_Spaceapps
   
   Climate Data: http://climatedata.us/#map
   
- 8 s before the Fire: Start Launching Drones and Other Aircrafts to Detect and Verify the Fires 

   Detecting Fires from the Sky: https://github.com/zyning/nasa-spaceapp-2018/blob/master/Detecting%20Fires%20from%20the%20Sky.pdf
   
- 3 s before the Fire: Potential Fire Alarms through Third Party Social Media

   Potential Collaboration Partner: https://twitter.com/wildfiretoday?lang=en
   
- 3 s after the Fire: Report a Fire through Geolocated Social Media Posts

   Home-made Code with 84.27% Accuracy on Validation Set: https://github.com/zyning/nasa-spaceapp-2018/tree/master/NASA
   
   Report for Wildfire Detection, Identification, and Visualization: https://github.com/zyning/nasa-spaceapp-2018/blob/master/NASA/NASA_report(1).pdf
   
- 5 s after the Fire: Drones and Other Aircrafts Provide Real Time Information about How a Fire is Unfolding

   Home-made Drone: https://github.com/zyning/nasa-spaceapp-2018/blob/master/Drone.pdf
   
- 7 s after the Fire: Social Medias Alert People around the Fire and Show Potential Exits and Entry Points

   Potential Collaboration Partner: Google Maps, Facebook, Twitter, Instagram, Snapchat
   
- 10 s after the Fire: Call for Firefighters. 

   Our mission, as Vigil (a Latin word, means "watchman who alerts fireman in Rome"), has accomplished

Inspired by the idea that social media platforms can be used to detect and locate disasters, we are seeing social media users as individual sensors to detect disasters. Based on the model of two branch neural network, we design our model that consists of a LSTM network and a 3 layer Convolutional neural network to identify wildfire from
crowd-souring materials including texts, photos and videos.

After obtaining the location of where users are and the identification of wildfire, we are designing to use drones to participate in rescuing people by lively fire detection and air quality monitoring, and provide best escape route for users.  


## Data 

In this section, we describe each of the datasets that we have used. This project relies on open data sources from social media platforms and other open sorce data provided by NASA. The main data sources that we used in the project are the following: 

* NASA climate data:  http://climatedata.us/#map

* Social Media: Due to the limited time we have from the Space App Challenge, we only filtered out 1400 posts with texts, images along with geo-coordinates attached as training set from social media platforms including Twitter and Flicker about hashtags #wildfire #CaliforniaWildFire #wildfires, and averagely split them into four categories: fireman, grassland fire, fire live scenes and smoky air caused by wildfires. Meanwhile, we randomly selected 50 posts from each categories for validation purpose.

* Fire Information for Resource Management System (FIRMS): Historic wildfire data for  prediction.
