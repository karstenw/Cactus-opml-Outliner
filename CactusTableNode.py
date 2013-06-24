
class CactusTableNode(NSObject):
    def __new__(cls, *args, **kwargs):
        return cls.alloc().init()

    def __repr__(self):
        return "<OutlineNode(%i, name='%s')" % (self.nodenr, self.name)

    def __init__(self, name, obj, parent, rootNode):
        self.initphase = True

        # this is outlinetype, not valueType
        self.typ = typ

        self.maxHeight = 1
        self.setParent_(parent)
        self.rootNode = rootNode
        self.setName_( name )
        self.setValue_( obj )

        # self.setNodeAttributes( obj )

        self.setAttributes_( obj )
        self.setComment_( "" )

        self.children = NSMutableArray.arrayWithCapacity_( 0 )
        self.editable = True

        self.maxHeight = self.setMaxLineHeight()

        self.retain