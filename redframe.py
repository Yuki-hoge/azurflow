import wx, threading, time
class myFrame(wx.Frame):
    def __init__(self, parent, title, x, y, w, h):
        wx.Frame.__init__(self, parent, title=title,style = wx.FRAME_SHAPED | wx.STAY_ON_TOP)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        image = wx.Image('redwhiteframe.png', wx.BITMAP_TYPE_PNG)
        image = image.Scale(w, h, wx.IMAGE_QUALITY_HIGH)
        self.bitmap = image.ConvertToBitmap()

        self.SetClientSize(image.GetSize())
        region = wx.Region(self.bitmap,wx.Colour(255,255,255))
        self.SetShape(region)
        self.SetPosition(wx.Point(x, y))

    def OnPaint(self, event=None):
        deviceContext = wx.PaintDC(self)
        deviceContext.DrawBitmap(self.bitmap, 0, 0, True)

def show_redframe(x, y, w, h):
  app = wx.App(False)
  frame = myFrame(None, "none", x, y, w, h)
  frame.Show()
  app.MainLoop()

if __name__ == '__main__':
  show_redframe(300, 300, 400, 400)
