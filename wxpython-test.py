import wx
app = wx.App()  # Need to create an App instance before doing anything
screen = wx.ScreenDC()
print(app)
size = screen.GetSize()
bmp = wx.Bitmap(size[0], size[1])
mem = wx.MemoryDC(bmp)
mem.Blit(0, 0, size[0], size[1], screen, 0, 0)
del mem  # Release bitmap
bmp.SaveFile('screenshot.png', wx.BITMAP_TYPE_PNG)
