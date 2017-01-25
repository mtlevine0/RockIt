#!/usr/bin/env python
import pika
import sys
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)


with open('songs.json') as songs_file:
    songs = json.load(songs_file)
    for song in songs['items']:
        songID = song['contentDetails']['videoId']
        message = "https://www.youtube.com/watch?v=" + songID
        channel.basic_publish(exchange='',
                              routing_key='task_queue',
                              body=message,
                              properties=pika.BasicProperties(
                                 delivery_mode = 2, # make message persistent
                              ))
        print(" [x] Sent %r" % message)
connection.close()