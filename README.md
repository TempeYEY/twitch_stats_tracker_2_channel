Twitch Channel Statistics Comparison Script
This Python script utilizes the Twitch API to compare the streaming statistics of two specified Twitch channels over a defined time period. It provides insights into various metrics such as the number of streams, the longest stream duration, average viewership, maximum viewership, and total streaming time.

Features:

Stream Count: 
Compares the number of streams between two channels.
Longest Stream: 
Identifies which channel had the longest stream and its duration.
Average Viewership: 
Compares the average number of viewers across all streams.
Maximum Viewership: 
Identifies which channel had the highest peak viewership.
Total Streaming Time: 
Calculates the total duration each channel spent streaming.

How to Use:

Specify the Twitch usernames of the channels you want to compare.
Set the start and end dates for the comparison period.
Run the script to fetch and display the statistics.

Requirements:

Python 3.x
Requests library (pip install requests)

Instructions:

Obtain a Twitch Client-ID by registering a Twitch application.
Replace CLIENT_ID in the script with your Twitch Client-ID.
Execute the script and view the comparison results.

Example:

python twitch_stats_tracker_2_channel.py

Note:

This script requires a valid Twitch Client-ID to access the Twitch API.
The script may need adjustments based on changes to the Twitch API or your specific requirements.
Feel free to modify and enhance the script according to your needs!
