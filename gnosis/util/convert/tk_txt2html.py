import tkinter
from . import dmTxt2Html
import string, os, traceback

Label = tkinter.Label
StringVar = tkinter.StringVar
dmTxt2Html.promo = string.replace(dmTxt2Html.promo, dmTxt2Html.cgi_home, '')

#-- Create some module scope global variables
root, history_frame, menu_frame, info_line = (None, None, None, None)
history_list = []
target, source, proxy_mode, conversion = (None, None, None, None)
counter = 0

def file_menu():
    file_btn = tkinter.Menubutton(menu_frame, text='File', underline=0)
    file_btn.pack(side=tkinter.LEFT, padx="2m")
    file_btn.menu = tkinter.Menu(file_btn)
    file_btn.menu.add_command(label="Source", underline=0, command=GetSource)
    file_btn.menu.add_command(label="Target", underline=0, command=GetTarget)
    file_btn.menu.add('separator')

    #-- types submenu (radio buttons)
    file_btn.menu.types = tkinter.Menu(file_btn.menu)
    file_btn.menu.types.add_radiobutton(label='HTML',
                                        variable=conversion, command=update_specs)
    file_btn.menu.types.add_radiobutton(label='PYTHON',
                                        variable=conversion, command=update_specs)
    file_btn.menu.types.add_radiobutton(label='FAQ',
                                        variable=conversion, command=update_specs)
    file_btn.menu.types.add_radiobutton(label='SMART_ASCII',
                                        variable=conversion, command=update_specs)
    file_btn.menu.types.add_radiobutton(label='RAW',
                                        variable=conversion, command=update_specs)
    file_btn.menu.types.add_radiobutton(label='INFER',
                                        variable=conversion, command=update_specs)
    file_btn.menu.add_cascade(label="Type", menu=file_btn.menu.types)

    #-- proxy mode submenu (radio buttons)
    file_btn.menu.proxy = tkinter.Menu(file_btn.menu)
    file_btn.menu.proxy.add_radiobutton(label='NAVIGATOR',
                                        variable=proxy_mode, command=update_specs)
    file_btn.menu.proxy.add_radiobutton(label='TRAP_LINKS',
                                        variable=proxy_mode, command=update_specs)
    file_btn.menu.proxy.add_radiobutton(label='ALL',
                                        variable=proxy_mode, command=update_specs)
    file_btn.menu.proxy.add_radiobutton(label='NONE',
                                        variable=proxy_mode, command=update_specs)
    file_btn.menu.add_cascade(label="Proxy Mode", menu=file_btn.menu.proxy)

    file_btn.menu.add('separator')
    file_btn.menu.add_command(label='Exit', underline=0, command=file_btn.quit)
    file_btn['menu'] = file_btn.menu
    return file_btn

def action_menu():
    action_btn = tkinter.Menubutton(menu_frame, text='Action', underline=0,)
    action_btn.pack(side=tkinter.LEFT, padx="2m")
    action_btn.menu = tkinter.Menu(action_btn)
    action_btn.menu.add_command(label='Convert!!', underline=0, command=doit_func)
    action_btn.menu.add('separator')
    action_btn.menu.add_command(label="Squeeze History", underline=0, command=clear_history)
    action_btn['menu'] = action_btn.menu
    return action_btn

def help_menu():
    help_btn = tkinter.Menubutton(menu_frame, text='Help', underline=0,)
    help_btn.pack(side=tkinter.LEFT, padx="2m")
    help_btn.menu = tkinter.Menu(help_btn)
    help_btn.menu.add_command(label="How To", underline=0, command=HowTo)
    help_btn.menu.add_command(label="About", underline=0, command=About)
    help_btn['menu'] = help_btn.menu
    return help_btn

def HowTo():
    view_window = tkinter.Toplevel(root)
    view_window.title('Txt2Html Help')
    help_text = open('txt2html.txt').read()
    text = tkinter.Text(view_window, height=40, width=110)
    scroll = tkinter.Scrollbar(view_window, command=text.yview)
    text.configure(yscrollcommand=scroll.set)
    text.tag_configure('fixed', font=('Courier', 10))
    text.insert(tkinter.END, help_text, 'fixed')
    text.pack(side=tkinter.LEFT)
    scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)

def About():
    view_window = tkinter.Toplevel(root)
    about_text = "TK_Txt2Html version 0.1 \n\nRelease to the Public Domain"
    tkinter.Message(view_window,
                    text=about_text,
                    justify=tkinter.CENTER,
                    anchor=tkinter.CENTER,
                    relief=tkinter.GROOVE,
                    width=250).pack(padx=10, pady=10)

