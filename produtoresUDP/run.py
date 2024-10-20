import subprocess

if __name__ == '__main__':
    movie = subprocess.Popen(["python", "movie_producer.py"])
    sports = subprocess.Popen(["python", "sport_producer.py"])
    movie.wait()
    sports.wait()
