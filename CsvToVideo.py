import csv
from MusicVideo import MusicVideo

class CsvToVideo:
    def timestamp_to_seconds(self, timestamp):        
        seconds = 0
        multipliers = [3600, 600, 60, 10, 1]
        counter = 0
        for t in timestamp:
            if t != ":":
                seconds = seconds + (multipliers[counter] * int(t))
                counter = counter + 1
        return seconds


    def read_csv(self, file_path):
        videos = []
        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    if row[1] != "":
                        videos.append(MusicVideo(row[1], row[2], row[3], self.timestamp_to_seconds(row[4])))
                    line_count += 1
        return videos

    