import requests
import datetime

# Twitch Client-ID
CLIENT_ID = "DEINE_API_CLIENT_ID"

# Channel Namen
channel1_name = "papaplatte"
channel2_name = "shroud"

# Start- und Enddatum für den Vergleich
start_date = datetime.date(2024, 1, 1)
end_date = datetime.date(2024, 5, 3)

def get_channel_stats(channel_name, start_date, end_date):

    url = f"https://api.twitch.tv/helix/users?login={channel_name}"
    headers = {"Client-ID": CLIENT_ID}
    response = requests.get(url, headers=headers)
    data = response.json()
    if response.status_code == 200 and "data" in data:
        user_id = data["data"][0]["id"]

        # Stream-Statistiken abrufen
        url = f"https://api.twitch.tv/helix/streams?user_id={user_id}"
        headers = {"Client-ID": CLIENT_ID}
        response = requests.get(url, headers=headers)
        data = response.json()

        if "data" in data and data["data"]:
            streams = data["data"]
            longest_stream = max(streams, key=lambda stream: stream["duration"])
            average_viewers = sum(stream["viewer_count"] for stream in streams) / len(streams)
            max_viewers = max(stream["viewer_count"] for stream in streams)
            filtered_streams = [stream for stream in streams
                                if start_date <= datetime.datetime.fromisoformat(stream["started_at"]).date() <= end_date]
            stream_count = len(filtered_streams)
            total_stream_minutes = sum((min(end_date, datetime.datetime.fromisoformat(stream["ended_at"]).date()) - max(start_date, datetime.datetime.fromisoformat(stream["started_at"]).date())).total_seconds() / 60
                                       for stream in streams if "ended_at" in stream and datetime.datetime.fromisoformat(stream["started_at"]).date() <= end_date and datetime.datetime.fromisoformat(stream["ended_at"]).date() >= start_date)
            longest_stream_minutes = longest_stream["duration"] // 60
            longest_stream_hours = longest_stream_minutes // 60
            total_stream_hours = total_stream_minutes // 60

            return {
                "stream_count": stream_count,
                "longest_stream_minutes": longest_stream_minutes,
                "longest_stream_hours": longest_stream_hours,
                "average_viewers": average_viewers,
                "max_viewers": max_viewers,
                "total_stream_minutes": total_stream_minutes,
                "total_stream_hours": total_stream_hours
            }
    else:
        print(f"Fehler beim Abrufen von Kanalinformationen für {channel_name}.")
        print(f"Status Code: {response.status_code}")  # Debugging Fehlercode
        return None


# Statistiken abrufen
channel1_stats = get_channel_stats(channel1_name, start_date, end_date)
channel2_stats = get_channel_stats(channel2_name, start_date, end_date)

# Statistiken ausgeben
print(f"Statistikvergleich vom {start_date.strftime('%d.%m.%Y')} bis zum {end_date.strftime('%d.%m.%Y')}:")
print(f"Channel - {channel1_name}:")
if channel1_stats:
    print(f"  - Anzahl Streams: {channel1_stats['stream_count']}")
    print(f"  - Längster Stream: {channel1_stats['longest_stream_hours']} Stunden und {channel1_stats['longest_stream_minutes'] % 60} Minuten")
    print(f"  - Durchschnittliche Zuschauer: {channel1_stats['average_viewers']}")
    print(f"  - Maximale Zuschauer: {channel1_stats['max_viewers']}")
    print(f"  - Gesamtzahl der gestreamten Zeit: {channel1_stats['total_stream_hours']} Stunden und {channel1_stats['total_stream_minutes'] % 60} Minuten")
else:
    print("Keine Daten verfügbar")
print(f"Channel - {channel2_name}:")
if channel2_stats:
    print(f"  - Anzahl Streams: {channel2_stats['stream_count']}")
    print(f"  - Längster Stream: {channel2_stats['longest_stream_hours']} Stunden und {channel2_stats['longest_stream_minutes'] % 60} Minuten")
    print(f"  - Durchschnittliche Zuschauer: {channel2_stats['average_viewers']}")
    print(f"  - Maximale Zuschauer: {channel2_stats['max_viewers']}")
    print(f"  - Gesamtzahl der gestreamten Zeit: {channel2_stats['total_stream_hours']} Stunden und {channel2_stats['total_stream_minutes'] % 60} Minuten")
else:
    print("Keine Daten verfügbar")

