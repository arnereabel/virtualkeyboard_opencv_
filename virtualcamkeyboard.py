import cv2
from cvzone.HandTrackingModule import  HandDetector
from time import sleep
cap = cv2.VideoCapture(0)   ### create a videocapture object
cap.set(3, 1900)            ### resize for more room on the screen for keyboard keys   prop id 3 is width and 4 is height
cap.set(4, 1080)



detector = HandDetector(detectionCon=0.7)  ### 0.8 is the dectionconfidence here 0.8 for a bit more precision judgeing the handmovement
### text keyboard letters in a list with 3 lists within to represent the 3 lines on the screen
keys = [["A", "Z", "E", "R", "T", "Y", "U", "I", "O", "P",],
         ["Q", "S", "D", "F", "G", "H", "J", "K", "L", "M"],
         ["W", "X", "C", "V", "B", "N", ",", ".", "/", "="]]
finalText = ""


def drawAll(img, buttonlist):
    for button in buttonlist:
        x, y = button.pos           #instead of self.pos, self.text and self.size   replace it with button to get all the button draws, all the information is already stored in the button object based on the Button class below
        width , height = button.size ### self.size # is not returning actual size so thats why this workaround (x + width, y + height)
        cv2.rectangle(img, button.pos, (x + width, y + height), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 18, y + 60), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)   ### self.pos[0]+25 self,  self.pos[1]to seperate the boxes +25 for first and second element ### replaces (self.pos[0]+25, self.pos[1]+25) becouse of workaround
    return img


### make a class for the letters position and attributes on screen
class Button():
    def __init__(self, pos, text, size=[75,75]):
        self.pos = pos
        self.text = text
        self.size = size
        #self.bgcolor = bgcolor
        #self.font = font

    ### maybe create a method for drawing so you can call the method when you want to draw because initialization is __init__ is needed only once but drawing is continuously each iteration of a frame from webcam
    # cv2.rectangle(img, (100, 100), (200, 200), (255, 0, 255),cv2.FILLED)
    # cv2.putText(img, "A", (125, 175), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
    ### replace the above static arguments with variables and put it in a method below

    # def draw(self,img):   # for each iteration ask for an image from webcam (img) and when draw is called return the image
    #     x, y = self.pos
    #     width , height = self.size ### self.size # is not returning actual size so thats why this workaround (x + width, y + height)
    #     cv2.rectangle(img, self.pos, (x + width, y + height), (255, 0, 255), cv2.FILLED)
    #     cv2.putText(img, self.text, (x + 18, y + 60), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)   ### self.pos[0]+25 self,  self.pos[1]to seperate the boxes +25 for first and second element ### replaces (self.pos[0]+25, self.pos[1]+25) becouse of workaround
    #    # return img
    ### instead of method in class make a function to draw

buttonlist = []

for keylist in range(len(keys)):
    for itemnr, key in enumerate(keys[keylist]):
        buttonlist.append(Button([100 * itemnr + 50, 100 * keylist + 50], key))

### put it in a list above
# myButton = Button([100, 100], 'A')   ### only called once her for initialization
# myButton1 = Button([200, 100], 'Z')
# myButton2 = Button([300, 100], 'E')
# myButton3 = Button([400, 100], 'R')   ### only called once her for initialization
# myButton4 = Button([500, 100], 'T')
# myButton5 = Button([600, 100], 'Y')

view = True
while (view):
    succes, img = cap.read()                 ### while succes is True stay in the loop,
    img = detector.findHands(img)
    lmlist, bboxInfo = detector.findPosition(img)
    img = drawAll(img, buttonlist)                           #call the drawAll function and pass it thru to again to the return

    # if there is something in the lmlist then do the following
    if lmlist:
        for button in buttonlist:               # loop through all the buttons
            x, y = button.pos                    # we need to know the location of each button and then need to know if our finger is near the button or not
            width, height = button.size         # go to mediapipe website and look at hand landmark model point 8, refers to index_finger_tip  https://google.github.io/mediapipe/solutions/hands

            if x < lmlist[8][0] < x+width and y < lmlist[8][1] < y+height:                      # by this we will get the x and y position  here we only need the x psoition so first in list refers to [0], then check if the point 8 is in between x < point < x + width and same for y
                cv2.rectangle(img, button.pos, (x + width, y + height), (150, 0, 150), cv2.FILLED)                         # change the color of the box to green when finger point 8 is in the range of the box   for the x axis so 3 boxes turn green
                cv2.putText(img, button.text, (x + 18, y + 60), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                # in the cvzone package there is a fuction to detect the distance between 8 and 12 to facilitate the click on button   finds the value between arguments 1, 2 and draws on image (8, 12, img)
                l,_,_ = detector.findDistance(0, 20, img, draw=False)     # we only need to get the length back with the l so we cann ignore the other parameters with _ wich ignores the other parameters in pyhton
                print(l)                                  # draw = False negates the line between point 8 and 12 to draw the distance onscreen

                # when clicked (distance between point 0 and point 20 > 180) update the string in the final text string and print it out
                if l > 250:
                    cv2.rectangle(img, button.pos, (x + width, y + height), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 18, y + 60), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                    finalText += button.text
                    sleep(0.5)   # single entry of text to counter the delay and alteration in the input with handgesture

    # put text on screen
    cv2.rectangle(img, (50,380), (1200,450), (0, 0, 0), cv2.FILLED)
    cv2.putText(img, finalText, (60, 430), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)
    # for x in range(0, 5):
    #     buttonlist.append(Button([100 * x, 100], 'A'))




    ### create a button by filling in the arguments defined in the Button class parameters
    # mybutton = Button([100, 100], 'A')  #putting it outside of loop because method draw is called now
    # img = myButton.draw(img)    ### by calling the mettehod it sends in the image(img) and gets back the image(img)
    # img = myButton1.draw(img)
    # img = myButton2.draw(img)
    # img = myButton3.draw(img)
    # img = myButton4.draw(img)
    # img = myButton5.draw(img)
    # make a test button for the letters that will be put in a class afterwards
    # cv2.rectangle(img,(100,100), (200,200), (255,0,255),cv2.FILLED)### create rectangles through the opencv instead of putting them on screen with x y z coördinates due to scaling
    # cv2.putText(img,"A", (125,175), cv2.FONT_HERSHEY_PLAIN,5,(255,255,255), 5) ### for all letters there is text(name),  location, font, size best is to put them in a class

    cv2.imshow('Image', img)                  ### call to show the image
    if cv2.waitKey(1) & 0xff == ord('q'):    ### waits for (1)ms and terminates with the bitwise adress set to q
        cv2.destroyAllWindows()              ### & is not the logical "AND" operator but the bit operation commonly used to mask things. It means to take the first 8 bits of the waitKey() call and compare those to the bits of ord("q")
        view = False                         ### cv2.waitKey(1) returns the character code of the currently pressed key and -1 if no key is pressed. the & 0xFF is a binary AND operation to ensure only the single byte (ASCII) representation of the key remains as for some operating systems cv2.waitKey(1) will return a code that is not a single byte. ord('q') always returns the ASCII representation of 'q' which is 113 (0x71 in hex).
                                             ### therefore if the user is pressing the q key when cv2.waitKey(1) is evaluated the following will be determined:

                                             ### cv2.waitKey(1) & 0xFF == cv2.ord('q')
                                             ### 0xXX71 & 0xFF == 0x71
                                             ### 0x71 == 0x71
                                             ### True

