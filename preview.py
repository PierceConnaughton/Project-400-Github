from turtle import width
from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap

def createPreview(tweet, name, username):
    #Set the font to be tweet font
    fontUserInfo = ImageFont.truetype("arial.ttf", 90, encoding="utf-8")
    fontUserText = ImageFont.truetype("arial.ttf", 110, encoding="utf-8")

    #Set the dimensions of the image
    wth = 2376
    hght = 1250

    #Set the colors of the image
    colorBg = 'black'
    colorUser = 'white'
    colorTag = (64, 64, 64)
    colorText = 'white'

    #Set the coordinates of everything on the tweet
    corPhoto = (250, 170)
    corName = (600, 185)
    corTag = (600, 305)
    corText = (250, 510)

    #Set space between lines
    lineMargin = 15

    #Set the username, tag, text and name of final image
    userName = name
    userTag = "@" + username
    text = tweet
    imgName = "tweet"

    #Create the lines of text for the image
    text_string_lines = wrap(text, 37)
    x = corText[0]
    y = corText[1]

    temp_img = Image.new('RGB', (0, 0))
    temp_img_draw_interf = ImageDraw.Draw(temp_img)

    #Get the height of the total text needed for drawing onto the image
    line_height = [
        temp_img_draw_interf.textsize(text_string_lines[i], font = fontUserText)[1]
        for i in range(len(text_string_lines))
    ]

    # Create the final image and draw the interface
    img = Image.new('RGB', (wth, hght), color='black')
    draw_interf = ImageDraw.Draw(img)

    # Draw the user name and user handle
    draw_interf.text(corName, userName, font=fontUserInfo, fill=colorUser)
    draw_interf.text(corTag, userTag, font=fontUserInfo, fill=colorTag)


    #Draw the lines of the tweet
    for index, line in enumerate(text_string_lines):
        draw_interf.text((x, y), line, font=fontUserText, fill=colorText)
        y += line_height[index] + lineMargin

    #Load the users photo and paste the photo onto the image
    #Then save the image
    userPhoto = Image.open('profile-modified.png', 'r')
    img.paste(userPhoto, corPhoto, mask=userPhoto)
    img.save(f'{imgName}.png')

    return img