# Vergleich der Ergebnisse
if channel1_stats and channel2_stats:
    # Streams
    if channel1_stats["stream_count"] > channel2_stats["stream_count"]:
        print(f"\n{channel1_name} hat mehr Streams ({channel1_stats['stream_count']}) als {channel2_name} ({channel2_stats['stream_count']}).")
    elif channel1_stats["stream_count"] < channel2_stats["stream_count"]:
        print(f"\n{channel2_name} hat mehr Streams ({channel2_stats['stream_count']}) als {channel1_name} ({channel1_stats['stream_count']}).")
    else:
        print(f"\n{channel1_name} und {channel2_name} haben die gleiche Anzahl an Streams ({channel1_stats['stream_count']}).")

    # Längster Stream
    if channel1_stats["longest_stream_hours"] > channel2_stats["longest_stream_hours"]:
        print(f"{channel1_name} hat den längsten Stream ({channel1_stats['longest_stream_hours']} Stunden und {channel1_stats['longest_stream_minutes'] % 60} Minuten) im Vergleich zu {channel2_name} ({channel2_stats['longest_stream_hours']} Stunden und {channel2_stats['longest_stream_minutes'] % 60} Minuten).")
    elif channel1_stats["longest_stream_hours"] < channel2_stats["longest_stream_hours"]:
        print(f"{channel2_name} hat den längsten Stream ({channel2_stats['longest_stream_hours']} Stunden und {channel2_stats['longest_stream_minutes'] % 60} Minuten) im Vergleich zu {channel1_name} ({channel1_stats['longest_stream_hours']} Stunden und {channel1_stats['longest_stream_minutes'] % 60} Minuten).")
    else:
        print(f"{channel1_name} und {channel2_name} haben die gleiche Länge des längsten Streams ({channel1_stats['longest_stream_hours']} Stunden und {channel1_stats['longest_stream_minutes'] % 60} Minuten).")

    # Durchschnittliche Zuschauer
    if channel1_stats["average_viewers"] > channel2_stats["average_viewers"]:
        print(f"{channel1_name} hat durchschnittlich mehr Zuschauer ({channel1_stats['average_viewers']}) als {channel2_name} ({channel2_stats['average_viewers']}).")
    elif channel1_stats["average_viewers"] < channel2_stats["average_viewers"]:
        print(f"{channel2_name} hat durchschnittlich mehr Zuschauer ({channel2_stats['average_viewers']}) als {channel1_name} ({channel1_stats['average_viewers']}).")
    else:
        print(f"{channel1_name} und {channel2_name} haben die gleiche durchschnittliche Zuschauerzahl ({channel1_stats['average_viewers']}).")

    # Maximale Zuschauer
    if channel1_stats["max_viewers"] > channel2_stats["max_viewers"]:
        print(f"{channel1_name} hatte maximal mehr Zuschauer ({channel1_stats['max_viewers']}) als {channel2_name} ({channel2_stats['max_viewers']}).")
    elif channel1_stats["max_viewers"] < channel2_stats["max_viewers"]:
        print(f"{channel2_name} hatte maximal mehr Zuschauer ({channel2_stats['max_viewers']}) als {channel1_name} ({channel1_stats['max_viewers']}).")
    else:
        print(f"{channel1_name} und {channel2_name} hatten maximal die gleiche Zuschauerzahl ({channel1_stats['max_viewers']}).")

    # Gesamtzahl der gestreamten Zeit
    if channel1_stats["total_stream_hours"] > channel2_stats["total_stream_hours"]:
        print(f"{channel1_name} hat insgesamt mehr gestreamt ({channel1_stats['total_stream_hours']} Stunden und {channel1_stats['total_stream_minutes'] % 60} Minuten) als {channel2_name} ({channel2_stats['total_stream_hours']} Stunden und {channel2_stats['total_stream_minutes'] % 60} Minuten).")
    elif channel1_stats["total_stream_hours"] < channel2_stats["total_stream_hours"]:
        print(f"{channel2_name} hat insgesamt mehr gestreamt ({channel2_stats['total_stream_hours']} Stunden und {channel2_stats['total_stream_minutes'] % 60} Minuten) als {channel1_name} ({channel1_stats['total_stream_hours']} Stunden und {channel1_stats['total_stream_minutes'] % 60} Minuten).")
    else:
        print(f"{channel1_name} und {channel2_name} haben insgesamt gleich lang gestreamt ({channel1_stats['total_stream_hours']} Stunden und {channel1_stats['total_stream_minutes'] % 60} Minuten).")
