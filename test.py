from addnoise import *
from operator import methodcaller
import  tkinter as tk
from functools import partial
image = cv2.imread(r'D:\Homework\Homework\ImageProcessing\test_img\origin.jpg')
def para_window(root, func_name):
    # 创建弹出窗口
    popup = tk.Toplevel(root)
    popup.title("Parameters")
    popup.geometry("200x150")

    Noise = Addnoise()
    be_called_function = getattr(Noise, func_name)  ##func_name=gauss
    # 就直接调用。如果有其他参数，一样地传就好了
    print(be_called_function.__code__.co_argcount)  ##有2个可选参数
    num_para = be_called_function.__code__.co_argcount - 2
    w = tk.Label(popup, text="函数有"+str(num_para)+"个参数")
    w.pack()

    entrylist=[]
    para=[]
    for i in range(0,num_para):
        e=tk.Entry(popup)
        e.pack()
        entrylist.append(e)

    def execFunc():
        ##TODO:根据函数名执行对应函数
        for i in range(0, num_para):
            para.append(entrylist[i].get())
        for i in range(0, num_para):
            print(para[i])

        be_called_function(image,para)##如何传para??
        ##如何调用？
        pass

    button = tk.Button(popup, text="ok", command=execFunc)
    button.pack()
    button = tk.Button(popup, text="exit", command=popup.destroy)
    button.pack()
if __name__ == "__main__":
    root = tk.Tk()
    app = para_window(root,"gauss")
    root.mainloop()