def GetSource():
    get_window = tkinter.Toplevel(root)
    get_window.title('Source File?')
    tkinter.Entry(get_window, width=30,
                  textvariable=source).pack(side=tkinter.LEFT, padx=5, pady=5)
    tkinter.Button(get_window, text="Change",
                   command=lambda: update_specs()).pack(side=tkinter.LEFT, padx=5, pady=5)

def GetTarget():
    get_window = tkinter.Toplevel(root)
    get_window.title('Target File?')
    tkinter.Entry(get_window, width=30,
                  textvariable=target).pack(side=tkinter.LEFT, padx=5, pady=5)
    tkinter.Button(get_window, text="Change",
                   command=lambda: update_specs()).pack(side=tkinter.LEFT, padx=5, pady=5)

def doit_func():
    global counter
    counter = counter+1
    update_specs()
    dmTxt2Html.main({'type': conversion.get(),
                     'proxy': proxy_mode.get(),
                     'source': source.get(),
                     'target': target.get()})
    show_run()

def update_specs():
    global conversion
    if conversion.get() in ('INFER', ''):
        conversion.set(dmTxt2Html.infer_type(source.get()))

    Label(info_line, text="Next", width=5,
          relief=tkinter.GROOVE, background="gray90").grid(row=0, column=0)
    Label(info_line, text=source.get(), width=20,
          relief=tkinter.GROOVE, background="gray90").grid(row=0, column=1)
    Label(info_line, text=target.get(), width=20,
          relief=tkinter.GROOVE, background="gray90").grid(row=0, column=2)
    Label(info_line, text=conversion.get(), width=20,
          relief=tkinter.GROOVE, background="gray90").grid(row=0, column=3)
    Label(info_line, text=proxy_mode.get(), width=20,
          relief=tkinter.GROOVE, background="gray90").grid(row=0, column=4)

def show_run():
    global history_list
    hist_line = tkinter.Frame(history_frame)
    hist_line.pack(side=tkinter.TOP, padx=2, pady=2)
    Label(hist_line, text=str(counter), width=5,
          relief=tkinter.SUNKEN).grid(row=0, column=0)
    Label(hist_line, text=source.get(), width=20,
          relief=tkinter.SUNKEN).grid(row=0, column=1)
    Label(hist_line, text=target.get(), width=20,
          relief=tkinter.SUNKEN).grid(row=0, column=2)
    Label(hist_line, text=conversion.get(), width=20,
          relief=tkinter.SUNKEN).grid(row=0, column=3)
    Label(hist_line, text=proxy_mode.get(), width=20,
          relief=tkinter.SUNKEN).grid(row=0, column=4)
    history_list.append(hist_line)

def init_vars():
    global target, source, proxy_mode, conversion
    source = tkinter.StringVar()
    target = tkinter.StringVar()
    proxy_mode = tkinter.StringVar()
    conversion = tkinter.StringVar()
    target.set('default.html')
    source.set('txt2html.txt')
    proxy_mode.set('NONE')
    conversion.set('INFER')

def clear_history():
    for history_line in history_frame.pack_slaves()[:-1]:
        history_line.destroy()

def main():
    global root, history_frame, info_line, menu_frame
    root = tkinter.Tk()
    root.option_readfile('optionDB')
    root.title('Txt2Html TK Shell')
    init_vars()


    #-- Create the menu frame, and add menus to the menu frame
    menu_frame = tkinter.Frame(root)
    menu_frame.pack(fill=tkinter.X, side=tkinter.TOP)
    menu_frame.tk_menuBar(file_menu(), action_menu(), help_menu())

    #-- Create the history frame (to be filled in during runtime)
    history_frame = tkinter.Frame(root)
    history_frame.pack(fill=tkinter.X, side=tkinter.BOTTOM, pady=2)

    #-- Create the info frame and fill with initial contents
    info_frame = tkinter.Frame(root)
    info_frame.pack(fill=tkinter.X, side=tkinter.BOTTOM)

    # first put the column labels in a sub-frame
    label_line = tkinter.Frame(info_frame, relief=tkinter.RAISED, borderwidth=1)
    label_line.pack(side=tkinter.TOP, padx=2, pady=1)
    Label(label_line, text="Run #", width=5, background="lightblue").grid(row=0, column=0)
    Label(label_line, text="Source:", width=20, background="lightblue").grid(row=0, column=1)
    Label(label_line, text="Target:", width=20, background="lightblue").grid(row=0, column=2)
    Label(label_line, text="Type:", width=20, background="lightblue").grid(row=0, column=3)
    Label(label_line, text="Proxy Mode:", width=20, background="lightblue").grid(row=0, column=4)

    # then put the "next run" information in a sub-frame
    info_line = tkinter.Frame(info_frame)
    info_line.pack(side=tkinter.TOP, padx=2, pady=1)
    update_specs()

    #-- Finally, let's actually do all that stuff created above
    root.mainloop()

if __name__=='__main__':
    try:
        main()
    except:
        traceback.print_exc()


