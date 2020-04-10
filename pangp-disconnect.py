import requests
import urllib3
import ipaddress

# Disable insecure warnings
requests.packages.urllib3.disable_warnings()

## Function for API key
def get_api_key(ip,username,password):
    url = "https://"+ip+"/api/?type=keygen&user="+username+"&password="+password
    response = requests.get(url, verify=False)
    r = response.text
    r = r[42:-26]
    return(r)

## Function to collect GP current user output
def get_current_gp(ip,key,gpgateway):
    url = "https://"+ip+"/api/?key="+key+"&type=op&cmd="+"<show><global-protect-gateway><current-user><gateway>"+gpgateway+"</gateway></current-user></global-protect-gateway></show>"
    response = requests.get(url, verify=False)
    with open("responsetext","w") as f:
        f.write(response.text)
    return(response.text)

## Function to disconnect user
def disconnect_user(ip,key,gpgateway,baduser,computer):
    url = "https://"+ip+"/api/?key="+key+"&type=op&cmd="+"<request><global-protect-gateway><client-logout><gateway>"+gpgateway+"-N</gateway><reason>force-logout</reason><user>"+baduser+"</user><computer>"+computer+"</computer></client-logout></global-protect-gateway></request>"
    response = requests.get(url, verify=False)
    return(response.text)


## Function to kill user who connect on more than 2 computers
def kill_user(file,ip,key,gpgateway):
    alluser = {}
    baduser = {}
    username = ""
    with open(file) as f:
        for line in f:
            if (line.find("<username>") != -1):
                username = line[line.find("<username>")+10:-12]
                if username not in alluser:
                    alluser[username] = "null"
                else:
                    baduser[username] = "null"

            if (line.find("<computer>") != -1):
                computer = line[line.find("<computer>")+10:-12]
                if username in baduser:
                    baduser[username] = computer
                    disconnect_user(ip, key, gpgateway, username, baduser.get(username))
                    print("User "+username+ " on computer "+baduser.get(username)+" was diconnected" )
                    baduser.pop(username, None)
                else:
                    alluser[username] = computer


    #print(alluser)
    #print(baduser)
    return(alluser)


if __name__ == "__main__":
    ## Get API key and authen
    ipaddr = input("Firewall IP address: ")
    user = input("Admin Username: ")
    passwd = input("Password: ")
    gpgateway = input("GP Gateway name : ")
    k = get_api_key(ipaddr,user,passwd)

    ## Process
    get_current_gp(ipaddr,k,gpgateway)
    kill_user("responsetext",ipaddr,k,gpgateway)
