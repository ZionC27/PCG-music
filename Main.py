from pydub import AudioSegment
from pydub.playback import play
import random
import numpy as np


#Variables
chord_structure = [
    (1, 1, "ABAB"),(1, 2, "ABCB"),(1, 3, "AABC"),(2, 1, "ABABA"),(2, 2, "ABACA"),
    (2, 3, "AABAB"),(2, 4, "ABCAB"),(2, 5, "AABCB"),(3, 1, "ABABCA"),(3, 2, "ABABCB"),
    (3, 3, "AABAAC"),(3, 4, "ABACAB"),(3, 5, "ABACAC"),(4, 1, "ABACBAB"),
    (4, 2, "ABAAABA"),(4, 3, "ABABABC"),(4, 4, "ABABCBA"),
    (5, 1, "ABACABAC"),(5, 2, "AABCAABC")
]
#number of verses
VerseNo = 10
#number of C and B
C_BNo = 12
#nunber of Drums
DrumNo = 11
#number of valid input for chord structres = 5
ChordstructNo = 5
#number of valid intput for mood eval
moodevalNo = 10

#number of options in each structure len
Chord_lenNo = [3, 5, 5, 4, 2]

def get_valid_Length_input(maxnum):
    while True:
        user_input = input("Enter Length from 1-" + str(maxnum) +": ")
        try:
            input_as_int = int(user_input)
            if 1 <= input_as_int <= maxnum:
                return input_as_int  
            else:
                print("Input is not between 1 and " + str(maxnum) +". Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_valid_mood_input(maxnum):
    while True:
        user_input = input("Enter mood from 1-" + str(maxnum) +": ")
        try:
            input_as_int = int(user_input)
            if 1 <= input_as_int <= maxnum:
                return input_as_int  
            else:
                print("Input is not between 1 and " + str(maxnum) +". Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# 1 or 10 is imposible so if thos cases go 1 up or down
def ifMoodextreme(mood):
    if mood == 1:
        mood = 2
        return mood 
    elif mood == 10:
        mood = 9
        return mood
    else:
        return mood

# Given the length and randomly chosen structure return the chord structure
def getChordStruct(var1, var2):
    found_value = None
    for num1, num2, alphabet_value in chord_structure:
        if num1 == var1 and num2 == var2:
            found_value = alphabet_value
            break
    return found_value

# Given length randomly choose structure 
def struct_choose(speed):
    cln = Chord_lenNo[speed-1]
    randVal = random.randint(1, cln)
    return getChordStruct(speed, randVal)

def HasChorus(struct):
    if 'C' in struct:
        return True
    
#choose notes based on mood
def getnotes(istrue, x):
    if x == 2 or x == 9:
        min = 1.5
        max = 1.2
    elif x < 3 or x > 8:
        min = 0.5
        max = 0.5
    else:
        min = 1
        max = 1
    n1 = random.randint(0, 9)
    n2 = random.randint(0, 11)
    n3 = random.randint(0, 11)
    while n3 == n2:
        n3 = random.randint(0, 11)
    n4 = random.randint(0, 10)
    n5 = random.choice([1, 2])
    if istrue:
        
        num1 = getfileVal("C:\Audiofile\Mood\Verse.txt", n1)
        num2 = getfileVal("C:\Audiofile\Mood\C_B.txt", n2)
        num3 = getfileVal("C:\Audiofile\Mood\C_B.txt", n3)
        num4 = getfileVal("C:\Audiofile\Mood\Drums.txt", n4)
        num5 = getfileVal("C:\Audiofile\Mood\Base_Verse.txt", n5)
        average = (int(num1) + int(num2) + int(num3) + int(num4) + int(num5)) / 5
        if x - min <= average <= x + max:
            print(str(n1),str(n2),str(n3),str(n4),str(n5))
            print(num1,num2,num3,num4,num5)
            # print(average)
            return [n1+1, n2+1, n3+1, n4+1, n5+1]
        
        else:
            return getnotes(istrue, x)
        
    else:
        num1 = getfileVal("C:\Audiofile\Mood\Verse.txt", n1)
        num2 = getfileVal("C:\Audiofile\Mood\C_B.txt", n2)
        n3 = 0
        num4 = getfileVal("C:\Audiofile\Mood\Drums.txt", n4)
        num5 = getfileVal("C:\Audiofile\Mood\Base_Verse.txt", n5)
        average = (int(num1) + int(num2) + int(num4) + int(num5) ) / 4
        if x - min <= average <= x + max:
            # print(str(n1),str(n2),str(n3),str(n4),str(n5))
            # print(num1,num2,num4,num5)
            # print(average)
            return [n1+1, n2+1, n3+1, n4+1, n5+1]
        else:
            return getnotes(istrue, x)


# # used for getting mood value from txt file
def getfileVal(path, val):
    with open(path, 'r') as file:

        file_contents = file.read()
    numbers = file_contents.split(',')
    return numbers[val]
        

# get the audio files and add them together according to the structure
def SongSticher(V1, V2, V3, songstruct):

    Music = 0
    path = "C:/Audiofile/I_V_vi_IV_1564/Verse"
    path2 = "C:/Audiofile/I_V_vi_IV_1564/C_B" 

    for st in songstruct:
        if st == 'A':
            temp = path + "/" + str(V1)+ "/"+ str(V1) +".wav"
            Music += AudioSegment.from_wav(temp)
        elif st == 'B':     
            temp = path2 + "/" + str(V2)+ "/"+ str(V2) +".wav"
            Music += AudioSegment.from_wav(temp)
        elif st == 'C':     
            temp = path2 + "/" + str(V3)+ "/"+ str(V3) +".wav"
            Music += AudioSegment.from_wav(temp)

    return Music

# combine drum
def drumSticher(beat, songstruct):
    Music = 0
    path = "C:/Audiofile/Drum"

    for i in range(0, len(songstruct)):
        current_char = songstruct[i]
        if i + 1 >= len(songstruct):
            next_char = ''
        else :
            next_char = songstruct[i + 1]   

        if current_char == 'A' and (next_char == 'A' or next_char == ''):
            temp = path + "/" + str(beat)+ "/D"+ str(beat) +".wav"
            Music += AudioSegment.from_wav(temp) * 4 
        else:
            temp = path + "/" + str(beat)+ "/D"+ str(beat) +".wav"
            Music += AudioSegment.from_wav(temp) * 3 
            temp = path + "/" + str(beat)+ "/D"+ str(beat)+ "_2"+".wav"
            Music += AudioSegment.from_wav(temp)
    
    return Music

def BaseSticher(s2, s3, songstruct, baseval):
    Music = 0
    path = "C:/Audiofile/I_V_vi_IV_1564/" 

    if baseval == 2  :
        A = path +"BaseVerse/2.wav"
        if s2 % 2 != 0:
            B = path + "BaseC_D/"+ str(s2 + 1)+".wav"
        else:
            B = path + "BaseC_D/"+ str(s2)+".wav"
        if s3 % 2 != 0:
            C = path + "BaseC_D/"+ str(s3 + 1)+".wav"
        else:
            C = path + "BaseC_D/"+ str(s3)+".wav"    
    else:
        A = path +"BaseVerse/1.wav"
        if s2 % 2 == 0:
            B = path + "BaseC_D/"+ str(s2 - 1)+".wav"
        else:
            B = path + "BaseC_D/"+ str(s2)+".wav"
        if s3 % 2 == 0:
            C = path + "BaseC_D/"+ str(s3 - 1)+".wav"
        else:
            C = path + "BaseC_D/"+ str(s3)+".wav"


    for st in songstruct:
        if st == 'A':
            Music += AudioSegment.from_wav(A) 
        elif st == 'B':
            Music += AudioSegment.from_wav(B) 
        elif st == 'C':
            Music += AudioSegment.from_wav(C) 

    return Music  

# get RootMeanSquaredError
def RootMeanSquaredError(mood, e1,e2,e3,e4,e5):
    
    if e3 == 0:
        ground_truth_mood_profile = np.array([mood, mood, mood, mood], dtype=np.int32)
        generated_mood_profile = np.array([e1,e2,e4,e5], dtype=np.int32)
    else:
        ground_truth_mood_profile = np.array([mood, mood, mood, mood, mood], dtype=np.int32)
        generated_mood_profile = np.array([e1,e2,e3,e4,e5], dtype=np.int32)
    # Calculate RMSE for the generated mood profile
    rmse = np.sqrt(np.mean((generated_mood_profile - ground_truth_mood_profile) ** 2))

    # Print the RMSE value
    print(f"RMSE for the generated mood profile: {rmse:.2f}")
    

def getEvalVal(a, b, c, drums, base):
    
    a_path = "C:\Audiofile\Mood\Verse.txt"
    b_path = "C:\Audiofile\Mood\C_B.txt"
    c_path = "C:\Audiofile\Mood\C_B.txt"
    drums_path = "C:\Audiofile\Mood\Drums.txt"
    base_path = "C:\Audiofile\Mood\Base_Verse.txt"

    A = getfileVal(a_path, a - 1)
    B = getfileVal(b_path, b - 1)
    if c != 0:
        C = getfileVal(c_path,  - 1)
    else:
        C = 0
    Drums = getfileVal(drums_path, drums - 1)

    if base % 2 == 0:
        Base = getfileVal(base_path, 1)
    else:
        Base = getfileVal(base_path, 2)
    return [A, B, C, Drums, Base]



def main():

    #get length input
    valid_input = get_valid_Length_input(ChordstructNo)
    #print("You entered a valid speed:", valid_input)

    #choose structure from length
    SongStructure = struct_choose(valid_input)
    print("The Structure of the song is :"+ SongStructure)


    chorusYN = HasChorus(SongStructure)

    #get mood input
    mood = get_valid_mood_input(moodevalNo)
    mood = ifMoodextreme(mood)


    s1, s2, s3, s4, s5 = getnotes(chorusYN, mood)
    print("The picked chords / drums / base: " + str(s1), str(s2),str(s3),str(s4),str(s5))

    sss = SongSticher(s1, s2, s3, SongStructure)
    #play(sss)

    ddd = drumSticher(s4, SongStructure)
    #play(ddd)

    bbb = BaseSticher(s2, s3, SongStructure, s5)
    #play(bbb)

    music = sss.overlay(ddd)
    music = music.overlay(bbb)
    #play(music)

    e1,e2,e3,e4,e5 = getEvalVal(s1, s2, s3, s4, s5)
    #print (e1,e2,e3,e4,e5)



    RootMeanSquaredError(mood, e1,e2,e3,e4,e5)

    #saving
    #music.export(out_f = "MusicFile.wav", format="wav")



main()