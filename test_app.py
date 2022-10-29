import skimage.io
import base64
from Image import PIL
from io import BytesIO
import app
def encodeBase64Image(image: PIL.Image) -> str:
    # https://stackoverflow.com/questions/31826335/how-to-convert-pil-image-image-object-to-base64-string
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
def decodeBase64Image(imageStr: str, name: str) -> PIL.Image:
    image = PIL.Image.open(BytesIO(base64.decodebytes(bytes(imageStr, "utf-8"))))
    print(f'Decoded image "{name}": {image.format} {image.width}x{image.height}')
    return image
image  = skimage.io.imread('assets/source.png')
image_base64 = encodeBase64Image(image)
# request.json({'image':image_base64})

if 'bounce back experiment' and True:
    app.init()
    response = app.inference({'image':image_base64})
    image = decodeBase64Image(response['original_image'], 'bounce-back-experiment')
    skimage.io.imsave('bounce_back_image.png',image)
    
