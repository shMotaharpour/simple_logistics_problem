## Terminology:
• Mission: A mission is indeed a geographical location within a route with specific
coordinates (latitude and longitude), id, and timestamp. The mission id is a unique string
which is dedicated only to the mission, and its timestamp is the time which the vehicle
visits the mission in the route.
• Delivery: A new delivery is also a geographical location which is not inside a route
• but without a specified route. It has only coordinates (latitude and longitude) and id.
• Route: A route is a series of missions in order (based on their timestamp) with specific
id and missions. The route index is an integer value specified
## Question:
Consider a case in which there are 3 routes and 7 new deliveries. Each of the routes
contains some missions and can accept only 3 more deliveries (has a capacity of 3). Our
goal is to assign each of the new deliveries to the route with minimum travel time
considering its capacity. The vehicle capacity is 10 m/s (36 km/h).
### Note:
Using Haversine distance instead of Euclidian distance is optional but not mandatory.
## Data:
The routes and deliveries data is provided as two json files (one for routes and the other
for deliveries)
