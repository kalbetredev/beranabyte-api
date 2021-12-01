def updateAttributes(object, **kwargs):
    for attr, value in kwargs.items():
        if value:
            setattr(object, attr, value)
