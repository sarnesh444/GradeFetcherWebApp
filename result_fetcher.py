import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from pathlib import Path
import time
from pandas import DataFrame

def main():
    st.title("Grade Fetcher Web App")
    st.sidebar.title("GITAM Grade Fetcher")
    st.markdown("A Web app to fetch the results of all the students at once!")
    snum = st.sidebar.text_input("Starting Reg Num",key='snum')
    enum = st.sidebar.text_input("Ending Reg Num", key='enum')
    sem = st.sidebar.text_input("Semester", key='sem')
    names=[]
    regnums=[]
    gpas=[]
    cgpas=[]
    if(st.sidebar.button("Fetch", key='fetch')):
        if(len(snum)==12 and len(enum)==12 and 1<=int(sem)<=8):
            driver_path = str(Path(__file__).parent.absolute()) + "\\chromedriver.exe"
            browser = webdriver.Chrome(driver_path)  # chrome-driver
            browser.get('https://doeresults.gitam.edu/onlineresults/pages/Newgrdcrdinput1.aspx')
            roll_no=int(snum)
            enum=int(enum)
            while roll_no <= enum:
                sem_drop_box = Select(browser.find_element_by_xpath("//*[@id='cbosem']"))  # selecting-semester-drop-box
                sem_drop_box.select_by_visible_text(sem)  # select-semester
                roll_no_box = browser.find_element_by_xpath("//*[@id='txtreg']")  # selecting-roll-no-box
                roll_no_box.clear()  # clearing-unwanted-text
                roll_no_box.send_keys(roll_no)  # filling-roll-no
                browser.find_element_by_xpath(
                    "//*[@id='Button1']").click()  # selecting-get-result-butoon-and-clicking-it
                if (browser.current_url == 'https://doeresults.gitam.edu/onlineresults/pages/View_Result_Grid.aspx'):

                    name = browser.find_element_by_xpath("//*[@id='lblname']")
                    roll = browser.find_element_by_xpath("//*[@id='lblregdno']")
                    cgpa = browser.find_element_by_xpath("//*[@id='lblgpa']")
                    gpa = browser.find_element_by_xpath("//*[@id='lblcgpa']")

                    names.append(name.text)
                    regnums.append(roll.text)
                    cgpas.append(cgpa.text)
                    gpas.append(gpa.text)
                    roll_no = roll_no + 1
                    browser.back()
                else:
                    roll_no = roll_no + 1
            browser.close()

            above_9,above_8,above_7,above_6,above_5,fail=0,0,0,0,0,0
            for g in gpas:
                g=float(g)
                if(9.0<=g<=10.0):
                    above_9+=1
                elif(8.0<=g<9.0):
                    above_8+=1
                elif(7.0<=g<8.0):
                    above_7+=1
                elif(6.0<=g<7.0):
                    above_6+=1
                elif(5.0<=g<6.0):
                    above_5+=1
                else:
                    fail+=1

            total=[]
            total.append(above_9)
            total.append(above_8)
            total.append(above_7)
            total.append(above_6)
            total.append(above_5)
            total.append(fail)
            labels=['>9','>8','>7','>6','>5','Fail']

            #pie chart
            plt.pie(total, labels=labels, autopct='%.2f')
            plt.axis('equal')# Equal aspect ratio ensures that pie is drawn as a circle.
            plt.title("Pie chart of GPAs")
            st.pyplot()


            #barplot
            data = [2, 3, 5, 6, 8, 12]
            my_cmap = cm.get_cmap('jet')
            my_norm = Normalize(vmin=0, vmax=8)
            plt.bar(labels,total,color=my_cmap(my_norm(data)))
            plt.title("Bar plot of GPAs")
            plt.yticks(total)
            plt.xlabel("Grades")
            plt.ylabel("Number of student(s)")
            st.pyplot()

            st.write("Number of students having GPA above_9:", above_9)
            st.write("Number of students having GPA above_8:", above_8)
            st.write("Number of students having GPA above_7:", above_7)
            st.write("Number of students having GPA above_6:", above_6)
            st.write("Number of students having GPA above_5:", above_5)
            st.write("Number of students having GPA failed:", fail)

            full=[]
            full.append(names)
            full.append(regnums)
            full.append(cgpas)
            full.append(gpas)
            df=DataFrame(full)
            st.write("DataFrame of student Details:")
            st.write(df)
            df.to_csv('Grades.csv')
        else:
            st.write("Please check the values entered")

if __name__ == '__main__':
    main()
