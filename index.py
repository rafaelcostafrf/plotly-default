from app import app
import callbacks

server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)