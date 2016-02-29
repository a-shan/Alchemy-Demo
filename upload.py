import requests  # available at https://github.com/kennethreitz/requests
import re  # regular expression
import logging
import os

'''
@description: uploads an image file to funkyimg.com 
@param image_path: absolute path to the image file to be uploaded 
'''
def upload(path):
    global image_path
    image_path = path
    upload_url = 'http://funkyimg.com/upload/'
 
    '''
    ===// Remote Upload //===    
    payload = {'url': 'http://funkyimg.com/i/CfJo.jpg'}
    r = requests.post(upload_url, data=payload)
    '''
    
    
    '''===// Recursive Upload //==='''
    loop_flag = False
    fail_counter = 0    
    
    while(loop_flag == False):    
        try:
            print "LOAD: Uploading Image...  "  
            
            logging.debug("Uploading Image: "+image_path)
            image_file = open(image_path, 'rb');
            files = {'images': image_file}
            r = requests.post(upload_url, files=files)
            
            logging.debug("Request Status Code: "+str(r.status_code))
            logging.debug("Request Text: "+r.text)
            logging.debug("Request Success Status: "+str(r.json()['success']))
            
            if(r.json()['success'] == True): #image upload is successful                
                print "STAT: Upload Successful"         
                loop_flag = True
                
            else:
                raise Exception("Request Success Status is not true") 
            
        except Exception:            
            image_file.close()      
            loop_flag = False
            fail_counter += 1
            print "STAT: Upload Failed! " + str(fail_counter) + " times"
            logging.exception("Upload Failed! "+str(fail_counter)+" times")
            ori_image_path = image_path
            image_path = image_path.replace("."+image_path.split(".")[-1],"-"+str(fail_counter)+"."+image_path.split(".")[-1])
            os.rename(ori_image_path, image_path)
            logging.debug("File Renamed: "+image_path)
            
       
    '''===// Recursive Code Retrieval //==='''
    loop_flag = False
    fail_counter = 0    
    
    while(loop_flag == False):    
        try:
            print "LOAD: Retrieving Image Code..."            
            code_url = 'http://funkyimg.com/upload/check/' + r.json()['jid']
            r2 = requests.get(code_url)
            logging.debug("Request Status Code: "+str(r2.status_code))
            logging.debug("Request Text: "+r2.text)
            logging.debug("Request Success Status: "+str(r2.json()['success']))
            
            if(r2.json()['success'] == True): #code retrieval is successful                
                m = re.search('(?<=p/)[A-Za-z0-9]*', r2.text)    
                print "STAT: Code Retrieval Successful"
                logging.debug("Retrieved Code is: "+m.group(0))            
                loop_flag = True                
            else:                
                raise Exception("Request Success Status is not true")
                
            return m.group(0)
            
        except Exception:
            loop_flag = False
            fail_counter += 1
            print "STAT: Code Retrieval Failed! " + str(fail_counter) + " times"
            logging.exception("Code Retrieval Failed! "+str(fail_counter)+" times")