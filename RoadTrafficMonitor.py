from tkinter import *
import tkinter
from tkinter import filedialog
import numpy as np
from tkinter.filedialog import askdirectory
from tkinter import simpledialog
import cv2
from keras.utils.np_utils import to_categorical
from keras.layers import Input
from keras.models import Model
from keras.layers import MaxPooling2D
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D
from keras.models import Sequential
import keras
import pickle
import matplotlib.pyplot as plt
import os
from keras.models import model_from_json
from PIL import Image, ImageTk

main = tkinter.Tk()
main.title("Enhanced Smart Learning for Road Traffic Conditions & Monitoring using Deep Learning Techniques") #designing main screen
main.geometry("1000x650")

global filename
global classifier

def upload():
  global filename
  filename = filedialog.askdirectory(initialdir = ".")
  text.delete('1.0', END)
  text.insert(END,filename+' Loaded')
  text.insert(END,"Dataset Loaded")

  
def processImages():
    text.delete('1.0', END)
    X_train = np.load('model/X.txt.npy')
    Y_train = np.load('model/Y.txt.npy')
    text.insert(END,'Total images found in dataset for training = '+str(X_train.shape[0])+"\n\n")
    test = X_train[30]
    test = cv2.resize(test,(600,400))
    cv2.imshow('Preprocess sample image showing as output', test)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
  

def generateModel():
  global classifier
  text.delete('1.0', END)
  if os.path.exists('model/model.json'):
      with open('model/model.json', "r") as json_file:
          loaded_model_json = json_file.read()
          classifier = model_from_json(loaded_model_json)
      classifier.load_weights("model/model_weights.h5")
      classifier._make_predict_function()   
      print(classifier.summary())
      f = open('model/history.pckl', 'rb')
      data = pickle.load(f)
      f.close()
      acc = data['accuracy']
      accuracy = acc[9] * 100






      text.insert(END,"CNN Training Model Accuracy = "+str(accuracy)+"\n")
  else:
      X_train = np.load('model/X.txt.npy')
      Y_train = np.load('model/Y.txt.npy')
      classifier = Sequential()
      classifier.add(Convolution2D(32, 3, 3, input_shape = (64, 64, 3), activation = 'relu'))
      classifier.add(MaxPooling2D(pool_size = (2, 2)))
      classifier.add(Convolution2D(32, 3, 3, activation = 'relu'))
      classifier.add(MaxPooling2D(pool_size = (2, 2)))
      classifier.add(Flatten())
      classifier.add(Dense(output_dim = 256, activation = 'relu'))
      classifier.add(Dense(output_dim = 4, activation = 'softmax'))
      print(classifier.summary())
      classifier.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
      hist = classifier.fit(X_train, Y_train, batch_size=16, epochs=10, shuffle=True, verbose=2)
      classifier.save_weights('model/model_weights.h5')            
      model_json = classifier.to_json()
      with open("model/model.json", "w") as json_file:
          json_file.write(model_json)
      f = open('model/history.pckl', 'wb')
      pickle.dump(hist.history, f)
      f.close()
      f = open('model/history.pckl', 'rb')
      data = pickle.load(f)
      f.close()
      acc = data['accuracy']
      accuracy = acc[9] * 100
      text.insert(END,"CNN Training Model Accuracy = "+str(accuracy)+"\n")
  
  
  
def predictTraffic():
    name = filedialog.askopenfilename(initialdir="testImages")    
    img = cv2.imread(name)
    img = cv2.resize(img, (64,64))
    im2arr = np.array(img)
    im2arr = im2arr.reshape(1,64,64,3)
    XX = np.asarray(im2arr)
    XX = XX.astype('float32')
    XX = XX/255
    preds = classifier.predict(XX)
    print(str(preds)+" "+str(np.argmax(preds)))
    predict = np.argmax(preds)
    print(predict)
    img = cv2.imread(name)
    img = cv2.resize(img,(450,450))
    msg = ''
    if predict == 0:
        cv2.putText(img, 'Accident Occured', (10, 25),  cv2.FONT_HERSHEY_SIMPLEX,0.6, (0, 255, 255), 2)
        msg = 'Accident Occured'
    if predict == 1:
        cv2.putText(img, 'Heavy Traffic Detected', (10, 25),  cv2.FONT_HERSHEY_SIMPLEX,0.6, (0, 255, 255), 2)
        msg = 'Heavy Traffic Detected'
    if predict == 2:
        cv2.putText(img, 'Fire Accident Occured', (10, 25),  cv2.FONT_HERSHEY_SIMPLEX,0.6, (0, 255, 255), 2)
        msg = 'Fire Accident Occured'
    if predict == 3:
        cv2.putText(img, 'Low Traffic', (10, 25),  cv2.FONT_HERSHEY_SIMPLEX,0.6, (0, 255, 255), 2)
        msg = 'Low Traffic Detected'
    cv2.imshow(msg,img)
    cv2.waitKey(0)

def graph():
    f = open('model/history.pckl', 'rb')
    data = pickle.load(f)
    f.close()

    accuracy = data['accuracy']
    loss = data['loss']

    plt.figure(figsize=(10,6))
    plt.grid(True)
    plt.xlabel('Iterations')
    plt.ylabel('Accuracy/Loss')
    plt.plot(loss, 'ro-', color = 'red')
    plt.plot(accuracy, 'ro-', color = 'green')
    plt.legend(['Loss', 'Accuracy'], loc='upper left')
    plt.title('CNN Accuracy & Loss Graph')
    plt.show()

bg_image = Image.open("C:\\Users\\DEVAD\\Downloads\\download 5.jpeg") # Replace with your image file path
bg_image = bg_image.resize((1500, 650), Image.ANTIALIAS)  # Resize to fit the window
bg_photo = ImageTk.PhotoImage(bg_image)

# Set image as label background
bg_label = Label(main, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
   
font = ('times', 16, 'bold')
title = Label(main, text='Enhanced Smart Learning for Road Traffic Conditions & Monitoring using Deep Learning Techniques', justify=LEFT)
title.config(bg='dodgerblue2', fg='green2')  
title.config(font=font)           
title.config(height=1, width=100)       
title.place(x=50,y=4)
title.pack()

font1 = ('times', 15, 'bold')
uploadButton = Button(main, text="Upload Dataset", command=upload)
uploadButton.place(x=10,y=100)
uploadButton.config(font=font1)

processButton = Button(main, text="Image Preprocessing", command=processImages)
processButton.place(x=280,y=100)
processButton.config(font=font1) 

cnnButton = Button(main, text="Generate CNN Traffic Model", command=generateModel)
cnnButton.place(x=10,y=150)
cnnButton.config(font=font1) 

predictButton = Button(main, text="Upload Test Image & Predict Traffic", command=predictTraffic)
predictButton.place(x=280,y=150)
predictButton.config(font=font1)

graphButton = Button(main, text="Accuracy & Loss Graph", command=graph)
graphButton.place(x=10,y=200)
graphButton.config(font=font1)

font1 = ('times', 12, 'bold')
text=Text(main,height=8,width=80)
scroll=Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=10,y=250)
text.config(font=font1) 


main.config(bg='Green')
main.mainloop()
