from Image import PIL
import base64 
from io import BytesIO
TODO = False
def decodeBase64Image(imageStr: str, name: str) -> PIL.Image:
    image = PIL.Image.open(BytesIO(base64.decodebytes(bytes(imageStr, "utf-8"))))
    print(f'Decoded image "{name}": {image.format} {image.width}x{image.height}')
    return image

def init():
    '''
    creates the globals that will be used every call
    '''
    global model 
    model = None
    pass
def inference(all_inputs:dict) -> dict:
    '''
    takes in dict created from request json, outputs dict
    to be wrapped up into a response json
    '''
    global model
    assert 'image' in all_inputs, 'TODO: what to do if image is not there?'
    image = all_inputs.get("image", None)
    image = decodeBase64Image(image)
    if False and 'prod':
        with torch.inference_mode():
            TODO
        #TODO: conversion of video to base64? 
        #TODO: or storage to google bucket and send back the link?
        return {'results':TODO}
    elif True and 'DEBUG: send back the original image':
        def encodeBase64Image(image: PIL.Image, name: str) -> str:
            # https://stackoverflow.com/questions/31826335/how-to-convert-pil-image-image-object-to-base64-string
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue())
        img_str = encodeBase64Image(image: PIL.Image, name: str)
        return {'original_image':img_str}
        
