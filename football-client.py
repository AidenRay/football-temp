import bme280
from Adafruit_IO import Client, Data, MQTTClient
import time
import random
# Set to your Adafruit IO key & username below.
ADAFRUIT_IO_KEY      = 'b12192c3b0d74edf98a2c0433fb508d6'
ADAFRUIT_IO_USERNAME = 'aidenray'



# Define callback functions which will be called when certain events happen.
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to feed changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print('Connected to Adafruit IO!  Listening for DemoFeed changes...')
    # Subscribe to changes on a feed named DemoFeed.
    client.subscribe('DemoFeed')




def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload):
    # Message function will be called when a subscribed feed has a new value.
    # The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.
    print('Feed {0} received new value: {1}'.format(feed_id, payload))


# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message

# Connect to the Adafruit IO server.
client.connect()

# Now the program needs to use a client loop function to ensure messages are
# sent and received.  There are a few options for driving the message loop,
# depending on what your program needs to do.

# The first option is to run a thread in the background so you can continue
# doing things in your program.
client.loop_background()
# Now send new values every 10 seconds.
print('Publishing a new message every 10 seconds (press Ctrl-C to quit)...')
while True:
    temperature,pressure,humidity = bme280.readBME280All()
    board_temp = bme280.on_board_temp()
    
    print('Publishing {0} to DemoFeed.'.format(temperature))
    client.publish('bme-temp', temperature)
    
    print('Publishing {0} to DemoFeed.'.format(pressure))
    client.publish('bme-pressure', pressure)
    
    print('Publishing {0} to DemoFeed.'.format(humidity))
    client.publish('bme-humidity', humidity)
    
    print('Publishing {0} to DemoFeed.'.format(board_temp))
    client.publish('rpi-chip-temp', board_temp)
    time.sleep(10)


#aio = Client(ADAFRUIT_IO_KEY)

#temperature,pressure,humidity = bme280.readBME280All()


#data = Data(value=temperature)
#aio.create_data('test',data)
#aio.send('F00','bar')

#data = aio.receive('test')
#print('Retrieved value from test has attributes: {0}'.format(data))
#print('Latest value from test: {0}'.format(data.value))
