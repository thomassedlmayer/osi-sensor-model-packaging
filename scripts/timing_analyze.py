import json
import numpy as np

timing_json_path = '/home/martin/development/flatbuf_test_data/flatb_builder/OSMPDummySensor_flatbuf_timing_11-18-45.json'
#timing_json_path = '/home/martin/development/flatbuf_test_data/flatb_builder/OSMPDummySource_flatbuf_timing_11-18-45.json'

#timing_json_path = '/tmp/OSMPDummySensor_Protobuf_timing_15-29-42.json'
#timing_json_path = '/tmp/OSMPDummySource_Protobuf_timing_15-29-41.json'

# Opening JSON file
f = open(timing_json_path)
  
# returns JSON object as 
# a dictionary
data = json.load(f)

if 'OSMPDummySensor' in data['Data'][0]['Instance']['ModelIdentity']:
    startEvent = 2
    nextEvent = 2
    eventCount = int(4)
    timeStrings = ['Model deserialize', 'Model calculation', 'Model serialize', 'Total']
else:
    startEvent = 0
    nextEvent = 0
    eventCount = int(3)
    timeStrings = ['Source generate', 'Source serialize', 'Total']

numTimeSteps = len(data['Data'][0]['OsiEvents']) // eventCount
timingMat = np.zeros((numTimeSteps, eventCount - 1))
matIdx = 0
prevTimeStamp = 0

# Iterating through the json
# list
for event in data['Data'][0]['OsiEvents']:
    if event[0] != nextEvent:
        print('Error in log event sequence')
        break
    curTimeStamp = event[1]
    if event[0] != startEvent:
        timingMat[np.unravel_index(matIdx, timingMat.shape)] = curTimeStamp - prevTimeStamp
        matIdx += 1

    nextEvent += 1
    nextEvent = nextEvent % eventCount
    prevTimeStamp = curTimeStamp

timingAvg = timingMat.sum(axis = 0) / numTimeSteps
timingAvg = np.append(timingAvg, timingAvg.sum())
timingMin = timingMat.min(axis = 0)
timingMax = timingMat.max(axis = 0)
print(timeStrings)
print(timingAvg)

# Closing file
f.close()