import React, { createContext, useContext, useState } from 'react';
import io from 'socket.io-client';

const SocketContext = createContext();

function SocketProvider({ children, setIsLoggedIn }) {
    const [socket, setSocket] = useState(null);
    const initializeSocket = () => {
        const newSocket = io.connect(process.env.REACT_APP_API_URL);
        newSocket.on('alive_message', (data) => {
            if (data === "is still alive?") {
                newSocket.emit('alive_message', 'alive');
            } else {
                console.log(data);
            }
        });
        newSocket.on('disconnect', () => {
            disconnectSocket();
        })
        setSocket(newSocket);
    };

    const disconnectSocket = () => {
        if (socket) {
            socket.disconnect();
            setSocket(null);
            setIsLoggedIn(false);
        }
    };

    const getSocket = () => {
        if (!socket) {
            initializeSocket();
        }
        return socket;
    };

    return (
        <SocketContext.Provider value={{ getSocket, disconnectSocket }}>
            {children}
        </SocketContext.Provider>
    );
};

function useSocket() {
    return useContext(SocketContext);
}

export { SocketProvider, useSocket };