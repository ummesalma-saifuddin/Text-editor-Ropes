from tkinter import *
from tkinter import filedialog
from ttkthemes import themed_tk as tk
from tkinter import ttk
import tkinter.font as font
from tkinter import Tk, W, E
from tkinter.ttk import Frame, Button, Entry, Style


lst_final_content = []
word = ""
word = str(word)


class Rope(object):

    def __init__(self, data='', parent=None):
        # checks if input is a string
        if isinstance(data, list):
            if len(data) == 0:
                self.__init__()
            elif len(data) == 1:
                self.__init__(data[0], parent=parent)
            else:
                self.current = self
                # Round-up division (to match rope arithmetic associativity)
                idiv = len(data) // 2 + (len(data) % 2 > 0)
                self.left = Rope(data[:idiv], parent=self.current)
                self.right = Rope(data[idiv:], parent=self.current)
                self.parent = parent
                self.data = ''
                self.weight = len(self.data.join(data[:idiv]))
        elif isinstance(data, str):
            self.left = None
            self.right = None
            self.data = data
            self.weight = len(data)
            self.parent = parent
            self.current = self
            if data == "":
                self.current = self
        else:
            raise TypeError('Only strings are currently supported')

    # checks if tree is balanced
    # def __eq__(self, other):
    #     if (self.left and self.right) and (other.left and other.right):
    #         return self.left == other.left and self.right == other.right
    #     elif (self.left and self.right) or (other.left and other.right):
    #         return False
    #     else:
    #         return self.data == other.data

    def search(self, node, i):
        # returns the letter present at a given index
        if node.weight <= i and node.right != None:
            return self.search(node.right, i-node.weight)
        elif node.left != None:
            return self.search(node.left, i)
        return node.data[i]

    def searchnode(self, node, i):
        if node.weight <= i and node.right != None:
            return self.searchnode(node.right, i-node.weight)
        elif node.left != None:
            return self.searchnode(node.left, i)
        return node, i

    def search_words(self, node, words):
        wordlist = words.split()
        index = []
        for i in wordlist:
            positions = []
            positions = self.search_word(node, i, positions)
            index = index+positions
        return index

    def search_word(self, node, word, positions):
        return_node = None
        if node.data == "":
            positions = self.search_word(node.left, word, positions)
            positions = self.search_word(node.right, word, positions)
        elif node.data == word:
            t = node
            index_s = 0
            while t.parent != None:
                if t.parent.right == t:
                    index_s += t.parent.weight
                t = t.parent
            index_e = index_s+len(node.data)-1
            positions.append((index_s, index_e))
            return positions
        return positions

    def length(self, rootnode):
        if rootnode.right == None and rootnode.left == None:
            return len(rootnode.data)
        elif rootnode.right == None and rootnode.left != None:
            return self.length(rootnode.left)
        elif rootnode.right != None and rootnode.left == None:
            return self.length(rootnode.right)
        else:
            return self.length(rootnode.right) + self.length(rootnode.left)

    def concatenation(self, node1, node2):
        self.left = node1
        self.right = node2
        self.weight = self.length(node1)
        node1.parent = self
        node2.parent = self
        self.current = self
        return self

    def printrope(self, rootnode):
        if (rootnode.right == None and rootnode.left == None):
            if rootnode.data != None:
                lst_final_content.append(rootnode.data)
                print(rootnode.data)
        elif rootnode.left == None:
            self.printrope(rootnode.right)
        elif rootnode.right == None:
            self.printrope(rootnode.left)
        else:
            self.printrope(rootnode.left)
            self.printrope(rootnode.right)

    def nuke(self, node):
        if node.parent.right == node:
            node.parent.right = None
        elif node.parent.left == node:
            node.parent.left = None
            node.parent.weight = node.parent.weight-node.weight
        node.parent = None

    def split(self, root, i, limit=None):
        arr = []
        node, t = self.searchnode(root, i)
        # Chops off the required strings
        while node != None:
            arr.append(node.data)
            self.nuke(node)
            i = i+node.weight
            node, t = self.searchnode(root, i)
            if node.data == "":
                node = None
            if i == limit:
                node = None
        r = Rope(arr)
        return r

    #         # remove link between right leaf and target
    def splits(self, root, i):
        node, t = self.searchnode(root, i)
        node0 = Rope(node.data[0:t])
        node1 = Rope(node.data[t:])
        node.data = ''
        node.weight = len(node0.data)
        node.left = node0
        node.right = node1
        node0.parent = node
        node1.parent = node
        l2 = self.split(root, i)
        l1 = self.split(root, 0)
        return l1, l2

    def insert(self, index, s):
        newrope1, newrope2 = (self.splits(self, index))

        temp = Rope()

        s_rope = Rope(s.split())
        temp.concatenation(newrope1, s_rope)
        final = Rope()
        final.concatenation(temp, newrope2)
        return final

    def delete(self, index_i, index_j):
        firsthalf, secondhalf = self.splits(self, index_j)
        revised_firsthalf, discard = firsthalf.splits(firsthalf, index_i)
        final = Rope()
        final.concatenation(revised_firsthalf, secondhalf)
        return final

        return final


app = Tk()
# app = tk.ThemedTk()

