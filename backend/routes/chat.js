const express = require('express');
const { 
  getUserChats, 
  getChatById, 
  createChat, 
  addMessage, 
  deleteChat 
} = require('../controllers/chatController');
const { protect } = require('../middleware/auth');

const router = express.Router();

// All chat routes are protected
router.use(protect);

// Get all user chats and create new chat
router.route('/')
  .get(getUserChats)
  .post(createChat);

// Get, update and delete specific chat
router.route('/:id')
  .get(getChatById)
  .delete(deleteChat);

// Add message to chat
router.post('/:id/messages', addMessage);

module.exports = router; 