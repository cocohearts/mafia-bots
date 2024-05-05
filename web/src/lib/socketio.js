import { io } from 'socket.io-client';

// Unique IDs on a browser-by-browser basis
let username = localStorage.getItem('username');
if (!username) {
  username = uuidv4();
  localStorage.setItem('username', username);
}

export const socket = io('ws://127.0.0.1:5000');
