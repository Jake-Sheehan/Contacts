from tkinter import *
import pages


def main():
    # Create root window
    root = Tk()
    # Set window size
    root.geometry('800x450')
    # Set window title
    root.title("Contacts")
    # Set window background color
    root.configure(background="#AAB8B6")
    # Create main frame containing widgets
    main_frame = pages.MainFrame(root)
    # Display the main frame
    main_frame.show()
    # Calling mainloop method which is used
    # when your application is ready to run,
    # and it tells the code to keep displaying
    root.mainloop()


if __name__ == "__main__":
    main()
