import socket

# Creating a HTML page.
html = '<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><style>table,td,th{margin-left:auto;margin-right:auto}body{font-family:Arial;text-align:center;margin:0 auto;padding-top:30px;background-color:#9b9bf0}.switch{position:relative;display:inline-block;width:120px;height:68px}.switch input{display:none}.slider{position:absolute;top:0;left:0;right:0;bottom:0;background-color:#ccc;border-radius:34px}.slider:before{position:absolute;content:"";height:52px;width:52px;left:8px;bottom:8px;background-color:#fff;-webkit-transition:.4s;transition:.4s;border-radius:68px}input:checked+.slider{background-color:#2196f3}input:checked+.slider:before{-webkit-transform:translateX(52px);-ms-transform:translateX(52px);transform:translateX(52px)}</style><script>function toggleCheckbox(e){var n=new XMLHttpRequest;e.checked?n.open("GET","/?r="+e.value+"&a=on",!0):n.open("GET","/?r="+e.value+"&a=off",!0),n.send()}</script></head><body><h1>App based Relay Control</h1><h3>________________</h3><table style="width:50%"><tr><td>Wall Light</td><td><label class="switch"><input type="checkbox" value="1" onchange="toggleCheckbox(this)"><span class="slider"></span></label></td></tr><tr><td>Spots</td><td><label class="switch"><input type="checkbox" value="2" onchange="toggleCheckbox(this)"><span class="slider"></span></label></td></tr><tr><td>Cove</td><td><label class="switch"><input type="checkbox" value="3" onchange="toggleCheckbox(this)"><span class="slider"></span></label></td></tr><tr><td>Socket</td><td><label class="switch"><input type="checkbox" value="4" onchange="toggleCheckbox(this)"><span class="slider"></span></label></td></tr></table></body></html>'

# creating a WEB socket for communication between the nodemcu and the webpage
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 2645))  # Binding(assiging) the socket for communication on port '2645'
s.listen(5)  # 5 signifies the number of maximum number of connections done on the port
print("Listening on port 2645")

while True:  # Creating an infinite loop
    try:
        if gc.mem_free() < 102000:
            gc.collect()  # Collecting allocated waste memory to free the memory

        (
            conn,
            addr,
        ) = (
            s.accept()
        )  # .accept returns 2 values that will be appended into variables respectively
        conn.settimeout(3.0)
        print("Connect Req. from: %s" % str(addr))
        request = conn.recv(
            1024
        )  # Listening for the reply from the WEB page and mentioning that the size should not exceed 1024 bytes.
        conn.settimeout(None)
        request = str(
            request
        )  # The request comes in a binary format and that should be converted intp a string before operating on it.
        print("Content = %s" % request)
        eIdx = request.find(
            "&a="
        )  # Finding the required parameters in the query. This is the Action of the relay that should be performed.
        # .find method returns the index of substring inside a string. The returned index will give the index of the first character of the substring inside the string.
        if eIdx > 0:  # Checking if the action is available or nor.
            idR = request.find("/?r=") + 4  # Finding the value of the relay required.
            idA = request.find(
                "&a="
            )  # Finding the index of the query for action of the relay.
            idE = request.find(" HTTP")  # Finding the end of the query.
            Rly = request[idR:idA]  # Taking the relay number.
            Act = request[idA + 3 : idE]  # Taking the action(ON/OFF).
            rObj = locals()[
                "Rly" + str(Rly)
            ]  # locals() will make the srting into a variable.(The variable name is in the boot.py file running in the NODE)
            if Act == "on":
                rObj.value(
                    0
                )  # updating the value of the required relay according to the action.
            elif Act == "off":
                rObj.value(1)
        conn.send(
            ("HTTP/1.1 200 OK\nContent-Type: text/html\nConnection: close\n\n")
        )  # Conforming the webpage that the request is been recieved and procssed.
        conn.sendall(html)  # Updating the HTML page
        conn.close()
    except OSError as e:  # If there is any error it will close the HTTP connection
        conn.close()
        print("Connection closed")
