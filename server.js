// Simple Express backend for Food Delivery Website
const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const path = require('path');
require('dotenv').config();

let OpenAI = null;
if (process.env.OPENAI_API_KEY) {
  try {
    const { Configuration, OpenAIApi } = require('openai');
    const configuration = new Configuration({ apiKey: process.env.OPENAI_API_KEY });
    OpenAI = new OpenAIApi(configuration);
  } catch (e) {
    console.warn('openai package not available, /api/chat will return a fallback response.');
    OpenAI = null;
  }
}

const app = express();
const PORT = 3001;

app.use(cors());
app.use(bodyParser.json());

// Serve frontend static files from project root (so frontend and API share same origin)
const publicDir = path.join(__dirname, '..');
app.use(express.static(publicDir));

// Sample menu data
const menu = [
  { id: 1, name: 'Pizza', price: 10 },
  { id: 2, name: 'Burger', price: 7 },
  { id: 3, name: 'Pasta', price: 8 }
];

// In-memory orders and feedback
const orders = [];
const feedbacks = [];

// Get menu
app.get('/api/menu', (req, res) => {
  res.json(menu);
});

// Place order
app.post('/api/order', (req, res) => {
  const order = req.body;
  orders.push(order);
  res.json({ success: true, message: 'Order placed successfully!' });
});

// Submit feedback
app.post('/api/feedback', (req, res) => {
  const feedback = req.body;
  feedbacks.push(feedback);
  res.json({ success: true, message: 'Feedback submitted!' });
});

// Get all orders (for admin)
app.get('/api/orders', (req, res) => {
  res.json(orders);
});

// Get all feedback (for admin)
app.get('/api/feedbacks', (req, res) => {
  res.json(feedbacks);
});

// Chat endpoint - proxies to OpenAI when configured
app.post('/api/chat', async (req, res) => {
  const { message } = req.body || {};
  if (!message || typeof message !== 'string') {
    return res.status(400).json({ error: 'Missing message in request body' });
  }

  if (!OpenAI) {
    // Basic fallback reply
    const lower = message.toLowerCase();
    let reply = "I'm here to help. Please ask about the menu or orders.";
    if (lower.includes('menu') || lower.includes('food')) reply = 'Our menu includes Pizza, Burger, and Pasta.';
    if (lower.includes('order')) reply = 'To place an order, use the order form on the website or tell me what you want.';
    return res.json({ reply });
  }

  try {
    const response = await OpenAI.createChatCompletion({
      model: 'gpt-3.5-turbo',
      messages: [
        { role: 'system', content: 'You are a friendly assistant for a food delivery website. Keep answers short.' },
        { role: 'user', content: message }
      ],
      max_tokens: 200,
      temperature: 0.7,
    });

    const reply = response.data.choices[0].message.content.trim();
    res.json({ reply });
  } catch (err) {
    console.error('OpenAI error:', err);
    res.status(500).json({ error: 'AI service error' });
  }
});

app.listen(PORT, () => {
  console.log(`Backend server running on http://localhost:${PORT}`);
});
