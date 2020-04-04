from PIL import Image, ImageDraw, ImageFont, ImageChops
import datetime


class MemeViolation(object):

    X_LOCATIONS = [
        (28, 149),
        (27, 189),
        (28, 223),
        (29, 262),
        (28, 302),
        (284, 149),
        (282, 184),
        (281, 220),
        (285, 258),
        (286, 300),
    ]

    TEXT_LOCATION = [
        (386, 298),
        (73, 347),
        (221, 347),
        (415, 347),
    ]

    def __init__(self, offenses, issuer, other_text=''):
        vals = [i+1 in offenses for i in range(10)]
        if other_text != '':
            vals[9] = True
        self.offenses = vals
        self.issuer = str(issuer)
        self.othertext = other_text

    def generate(self):
        mv_img = Image.open('assets/memeviolation.jpg')
        x_img = Image.open('assets/x.png')

        title_font = ImageFont.truetype('arial', 15)

        for isoffense, loc in zip(self.offenses, MemeViolation.X_LOCATIONS):
            if isoffense:
                x, y = loc
                x -= 20
                y -= 22
                mv_img.paste(x_img, (x, y), x_img)

        draw = ImageDraw.Draw(mv_img)

        # font = ImageFont.truetype('arial', 10)
        _, h = draw.textsize('test', font=title_font)

        draw.text(MemeViolation.center(MemeViolation.TEXT_LOCATION[0], h=h),
                  self.othertext, fill=(0, 0, 0), font=title_font)
        draw.text(MemeViolation.center(MemeViolation.TEXT_LOCATION[1], h=h),
                  str(datetime.date.today()), fill=(0, 0, 0), font=title_font)
        draw.text(MemeViolation.center(MemeViolation.TEXT_LOCATION[2], h=h),
                  datetime.datetime.now().strftime('%H:%M'), fill=(0, 0, 0), font=title_font)
        draw.text(MemeViolation.center(MemeViolation.TEXT_LOCATION[3], h=h),
                  self.issuer, fill=(0, 0, 0), font=title_font)
        # draw.text((10, 10), "Meme Violation: ", fill=(0, 0, 0), fnt=title_font)
        # line_width = 5
        # draw.line(((0, 50), (400, 50)), width=line_width, fill='black')
        # draw.line(((0, 180), (400, 180)), width=line_width, fill='black')

        # mv_img.save('pil_text.png')
        return mv_img

    @staticmethod
    def center(anchor, w=None, h=None):
        x, y = anchor
        if h:
            y -= h // 2
        if w:
            x -= w // 2

        return x, y

