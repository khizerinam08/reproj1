const Chat = require('../models/Chat');

// @desc    Get all chats for a user
// @route   GET /api/chats
// @access  Private
const getUserChats = async (req, res) => {
  try {
    const chats = await Chat.find({ user: req.user._id }).sort({ updatedAt: -1 });
    res.json(chats);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Server error' });
  }
};

// @desc    Get a single chat
// @route   GET /api/chats/:id
// @access  Private
const getChatById = async (req, res) => {
  try {
    const chat = await Chat.findById(req.params.id);
    
    // Check if chat exists
    if (!chat) {
      return res.status(404).json({ message: 'Chat not found' });
    }
    
    // Make sure the logged in user owns the chat
    if (chat.user.toString() !== req.user._id.toString()) {
      return res.status(401).json({ message: 'Not authorized to access this chat' });
    }
    
    res.json(chat);
  } catch (error) {
    console.error(error);
    if (error.kind === 'ObjectId') {
      return res.status(404).json({ message: 'Chat not found' });
    }
    res.status(500).json({ message: 'Server error' });
  }
};

// @desc    Create a new chat
// @route   POST /api/chats
// @access  Private
const createChat = async (req, res) => {
  try {
    const { title, initialMessage } = req.body;
    
    const chat = new Chat({
      user: req.user._id,
      title: title || 'New Chat',
      messages: initialMessage ? [
        {
          sender: 'user',
          content: initialMessage
        }
      ] : []
    });
    
    const createdChat = await chat.save();
    res.status(201).json(createdChat);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Server error' });
  }
};

// @desc    Add message to chat
// @route   POST /api/chats/:id/messages
// @access  Private
const addMessage = async (req, res) => {
  try {
    const { sender, content } = req.body;
    
    if (!sender || !content) {
      return res.status(400).json({ message: 'Please provide sender and content' });
    }
    
    const chat = await Chat.findById(req.params.id);
    
    // Check if chat exists
    if (!chat) {
      return res.status(404).json({ message: 'Chat not found' });
    }
    
    // Make sure the logged in user owns the chat
    if (chat.user.toString() !== req.user._id.toString()) {
      return res.status(401).json({ message: 'Not authorized to access this chat' });
    }
    
    // Add message to chat
    chat.messages.push({
      sender,
      content
    });
    
    // Save chat with new message
    await chat.save();
    
    res.status(201).json(chat);
  } catch (error) {
    console.error(error);
    if (error.kind === 'ObjectId') {
      return res.status(404).json({ message: 'Chat not found' });
    }
    res.status(500).json({ message: 'Server error' });
  }
};

// @desc    Delete a chat
// @route   DELETE /api/chats/:id
// @access  Private
const deleteChat = async (req, res) => {
  try {
    const chat = await Chat.findById(req.params.id);
    
    // Check if chat exists
    if (!chat) {
      return res.status(404).json({ message: 'Chat not found' });
    }
    
    // Make sure the logged in user owns the chat
    if (chat.user.toString() !== req.user._id.toString()) {
      return res.status(401).json({ message: 'Not authorized to delete this chat' });
    }
    
    await chat.deleteOne();
    res.json({ message: 'Chat removed' });
  } catch (error) {
    console.error(error);
    if (error.kind === 'ObjectId') {
      return res.status(404).json({ message: 'Chat not found' });
    }
    res.status(500).json({ message: 'Server error' });
  }
};

module.exports = {
  getUserChats,
  getChatById,
  createChat,
  addMessage,
  deleteChat
}; 