from webserver.server import Server

def main():
    server = Server("Redmip", "asd12345")
    server.create_MQTT_clientID()
    server.connect_MQTT()
    server.publish_feed("Dario",10)


if __name__=="__main__":
    main()
