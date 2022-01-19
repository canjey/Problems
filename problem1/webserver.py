from http.server import HTTPServer, BaseHTTPRequestHandler
from sys import path
import cgi
import socket, ssl
import os

taskList = ['Work', 'Eat', 'Shower']

class requestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('/taskList'):
            # content_length = int(self.headers['Content-Length'])
            self.send_response(200)
            self.send_header('content-type','text/html')
            self.end_headers()
            
            output = ''
            output += '<html><body>'
            output += '<h1> To Do List </h1>'
            output += '<a href = "/taskList/new">Add new Task</a></br>'
            for task in taskList:
                output+= task 
                output +='<a href = "/taskList/%s/remove">X</a>' % task
                output += '</br> '
            output += '</html></body>'

            self.wfile.write(output.encode())


        if self.path.endswith('/new'):
            self.send_response(200)
            self.send_header('content-type','text/html')
            self.end_headers()
            
            output = ''
            output += '<html><body>'
            output += '<h1>Add New Task</h1>'

            output += '<form method = "POST" enctype="multipart/form-data" action ="taskList/new">'
            output += '<input name = "task" type ="text" placeholder="Add task">'
            output += '<input type ="submit" value = "Add" >'
            output += '</form>'
            output += '</body></html>'

            self.wfile.write(output.encode())

        if self.path.endswith('/remove'):
            listIDPath = self.path.split('/')[2]
            print(listIDPath)
            self.send_response(200)
            self.send_header('content-type','text/html')
            self.end_headers()

            output = ''
            output += '<html><body>'
            output += '<h1>Do you want to remove task : %s  </h1>' %listIDPath.replace('%20', ' ')
            output += '<form method = "POST" enctype = "multipart/form-data" action = "/taskList/%s/remove">' %listIDPath
            output += '<input type = "submit" value = "Remove">'
            output += '</br>'
            output += '</form>'
            output += '<a href = "/taskList"> Cancel </a>'

            output += '</body></html>'
            self.wfile.write(output.encode())


    def do_POST(self):
        if self.path.endswith("/new"):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                new_task = fields.get('task')
                taskList.append(new_task[0])

            self.send_response(301)
            self.send_header('content-type','text/html')
            self.send_header('location', '/taskList')
            self.end_headers()


        if self.path.endswith("/remove"):
            listIDPath = self.path.split('/')[2]
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            if ctype == 'multipart/form-data':
                print(listIDPath)
                list_item = listIDPath.replace("%20",' ')
                print(list_item)
                taskList.remove(list_item)

            self.send_response(301)
            self.send_header('content-type','text/html')
            self.send_header('location', '/taskList')
            self.end_headers()





def main():
    PORT = 8020
    server = HTTPServer(('', PORT), requestHandler)
    print('Server running on port %s' %PORT)
    server.serve_forever()

if __name__ == '__main__':
    main()