import tkinter
import Spam_Detection
import Text_Summarization
import Emotional_Analysis
import threading
import subprocess
import OCR

# Window settings
window = tkinter.Tk()
window.title("Text Analysis")

# Variables
path = ""
img = ""


# Methods

def loadData(e=""):
    global graph_display, path, img
    path = tkinter.filedialog.askopenfilename(title="Open", filetype=((".txt | .png | .jpg", "*.*"),)).lower()
    if path.endswith(".txt"):
        text = ""

        with open(path, "r", encoding="utf-8") as p:
            text = p.read()
        
        text_display.delete(1.0, tkinter.END)
        text_display.insert(tkinter.INSERT, text)

    elif path.endswith(".png") or path.endswith(".jpg") or path.endswith(".jpeg"):
        text = getOcrData(path)

        text_display.delete(1.0, tkinter.END)
        text_display.insert(tkinter.INSERT, text)

    else:
        tkinter.messagebox.showwarning("Warning", "You need to select .txt or .png or .jpg or .jpeg file only.")
        return

    spam_lbl.config(bg="SystemButtonFace", text=" ")
    sentiment_lbl.config(bg="SystemButtonFace", text=" ")
    img = tkinter.PhotoImage(file='C:/Users/prady/Desktop/Project/Dependencies/clean.png')
    graph_display.config(image=img)


def getOcrData(path):
    ocr_obj = OCR.Ocr()
    text = ocr_obj.imgToText(path).strip()

    if text == "":
        tkinter.messagebox.showwarning("Warning", "OCR algorithm did not detected any text in the selected image.")
        return ""
    
    return text


def displaySpamDetectionOutput():
    text = text_display.get(1.0, tkinter.END).strip()

    if text == "":
        tkinter.messagebox.showwarning("Warning", "Load the text or enter text in the text box.")
        return
    
    spam_detection_obj = Spam_Detection.DetectSpam()
    ans = spam_detection_obj.spam_analysis(text)
    if ans == "Not Spam":
        spam_lbl.config(bg="green", text="Not Spam")
    else:
        spam_lbl.config(bg="red", text="Spam")


def displayTextSummarizationOutput():
    text = text_display.get(1.0, tkinter.END).strip()

    if text == "":
        tkinter.messagebox.showwarning("Warning", "Load the text or enter text in the text box.")
        return

    text_summarization_obj = Text_Summarization.Summarization()
    summarized_text = text_summarization_obj.summarize(text)

    with open("Summarized_Text.txt", "w", encoding="utf-8") as p:
            p.write(summarized_text)

    if summarized_text.strip() == "":
        tkinter.messagebox.showwarning("Warning", "You have not provided the enough text to the algorithm try to give a big paragraph.")
        return ""
    
    cmd = subprocess.Popen("Summarized_Text.txt", shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    output = str(cmd.stderr.read(), "utf-8")

    if output != "":
        tkinter.messagebox.showerror("Error", output)


def displayEmotionalAnalysisOutput():
    global img

    text = text_display.get(1.0, tkinter.END).strip()

    if text == "":
        tkinter.messagebox.showwarning("Warning", "Load the text or enter text in the text box.")
        return

    emotional_analysis_obj = Emotional_Analysis.Emotions(text)
    emotion = emotional_analysis_obj.analyze_sentiment()
    emotional_analysis_obj.sentiment_graph()

    print(emotion)

    img = tkinter.PhotoImage(file='C:/Users/prady/Desktop/Project/Dependencies/graph.png')

    if emotion == "Positive Sentiment":
        sentiment_lbl.config(bg="green", text=emotion, fg="white")
        graph_display.config(image=img)
    elif emotion == "Neutral Sentiment":
        sentiment_lbl.config(bg="white", text=emotion, fg="black")
        graph_display.config(image=img)
    else:
        sentiment_lbl.config(bg="red", text=emotion, fg="white")
        graph_display.config(image=img)


# Heading label
heading = tkinter.Label(window, text="Text Analysis", font=("Times New Roman", 26))
heading.pack(fill=tkinter.BOTH, expand=tkinter.TRUE)

# Load Button
load_btn = tkinter.Button(window, text="Load Image/Text", command=lambda: threading.Thread(target=loadData).start())
load_btn.pack()

# Display area
disp_area = tkinter.Frame(window)
disp_area.pack(fill=tkinter.BOTH, expand=tkinter.TRUE)

# Text display area
text_disp_area = tkinter.Frame(disp_area)
text_disp_area.grid(row=0, column=0, padx=6, pady=10)

# Scrollbar
vscroll = tkinter.Scrollbar(text_disp_area, orient=tkinter.VERTICAL, troughcolor='red', bg='orange')
vscroll.pack(side=tkinter.RIGHT, fill=tkinter.Y, anchor=tkinter.NE)

# Text display
text_display = tkinter.Text(text_disp_area, font=("Times New Roman", 11), wrap="word", undo=tkinter.TRUE)
text_display.config(yscrollcommand=vscroll.set)
vscroll.config(command=text_display.yview)
text_display.pack()

# Graph display
graph_display = tkinter.Label(disp_area, image=None)
graph_display.grid(row=0, column=1, padx=6, pady=10)

# Spam label
spam_lbl = tkinter.Label(window, text=" ", font=("Times New Roman", 11), bg="SystemButtonFace", fg="white")
spam_lbl.pack(fill=tkinter.BOTH, expand=tkinter.TRUE)

# Sentiment label
sentiment_lbl = tkinter.Label(window, text=" ", font=("Times New Roman", 11), bg="SystemButtonFace")
sentiment_lbl.pack(fill=tkinter.BOTH, expand=tkinter.TRUE)

# Buttons area
buttons_area = tkinter.Frame(window)
buttons_area.pack()

# Spam detection button
spam_detect_btn = tkinter.Button(buttons_area, text="Spam Detection", command=lambda: threading.Thread(target=displaySpamDetectionOutput).start())
spam_detect_btn.grid(row=0, column=0, padx=6, pady=6)

# Text summarization button
text_summarization_btn = tkinter.Button(buttons_area, text="Text Summarization", command=lambda: threading.Thread(target=displayTextSummarizationOutput).start())
text_summarization_btn.grid(row=0, column=1, padx=6, pady=6)

# Emotional analysis button
emotional_analysis_btn = tkinter.Button(buttons_area, text="Emotional Analysis", command=lambda: threading.Thread(target=displayEmotionalAnalysisOutput).start())
emotional_analysis_btn.grid(row=0, column=2, padx=6, pady=6)

window.mainloop()
