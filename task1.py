class Element:
    def __init__(self, data=None, nextE=None):
        self.data = data
        self.nextE = nextE


class MyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, e, func=None):
        next = self.head
        if next is None:
            self.head = e
            self.tail = e.nextE
        else:
            if func is None:
                prev = next
                next = next.nextE
                while next is not None:
                    if prev.data > next.data:
                        temp = next
                        next = prev
                        next.nextE = temp.nextE
                        prev = temp
                        prev.nextE = next
                    prev = next
                    next = next.nextE
                prev = self.head
                next = prev.nextE
                while next is not None:
                    while e.data < next.data:
                        prev = next
                        next = next.nextE
                    prev.nextE = e
                    e.nextE = next



    def __str__(self):
        temp = self.head
        content = ''
        while temp is not None:
            content += temp.data
            temp = temp.nextE
        return content

    def get(self, e):
        temp = self.head
        while temp is not None:
            if temp == e:
                return temp.data
            temp = temp.nextE
        raise Exception("Element not found")

    def delete(self, e):
        temp = self.head
        prev = self.head
        if temp == e:
            self.head = temp.nextE
            temp = None
        else:
            while temp is not None:
                if temp == e:
                    break
                prev = temp
                temp = temp.nextE
            if temp is None:
                raise Exception("Element not found")
            if temp == self.tail:
                self.tail = prev
            prev.nextE = temp.nextE
            temp = None
