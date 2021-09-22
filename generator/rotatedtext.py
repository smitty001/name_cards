# rotatedtext.py
from reportlab.platypus.flowables import Flowable


class verticalText(Flowable):

    def __init__(self, text):
        Flowable.__init__(self)
        self.text = text

    def draw(self):
        canvas = self.canv
        canvas.rotate(180)
        fs = canvas._fontsize
        canvas.translate(1, -fs/1.2)
        canvas.drawString(0, 0, self.text)

    def wrap(self, aW, aH):
        canv = self.canv
        fn, fs = canv._fontname, canv._fontsize
        return canv._leading, 1 + canv.stringWidth(self.text, fn, fs)