# app.get_themes()                 # Returns a list of all themes that can be set
# app.set_theme("vista")
app.geometry("1500x1000")
app.title("Fast String Concatenation")
app['bg'] = '#49A'
Label(app,
      text="Fast String Concatenation",
      fg="black",
      bg='#49A',
      font="Times 30 bold italic"
      ).pack()
myFont = font.Font(family='Helvetica', size=13)
# Text Widget + Font Size
txt = Text(app, font=('Verdana', 12))
txt.pack()


def findword():
    search_window = Toplevel(app)
    newtxt = Text(search_window, font=('Verdana', 8))
    newtxt.pack()
    btn_new = Button(search_window, text='Search',
                     command=lambda: search_w(newtxt, search_window))
    btn_new.pack()
    search_window.mainloop()


def search_w(txt, search_window):

    text = txt.get("1.0", 'end-1c')
    text = str(text)
    text.lower()
    print("find this word", text)
    print("search current")
    currentrope.printrope(currentrope)
    print("current rope content khatam")
    # print(currentrope.search(currentrope, 15))

    x = currentrope.search_words(currentrope, str(text))

    w = Label(search_window, text=(
        "This word is found at the following index(es):", x))
    w.pack()
    print(x)


def getText(app):
    global currentrope
    global text_in_textbox
    global split_len
    global length_text
    text_in_textbox = txt.get("1.0", 'end-1c')

    length_text = len(text_in_textbox)
    split_len = len(text_in_textbox.split())

    currentrope = Rope(text_in_textbox.split())

    btn_txt = Button(app, text=text_in_textbox,
                     command=lambda: edit_window(app))
    btn_txt.pack(ipady=10)
    # btn_.place(x=0, y=1050, height=100, width=500)
    txt.delete(1.0, END)
    # f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    # if f is None:
    #     return
    # f.write(text_in_textbox)
    # f.close()


def update_rope(newtxt, next_window, app):
    global currentrope
    global lst_final_content

    text = newtxt.get("1.0", 'end-1c')

    new_rope = Rope(text.split())
    final_rope = Rope()
    x = length_text - split_len + 1

    final_r = final_rope.concatenation(currentrope, new_rope)
    final_r.printrope(final_r)

    currentrope = final_r

    text_in = ' '.join(lst_final_content)

    print("current")
    currentrope.printrope(currentrope)
    print("final")
    final_r.printrope(final_r)
    next_window.destroy()
    btn = Button(app, text=text_in, command=lambda: edit_window(app))
    lst_final_content = []
    btn.pack()


def delete_text(newtxt, next_window, app):
    global currentrope
    global lst_final_content
    text = newtxt.get("1.0", 'end-1c')
    x = currentrope.search_words(currentrope, str(text))
    totaldels = len(x)
    count = 0

    for j in range(totaldels):
        currentrope = currentrope.delete(x[0][0], x[0][1]+1)
        count = count+1
        if totaldels != count:
            x = currentrope.search_words(currentrope, str(text))

    # for i in x:
    #     if count==totaldels:
    #         currentrope = currentrope.delete(i[0], i[1]+1)

    print("final deleted rope")
    currentrope.printrope(currentrope)
    print("list", lst_final_content)
    text_in = ' '.join(lst_final_content)
    next_window.destroy()
    btn = Button(app, text=text_in, command=lambda: edit_window(app))
    lst_final_content = []
    btn.pack()


def delete(app):
    next_window = Toplevel(app)
    newtxt = Text(next_window, font=('Verdana', 8))
    newtxt.pack()

    btn = Button(next_window, text='Done',
                 command=lambda: delete_text(newtxt, next_window, app))
    btn.pack()


def add_text(app):

    next_window = Toplevel(app)
    newtxt = Text(next_window, font=('Verdana', 8))
    newtxt.pack()

    btn = Button(next_window, text='Update',
                 command=lambda: update_rope(newtxt, next_window, app))
    btn.pack()


def edit_window(app):
    # global newWindow
    newWindow = Toplevel(app)
    btn = Button(newWindow, text='Add', command=lambda: add_text(app))
    btn.pack()
    btn = Button(newWindow, text='Delete', command=lambda: delete(app))
    btn.pack()


def openfile():
    result = filedialog.askopenfile(
        initialdir="/", title="select file", defaultextension=".txt")
    s = ""
    for c in result:
        s = s+c
        print(c)


myFont = font.Font(family='Helvetica', size=13)

# Delete Button
btn = Button(app, text='Save Text',
             command=lambda: getText(app))

# btn['font'] = myFont
# btn.pack()
btn.pack(side=RIGHT, padx=5)
btn.place(x=130, y=70, height=70, width=90)
# btn.config(font=('helvetica', 20, 'underline italic'))
# btn.grid(row=0, column=0, sticky=W, pady=2)
btn2 = Button(app, text='Open File',
              command=openfile)
# btn2['font'] = myFont
btn2.pack(side=RIGHT)
btn2.place(x=130, y=160, height=70, width=90)

# : txt.delete(1.0, END))
btn = Button(app, text='Edit Text',
             command=lambda: edit_window(app))
# btn['font'] = myFont
btn.pack(side=RIGHT, padx=15, pady=20)
btn.place(x=130, y=250, height=70, width=90)
btn = Button(app, text='Search',
             command=lambda: findword())

# btn['font'] = myFont
btn.pack(side=RIGHT)
btn.place(x=130, y=340, height=70, width=90)
app.mainloop()
