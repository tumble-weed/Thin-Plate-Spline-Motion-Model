# based on https://docs.banana.dev/banana-docs/core-concepts/sdks/python
import banana_dev as banana
import base64
TODO = None

api_key = TODO
model_key = TODO
model_inputs = {'image':TODO} # anything you want to send to your model

out = banana.run(api_key, model_key, model_inputs)

print(out)
#TODO: convert out back to video and display
fh = open("video.mp4", "wb")
fh.write(base64.b64decode(out['result']))
fh.close()
