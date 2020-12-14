from Tools import tools_v000 as tools
import os
from os.path import dirname

# -2 for the name of this project AM
save_path = dirname(__file__)[ : -2]
propertiesFolder_path = save_path + "Properties"

# Example of used
# user_text = tools.readProperty(propertiesFolder_path, 'AM', 'user_text=')

debug_mode = True

def launchProcess(src_path) :
    print ("Start : " + src_path)

    # search if the treatment is already begin or not
    try :
        ToBeTreated_lines = tools.search_string_in_file(src_path, 'ToBeTreated = True')
    except :
        # to don't look if the file is readable or not catch the error when it's not
        ToBeTreated_lines = ""
        pass
    
    if len(ToBeTreated_lines) > 0 :
        Ongoing_lines = tools.search_string_in_file(src_path, 'Ongoing = True')
        if len(Ongoing_lines) == 0 :
            tools.writeToFile(src_path, "\n\n")
            tools.writeToFile(src_path, "Ongoing = True")
            tools.writeToFile(src_path, "\n\n")
            
            # search for given strings in the file 
            matched_lines = tools.search_multiple_strings_in_file(src_path, ['contact_id = ', 'user_name = '])
            if debug_mode == True :
                print('Total Matched lines : ', len(matched_lines))
            contact_id = ""
            user_name = ""
            for elem in matched_lines:
                if debug_mode == True :
                    print('Word = ', elem[0], ' :: Line Number = ', elem[1], ' :: Line = ', elem[2])
                    print(elem[2][len(elem[0]):])
                if elem[0] == 'contact_id = ' :
                    contact_id = elem[2][len(elem[0]):]
                else :
                    if elem[0] == 'user_name = ' :
                        user_name = elem[2][len(elem[0]):]
            tryToCorrectProblem(contact_id, user_name, src_path)
        else :
            print ("====================================================")
            print ("=============== Already in traitment ===============")
            print ("====================================================")
    else :
        print ("==========================================")
        print ("It's not a file that I can treat by myself")
        print ("==========================================")
        
def tryToCorrectProblem(contact_id, user_name, src_path) :
    # Look first into AM, to collect all the info
    AM_site(contact_id, user_name, src_path) 

    # Look if in LDAP everything is also ok
    # user into the User
    # user into the exxtra group
    # user into the Binda group (if necessary)
    # user into the eSolife group (if necessary)
    # user into the loans group (if necessary)
    # op.runldapJXplorer()

    # Look if for BINDA everything is also ok (DB Part)

    # Open the file with the info
    tools.openFile(src_path)

def AM_site(contact_id, user_name, src_path) :
    print('contact_id : ' +contact_id)
    print('user_name : ' +user_name)
    tools.openBrowserChrome()
    driver = tools.driver

    driver.get("http://sx-dll-wlsbp01:7011/Exxtra/")

    # Gestion des personnes de contact
    tools.waitLoadingPageByXPATH("/html/body/div[1]/div[1]/div[4]/div/form/div[1]/ul/li[4]/a")
    contact_button = driver.find_element_by_xpath("/html/body/div[1]/div[1]/div[4]/div/form/div[1]/ul/li[4]/a")
    contact_button.click()

    # ===== Search Part ======
    if len(contact_id) > 0 :
        tools.waitLoadingPageByID("contact_ID")
        contact_ID_input = driver.find_element_by_id("contact_ID")
        contact_ID_input.send_keys(contact_id)
    
    if len(user_name) > 0 :
        tools.waitLoadingPageByID("userName")
        contact_ID_input = driver.find_element_by_id("userName")
        contact_ID_input.send_keys(user_name)

    tools.waitLoadingPageByID("search")
    search_button = driver.find_element_by_id("search")
    search_button.click()
    
    # Select result
    tools.waitLoadingPageByID("dataTable1_data")
    dataTable1_data = driver.find_element_by_id("dataTable1_data")
    dataTable1_data.click()

    # ===== Result Page =====
    # Recover information
    # email
    tools.waitLoadingPageByXPATH("/html/body/div[1]/div[2]/div/div/div[3]/form/div[2]/div[2]/table[1]/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[3]/td[3]/a")
    email_value = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div[3]/form/div[2]/div[2]/table[1]/tbody/tr/td[2]/table/tbody/tr[2]/td/table/tbody/tr[3]/td[3]/a").text

    # contact_ID
    if len(contact_id) == 0 :
        tools.waitLoadingPageByXPATH("/html/body/div[1]/div[2]/div/div/div[3]/form/div[2]/div[2]/table[1]/tbody/tr/td[1]/table/tbody/tr[2]/td/table/tbody/tr[4]/td[3]")
        contact_id = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div[3]/form/div[2]/div[2]/table[1]/tbody/tr/td[1]/table/tbody/tr[2]/td/table/tbody/tr[4]/td[3]").text

    # userName
    if len(user_name) == 0 :
        tools.waitLoadingPageByXPATH("/html/body/div[1]/div[2]/div/div/div[3]/form/div[3]/div[2]/div[1]/div[2]/table[1]/tbody/tr[1]/td[3]")
        user_name = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div/div[3]/form/div[3]/div[2]/div[1]/div[2]/table[1]/tbody/tr[1]/td[3]").text
    
    if debug_mode == True :
        print("email = " + email_value)
        print("contact_id = " + contact_id)
        print("user_name = " + user_name)

    # Saved those information into the file
    tools.writeToFile(src_path, "email = " + email_value + "\n")
    tools.writeToFile(src_path, "contact_id = " + contact_id + "\n")
    tools.writeToFile(src_path, "user_name = " + user_name + "\n")