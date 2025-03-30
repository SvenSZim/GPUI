from ui import LayoutManager, ElementCore, Rect


myBod: ElementCore = ElementCore(Rect((20, 90), (40, 190)))
myBod2: ElementCore = ElementCore(Rect((200, 100), (200, 100)))
myBod3: ElementCore = ElementCore(Rect((300, 100), (200, 100)))
myBod.align(myBod2, 0)
myBod.align(myBod3, 1)
LayoutManager.applyLayout()


print('\n1', myBod.getBody())
print('\n2', myBod2.getBody())
