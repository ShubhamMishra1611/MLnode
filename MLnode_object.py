class MLnode_obj:
    def __init__(self, initial_objects=None):
        self.objects = list(initial_objects) if initial_objects is not None else []
    
    def __len__(self):
        return len(self.objects)
    
    def __getitem__(self, index):
        return self.objects[index]
    
    def __setitem__(self, index, obj):
        while len(self.objects) <= index:
            self.objects.append(None)
        self.objects[index] = obj

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.objects})'